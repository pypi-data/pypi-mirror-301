# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import logging as _logging
from importlib.metadata import version as _version

try:
    __version__ = _version("luminarycloud")
except:
    __version__ = "0.0.0"

# Log SDK version number
logger = _logging.getLogger("luminarycloud")
logger.debug(f"Imported Luminary Cloud SDK v{__version__}")

from ._client import (
    Client,
    get_default_client,
    set_default_client,
)
from .geometry import get_geometry, Geometry
from .mesh import (
    get_mesh,
    get_mesh_metadata,
    Mesh,
    MeshAdaptationParameters,
)
from .project import (
    create_project,
    get_project,
    list_projects,
    Project,
)
from .simulation import (
    get_simulation,
    Simulation,
)
from .simulation_template import (
    get_simulation_template,
    SimulationTemplate,
)
from .simulation_param import (
    SimulationParam,
)
from .solution import (
    Solution,
)
from .vector3 import (
    Vector3,
)
from .reference_values import (
    ReferenceValues,
)


def use_itar_environment() -> None:
    """
    Configures the SDK to make API calls to the Luminary Cloud ITAR Environment,
    rather than the Standard Environment.

    This function only needs to be called once in your script, before making any
    API calls.

    Examples
    --------

    >>> import luminarycloud as lc
    >>> lc.use_itar_environment()
    >>> lc.list_projects() # lists projects in the user's ITAR environment
    """
    set_default_client(
        Client(
            target="apis-itar.luminarycloud.com",
            # below params are kwargs to Auth0Client constructor
            domain="luminarycloud-itar-prod.us.auth0.com",
            client_id="gkW9O4wZWnTHOXhiejHOKDO4cuPF3S0y",
            audience="https://api-itar-prod.luminarycloud.com",
        )
    )
    logger.info("using Luminary Cloud ITAR Environment")


def use_standard_environment() -> None:
    """
    Configures the SDK to make API calls to the Luminary Cloud Standard Environment,
    rather than the ITAR Environment.

    This function only needs to be called once in your script, before making any
    API calls.

    Examples
    --------

    >>> import luminarycloud as lc
    >>> lc.use_standard_environment()
    >>> lc.list_projects() # lists projects in the user's Standard environment
    """
    set_default_client(Client())
    logger.info("using Luminary Cloud Standard Environment")
