"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe._2410 import AlignConnectedComponentOptions
    from mastapy._private.system_model.fe._2411 import AlignmentMethod
    from mastapy._private.system_model.fe._2412 import AlignmentMethodForRaceBearing
    from mastapy._private.system_model.fe._2413 import AlignmentUsingAxialNodePositions
    from mastapy._private.system_model.fe._2414 import AngleSource
    from mastapy._private.system_model.fe._2415 import BaseFEWithSelection
    from mastapy._private.system_model.fe._2416 import BatchOperations
    from mastapy._private.system_model.fe._2417 import BearingNodeAlignmentOption
    from mastapy._private.system_model.fe._2418 import BearingNodeOption
    from mastapy._private.system_model.fe._2419 import BearingRaceNodeLink
    from mastapy._private.system_model.fe._2420 import BearingRacePosition
    from mastapy._private.system_model.fe._2421 import ComponentOrientationOption
    from mastapy._private.system_model.fe._2422 import ContactPairWithSelection
    from mastapy._private.system_model.fe._2423 import CoordinateSystemWithSelection
    from mastapy._private.system_model.fe._2424 import CreateConnectedComponentOptions
    from mastapy._private.system_model.fe._2425 import (
        CreateMicrophoneNormalToSurfaceOptions,
    )
    from mastapy._private.system_model.fe._2426 import DegreeOfFreedomBoundaryCondition
    from mastapy._private.system_model.fe._2427 import (
        DegreeOfFreedomBoundaryConditionAngular,
    )
    from mastapy._private.system_model.fe._2428 import (
        DegreeOfFreedomBoundaryConditionLinear,
    )
    from mastapy._private.system_model.fe._2429 import ElectricMachineDataSet
    from mastapy._private.system_model.fe._2430 import ElectricMachineDynamicLoadData
    from mastapy._private.system_model.fe._2431 import ElementFaceGroupWithSelection
    from mastapy._private.system_model.fe._2432 import ElementPropertiesWithSelection
    from mastapy._private.system_model.fe._2433 import FEEntityGroupWithSelection
    from mastapy._private.system_model.fe._2434 import FEExportSettings
    from mastapy._private.system_model.fe._2435 import FEPartDRIVASurfaceSelection
    from mastapy._private.system_model.fe._2436 import FEPartWithBatchOptions
    from mastapy._private.system_model.fe._2437 import FEStiffnessGeometry
    from mastapy._private.system_model.fe._2438 import FEStiffnessTester
    from mastapy._private.system_model.fe._2439 import FESubstructure
    from mastapy._private.system_model.fe._2440 import FESubstructureExportOptions
    from mastapy._private.system_model.fe._2441 import FESubstructureNode
    from mastapy._private.system_model.fe._2442 import FESubstructureNodeModeShape
    from mastapy._private.system_model.fe._2443 import FESubstructureNodeModeShapes
    from mastapy._private.system_model.fe._2444 import FESubstructureType
    from mastapy._private.system_model.fe._2445 import FESubstructureWithBatchOptions
    from mastapy._private.system_model.fe._2446 import FESubstructureWithSelection
    from mastapy._private.system_model.fe._2447 import (
        FESubstructureWithSelectionComponents,
    )
    from mastapy._private.system_model.fe._2448 import (
        FESubstructureWithSelectionForHarmonicAnalysis,
    )
    from mastapy._private.system_model.fe._2449 import (
        FESubstructureWithSelectionForModalAnalysis,
    )
    from mastapy._private.system_model.fe._2450 import (
        FESubstructureWithSelectionForStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2451 import GearMeshingOptions
    from mastapy._private.system_model.fe._2452 import (
        IndependentMASTACreatedCondensationNode,
    )
    from mastapy._private.system_model.fe._2453 import (
        LinkComponentAxialPositionErrorReporter,
    )
    from mastapy._private.system_model.fe._2454 import LinkNodeSource
    from mastapy._private.system_model.fe._2455 import MaterialPropertiesWithSelection
    from mastapy._private.system_model.fe._2456 import (
        NodeBoundaryConditionStaticAnalysis,
    )
    from mastapy._private.system_model.fe._2457 import NodeGroupWithSelection
    from mastapy._private.system_model.fe._2458 import NodeSelectionDepthOption
    from mastapy._private.system_model.fe._2459 import (
        OptionsWhenExternalFEFileAlreadyExists,
    )
    from mastapy._private.system_model.fe._2460 import PerLinkExportOptions
    from mastapy._private.system_model.fe._2461 import PerNodeExportOptions
    from mastapy._private.system_model.fe._2462 import RaceBearingFE
    from mastapy._private.system_model.fe._2463 import RaceBearingFESystemDeflection
    from mastapy._private.system_model.fe._2464 import RaceBearingFEWithSelection
    from mastapy._private.system_model.fe._2465 import ReplacedShaftSelectionHelper
    from mastapy._private.system_model.fe._2466 import SystemDeflectionFEExportOptions
    from mastapy._private.system_model.fe._2467 import ThermalExpansionOption
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe._2410": ["AlignConnectedComponentOptions"],
        "_private.system_model.fe._2411": ["AlignmentMethod"],
        "_private.system_model.fe._2412": ["AlignmentMethodForRaceBearing"],
        "_private.system_model.fe._2413": ["AlignmentUsingAxialNodePositions"],
        "_private.system_model.fe._2414": ["AngleSource"],
        "_private.system_model.fe._2415": ["BaseFEWithSelection"],
        "_private.system_model.fe._2416": ["BatchOperations"],
        "_private.system_model.fe._2417": ["BearingNodeAlignmentOption"],
        "_private.system_model.fe._2418": ["BearingNodeOption"],
        "_private.system_model.fe._2419": ["BearingRaceNodeLink"],
        "_private.system_model.fe._2420": ["BearingRacePosition"],
        "_private.system_model.fe._2421": ["ComponentOrientationOption"],
        "_private.system_model.fe._2422": ["ContactPairWithSelection"],
        "_private.system_model.fe._2423": ["CoordinateSystemWithSelection"],
        "_private.system_model.fe._2424": ["CreateConnectedComponentOptions"],
        "_private.system_model.fe._2425": ["CreateMicrophoneNormalToSurfaceOptions"],
        "_private.system_model.fe._2426": ["DegreeOfFreedomBoundaryCondition"],
        "_private.system_model.fe._2427": ["DegreeOfFreedomBoundaryConditionAngular"],
        "_private.system_model.fe._2428": ["DegreeOfFreedomBoundaryConditionLinear"],
        "_private.system_model.fe._2429": ["ElectricMachineDataSet"],
        "_private.system_model.fe._2430": ["ElectricMachineDynamicLoadData"],
        "_private.system_model.fe._2431": ["ElementFaceGroupWithSelection"],
        "_private.system_model.fe._2432": ["ElementPropertiesWithSelection"],
        "_private.system_model.fe._2433": ["FEEntityGroupWithSelection"],
        "_private.system_model.fe._2434": ["FEExportSettings"],
        "_private.system_model.fe._2435": ["FEPartDRIVASurfaceSelection"],
        "_private.system_model.fe._2436": ["FEPartWithBatchOptions"],
        "_private.system_model.fe._2437": ["FEStiffnessGeometry"],
        "_private.system_model.fe._2438": ["FEStiffnessTester"],
        "_private.system_model.fe._2439": ["FESubstructure"],
        "_private.system_model.fe._2440": ["FESubstructureExportOptions"],
        "_private.system_model.fe._2441": ["FESubstructureNode"],
        "_private.system_model.fe._2442": ["FESubstructureNodeModeShape"],
        "_private.system_model.fe._2443": ["FESubstructureNodeModeShapes"],
        "_private.system_model.fe._2444": ["FESubstructureType"],
        "_private.system_model.fe._2445": ["FESubstructureWithBatchOptions"],
        "_private.system_model.fe._2446": ["FESubstructureWithSelection"],
        "_private.system_model.fe._2447": ["FESubstructureWithSelectionComponents"],
        "_private.system_model.fe._2448": [
            "FESubstructureWithSelectionForHarmonicAnalysis"
        ],
        "_private.system_model.fe._2449": [
            "FESubstructureWithSelectionForModalAnalysis"
        ],
        "_private.system_model.fe._2450": [
            "FESubstructureWithSelectionForStaticAnalysis"
        ],
        "_private.system_model.fe._2451": ["GearMeshingOptions"],
        "_private.system_model.fe._2452": ["IndependentMASTACreatedCondensationNode"],
        "_private.system_model.fe._2453": ["LinkComponentAxialPositionErrorReporter"],
        "_private.system_model.fe._2454": ["LinkNodeSource"],
        "_private.system_model.fe._2455": ["MaterialPropertiesWithSelection"],
        "_private.system_model.fe._2456": ["NodeBoundaryConditionStaticAnalysis"],
        "_private.system_model.fe._2457": ["NodeGroupWithSelection"],
        "_private.system_model.fe._2458": ["NodeSelectionDepthOption"],
        "_private.system_model.fe._2459": ["OptionsWhenExternalFEFileAlreadyExists"],
        "_private.system_model.fe._2460": ["PerLinkExportOptions"],
        "_private.system_model.fe._2461": ["PerNodeExportOptions"],
        "_private.system_model.fe._2462": ["RaceBearingFE"],
        "_private.system_model.fe._2463": ["RaceBearingFESystemDeflection"],
        "_private.system_model.fe._2464": ["RaceBearingFEWithSelection"],
        "_private.system_model.fe._2465": ["ReplacedShaftSelectionHelper"],
        "_private.system_model.fe._2466": ["SystemDeflectionFEExportOptions"],
        "_private.system_model.fe._2467": ["ThermalExpansionOption"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AlignConnectedComponentOptions",
    "AlignmentMethod",
    "AlignmentMethodForRaceBearing",
    "AlignmentUsingAxialNodePositions",
    "AngleSource",
    "BaseFEWithSelection",
    "BatchOperations",
    "BearingNodeAlignmentOption",
    "BearingNodeOption",
    "BearingRaceNodeLink",
    "BearingRacePosition",
    "ComponentOrientationOption",
    "ContactPairWithSelection",
    "CoordinateSystemWithSelection",
    "CreateConnectedComponentOptions",
    "CreateMicrophoneNormalToSurfaceOptions",
    "DegreeOfFreedomBoundaryCondition",
    "DegreeOfFreedomBoundaryConditionAngular",
    "DegreeOfFreedomBoundaryConditionLinear",
    "ElectricMachineDataSet",
    "ElectricMachineDynamicLoadData",
    "ElementFaceGroupWithSelection",
    "ElementPropertiesWithSelection",
    "FEEntityGroupWithSelection",
    "FEExportSettings",
    "FEPartDRIVASurfaceSelection",
    "FEPartWithBatchOptions",
    "FEStiffnessGeometry",
    "FEStiffnessTester",
    "FESubstructure",
    "FESubstructureExportOptions",
    "FESubstructureNode",
    "FESubstructureNodeModeShape",
    "FESubstructureNodeModeShapes",
    "FESubstructureType",
    "FESubstructureWithBatchOptions",
    "FESubstructureWithSelection",
    "FESubstructureWithSelectionComponents",
    "FESubstructureWithSelectionForHarmonicAnalysis",
    "FESubstructureWithSelectionForModalAnalysis",
    "FESubstructureWithSelectionForStaticAnalysis",
    "GearMeshingOptions",
    "IndependentMASTACreatedCondensationNode",
    "LinkComponentAxialPositionErrorReporter",
    "LinkNodeSource",
    "MaterialPropertiesWithSelection",
    "NodeBoundaryConditionStaticAnalysis",
    "NodeGroupWithSelection",
    "NodeSelectionDepthOption",
    "OptionsWhenExternalFEFileAlreadyExists",
    "PerLinkExportOptions",
    "PerNodeExportOptions",
    "RaceBearingFE",
    "RaceBearingFESystemDeflection",
    "RaceBearingFEWithSelection",
    "ReplacedShaftSelectionHelper",
    "SystemDeflectionFEExportOptions",
    "ThermalExpansionOption",
)
