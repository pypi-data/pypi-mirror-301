"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model.couplings._2636 import BeltDrive
    from mastapy._private.system_model.part_model.couplings._2637 import BeltDriveType
    from mastapy._private.system_model.part_model.couplings._2638 import Clutch
    from mastapy._private.system_model.part_model.couplings._2639 import ClutchHalf
    from mastapy._private.system_model.part_model.couplings._2640 import ClutchType
    from mastapy._private.system_model.part_model.couplings._2641 import ConceptCoupling
    from mastapy._private.system_model.part_model.couplings._2642 import (
        ConceptCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2643 import (
        ConceptCouplingHalfPositioning,
    )
    from mastapy._private.system_model.part_model.couplings._2644 import Coupling
    from mastapy._private.system_model.part_model.couplings._2645 import CouplingHalf
    from mastapy._private.system_model.part_model.couplings._2646 import (
        CrowningSpecification,
    )
    from mastapy._private.system_model.part_model.couplings._2647 import CVT
    from mastapy._private.system_model.part_model.couplings._2648 import CVTPulley
    from mastapy._private.system_model.part_model.couplings._2649 import (
        PartToPartShearCoupling,
    )
    from mastapy._private.system_model.part_model.couplings._2650 import (
        PartToPartShearCouplingHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2651 import (
        PitchErrorFlankOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2652 import Pulley
    from mastapy._private.system_model.part_model.couplings._2653 import (
        RigidConnectorStiffnessType,
    )
    from mastapy._private.system_model.part_model.couplings._2654 import (
        RigidConnectorTiltStiffnessTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2655 import (
        RigidConnectorToothLocation,
    )
    from mastapy._private.system_model.part_model.couplings._2656 import (
        RigidConnectorToothSpacingType,
    )
    from mastapy._private.system_model.part_model.couplings._2657 import (
        RigidConnectorTypes,
    )
    from mastapy._private.system_model.part_model.couplings._2658 import RollingRing
    from mastapy._private.system_model.part_model.couplings._2659 import (
        RollingRingAssembly,
    )
    from mastapy._private.system_model.part_model.couplings._2660 import (
        ShaftHubConnection,
    )
    from mastapy._private.system_model.part_model.couplings._2661 import (
        SplineFitOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2662 import (
        SplineLeadRelief,
    )
    from mastapy._private.system_model.part_model.couplings._2663 import (
        SplinePitchErrorInputType,
    )
    from mastapy._private.system_model.part_model.couplings._2664 import (
        SplinePitchErrorOptions,
    )
    from mastapy._private.system_model.part_model.couplings._2665 import SpringDamper
    from mastapy._private.system_model.part_model.couplings._2666 import (
        SpringDamperHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2667 import Synchroniser
    from mastapy._private.system_model.part_model.couplings._2668 import (
        SynchroniserCone,
    )
    from mastapy._private.system_model.part_model.couplings._2669 import (
        SynchroniserHalf,
    )
    from mastapy._private.system_model.part_model.couplings._2670 import (
        SynchroniserPart,
    )
    from mastapy._private.system_model.part_model.couplings._2671 import (
        SynchroniserSleeve,
    )
    from mastapy._private.system_model.part_model.couplings._2672 import TorqueConverter
    from mastapy._private.system_model.part_model.couplings._2673 import (
        TorqueConverterPump,
    )
    from mastapy._private.system_model.part_model.couplings._2674 import (
        TorqueConverterSpeedRatio,
    )
    from mastapy._private.system_model.part_model.couplings._2675 import (
        TorqueConverterTurbine,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model.couplings._2636": ["BeltDrive"],
        "_private.system_model.part_model.couplings._2637": ["BeltDriveType"],
        "_private.system_model.part_model.couplings._2638": ["Clutch"],
        "_private.system_model.part_model.couplings._2639": ["ClutchHalf"],
        "_private.system_model.part_model.couplings._2640": ["ClutchType"],
        "_private.system_model.part_model.couplings._2641": ["ConceptCoupling"],
        "_private.system_model.part_model.couplings._2642": ["ConceptCouplingHalf"],
        "_private.system_model.part_model.couplings._2643": [
            "ConceptCouplingHalfPositioning"
        ],
        "_private.system_model.part_model.couplings._2644": ["Coupling"],
        "_private.system_model.part_model.couplings._2645": ["CouplingHalf"],
        "_private.system_model.part_model.couplings._2646": ["CrowningSpecification"],
        "_private.system_model.part_model.couplings._2647": ["CVT"],
        "_private.system_model.part_model.couplings._2648": ["CVTPulley"],
        "_private.system_model.part_model.couplings._2649": ["PartToPartShearCoupling"],
        "_private.system_model.part_model.couplings._2650": [
            "PartToPartShearCouplingHalf"
        ],
        "_private.system_model.part_model.couplings._2651": ["PitchErrorFlankOptions"],
        "_private.system_model.part_model.couplings._2652": ["Pulley"],
        "_private.system_model.part_model.couplings._2653": [
            "RigidConnectorStiffnessType"
        ],
        "_private.system_model.part_model.couplings._2654": [
            "RigidConnectorTiltStiffnessTypes"
        ],
        "_private.system_model.part_model.couplings._2655": [
            "RigidConnectorToothLocation"
        ],
        "_private.system_model.part_model.couplings._2656": [
            "RigidConnectorToothSpacingType"
        ],
        "_private.system_model.part_model.couplings._2657": ["RigidConnectorTypes"],
        "_private.system_model.part_model.couplings._2658": ["RollingRing"],
        "_private.system_model.part_model.couplings._2659": ["RollingRingAssembly"],
        "_private.system_model.part_model.couplings._2660": ["ShaftHubConnection"],
        "_private.system_model.part_model.couplings._2661": ["SplineFitOptions"],
        "_private.system_model.part_model.couplings._2662": ["SplineLeadRelief"],
        "_private.system_model.part_model.couplings._2663": [
            "SplinePitchErrorInputType"
        ],
        "_private.system_model.part_model.couplings._2664": ["SplinePitchErrorOptions"],
        "_private.system_model.part_model.couplings._2665": ["SpringDamper"],
        "_private.system_model.part_model.couplings._2666": ["SpringDamperHalf"],
        "_private.system_model.part_model.couplings._2667": ["Synchroniser"],
        "_private.system_model.part_model.couplings._2668": ["SynchroniserCone"],
        "_private.system_model.part_model.couplings._2669": ["SynchroniserHalf"],
        "_private.system_model.part_model.couplings._2670": ["SynchroniserPart"],
        "_private.system_model.part_model.couplings._2671": ["SynchroniserSleeve"],
        "_private.system_model.part_model.couplings._2672": ["TorqueConverter"],
        "_private.system_model.part_model.couplings._2673": ["TorqueConverterPump"],
        "_private.system_model.part_model.couplings._2674": [
            "TorqueConverterSpeedRatio"
        ],
        "_private.system_model.part_model.couplings._2675": ["TorqueConverterTurbine"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BeltDrive",
    "BeltDriveType",
    "Clutch",
    "ClutchHalf",
    "ClutchType",
    "ConceptCoupling",
    "ConceptCouplingHalf",
    "ConceptCouplingHalfPositioning",
    "Coupling",
    "CouplingHalf",
    "CrowningSpecification",
    "CVT",
    "CVTPulley",
    "PartToPartShearCoupling",
    "PartToPartShearCouplingHalf",
    "PitchErrorFlankOptions",
    "Pulley",
    "RigidConnectorStiffnessType",
    "RigidConnectorTiltStiffnessTypes",
    "RigidConnectorToothLocation",
    "RigidConnectorToothSpacingType",
    "RigidConnectorTypes",
    "RollingRing",
    "RollingRingAssembly",
    "ShaftHubConnection",
    "SplineFitOptions",
    "SplineLeadRelief",
    "SplinePitchErrorInputType",
    "SplinePitchErrorOptions",
    "SpringDamper",
    "SpringDamperHalf",
    "Synchroniser",
    "SynchroniserCone",
    "SynchroniserHalf",
    "SynchroniserPart",
    "SynchroniserSleeve",
    "TorqueConverter",
    "TorqueConverterPump",
    "TorqueConverterSpeedRatio",
    "TorqueConverterTurbine",
)
