# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from dataclasses import dataclass

from ._proto.api.v0.luminarycloud.common import common_pb2 as commonpb


@dataclass
class Vector3:
    """Represents a 3-dimensional vector."""

    x: float = 0.0
    y: float = 0.0
    z: float = 0.0

    def _to_proto(self) -> commonpb.Vector3:
        return commonpb.Vector3(x=self.x, y=self.y, z=self.z)
