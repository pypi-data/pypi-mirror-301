# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import cgi
import io
import logging
import os
import requests
from tempfile import TemporaryDirectory
from typing import cast, Optional, Union
from urllib.parse import urlparse

from luminarycloud._helpers import util
from luminarycloud._helpers.util import _chunker

from ..enum import MeshType
from .._proto.api.v0.luminarycloud.common import common_pb2 as commonpb
from .._proto.api.v0.luminarycloud.mesh.mesh_pb2 import Mesh, UploadMeshRequest, UploadMeshResponse
from .._client import Client

logger = logging.getLogger(__name__)

_EXTENSION_TO_MESH_TYPE = {
    ".cgns": MeshType.CGNS,
    ".ansys": MeshType.ANSYS,
    ".lcmesh": MeshType.UNSPECIFIED,
}


def _deduce_mesh_type(path: Union[os.PathLike, str]) -> MeshType:
    """
    Deduce mesh type for the file at the given path.

    Currently, only uses the file extension to deduce type.

    Parameters
    ----------
    path: PathLike or str
        The relative or absolute file path of the mesh file.

    Returns
    -------
    MeshType
        The deduced mesh file format type. If the type cannot be deduced, returns
        MeshType.UNSPECIFIED.
    """
    _, file_ext = os.path.splitext(path)
    return _EXTENSION_TO_MESH_TYPE.get(file_ext, MeshType.UNSPECIFIED)


def _upload_mesh_from_stream(
    client: Client,
    binary_stream: io.BufferedIOBase,
    project_id: str,
    filename: str,
    size: int,
    sha256checksum: bytes,
    mesh_type: MeshType,
    *,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    chunk_size: Optional[int] = None,
    do_not_read_zones_openfoam: Optional[bool] = None,
) -> UploadMeshResponse:
    """
    Upload mesh from a binary stream.

    Parameters
    ----------
    client: Client
        A LuminaryCloud Client (see client.py)
    binary_stream: io.BufferedIOBase
        A fresh read stream of the mesh file to upload
    project_id: str
        The ID of the project to upload the mesh under
    filename: str
        The filename of the mesh. Must include the appropriate filename extension.
    size: int
        The size of the stream to be read
    sha256checksum: str
        The digest of the mesh file to upload
    mesh_type : MeshType
        The file format of the mesh file.
    name: str
        (Optional) the name of the mesh resource on Luminary Cloud. defaults to the filename
        (without the extension).
    chunk_size: int
        (Optional) the default size is 1MB.
    do_not_read_zones_openfoam : bool
        (Optional) If true, disables reading cell zones in the polyMesh/cellZones file
        for OpenFOAM meshes. Default false.
    """

    assert size > 0, "stream size must be positive"
    fparts = filename.split(".", maxsplit=1)
    if len(fparts) < 2:
        logger.error("Filename is missing extension.")
        raise ValueError("Filename is missing an extension.")
    mesh_name, file_ext = fparts
    if name is not None:
        mesh_name = cast(str, name)
    logger.debug(f"Uploading mesh with name '{mesh_name}' and extension '{file_ext}'.")

    logger.debug("Uploading chunks.")
    response = None
    next_upload_token = ""
    file_metadata = commonpb.FileMetadata(
        name=mesh_name, ext=file_ext, size=size, sha256_checksum=sha256checksum
    )
    for offset, chunk in _chunker(binary_stream, chunk_size):
        req = UploadMeshRequest(
            project_id=project_id,
            name=mesh_name,
            upload_token=next_upload_token,
            file_chunk=commonpb.FileChunk(
                metadata=file_metadata,
                bytes=commonpb.ByteChunk(
                    start_offset=offset,
                    data=chunk,
                ),
            ),
            mesh_type=mesh_type,
        )
        if scaling is not None:
            req.scaling = cast(float, scaling)
        if do_not_read_zones_openfoam is not None:
            req.do_not_read_zones_openfoam = do_not_read_zones_openfoam
        response = client.UploadMesh(req)
        next_upload_token = response.upload_token

    if response is None:
        logger.error("Stream is empty.")
        raise ValueError("Empty stream")

    return cast(UploadMeshResponse, response)


def _is_valid_upload_url(path: Union[os.PathLike, str]) -> bool:
    parsed = urlparse(str(path))
    return parsed.scheme in ("http", "https")


def upload_mesh_from_local_file(
    client: Client,
    project_id: str,
    path: Union[os.PathLike, str],
    *,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    chunk_size: Optional[int] = None,
    mesh_type: Optional[MeshType] = None,
    do_not_read_zones_openfoam: Optional[bool] = None,
) -> Mesh:
    """
    Upload a mesh from a local file.

    The mesh file format is inferred from the filename extension.
    For supported formats, see: https://docs.luminarycloud.com/en/articles/9275233-upload-a-mesh

    Parameters
    ----------
    client: Client
        A LuminaryCloud Client (see client.py)
    project_id: str
        The ID of the project to upload the mesh under
    path: PathLike or str
        The relative or absolute file path of the mesh file to upload.
    name: str
        (Optional) the name of the mesh resource on Luminary Cloud. defaults to the filename
        (without the extension).
    chunk_size: int
        (Optional) the default size is 1MB.
    mesh_type : MeshType
        (Optional) The file format of the mesh file.
    do_not_read_zones_openfoam : bool
        (Optional) If true, disables reading cell zones in the polyMesh/cellZones file
        for OpenFOAM meshes. Default false.
    """
    if not os.path.exists(path):
        logger.error("File not found.")
        raise FileNotFoundError

    if mesh_type is None:
        mesh_type = _deduce_mesh_type(path)

    with open(path, "rb") as fp:
        response = _upload_mesh_from_stream(
            client,
            fp,
            project_id,
            os.path.basename(path),
            os.path.getsize(path),
            util.digest_sha256(path),
            mesh_type,
            name=name,
            scaling=scaling,
            chunk_size=chunk_size,
            do_not_read_zones_openfoam=do_not_read_zones_openfoam,
        )

    return response.mesh


