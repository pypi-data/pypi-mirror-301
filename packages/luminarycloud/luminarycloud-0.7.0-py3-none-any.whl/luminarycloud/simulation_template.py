# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
from datetime import datetime
from os import PathLike
from typing import Optional

from ._wrapper import ProtoWrapper, ProtoWrapperBase
from ._client import get_default_client
from ._helpers.simulation_params_from_json import simulation_params_from_json_path
from ._helpers.timestamp_to_datetime import timestamp_to_datetime
from ._proto.api.v0.luminarycloud.simulation_template import (
    simulation_template_pb2 as simtemplatepb,
)
from ._proto.client import simulation_pb2 as clientpb


@ProtoWrapper(simtemplatepb.SimulationTemplate)
class SimulationTemplate(ProtoWrapperBase):
    """
    Represents a simulation template object.

    Simulation templates can be used to create simulations with the same parameters.
    However, unlike simulations, the parameters of a simulation template are mutable.
    They can be used to partially set up the parameters of a simulation and then be
    persisted to the Luminary Cloud backend.
    """

    id: str
    "Simulation template ID."
    name: str
    "Simulation name."
    parameters: clientpb.SimulationParam
    "Simulation description."

    _proto: simtemplatepb.SimulationTemplate

    @property
    def create_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.create_time)

    @property
    def update_time(self) -> datetime:
        return timestamp_to_datetime(self._proto.update_time)

    def update(
        self,
        *,
        name: Optional[str] = None,
        parameters: Optional[clientpb.SimulationParam] = None,
        params_json_path: Optional[PathLike] = None,
    ) -> None:
        """
        Update simulation template.

        Parameters
        ----------
        name : str, optional
            New project name.
        parameters : str, optional
            New complete simulation parameters. Ignored if `params_json_path` is set.
        params_json_path : path-like, optional
            Path to local JSON file containing simulation params.
        """
        if params_json_path is not None:
            parameters = simulation_params_from_json_path(params_json_path)
        req = simtemplatepb.UpdateSimulationTemplateRequest(
            id=self.id,
            name=name,
            parameters=parameters,
        )
        res = get_default_client().UpdateSimulationTemplate(req)
        self._proto = res.simulation_template

    def delete(self) -> None:
        """
        Delete the simulation template.
        """
        req = simtemplatepb.DeleteSimulationTemplateRequest(id=self.id)
        get_default_client().DeleteSimulationTemplate(req)


def get_simulation_template(id: str) -> SimulationTemplate:
    """
    Retrieve a specific simulation template by ID.

    Parameters
    ----------
    id : str
        Simulation template ID.
    """
    req = simtemplatepb.GetSimulationTemplateRequest(id=id)
    res = get_default_client().GetSimulationTemplate(req)
    return SimulationTemplate(res.simulation_template)
