from .extension import (
    Component,
    Port,
    Model,
    SMatrix,
    Technology,
    register_model_class,
    Z_MAX,
    config,
)
from .utils import C_0, _filename_cleanup, _safe_hash
from .cache import _Cache, _cache_path
from . import tidy3d_model

import numpy
import pydantic
import tidy3d
from tidy3d.plugins.mode import ModeSolver

import copy as libcopy
import json
import pathlib
import warnings
import zlib
from typing import Any, Optional, Union, Literal
from collections.abc import Sequence


class _EMEModelRunner:
    cache = _Cache(tidy3d_model.CACHE_SIZE)

    def __init__(
        self,
        simulation: tidy3d.EMESimulation,
        ports: dict[str, Port],
        port_groups: tuple[tuple[str], tuple[str]],
        mesh_refinement: Union[tidy3d.components.grid.grid_spec.GridSpec1d, float],
        technology: Technology,
        folder_name: str,
        data_path: str,
        verbose: bool,
    ) -> None:
        key = (tidy3d_model._tidy3d_to_bytes(simulation), folder_name, data_path, verbose)
        runner = _EMEModelRunner.cache[key]
        if runner is None or runner.status["message"] == "error":
            task_name = "EME" if "EME" not in ports else ("EME " + " ".join(ports))
            runner = tidy3d_model._simulation_runner(
                simulation=simulation,
                task_name=task_name,
                remote_path=folder_name,
                data_path=data_path,
                verbose=verbose,
            )
            _EMEModelRunner.cache[key] = runner
        self.runners = {0: runner}

        # Port modes for decomposition
        for name in port_groups[0] + port_groups[1]:
            self.runners[name] = tidy3d_model._ModeSolverRunner(
                port=ports[name],
                frequencies=simulation.freqs,
                mesh_refinement=mesh_refinement,
                technology=technology,
                verbose=verbose,
            )

        self.ports = ports
        self.port_groups = port_groups
        self._s_matrix = None

        # If the model uses any symmetry, it will impact the mode numbering of the ports.
        # We need to remap port modes from the symmetry-applied to the full version.
        if simulation.symmetry != (0, 0, 0):
            full_sim = simulation.copy(update={"symmetry": (0, 0, 0)})
            for name in port_groups[0] + port_groups[1]:
                source = ports[name].to_tidy3d_monitor(simulation.freqs)
                mode_solver = ModeSolver(
                    simulation=full_sim,
                    plane=source.bounding_box,
                    mode_spec=source.mode_spec,
                    freqs=source.freqs,
                    direction=source.store_fields_direction,
                )
                self.runners[(name, "full")] = tidy3d_model._simulation_runner(
                    simulation=mode_solver,
                    task_name=name + "-no_sym",
                    remote_path=folder_name,
                    data_path=data_path,
                    verbose=verbose,
                )

    @property
    def status(self) -> dict[str, Any]:
        """Monitor S matrix computation progress."""
        all_stat = [runner.status for runner in self.runners.values()]
        if all(s["message"] == "success" for s in all_stat):
            message = "success"
            progress = 100
        elif any(s["message"] == "error" for s in all_stat):
            message = "error"
            progress = 100
        else:
            message = "running"
            progress = sum(
                100 if s["message"] == "success" else s["progress"] for s in all_stat
            ) / len(all_stat)
        return {"progress": progress, "message": message}

    @property
    def s_matrix(self) -> SMatrix:
        """Get the model S matrix."""
        if self._s_matrix is None:
            # Original S matrix in EME basis
            eme_data = self.runners[0].data
            eme_modes = eme_data.port_modes_tuple
            eme_modes = (eme_modes[0], eme_modes[1].time_reversed_copy)

            num_eme_modes = (
                eme_modes[0].monitor.mode_spec.num_modes,
                eme_modes[1].monitor.mode_spec.num_modes,
            )
            num_freqs = len(eme_data.simulation.freqs)
            s = numpy.empty((num_freqs, sum(num_eme_modes), sum(num_eme_modes)), dtype=complex)
            s[:, : num_eme_modes[0], : num_eme_modes[0]] = (
                eme_data.smatrix.S11.isel(sweep_index=0, drop=True)
                .transpose("f", "mode_index_out", "mode_index_in")
                .values
            )
            s[:, : num_eme_modes[0], num_eme_modes[0] :] = (
                eme_data.smatrix.S12.isel(sweep_index=0, drop=True)
                .transpose("f", "mode_index_out", "mode_index_in")
                .values
            )
            s[:, num_eme_modes[0] :, : num_eme_modes[0]] = (
                eme_data.smatrix.S21.isel(sweep_index=0, drop=True)
                .transpose("f", "mode_index_out", "mode_index_in")
                .values
            )
            s[:, num_eme_modes[0] :, num_eme_modes[0] :] = (
                eme_data.smatrix.S22.isel(sweep_index=0, drop=True)
                .transpose("f", "mode_index_out", "mode_index_in")
                .values
            )

            # Port mode transformation matrix
            # M_ij = <e_i, e_j'> / <e_i, e_i>
            # S' = pinv(M)×S×M
            port_names = self.port_groups[0] + self.port_groups[1]
            num_modes = sum(self.ports[name].num_modes for name in port_names)
            m = numpy.zeros((num_freqs, sum(num_eme_modes), num_modes), dtype=complex)
            mode_index = 0
            mode_sign = {}
            for i in range(2):
                norms = eme_modes[i].dot(eme_modes[i], conjugate=False)
                for name in self.port_groups[i]:
                    port_modes = self.ports[name].num_modes
                    port_data = self.runners[name].data
                    mode_sign[name] = tidy3d_model._mode_normalization_signs(port_data)
                    projection = eme_modes[i].outer_dot(port_data)
                    m_block = (
                        projection.transpose("mode_index_1", "mode_index_0", "f").values
                        / norms.transpose("mode_index", "f").values
                    )
                    # Mode data from EME comes with max(num_eme_modes) modes
                    m_block = m_block[:, : num_eme_modes[i], :].T
                    if i == 0:
                        m[:, : num_eme_modes[0], mode_index : mode_index + port_modes] = m_block
                    else:
                        m[:, num_eme_modes[0] :, mode_index : mode_index + port_modes] = m_block
                    mode_index += port_modes
            s = numpy.linalg.pinv(m) @ s @ m

            elements = {}
            j = 0
            for src in port_names:
                for src_mode in range(self.ports[src].num_modes):
                    src_sign = mode_sign[src][src_mode]
                    i = 0
                    for dst in port_names:
                        for dst_mode in range(self.ports[dst].num_modes):
                            dst_sign = mode_sign[dst][dst_mode]
                            elements[f"{src}@{src_mode}", f"{dst}@{dst_mode}"] = (
                                s[:, i, j] * dst_sign / src_sign
                            )
                            i += 1
                    j += 1

            # If symmetry was used, calculate and apply mode mapping
            if eme_data.simulation.symmetry != (0, 0, 0):
                mode_map = {}
                for name, port in self.ports.items():
                    if not isinstance(port, Port):
                        mode_map[name] = list(range(port.num_modes))
                        continue
                    mode_map[name] = [-1] * port.num_modes
                    data_sym = self.runners[name].data
                    data_full = self.runners[(name, "full")].data
                    overlap = None
                    f = self.frequencies.size // 2
                    n_sym = data_sym.n_complex.isel(f=f).values.squeeze()
                    n_full = data_full.n_complex.isel(f=f).values.squeeze()
                    n_sym = numpy.repeat(n_sym.reshape((-1, 1)), n_sym.size, axis=1)
                    n_full = numpy.repeat(n_full.reshape((1, -1)), n_full.size, axis=0)
                    matches = (
                        numpy.abs(n_sym - n_full) / numpy.abs(n_full) < tidy3d_model.INDEX_THRESHOLD
                    )
                    for sym_index in range(port.num_modes):
                        candidates = matches[sym_index].nonzero()[0].tolist()
                        if len(candidates) == 1:
                            mode_map[name][sym_index] = candidates[0]
                        elif len(candidates) > 1:
                            if overlap is None:
                                overlap = abs(data_sym.outer_dot(data_full).isel(f=f, drop=True))
                            ovlp = overlap.isel(mode_index_0=sym_index).values.squeeze()
                            full_index = numpy.argmax(ovlp).item()
                            if ovlp[full_index] >= tidy3d_model.OVERLAP_THRESHOLD:
                                mode_map[name][sym_index] = full_index

                new_elements = {}
                for src, src_port in self.ports.items():
                    src_map = mode_map[src]
                    for dst, dst_port in self.ports.items():
                        dst_map = mode_map[dst]
                        for src_mode in range(src_port.num_modes):
                            new_src_mode = src_map[src_mode]
                            if new_src_mode < 0:
                                continue
                            for dst_mode in range(dst_port.num_modes):
                                new_dst_mode = dst_map[dst_mode]
                                if new_dst_mode < 0:
                                    continue
                                key = (f"{src}@{src_mode}", f"{dst}@{dst_mode}")
                                new_key = (f"{src}@{new_src_mode}", f"{dst}@{new_dst_mode}")
                                element = elements.get(key)
                                if element is not None:
                                    new_elements[new_key] = element
                elements = new_elements

            self._s_matrix = SMatrix(eme_data.simulation.freqs, elements, self.ports)

        return self._s_matrix