def upload_mesh_from_url(
    client: Client,
    project_id: str,
    url: str,
    *,
    timeout: int = 5,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    chunk_size: Optional[int] = None,
    mesh_type: Optional[MeshType] = None,
    do_not_read_zones_openfoam: Optional[bool] = None,
) -> Mesh:
    """
    Upload a mesh from a URL.

    The mesh file format is inferred from the filename extension.
    For supported formats, see: https://docs.luminarycloud.com/en/articles/9275233-upload-a-mesh

    Parameters
    ----------
    client: Client
        A LuminaryCloud Client (see client.py)
    project_id: str
        The ID of the project to upload the mesh under
    url: str
        The url of the mesh file.
    timeout: int
        (Optional) timeout (in seconds) for the download request.
    name: str
        (Optional) the name of the mesh resource on Luminary Cloud. defaults to the filename
        (without the extension).
    chunk_size: int
        (Optional) the default size is 1MB.
    mesh_type: MeshType
        (Optional) the file format of the mesh file.
    do_not_read_zones_openfoam : bool
        (Optional) If true, disables reading cell zones in the polyMesh/cellZones file
        for OpenFOAM meshes. Default false.
    """
    if chunk_size is None:
        chunk_size = util.DEFAULT_CHUNK_SIZE_BYTES

    logger.debug("Creating temporary directory.")
    with TemporaryDirectory() as tmpdir:
        logger.debug(f"Created temporary directory: {tmpdir}")
        logger.debug("Initiating download request.")
        with requests.get(url, stream=True, timeout=timeout) as r:
            r = cast(requests.Response, r)
            r.raise_for_status()
            logger.debug("Successfully started streaming download.")
            try:
                header = r.headers["Content-Disposition"]
                value, params = cgi.parse_header(header)
                if value != "attachment":
                    raise Exception("Expected header Content-Disposition: attachment")
                filename = params["filename"]
                logger.debug(f"Got filename from Content-Disposition header: {filename}")
            except Exception as e:
                logger.warning("Failed to get filename from headers.", exc_info=e)
                filename = os.path.basename(urlparse(url).path)
                logger.debug(f"Got filename from basename of download URL: {filename}")
            filepath = os.path.join(tmpdir, filename)
            logger.debug(f"Creating file: {filepath}.")
            with open(filepath, "wb") as f:
                logger.debug(f"Writing stream to file: {filepath}")
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
        return upload_mesh_from_local_file(
            client,
            project_id,
            filepath,
            name=name,
            scaling=scaling,
            chunk_size=chunk_size,
            mesh_type=mesh_type,
            do_not_read_zones_openfoam=do_not_read_zones_openfoam,
        )


def upload_mesh(
    client: Client,
    project_id: str,
    path: Union[os.PathLike, str],
    *,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    chunk_size: Optional[int] = None,
    mesh_type: Optional[MeshType] = None,
    do_not_read_zones_openfoam: Optional[bool] = None,
) -> Mesh:
    """
    Upload a mesh from a local file or a URL.

    Parameters
    ----------
    client: Client
        A LuminaryCloud Client (see client.py)
    project_id: str
        The ID of the project to upload the mesh under
    path: PathLike or str
        The URL or file path of the mesh file to upload.
    name: str
        (Optional) the name of the mesh resource on Luminary Cloud. defaults to the filename
        (without the extension).
    chunk_size: int
        (Optional) the default size is 1MB.
    mesh_type : MeshType
        (Optional) the file format of the mesh file.
    do_not_read_zones_openfoam : bool
        (Optional) If true, disables reading cell zones in the polyMesh/cellZones file
        for OpenFOAM meshes. Default false.
    """
    if _is_valid_upload_url(path):
        logger.info(f"Attempting to upload mesh from URL: {path}")
        return upload_mesh_from_url(
            client,
            project_id,
            str(path),
            name=name,
            scaling=scaling,
            chunk_size=chunk_size,
            mesh_type=mesh_type,
            do_not_read_zones_openfoam=do_not_read_zones_openfoam,
        )
    else:
        logger.info(f"Attempting to upload mesh from local file: {path}")
        return upload_mesh_from_local_file(
            client,
            project_id,
            path,
            name=name,
            scaling=scaling,
            chunk_size=chunk_size,
            mesh_type=mesh_type,
            do_not_read_zones_openfoam=do_not_read_zones_openfoam,
        )
