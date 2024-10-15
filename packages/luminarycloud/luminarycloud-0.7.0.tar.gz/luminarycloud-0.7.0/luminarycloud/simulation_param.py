# Copyright 2024 Luminary Cloud, Inc. All Rights Reserved.
from functools import wraps
from typing import Type, TypeVar

from google.protobuf.message import Message

from luminarycloud._helpers.cond import params_to_str
from luminarycloud._helpers.defaults import _reset_defaults
from luminarycloud._proto.client.simulation_pb2 import (
    BladeElementAirfoilData,
    BoundaryConditionsFluid,
    BoundaryConditionsHeat,
    BoundaryLayerProfile,
    FrameTransforms,
    HeatSource,
    MaterialEntity,
    MonitorPlane,
    MotionData,
    ParticleGroup,
    PeriodicPair,
    PhysicalBehavior,
    Physics,
    PorousBehavior,
    SimulationParam,
    SlidingInterfaces,
    VolumeEntity,
    VolumeMaterialRelationship,
    VolumePhysicsRelationship,
)

_P = TypeVar("P", bound=Message)


def _monkey_patch(cls: Type[_P]) -> Type[_P]:

    __class__ = cls
    init = cls.__init__

    @wraps(cls.__init__, assigned=["__signature__"])
    def init_with_defaults(self, *args, **kwargs):
        super().__init__()
        _reset_defaults(self)
        init(self, *args, **kwargs)

    cls.__init__ = init_with_defaults


_monkey_patch(SimulationParam)
_monkey_patch(FrameTransforms)
_monkey_patch(VolumeMaterialRelationship)
_monkey_patch(VolumePhysicsRelationship)
_monkey_patch(BoundaryLayerProfile)
_monkey_patch(BoundaryConditionsHeat)
_monkey_patch(HeatSource)
_monkey_patch(SlidingInterfaces)
_monkey_patch(PeriodicPair)
_monkey_patch(BladeElementAirfoilData)
_monkey_patch(BoundaryConditionsFluid)
_monkey_patch(PhysicalBehavior)
_monkey_patch(PorousBehavior)
_monkey_patch(MaterialEntity)
_monkey_patch(VolumeEntity)
_monkey_patch(MotionData)
_monkey_patch(ParticleGroup)
_monkey_patch(MonitorPlane)
_monkey_patch(Physics)

SimulationParam.__repr__ = params_to_str