class EMEModel(Model):
    """S matrix model based on Eigenmode Expansion calculation.

    Args:
        eme_grid_spec: 1D grid in the that specifies the EME cells where
          mode solving is performed along the propagation direction.
        medium: Background medium. If ``None``, the technology default is
          used.
        symmetry: Component symmetries.
        monitors: Extra field monitors added to the simulation.
        structures: Additional structures included in the simulations.
        grid_spec: Simulation grid specification. A single float can be used
          to specify the ``min_steps_per_wvl`` for an auto grid.
        subpixel: Flag controlling subpixel averaging in the simulation
          grid.
        bounds: Bound overrides for the final simulation.
        constraint: Constraint for EME propagation. Possible values are
          ``"passive"`` and ``"unitary"``.
        verbose: Control solver verbosity.

    If not set, the default values for the component simulations are defined
    based on the wavelengths used in the ``s_matrix`` call.
    """

    _data_cache = {}

    def __init__(
        self,
        eme_grid_spec: tidy3d.components.eme.grid.EMESubgridType,
        medium: Optional[tidy3d.components.medium.MediumType3D] = None,
        symmetry: Sequence[int] = (0, 0, 0),
        monitors: Sequence[tidy3d.components.monitor.MonitorType] = (),
        structures: Sequence[tidy3d.Structure] = (),
        grid_spec: Union[float, tidy3d.GridSpec] = None,
        subpixel: bool = True,
        bounds: Sequence[Sequence[Optional[float]]] = ((None, None, None), (None, None, None)),
        constraint: Optional[Literal["passive", "unitary"]] = None,
        verbose: bool = True,
    ) -> None:
        super().__init__(
            eme_grid_spec=eme_grid_spec,
            medium=medium,
            symmetry=symmetry,
            monitors=monitors,
            structures=structures,
            grid_spec=grid_spec,
            subpixel=subpixel,
            bounds=bounds,
            constraint=constraint,
            verbose=verbose,
        )
        self.eme_grid_spec = eme_grid_spec
        self.medium = medium
        self.symmetry = symmetry
        self.monitors = monitors
        self.structures = structures
        self.grid_spec = grid_spec
        self.subpixel = subpixel
        self.bounds = bounds
        self.constraint = constraint
        self.verbose = verbose

    def __copy__(self) -> "EMEModel":
        return EMEModel(
            self.eme_grid_spec,
            self.medium,
            self.symmetry,
            self.monitors,
            self.structures,
            self.grid_spec,
            self.subpixel,
            self.bounds,
            self.constraint,
            self.verbose,
        )

    def __deepcopy__(self, memo: dict = None) -> "EMEModel":
        return EMEModel(
            self.eme_grid_spec,
            self.medium,
            libcopy.deepcopy(self.symmetry),
            libcopy.deepcopy(self.monitors),
            libcopy.deepcopy(self.structures),
            self.grid_spec,
            self.subpixel,
            libcopy.deepcopy(self.bounds),
            self.constraint,
            self.verbose,
        )

    def __str__(self) -> str:
        return "EMEModel"

    def __repr__(self) -> str:
        return (
            f"EMEModel(eme_grid_spec={self.eme_grid_spec!r}, medium={self.medium!r}, "
            f"symmetry={self.symmetry!r}, monitors={self.monitors!r}, "
            f"structures={self.structures!r}, grid_spec={self.grid_spec!r}, "
            f"subpixel={self.subpixel!r}, bounds={self.bounds!r}, constraint={self.constraint!r}, "
            f"verbose={self.verbose!r})"
        )

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, EMEModel) and self.as_bytes == other.as_bytes

    @staticmethod
    def clear_cache() -> None:
        """Clear the runtime cache for EME and mode simulations, but not the file cache."""
        _EMEModelRunner.cache.clear()
        tidy3d_model._ModeSolverRunner.cache.clear()

    @staticmethod
    def cache_size(size: Optional[int] = None) -> int:
        """Get/set the runtime cache size for EME and mode simulations.

        Args:
            size: Set a new cache size. A negative value removes the size
              limit.

        Returns:
            Current cache size.
        """
        if size is None:
            size = max(_EMEModelRunner.cache.size, tidy3d_model._ModeSolverRunner.cache.size)
        _EMEModelRunner.cache.size = size
        tidy3d_model._ModeSolverRunner.cache.size = size
        return size

    def data_path_for(self, component: Component) -> pathlib.Path:
        return _cache_path(_safe_hash(component.name.encode("utf-8")))

    def data_file_for(self, component: Component) -> Optional[pathlib.Path]:
        result = EMEModel._data_cache.get(component.as_bytes, None)
        if not result:
            raise RuntimeError(
                "No data found in runtime cache. Please run the model for this component before "
                "trying to load the simulation data to populate the cache."
            )
        return result

    def simulation_data_for(self, component: Component) -> Optional[tidy3d.EMESimulationData]:
        """Return the EME simulation data for a given component."""
        data_file = self.data_file_for(component)
        if data_file.is_file():
            return tidy3d.EMESimulationData.from_file(str(data_file))
        return None

    @staticmethod
    def _group_ports(ports: dict[str, Port]) -> tuple[int, tuple[tuple[str], tuple[str]]]:
        port_groups = {}
        for name, port in ports.items():
            if not isinstance(port, Port):
                warnings.warn(
                    f"EMEModel only works with Port instances. Port named '{name}'"
                    f"of type {type(port)} will be ignored.",
                    RuntimeWarning,
                    2,
                )
                continue
            fraction = port.input_direction % 90
            if fraction > 1e-12 and 90 - fraction > 1e-12:
                raise RuntimeError(f"Input direction of port '{name}' is not a multiple of 90°.")
            direction = round(port.input_direction % 360) // 90
            coordinate = port.center[direction % 2]
            key = (coordinate, direction)
            port_groups[key] = port_groups.get(key, ()) + (name,)

        if len(port_groups) == 1:
            key, group = next(iter(port_groups.items()))
            if key < 2:
                return (key[1], (group, ()))
            else:
                return (key[1] - 2, ((), group))

        if len(port_groups) == 2:
            key0, key1 = sorted(port_groups)
            if key1[1] - key0[1] == 2 and key0[0] < key1[0]:
                return (key0[1], (port_groups[key0], port_groups[key1]))

        raise RuntimeError(
            "Component ports need to be placed at 2 opposite sides, facing each other. Multiple "
            "ports on each side are allowed as long as they are aligned in the normal direction."
        )

    def get_simulation(
        self, component: Component, frequencies: Sequence[float]
    ) -> tuple[tidy3d.EMESimulation, tuple[tuple[str], tuple[str]]]:
        """Create an EME simulation for a component.

        Args:
            component: Instance of Component for calculation.
            frequencies: Sequence of frequencies for the simulation.

        Returns:
            EME simulation and 2 tuples with the names of the ports on each side of the domain.
        """
        # TODO:
        # calculate port_offset from simulation bounds and port positions
        # _EMEModelRunner has to create the mode solver simulations to project the output

        ports = component.ports
        axis, port_groups = self._group_ports(ports)

        frequencies = numpy.array(frequencies, dtype=float, ndmin=1)
        fmin = frequencies.min()
        fmax = frequencies.max()
        fmed = 0.5 * (fmin + fmax)
        max_wavelength = C_0 / fmin
        min_wavelength = C_0 / fmax

        medium = component.technology.background_medium if self.medium is None else self.medium

        grid_spec = (
            self.grid_spec
            if isinstance(self.grid_spec, tidy3d.GridSpec)
            else tidy3d.GridSpec.auto(
                wavelength=min_wavelength,
                min_steps_per_wvl=config.default_mesh_refinement
                if self.grid_spec is None
                else self.grid_spec,
            )
        )

        extrusion_tolerance = 0
        if isinstance(grid_spec.grid_z, tidy3d.AutoGrid):
            grid_lda = min_wavelength if grid_spec.wavelength is None else grid_spec.wavelength
            n_max = tidy3d_model._get_max_refractive_index(
                component.technology.extrusion_specs, medium, fmed
            )
            extrusion_tolerance = grid_lda / (grid_spec.grid_z.min_steps_per_wvl * n_max)
        elif isinstance(grid_spec.grid_z, tidy3d.UniformGrid):
            extrusion_tolerance = grid_spec.grid_z.dl
        elif isinstance(grid_spec.grid_z, tidy3d.CustomGrid) and len(grid_spec.grid_z.dl) > 0:
            extrusion_tolerance = min(grid_spec.grid_z.dl)

        (xmin, ymin), (xmax, ymax) = component.bounds()
        structures = [
            struct.to_tidy3d()
            for struct in component.extrude(
                0.5 * max_wavelength + max(xmax - xmin, ymax - ymin),
                extrusion_tolerance=extrusion_tolerance,
            )
        ]

        # Sort to improve caching, but don't reorder different media
        i = 0
        while i < len(structures):
            current_medium = structures[i].medium
            j = i + 1
            while j < len(structures) and structures[j].medium == current_medium:
                j += 1
            # Even if j == i + 1 we want to sort internal geometries
            structures[i:j] = (
                tidy3d.Structure(geometry=geometry, medium=current_medium)
                for geometry in sorted(
                    [tidy3d_model._inner_geometry_sort(s.geometry) for s in structures[i:j]],
                    key=tidy3d_model._geometry_key,
                )
            )
            i = j

        # Simulation bounds
        zmin = 1e30
        zmax = -1e30
        for name in port_groups[0] + port_groups[1]:
            source = ports[name].to_tidy3d_source(frequencies)
            xmin = min(xmin, source.bounds[0][0])
            ymin = min(ymin, source.bounds[0][1])
            zmin = min(zmin, source.bounds[0][2])
            xmax = max(xmax, source.bounds[1][0])
            ymax = max(ymax, source.bounds[1][1])
            zmax = max(zmax, source.bounds[1][2])
        for s in structures:
            for i in range(2):
                lim = s.geometry.bounds[i][2]
                if -Z_MAX <= lim <= Z_MAX:
                    zmin = min(zmin, lim)
                    zmax = max(zmax, lim)
        if zmin > zmax:
            raise RuntimeError("No valid extrusion elements present in the component.")

        bounds = numpy.array(((xmin, ymin, zmin), (xmax, ymax, zmax)))

        # Bounds override
        for i in range(3):
            if self.bounds[0][i] is not None:
                bounds[0, i] = self.bounds[0][i]
                j = 0
                while j < len(structures):
                    if structures[j].geometry.bounds[1][i] < bounds[0, i]:
                        structures.pop(j)
                    else:
                        j += 1
            if self.bounds[1][i] is not None:
                bounds[1, i] = self.bounds[1][i]
                j = 0
                while j < len(structures):
                    if structures[j].geometry.bounds[0][i] > bounds[1, i]:
                        structures.pop(j)
                    else:
                        j += 1

        port_offsets = []
        safe_margin = min_wavelength / 4
        for i in range(2):
            sign = 2 * i - 1
            if len(port_groups[i]) > 0:
                port_offset = sign * (bounds[i][axis] - ports[port_groups[i][0]].center[axis])
                if port_offset < safe_margin:
                    port_offset = safe_margin
                    bounds[i][axis] = ports[port_groups[i][0]].center[axis] + sign * safe_margin
            else:
                port_offset = 0
            port_offsets.append(port_offset)

        center = tuple(bounds.mean(axis=0))
        size = tuple(bounds[1] - bounds[0])

        eme_simulation = tidy3d.EMESimulation(
            freqs=frequencies,
            center=center,
            size=size,
            medium=medium,
            symmetry=self.symmetry,
            structures=structures + list(self.structures),
            monitors=list(self.monitors),
            grid_spec=grid_spec,
            eme_grid_spec=self.eme_grid_spec,
            subpixel=self.subpixel,
            axis=axis,
            port_offsets=port_offsets,
            constraint=self.constraint,
        )

        return eme_simulation, port_groups

    def start(
        self,
        component: Component,
        frequencies: Sequence[float],
        **kwargs,
    ) -> _EMEModelRunner:
        """Start computing the S matrix response from a component.

        Args:
            component: Component from which to compute the S matrix.
            frequencies: Sequence of frequencies at which to perform the
              computation.
            **kwargs: Unused.

        Returns:
            Result object with attributes ``status`` and ``s_matrix``.

        Important:
            When using geometry symmetry, the mode numbering in ``inputs``
            is relative to the solver run *with the symmetry applied*, not
            the mode number presented in the final S matrix.
        """
        simulation, port_groups = self.get_simulation(component, frequencies)
        folder_name = _filename_cleanup(component.name)

        mesh_refinement = (
            config.default_mesh_refinement
            if self.grid_spec is None or isinstance(self.grid_spec, tidy3d.GridSpec)
            else self.grid_spec
        )

        if len(folder_name) == 0:
            folder_name = "default"
        result = _EMEModelRunner(
            simulation=simulation,
            ports=component.ports,
            port_groups=port_groups,
            mesh_refinement=mesh_refinement,
            technology=component.technology,
            folder_name=folder_name,
            data_path=self.data_path_for(component),
            verbose=self.verbose,
        )

        if isinstance(result.runners[0], tidy3d_model._Tidy3DTaskRunner):
            EMEModel._data_cache[component.as_bytes] = result.runners[0].data_file()

        return result

    @property
    def as_bytes(self) -> bytes:
        """Serialize this model."""
        obj = {
            "eme_grid_spec": tidy3d_model._convert_arrays(self.eme_grid_spec.dict()),
            "symmetry": self.symmetry,
            "subpixel": self.subpixel,
            "bounds": self.bounds,
            "constraint": self.constraint,
            "verbose": self.verbose,
        }

        if self.medium is not None:
            obj["medium"] = json.loads(self.medium.json())
        if len(self.monitors) > 0:
            obj["monitors"] = [m.dict() for m in self.monitors]
        if len(self.structures) > 0:
            obj["structures"] = [tidy3d_model._convert_arrays(s.dict()) for s in self.structures]
        if self.grid_spec is not None:
            obj["grid_spec"] = (
                self.grid_spec.dict()
                if isinstance(self.grid_spec, tidy3d.GridSpec)
                else self.grid_spec
            )

        # Note: keys are sorted to guarantee the representation is consistent for caching
        return zlib.compress(json.dumps(obj, sort_keys=True).encode("utf-8"))

    @classmethod
    def from_bytes(cls, byte_repr: bytes) -> "EMEModel":
        """De-serialize this model."""
        obj = json.loads(zlib.decompress(byte_repr).decode("utf-8"))

        for field, field_type in [
            ("eme_grid_spec", tidy3d.components.eme.grid.EMESubgridType),
            ("medium", tidy3d.components.medium.MediumType3D),
        ]:
            if obj.get(field, None) is not None:
                obj[field] = pydantic.v1.parse_obj_as(
                    field_type, obj[field], type_name=obj[field]["type"]
                )

        if isinstance(obj.get("grid_spec", None), dict):
            obj["grid_spec"] = pydantic.v1.parse_obj_as(
                tidy3d.GridSpec,
                obj["grid_spec"],
                type_name=obj["grid_spec"]["type"],
            )

        obj["monitors"] = [
            pydantic.v1.parse_obj_as(
                tidy3d.components.monitor.MonitorType, mon, type_name=mon["type"]
            )
            for mon in obj.get("monitors", ())
        ]

        obj["structures"] = [
            pydantic.v1.parse_obj_as(tidy3d.Structure, s, type_name=s["type"])
            for s in obj.get("structures", ())
        ]

        return cls(**obj)


register_model_class(EMEModel)
