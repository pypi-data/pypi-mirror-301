# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from datetime import datetime
from os import PathLike
from typing import Optional, Union

from ._client import get_default_client
from ._helpers import (
    create_geometry,
    create_simulation,
    timestamp_to_datetime,
    upload_mesh,
    simulation_params_from_json_path,
)
from ._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb
from ._proto.api.v0.luminarycloud.mesh import mesh_pb2 as meshpb
from ._proto.api.v0.luminarycloud.project import project_pb2 as projectpb
from ._proto.api.v0.luminarycloud.simulation import simulation_pb2 as simulationpb
from ._proto.api.v0.luminarycloud.simulation_template import (
    simulation_template_pb2 as simtemplatepb,
)
from ._proto.client.simulation_pb2 import SimulationParam
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from .enum import MeshType
from .geometry import Geometry
from .mesh import Mesh, MeshAdaptationParameters
from .simulation import Simulation
from .simulation_template import SimulationTemplate


@ProtoWrapper(projectpb.Project)
class Project(ProtoWrapperBase):
    """Represents a Project object."""

    id: str
    name: str
    description: str
    storage_usage_bytes: int

    _proto: projectpb.Project

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.update_time)

    def update(
        self,
        *,
        name: str = "",
        description: str = "",
    ) -> None:
        """
        Update/Edit project attributes.

        Mutates self.

        Parameters
        ----------
        name : str, optional
            New project name.
        description : str, optional
            New project description.
        """
        req = projectpb.UpdateProjectRequest(
            id=self.id,
            name=name,
            description=description,
        )
        res = get_default_client().UpdateProject(req)
        self._proto = res.project

    def delete(self) -> None:
        """
        Delete the project.
        """
        req = projectpb.DeleteProjectRequest(
            id=self.id,
        )
        get_default_client().DeleteProject(req)

    def create_geometry(
        self,
        cad_file_path: PathLike,
        *,
        name: Optional[str] = None,
        scaling: Optional[float] = None,
        wait: bool = False,
    ) -> Geometry:
        """
        Create a new geometry in the project by uploading a supported CAD file.

        For more information on supported formats and best practices, see:
        https://docs.luminarycloud.com/en/articles/9274255-upload-cad

        Parameters
        ----------
        cad_file_path : PathLike or str
            Path or URL to the CAD file to upload.

        Other Parameters
        ----------------
        name : str, optional
            Name of the geometry on Luminary Cloud. A default name will be used
            if unset.
        scaling : float, optional
            Scaling to apply to the source CAD file upon import. Defaults to 1.0
            if unset.
        wait : bool, optional
            If set to True, this function will block until the geometry import
            completes. Otherwise, it will return immediately and the import will
            occur in the background. Defaults to False.

        Returns
        -------
        Geometry
            The newly created Geometry.
        """
        _geometry = create_geometry(
            get_default_client(),
            project_id=self.id,
            cad_file_path=cad_file_path,
            name=name,
            scaling=scaling,
            wait=wait,
        )
        return Geometry(_geometry)

    def list_geometries(self) -> list[Geometry]:
        """
        List all geometries in project.

        Returns
        -------
        list[Geometry]
            A list of all available Geometries in the project.
        """
        req = geometrypb.ListGeometriesRequest(project_id=self.id)
        res: geometrypb.ListGeometriesResponse = get_default_client().ListGeometries(req)
        return [Geometry(g) for g in res.geometries]

    def upload_mesh(
        self,
        path: Union[PathLike, str],
        *,
        name: Optional[str] = None,
        scaling: Optional[float] = None,
        chunk_size: Optional[int] = None,
        mesh_type: Optional[MeshType] = None,
        do_not_read_zones_openfoam: Optional[bool] = None,
    ) -> Mesh:
        """
        Upload a mesh to the project.

        For more information on supported formats and best practices see:
        https://docs.luminarycloud.com/en/articles/9275233-upload-a-mesh

        Parameters
        ----------
        path : pathlike or str
            Path or URL to the mesh file to upload.

        Other Parameters
        ----------------
        name : str, optional
            Name of the mesh resource on Luminary Cloud. Defaults to
            the filename without the extension.
        scaling : float, optional
            If set, apply a scaling factor to the mesh.
        chunk_size : int, optional
            Number of bytes per uploaded chunk. Default size is 1 MB.
        mesh_type : MeshType, optional
            The file format of the mesh file. Required for OpenFOAM format.
        do_not_read_zones_openfoam : bool, default False
            If true, disables reading cell zones in the polyMesh/cellZones file
            for OpenFOAM meshes.
        """
        _mesh = upload_mesh(
            get_default_client(),
            project_id=self.id,
            path=path,
            mesh_type=mesh_type,
            name=name,
            scaling=scaling,
            chunk_size=chunk_size,
            do_not_read_zones_openfoam=do_not_read_zones_openfoam,
        )
        return Mesh(_mesh)

    def create_mesh(
        self,
        *,
        name: str,
        adaptation_params: MeshAdaptationParameters,
    ) -> Mesh:
        """
        Create a new mesh in the project.

        Parameters
        ----------
        name : str
            (Optional) Mesh name. Max 256 characters.
        adaptation_params : MeshAdaptationParameters
            (Required) Should be specified if creating a new mesh via mesh
            adaptation. Note: this parameter will become optional in the future
            when additional ways of creating a mesh are supported.
        """
        req = meshpb.CreateMeshRequest(
            project_id=self.id, name=name, mesh_adaptation_params=adaptation_params._to_proto()
        )
        res = get_default_client().CreateMesh(req)
        return Mesh(res.mesh)

    def list_meshes(self) -> list[Mesh]:
        """
        List all meshes in project.
        """
        req = meshpb.ListMeshesRequest(project_id=self.id)
        res = get_default_client().ListMeshes(req)
        return [Mesh(m) for m in res.meshes]

    def create_simulation(
        self,
        mesh_id: str,
        name: str,
        simulation_template_id: str,
        *,
        description: str = "",
        batch_processing: bool = False,
    ) -> Simulation:
        """
        Create a new simulation.

        Parameters
        ----------
        mesh_id : str
            Mesh ID.
        name : str
            Simulation name. If empty, a default name will be generated.
        simulation_template_id : str
            ID of the SimulationTemplate used to set up the simulation.

        Other Parameters
        ----------------
        description : str, optional
            Simulation description.
        batch_processing : bool, default False
            If True, batch processing will be used for this
            simulation.
            Use Batch Processing on simulations that are not time-sensitive to
            save up to 65% in credits.
        """
        _simulation = create_simulation(
            get_default_client(),
            self.id,
            mesh_id,
            name,
            simulation_template_id,
            description=description,
            batch_processing=batch_processing,
        )
        return Simulation(_simulation)

    def list_simulations(self) -> list[Simulation]:
        """
        List all simulations in project.
        """
        req = simulationpb.ListSimulationsRequest(project_id=self.id)
        res = get_default_client().ListSimulations(req)
        return [Simulation(s) for s in res.simulations]

    def list_simulation_templates(self) -> list[SimulationTemplate]:
        """
        List all simulation templates in project.
        """
        req = simtemplatepb.ListSimulationTemplatesRequest(project_id=self.id)
        res = get_default_client().ListSimulationTemplates(req)
        return [SimulationTemplate(s) for s in res.simulation_templates]

    def create_simulation_template(
        self,
        name: str,
        *,
        parameters: Optional[SimulationParam] = None,
        params_json_path: Optional[PathLike] = None,
    ) -> SimulationTemplate:
        """
        Create a new simulation template object.

        Parameters
        ----------
        name : str
            Human-readable name to identify the template.
            Does not need to be unique. Max 256 characters.

        Other Parameters
        ----------------
        parameters : SimulationParam, optional
            Complete simulation parameters. Ignored if `params_json_path` is set.
        params_json_path : path-like, optional
            Path to local JSON file containing simulation params.
        """
        if params_json_path is not None:
            parameters = simulation_params_from_json_path(params_json_path)
        req = simtemplatepb.CreateSimulationTemplateRequest(
            project_id=self.id, name=name, parameters=parameters
        )
        res = get_default_client().CreateSimulationTemplate(req)
        return SimulationTemplate(res.simulation_template)


def create_project(
    name: str,
    description: str = "",
) -> Project:
    """
    Create a project owned by the user.

    Parameters
    ----------
    name : str
        Project name.
    description : str
        Project description.
    """
    req = projectpb.CreateProjectRequest(name=name, description=description)
    res = get_default_client().CreateProject(req)
    return Project(res.project)


def get_project(
    id: str,
) -> Project:
    """
    Get a specific project by ID.

    Parameters
    ----------
    id : str
        Project ID.
    """
    req = projectpb.GetProjectRequest(id=id)
    res = get_default_client().GetProject(req)
    return Project(res.project)


def list_projects() -> list[Project]:
    """
    List projects accessible by the user.
    """
    req = projectpb.ListProjectsRequest()
    res = get_default_client().ListProjects(req)
    return [Project(p) for p in res.projects]
