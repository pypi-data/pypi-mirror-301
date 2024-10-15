# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from luminarycloud._proto.api.v0.luminarycloud.geometry import geometry_pb2 as geometrypb
from luminarycloud._proto.upload import upload_pb2 as uploadpb
from os import PathLike
from .._client import Client
from .upload import gcs_resumable_upload
from typing import Any, Optional
from luminarycloud._helpers import util

import logging

logger = logging.getLogger(__name__)


def create_geometry(
    client: Client,
    cad_file_path: PathLike,
    project_id: str,
    *,
    name: Optional[str] = None,
    scaling: Optional[float] = None,
    wait: bool = False,
    upload_method: Any = uploadpb.METHOD_GCS_RESUMABLE,  # TODO: define enum types like other enums in SDK
) -> geometrypb.Geometry:

    cad_file_meta = util.get_file_metadata(cad_file_path)
    logger.info(
        f"creating geometry in {project_id} by uploading file: {cad_file_meta.name}.{cad_file_meta.ext}, "
        + f"size: {cad_file_meta.size} bytes, sha256: {cad_file_meta.sha256_checksum}, "
        + f"crc32c: {cad_file_meta.crc32c_checksum}"
    )

    # create upload
    create_upload_res: uploadpb.CreateUploadReply = client.CreateUpload(
        uploadpb.CreateUploadRequest(
            project_id=project_id,
            file_meta=cad_file_meta,
        )
    )
    upload_id = create_upload_res.upload.id
    logger.debug(f"created upload: {upload_id}")

    # start upload
    start_res: uploadpb.StartUploadReply = client.StartUpload(
        uploadpb.StartUploadRequest(upload_id=upload_id, method=upload_method)
    )
    logger.debug(f"started upload with method: {upload_method}")

    if upload_method == uploadpb.METHOD_GCS_RESUMABLE:
        # upload data
        gcs_resumable_upload(
            filepath=cad_file_path,
            signed_url=start_res.upload.gcs_resumable.signed_url,
            http_headers=start_res.upload.gcs_resumable.http_headers,
        )
        logger.debug(f"successfully uploaded data")
    else:
        raise NotImplementedError("only METHOD_GCS_RESUMABLE is supported")

    # finish upload
    finish_res: uploadpb.FinishUploadReply = client.FinishUpload(
        uploadpb.FinishUploadRequest(upload_id=upload_id)
    )
    logger.debug(f"finished upload")

    # create geometry
    if name is None:
        # if the caller did not provide a name, use the file name
        name = cad_file_meta.name
    if scaling is None:
        # default to no scaling
        scaling = 1.0
    create_geo_res: geometrypb.CreateGeometryResponse = client.CreateGeometry(
        geometrypb.CreateGeometryRequest(
            project_id=project_id, name=name, url=finish_res.url, scaling=scaling, wait=wait
        )
    )
    geo = create_geo_res.geometry
    logger.info(f"created geometry {geo.name} ({geo.id})")
    return geo
