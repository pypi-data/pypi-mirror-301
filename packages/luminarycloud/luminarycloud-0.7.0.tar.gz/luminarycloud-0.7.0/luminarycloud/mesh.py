# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from datetime import datetime
from ._wrapper import ProtoWrapper, ProtoWrapperBase
from ._client import get_default_client
from ._helpers.timestamp_to_datetime import timestamp_to_datetime
from ._helpers.wait_for_mesh import wait_for_mesh
from .enum import MeshStatus
from ._proto.api.v0.luminarycloud.mesh import mesh_pb2 as meshpb


@ProtoWrapper(meshpb.Mesh)
class Mesh(ProtoWrapperBase):
    """Represents a Mesh object."""

    id: str
    "Mesh ID."
    name: str
    "Mesh name."
    status: MeshStatus
    "Mesh status. May not reflect the current status."

    _proto: meshpb.Mesh

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    def update(
        self,
        *,
        name: str = "",
    ) -> None:
        """
        Update mesh attributes.

        Mutates self.

        Parameters
        ----------
        name : str
            New mesh name, maximum length of 256 characters.
        """
        req = meshpb.UpdateMeshRequest(
            id=self.id,
            name=name,
        )
        res: meshpb.UpdateMeshResponse = get_default_client().UpdateMesh(req)
        self._proto = res.mesh

    def wait(
        self,
        *,
        interval_seconds: float = 5,
        timeout_seconds: float = float("inf"),
    ) -> MeshStatus:
        """
        Wait until the mesh has either completed or failed processing.

        Parameters
        ----------
        interval_seconds : float, optional
            Number of seconds between polls. Default is 5 seconds.
        timeout_seconds : float, optional
            Number of seconds before timeout.

        Returns
        -------
        luminarycloud.enum.MeshStatus
            Current status of the mesh.
        """
        wait_for_mesh(
            get_default_client(),
            self._proto,
            interval_seconds=interval_seconds,
            timeout_seconds=timeout_seconds,
        )
        self._proto = get_mesh(self.id)._proto
        return self.status

    def delete(self) -> None:
        """
        Delete the mesh.
        """
        req = meshpb.DeleteMeshRequest(
            id=self.id,
        )
        get_default_client().DeleteMesh(req)


class MeshAdaptationParameters:
    """
    Parameters used to create a new mesh with mesh adaptation.

    Attributes
    ----------
    source_simulation_id : str
        (Required) The simluation ID of a previously completed simulation. The
        source simulation will be used to extract the input mesh and mesh
        adaptation sensor from the solution.

    target_cv_count : int
        (Required) Target count of mesh CVs.

    h_ratio : float
        (Required) Boundary layer scaling.
    """

    source_simulation_id: str
    target_cv_count: int
    h_ratio: float

    def __init__(self, source_simulation_id: str, target_cv_count: int, h_ratio: float) -> None:
        self.source_simulation_id = source_simulation_id
        self.target_cv_count = target_cv_count
        self.h_ratio = h_ratio

    def _to_proto(self) -> meshpb.CreateMeshRequest.MeshAdaptationParams:
        return meshpb.CreateMeshRequest.MeshAdaptationParams(
            source_simulation_id=self.source_simulation_id,
            target_cv_count=self.target_cv_count,
            h_ratio=self.h_ratio,
        )


def get_mesh(id: str) -> Mesh:
    """
    Get a specific mesh with the given ID.

    Parameters
    ----------
    id : str
        Mesh ID.
    """
    req = meshpb.GetMeshRequest(id=id)
    res = get_default_client().GetMesh(req)
    return Mesh(res.mesh)


def get_mesh_metadata(id: str) -> meshpb.MeshMetadata:
    """
    Returns the mesh metadata of a specific mesh with the given ID.

    Parameters
    ----------
    id : str
        Mesh ID.
    """
    res: meshpb.GetMeshMetadataResponse = get_default_client().GetMeshMetadata(
        meshpb.GetMeshMetadataRequest(id=id)
    )
    return res.mesh_metadata
