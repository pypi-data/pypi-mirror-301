"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.links._2474 import FELink
    from mastapy._private.system_model.fe.links._2475 import ElectricMachineStatorFELink
    from mastapy._private.system_model.fe.links._2476 import FELinkWithSelection
    from mastapy._private.system_model.fe.links._2477 import GearMeshFELink
    from mastapy._private.system_model.fe.links._2478 import (
        GearWithDuplicatedMeshesFELink,
    )
    from mastapy._private.system_model.fe.links._2479 import MultiAngleConnectionFELink
    from mastapy._private.system_model.fe.links._2480 import MultiNodeConnectorFELink
    from mastapy._private.system_model.fe.links._2481 import MultiNodeFELink
    from mastapy._private.system_model.fe.links._2482 import (
        PlanetaryConnectorMultiNodeFELink,
    )
    from mastapy._private.system_model.fe.links._2483 import PlanetBasedFELink
    from mastapy._private.system_model.fe.links._2484 import PlanetCarrierFELink
    from mastapy._private.system_model.fe.links._2485 import PointLoadFELink
    from mastapy._private.system_model.fe.links._2486 import RollingRingConnectionFELink
    from mastapy._private.system_model.fe.links._2487 import ShaftHubConnectionFELink
    from mastapy._private.system_model.fe.links._2488 import SingleNodeFELink
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.links._2474": ["FELink"],
        "_private.system_model.fe.links._2475": ["ElectricMachineStatorFELink"],
        "_private.system_model.fe.links._2476": ["FELinkWithSelection"],
        "_private.system_model.fe.links._2477": ["GearMeshFELink"],
        "_private.system_model.fe.links._2478": ["GearWithDuplicatedMeshesFELink"],
        "_private.system_model.fe.links._2479": ["MultiAngleConnectionFELink"],
        "_private.system_model.fe.links._2480": ["MultiNodeConnectorFELink"],
        "_private.system_model.fe.links._2481": ["MultiNodeFELink"],
        "_private.system_model.fe.links._2482": ["PlanetaryConnectorMultiNodeFELink"],
        "_private.system_model.fe.links._2483": ["PlanetBasedFELink"],
        "_private.system_model.fe.links._2484": ["PlanetCarrierFELink"],
        "_private.system_model.fe.links._2485": ["PointLoadFELink"],
        "_private.system_model.fe.links._2486": ["RollingRingConnectionFELink"],
        "_private.system_model.fe.links._2487": ["ShaftHubConnectionFELink"],
        "_private.system_model.fe.links._2488": ["SingleNodeFELink"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FELink",
    "ElectricMachineStatorFELink",
    "FELinkWithSelection",
    "GearMeshFELink",
    "GearWithDuplicatedMeshesFELink",
    "MultiAngleConnectionFELink",
    "MultiNodeConnectorFELink",
    "MultiNodeFELink",
    "PlanetaryConnectorMultiNodeFELink",
    "PlanetBasedFELink",
    "PlanetCarrierFELink",
    "PointLoadFELink",
    "RollingRingConnectionFELink",
    "ShaftHubConnectionFELink",
    "SingleNodeFELink",
)
