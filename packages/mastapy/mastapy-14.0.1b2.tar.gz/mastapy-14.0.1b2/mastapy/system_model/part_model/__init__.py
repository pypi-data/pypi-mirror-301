"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.part_model._2489 import Assembly
    from mastapy._private.system_model.part_model._2490 import AbstractAssembly
    from mastapy._private.system_model.part_model._2491 import AbstractShaft
    from mastapy._private.system_model.part_model._2492 import AbstractShaftOrHousing
    from mastapy._private.system_model.part_model._2493 import (
        AGMALoadSharingTableApplicationLevel,
    )
    from mastapy._private.system_model.part_model._2494 import (
        AxialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2495 import Bearing
    from mastapy._private.system_model.part_model._2496 import BearingF0InputMethod
    from mastapy._private.system_model.part_model._2497 import (
        BearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2498 import Bolt
    from mastapy._private.system_model.part_model._2499 import BoltedJoint
    from mastapy._private.system_model.part_model._2500 import Component
    from mastapy._private.system_model.part_model._2501 import ComponentsConnectedResult
    from mastapy._private.system_model.part_model._2502 import ConnectedSockets
    from mastapy._private.system_model.part_model._2503 import Connector
    from mastapy._private.system_model.part_model._2504 import Datum
    from mastapy._private.system_model.part_model._2505 import (
        ElectricMachineSearchRegionSpecificationMethod,
    )
    from mastapy._private.system_model.part_model._2506 import EnginePartLoad
    from mastapy._private.system_model.part_model._2507 import EngineSpeed
    from mastapy._private.system_model.part_model._2508 import ExternalCADModel
    from mastapy._private.system_model.part_model._2509 import FEPart
    from mastapy._private.system_model.part_model._2510 import FlexiblePinAssembly
    from mastapy._private.system_model.part_model._2511 import GuideDxfModel
    from mastapy._private.system_model.part_model._2512 import GuideImage
    from mastapy._private.system_model.part_model._2513 import GuideModelUsage
    from mastapy._private.system_model.part_model._2514 import (
        InnerBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2515 import (
        InternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2516 import LoadSharingModes
    from mastapy._private.system_model.part_model._2517 import LoadSharingSettings
    from mastapy._private.system_model.part_model._2518 import MassDisc
    from mastapy._private.system_model.part_model._2519 import MeasurementComponent
    from mastapy._private.system_model.part_model._2520 import Microphone
    from mastapy._private.system_model.part_model._2521 import MicrophoneArray
    from mastapy._private.system_model.part_model._2522 import MountableComponent
    from mastapy._private.system_model.part_model._2523 import OilLevelSpecification
    from mastapy._private.system_model.part_model._2524 import OilSeal
    from mastapy._private.system_model.part_model._2525 import (
        OuterBearingRaceMountingOptions,
    )
    from mastapy._private.system_model.part_model._2526 import Part
    from mastapy._private.system_model.part_model._2527 import PlanetCarrier
    from mastapy._private.system_model.part_model._2528 import PlanetCarrierSettings
    from mastapy._private.system_model.part_model._2529 import PointLoad
    from mastapy._private.system_model.part_model._2530 import PowerLoad
    from mastapy._private.system_model.part_model._2531 import (
        RadialInternalClearanceTolerance,
    )
    from mastapy._private.system_model.part_model._2532 import (
        RollingBearingElementLoadCase,
    )
    from mastapy._private.system_model.part_model._2533 import RootAssembly
    from mastapy._private.system_model.part_model._2534 import (
        ShaftDiameterModificationDueToRollingBearingRing,
    )
    from mastapy._private.system_model.part_model._2535 import SpecialisedAssembly
    from mastapy._private.system_model.part_model._2536 import UnbalancedMass
    from mastapy._private.system_model.part_model._2537 import (
        UnbalancedMassInclusionOption,
    )
    from mastapy._private.system_model.part_model._2538 import VirtualComponent
    from mastapy._private.system_model.part_model._2539 import (
        WindTurbineBladeModeDetails,
    )
    from mastapy._private.system_model.part_model._2540 import (
        WindTurbineSingleBladeDetails,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.part_model._2489": ["Assembly"],
        "_private.system_model.part_model._2490": ["AbstractAssembly"],
        "_private.system_model.part_model._2491": ["AbstractShaft"],
        "_private.system_model.part_model._2492": ["AbstractShaftOrHousing"],
        "_private.system_model.part_model._2493": [
            "AGMALoadSharingTableApplicationLevel"
        ],
        "_private.system_model.part_model._2494": ["AxialInternalClearanceTolerance"],
        "_private.system_model.part_model._2495": ["Bearing"],
        "_private.system_model.part_model._2496": ["BearingF0InputMethod"],
        "_private.system_model.part_model._2497": ["BearingRaceMountingOptions"],
        "_private.system_model.part_model._2498": ["Bolt"],
        "_private.system_model.part_model._2499": ["BoltedJoint"],
        "_private.system_model.part_model._2500": ["Component"],
        "_private.system_model.part_model._2501": ["ComponentsConnectedResult"],
        "_private.system_model.part_model._2502": ["ConnectedSockets"],
        "_private.system_model.part_model._2503": ["Connector"],
        "_private.system_model.part_model._2504": ["Datum"],
        "_private.system_model.part_model._2505": [
            "ElectricMachineSearchRegionSpecificationMethod"
        ],
        "_private.system_model.part_model._2506": ["EnginePartLoad"],
        "_private.system_model.part_model._2507": ["EngineSpeed"],
        "_private.system_model.part_model._2508": ["ExternalCADModel"],
        "_private.system_model.part_model._2509": ["FEPart"],
        "_private.system_model.part_model._2510": ["FlexiblePinAssembly"],
        "_private.system_model.part_model._2511": ["GuideDxfModel"],
        "_private.system_model.part_model._2512": ["GuideImage"],
        "_private.system_model.part_model._2513": ["GuideModelUsage"],
        "_private.system_model.part_model._2514": ["InnerBearingRaceMountingOptions"],
        "_private.system_model.part_model._2515": ["InternalClearanceTolerance"],
        "_private.system_model.part_model._2516": ["LoadSharingModes"],
        "_private.system_model.part_model._2517": ["LoadSharingSettings"],
        "_private.system_model.part_model._2518": ["MassDisc"],
        "_private.system_model.part_model._2519": ["MeasurementComponent"],
        "_private.system_model.part_model._2520": ["Microphone"],
        "_private.system_model.part_model._2521": ["MicrophoneArray"],
        "_private.system_model.part_model._2522": ["MountableComponent"],
        "_private.system_model.part_model._2523": ["OilLevelSpecification"],
        "_private.system_model.part_model._2524": ["OilSeal"],
        "_private.system_model.part_model._2525": ["OuterBearingRaceMountingOptions"],
        "_private.system_model.part_model._2526": ["Part"],
        "_private.system_model.part_model._2527": ["PlanetCarrier"],
        "_private.system_model.part_model._2528": ["PlanetCarrierSettings"],
        "_private.system_model.part_model._2529": ["PointLoad"],
        "_private.system_model.part_model._2530": ["PowerLoad"],
        "_private.system_model.part_model._2531": ["RadialInternalClearanceTolerance"],
        "_private.system_model.part_model._2532": ["RollingBearingElementLoadCase"],
        "_private.system_model.part_model._2533": ["RootAssembly"],
        "_private.system_model.part_model._2534": [
            "ShaftDiameterModificationDueToRollingBearingRing"
        ],
        "_private.system_model.part_model._2535": ["SpecialisedAssembly"],
        "_private.system_model.part_model._2536": ["UnbalancedMass"],
        "_private.system_model.part_model._2537": ["UnbalancedMassInclusionOption"],
        "_private.system_model.part_model._2538": ["VirtualComponent"],
        "_private.system_model.part_model._2539": ["WindTurbineBladeModeDetails"],
        "_private.system_model.part_model._2540": ["WindTurbineSingleBladeDetails"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "Assembly",
    "AbstractAssembly",
    "AbstractShaft",
    "AbstractShaftOrHousing",
    "AGMALoadSharingTableApplicationLevel",
    "AxialInternalClearanceTolerance",
    "Bearing",
    "BearingF0InputMethod",
    "BearingRaceMountingOptions",
    "Bolt",
    "BoltedJoint",
    "Component",
    "ComponentsConnectedResult",
    "ConnectedSockets",
    "Connector",
    "Datum",
    "ElectricMachineSearchRegionSpecificationMethod",
    "EnginePartLoad",
    "EngineSpeed",
    "ExternalCADModel",
    "FEPart",
    "FlexiblePinAssembly",
    "GuideDxfModel",
    "GuideImage",
    "GuideModelUsage",
    "InnerBearingRaceMountingOptions",
    "InternalClearanceTolerance",
    "LoadSharingModes",
    "LoadSharingSettings",
    "MassDisc",
    "MeasurementComponent",
    "Microphone",
    "MicrophoneArray",
    "MountableComponent",
    "OilLevelSpecification",
    "OilSeal",
    "OuterBearingRaceMountingOptions",
    "Part",
    "PlanetCarrier",
    "PlanetCarrierSettings",
    "PointLoad",
    "PowerLoad",
    "RadialInternalClearanceTolerance",
    "RollingBearingElementLoadCase",
    "RootAssembly",
    "ShaftDiameterModificationDueToRollingBearingRing",
    "SpecialisedAssembly",
    "UnbalancedMass",
    "UnbalancedMassInclusionOption",
    "VirtualComponent",
    "WindTurbineBladeModeDetails",
    "WindTurbineSingleBladeDetails",
)
