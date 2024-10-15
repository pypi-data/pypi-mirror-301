# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from os import PathLike
import os
from typing import Mapping
import requests
import logging

logger = logging.getLogger(__name__)


def gcs_resumable_upload(
    filepath: PathLike, signed_url: str, http_headers: Mapping[str, str]
) -> None:
    """
    Performs a resumable upload to a GCS signed url.
    Based on: https://cloud.google.com/storage/docs/performing-resumable-uploads
    TODO(LC-19950): add retries and multi-chunk uploads (https://cloud.google.com/storage/docs/performing-resumable-uploads#chunked-upload)
    """

    # initiate the upload
    try:
        post_res = requests.post(
            url=signed_url,
            headers=http_headers,
            json={},  # intentionally empty, we're not uploading the file data yet
        )
        logger.debug(
            f"sucessfully initialized signed URL upload for {filepath}, POST status code: {post_res.status_code}"
        )
    except:
        # don't log the signed_url, just to be safe
        msg = (
            f"failed to initialize signed URL upload for {filepath}, POST status code: {post_res.status_code}, content: "
            + str(post_res.content)
        )
        logger.error(msg)
        raise Exception(msg)

    # upload the file
    try:
        # we need to grab the session_uri from the response; this will be the URL we
        # use to actually PUT the data
        session_uri = post_res.headers["Location"]
        size = os.path.getsize(filepath)
        with open(filepath, "rb") as fp:
            put_res = requests.put(
                url=session_uri,
                headers={
                    "content-length": str(size),
                },
                data=fp.read(size),
            )
            logger.debug(f"sucessfully uploaded {filepath}, PUT status code: {put_res.status_code}")
    except:
        # don't log the session_uri, just to be safe
        msg = (
            f"failed to upload {filepath}, PUT status code: {put_res.status_code}, content: "
            + str(put_res.content)
        )
        logger.error(msg)
        raise Exception(msg)
