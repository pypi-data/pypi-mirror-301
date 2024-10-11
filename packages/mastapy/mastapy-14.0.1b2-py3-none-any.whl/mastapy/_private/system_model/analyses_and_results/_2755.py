"""CompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2706

_CONCEPT_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "ConceptCouplingConnection",
)
_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "CouplingConnection"
)
_SPRING_DAMPER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "SpringDamperConnection"
)
_TORQUE_CONVERTER_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "TorqueConverterConnection",
)
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings",
    "PartToPartShearCouplingConnection",
)
_CLUTCH_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings", "ClutchConnection"
)
_ABSTRACT_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaft"
)
_MICROPHONE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Microphone")
_MICROPHONE_ARRAY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MicrophoneArray"
)
_ABSTRACT_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractAssembly"
)
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AbstractShaftOrHousing"
)
_BEARING = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bearing")
_BOLT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Bolt")
_BOLTED_JOINT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "BoltedJoint")
_COMPONENT = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Component")
_CONNECTOR = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Connector")
_DATUM = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Datum")
_EXTERNAL_CAD_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ExternalCADModel"
)
_FE_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "FEPart")
_FLEXIBLE_PIN_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "FlexiblePinAssembly"
)
_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Assembly")
_GUIDE_DXF_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "GuideDxfModel"
)
_MASS_DISC = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "MassDisc")
_MEASUREMENT_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MeasurementComponent"
)
_MOUNTABLE_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "MountableComponent"
)
_OIL_SEAL = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "OilSeal")
_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")
_PLANET_CARRIER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PlanetCarrier"
)
_POINT_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PointLoad")
_POWER_LOAD = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "PowerLoad")
_ROOT_ASSEMBLY = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "RootAssembly")
_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)
_UNBALANCED_MASS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMass"
)
_VIRTUAL_COMPONENT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "VirtualComponent"
)
_SHAFT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.ShaftModel", "Shaft")
_CONCEPT_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGear"
)
_CONCEPT_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConceptGearSet"
)
_FACE_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGear")
_FACE_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "FaceGearSet"
)
_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)
_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGearSet"
)
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialPlanetGear"
)
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialSunGear"
)
_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")
_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGearSet"
)
_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGear"
)
_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)
_CYLINDRICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGear"
)
_CYLINDRICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalGearSet"
)
_CYLINDRICAL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "CylindricalPlanetGear"
)
_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")
_GEAR_SET = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSet")
_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGear"
)
_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "HypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGear"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGear"
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidHypoidGearSet"
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGear",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearSet",
)
_PLANETARY_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "PlanetaryGearSet"
)
_SPIRAL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGear"
)
_SPIRAL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "SpiralBevelGearSet"
)
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGear"
)
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelDiffGearSet"
)
_STRAIGHT_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGear"
)
_STRAIGHT_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelGearSet"
)
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelPlanetGear"
)
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)
_WORM_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGear")
_WORM_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "WormGearSet"
)
_ZEROL_BEVEL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGear"
)
_ZEROL_BEVEL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ZerolBevelGearSet"
)
_CYCLOIDAL_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalAssembly"
)
_CYCLOIDAL_DISC = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "CycloidalDisc"
)
_RING_PINS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Cycloidal", "RingPins"
)
_PART_TO_PART_SHEAR_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCoupling"
)
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "PartToPartShearCouplingHalf"
)
_BELT_DRIVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "BeltDrive"
)
_CLUTCH = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Clutch")
_CLUTCH_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchHalf"
)
_CONCEPT_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCoupling"
)
_CONCEPT_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ConceptCouplingHalf"
)
_COUPLING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Coupling"
)
_COUPLING_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CouplingHalf"
)
_CVT = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVT")
_CVT_PULLEY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "CVTPulley"
)
_PULLEY = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Couplings", "Pulley")
_SHAFT_HUB_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ShaftHubConnection"
)
_ROLLING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRing"
)
_ROLLING_RING_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RollingRingAssembly"
)
_SPRING_DAMPER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamper"
)
_SPRING_DAMPER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SpringDamperHalf"
)
_SYNCHRONISER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "Synchroniser"
)
_SYNCHRONISER_HALF = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserHalf"
)
_SYNCHRONISER_PART = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserPart"
)
_SYNCHRONISER_SLEEVE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "SynchroniserSleeve"
)
_TORQUE_CONVERTER = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverter"
)
_TORQUE_CONVERTER_PUMP = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterPump"
)
_TORQUE_CONVERTER_TURBINE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterTurbine"
)
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "ShaftToMountableComponentConnection",
)
_CVT_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CVTBeltConnection"
)
_BELT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "BeltConnection"
)
_COAXIAL_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "CoaxialConnection"
)
_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "Connection"
)
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "InterMountableComponentConnection",
)
_PLANETARY_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "PlanetaryConnection"
)
_ROLLING_RING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets", "RollingRingConnection"
)
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets",
    "AbstractShaftToMountableComponentConnection",
)
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelDifferentialGearMesh"
)
_CONCEPT_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConceptGearMesh"
)
_FACE_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "FaceGearMesh"
)
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelDiffGearMesh"
)
_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "BevelGearMesh"
)
_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ConicalGearMesh"
)
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "AGMAGleasonConicalGearMesh"
)
_CYLINDRICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "CylindricalGearMesh"
)
_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "HypoidGearMesh"
)
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidConicalGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidHypoidGearMesh",
)
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears",
    "KlingelnbergCycloPalloidSpiralBevelGearMesh",
)
_SPIRAL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "SpiralBevelGearMesh"
)
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "StraightBevelGearMesh"
)
_WORM_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "WormGearMesh"
)
_ZEROL_BEVEL_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "ZerolBevelGearMesh"
)
_GEAR_MESH = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears", "GearMesh"
)
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscCentralBearingConnection",
)
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "CycloidalDiscPlanetaryBearingConnection",
)
_RING_PINS_TO_DISC_CONNECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal",
    "RingPinsToDiscConnection",
)
_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults", "CompoundHarmonicAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Iterable, Type, TypeVar

    from mastapy._private import _7725
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6015,
        _6016,
        _6017,
        _6018,
        _6019,
        _6020,
        _6021,
        _6022,
        _6023,
        _6024,
        _6025,
        _6026,
        _6027,
        _6028,
        _6029,
        _6030,
        _6031,
        _6032,
        _6033,
        _6034,
        _6035,
        _6036,
        _6037,
        _6038,
        _6039,
        _6040,
        _6041,
        _6042,
        _6043,
        _6044,
        _6045,
        _6046,
        _6047,
        _6048,
        _6049,
        _6050,
        _6051,
        _6052,
        _6053,
        _6054,
        _6055,
        _6056,
        _6057,
        _6058,
        _6059,
        _6060,
        _6061,
        _6062,
        _6063,
        _6064,
        _6065,
        _6066,
        _6067,
        _6068,
        _6069,
        _6070,
        _6071,
        _6072,
        _6073,
        _6074,
        _6075,
        _6076,
        _6077,
        _6078,
        _6079,
        _6080,
        _6081,
        _6082,
        _6083,
        _6084,
        _6085,
        _6086,
        _6087,
        _6088,
        _6089,
        _6090,
        _6091,
        _6092,
        _6093,
        _6094,
        _6095,
        _6096,
        _6097,
        _6098,
        _6099,
        _6100,
        _6101,
        _6102,
        _6103,
        _6104,
        _6105,
        _6106,
        _6107,
        _6108,
        _6109,
        _6110,
        _6111,
        _6112,
        _6113,
        _6114,
        _6115,
        _6116,
        _6117,
        _6118,
        _6119,
        _6120,
        _6121,
        _6122,
        _6123,
        _6124,
        _6125,
        _6126,
        _6127,
        _6128,
        _6129,
        _6130,
        _6131,
        _6132,
        _6133,
        _6134,
        _6135,
        _6136,
        _6137,
        _6138,
        _6139,
        _6140,
        _6141,
        _6142,
        _6143,
        _6144,
        _6145,
    )
    from mastapy._private.system_model.connections_and_sockets import (
        _2320,
        _2323,
        _2324,
        _2327,
        _2328,
        _2336,
        _2342,
        _2347,
        _2350,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import (
        _2397,
        _2399,
        _2401,
        _2403,
        _2405,
        _2407,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import (
        _2390,
        _2393,
        _2396,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import (
        _2354,
        _2356,
        _2358,
        _2360,
        _2362,
        _2364,
        _2366,
        _2368,
        _2370,
        _2373,
        _2374,
        _2375,
        _2378,
        _2380,
        _2382,
        _2384,
        _2386,
    )
    from mastapy._private.system_model.part_model import (
        _2489,
        _2490,
        _2491,
        _2492,
        _2495,
        _2498,
        _2499,
        _2500,
        _2503,
        _2504,
        _2508,
        _2509,
        _2510,
        _2511,
        _2518,
        _2519,
        _2520,
        _2521,
        _2522,
        _2524,
        _2526,
        _2527,
        _2529,
        _2530,
        _2533,
        _2535,
        _2536,
        _2538,
    )
    from mastapy._private.system_model.part_model.couplings import (
        _2636,
        _2638,
        _2639,
        _2641,
        _2642,
        _2644,
        _2645,
        _2647,
        _2648,
        _2649,
        _2650,
        _2652,
        _2658,
        _2659,
        _2660,
        _2665,
        _2666,
        _2667,
        _2669,
        _2670,
        _2671,
        _2672,
        _2673,
        _2675,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2627, _2628, _2629
    from mastapy._private.system_model.part_model.gears import (
        _2572,
        _2573,
        _2574,
        _2575,
        _2576,
        _2577,
        _2578,
        _2579,
        _2580,
        _2581,
        _2582,
        _2583,
        _2584,
        _2585,
        _2586,
        _2587,
        _2588,
        _2589,
        _2591,
        _2593,
        _2594,
        _2595,
        _2596,
        _2597,
        _2598,
        _2599,
        _2600,
        _2601,
        _2602,
        _2603,
        _2604,
        _2605,
        _2606,
        _2607,
        _2608,
        _2609,
        _2610,
        _2611,
        _2612,
        _2613,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2541

    Self = TypeVar("Self", bound="CompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CompoundHarmonicAnalysis._Cast_CompoundHarmonicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CompoundHarmonicAnalysis:
    """Special nested class for casting CompoundHarmonicAnalysis to subclasses."""

    __parent__: "CompoundHarmonicAnalysis"

    @property
    def compound_analysis(self: "CastSelf") -> "_2706.CompoundAnalysis":
        return self.__parent__._cast(_2706.CompoundAnalysis)

    @property
    def marshal_by_ref_object_permanent(
        self: "CastSelf",
    ) -> "_7725.MarshalByRefObjectPermanent":
        from mastapy._private import _7725

        return self.__parent__._cast(_7725.MarshalByRefObjectPermanent)

    @property
    def compound_harmonic_analysis(self: "CastSelf") -> "CompoundHarmonicAnalysis":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class CompoundHarmonicAnalysis(_2706.CompoundAnalysis):
    """CompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @enforce_parameter_types
    def results_for_concept_coupling_connection(
        self: "Self", design_entity: "_2399.ConceptCouplingConnection"
    ) -> "Iterable[_6042.ConceptCouplingConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptCouplingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling_connection(
        self: "Self", design_entity: "_2401.CouplingConnection"
    ) -> "Iterable[_6053.CouplingConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CouplingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper_connection(
        self: "Self", design_entity: "_2405.SpringDamperConnection"
    ) -> "Iterable[_6120.SpringDamperConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpringDamperConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_connection(
        self: "Self", design_entity: "_2407.TorqueConverterConnection"
    ) -> "Iterable[_6135.TorqueConverterConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.TorqueConverterConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft(
        self: "Self", design_entity: "_2491.AbstractShaft"
    ) -> "Iterable[_6016.AbstractShaftCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AbstractShaftCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_microphone(
        self: "Self", design_entity: "_2520.Microphone"
    ) -> "Iterable[_6093.MicrophoneCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.MicrophoneCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Microphone)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MICROPHONE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_microphone_array(
        self: "Self", design_entity: "_2521.MicrophoneArray"
    ) -> "Iterable[_6092.MicrophoneArrayCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.MicrophoneArrayCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.MicrophoneArray)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MICROPHONE_ARRAY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_assembly(
        self: "Self", design_entity: "_2490.AbstractAssembly"
    ) -> "Iterable[_6015.AbstractAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AbstractAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_or_housing(
        self: "Self", design_entity: "_2492.AbstractShaftOrHousing"
    ) -> "Iterable[_6017.AbstractShaftOrHousingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AbstractShaftOrHousingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT_OR_HOUSING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bearing(
        self: "Self", design_entity: "_2495.Bearing"
    ) -> "Iterable[_6023.BearingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BearingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEARING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bolt(
        self: "Self", design_entity: "_2498.Bolt"
    ) -> "Iterable[_6034.BoltCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BoltCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BOLT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bolted_joint(
        self: "Self", design_entity: "_2499.BoltedJoint"
    ) -> "Iterable[_6035.BoltedJointCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BoltedJointCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BOLTED_JOINT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_component(
        self: "Self", design_entity: "_2500.Component"
    ) -> "Iterable[_6040.ComponentCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ComponentCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Component)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_connector(
        self: "Self", design_entity: "_2503.Connector"
    ) -> "Iterable[_6051.ConnectorCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConnectorCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Connector)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONNECTOR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_datum(
        self: "Self", design_entity: "_2504.Datum"
    ) -> "Iterable[_6066.DatumCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.DatumCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Datum)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_DATUM],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_external_cad_model(
        self: "Self", design_entity: "_2508.ExternalCADModel"
    ) -> "Iterable[_6067.ExternalCADModelCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ExternalCADModelCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_EXTERNAL_CAD_MODEL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_fe_part(
        self: "Self", design_entity: "_2509.FEPart"
    ) -> "Iterable[_6071.FEPartCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.FEPartCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FE_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_flexible_pin_assembly(
        self: "Self", design_entity: "_2510.FlexiblePinAssembly"
    ) -> "Iterable[_6072.FlexiblePinAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.FlexiblePinAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FLEXIBLE_PIN_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_assembly(
        self: "Self", design_entity: "_2489.Assembly"
    ) -> "Iterable[_6022.AssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_guide_dxf_model(
        self: "Self", design_entity: "_2511.GuideDxfModel"
    ) -> "Iterable[_6076.GuideDxfModelCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.GuideDxfModelCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GUIDE_DXF_MODEL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_mass_disc(
        self: "Self", design_entity: "_2518.MassDisc"
    ) -> "Iterable[_6090.MassDiscCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.MassDiscCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MASS_DISC],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_measurement_component(
        self: "Self", design_entity: "_2519.MeasurementComponent"
    ) -> "Iterable[_6091.MeasurementComponentCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.MeasurementComponentCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MEASUREMENT_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_mountable_component(
        self: "Self", design_entity: "_2522.MountableComponent"
    ) -> "Iterable[_6094.MountableComponentCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.MountableComponentCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_MOUNTABLE_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_oil_seal(
        self: "Self", design_entity: "_2524.OilSeal"
    ) -> "Iterable[_6095.OilSealCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.OilSealCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_OIL_SEAL],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part(
        self: "Self", design_entity: "_2526.Part"
    ) -> "Iterable[_6096.PartCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PartCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planet_carrier(
        self: "Self", design_entity: "_2527.PlanetCarrier"
    ) -> "Iterable[_6102.PlanetCarrierCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PlanetCarrierCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANET_CARRIER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_point_load(
        self: "Self", design_entity: "_2529.PointLoad"
    ) -> "Iterable[_6103.PointLoadCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PointLoadCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_POINT_LOAD],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_power_load(
        self: "Self", design_entity: "_2530.PowerLoad"
    ) -> "Iterable[_6104.PowerLoadCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PowerLoadCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_POWER_LOAD],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_root_assembly(
        self: "Self", design_entity: "_2533.RootAssembly"
    ) -> "Iterable[_6111.RootAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RootAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROOT_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_specialised_assembly(
        self: "Self", design_entity: "_2535.SpecialisedAssembly"
    ) -> "Iterable[_6115.SpecialisedAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpecialisedAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPECIALISED_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_unbalanced_mass(
        self: "Self", design_entity: "_2536.UnbalancedMass"
    ) -> "Iterable[_6138.UnbalancedMassCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.UnbalancedMassCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_UNBALANCED_MASS],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_virtual_component(
        self: "Self", design_entity: "_2538.VirtualComponent"
    ) -> "Iterable[_6139.VirtualComponentCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.VirtualComponentCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_VIRTUAL_COMPONENT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft(
        self: "Self", design_entity: "_2541.Shaft"
    ) -> "Iterable[_6112.ShaftCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ShaftCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear(
        self: "Self", design_entity: "_2580.ConceptGear"
    ) -> "Iterable[_6044.ConceptGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear_set(
        self: "Self", design_entity: "_2581.ConceptGearSet"
    ) -> "Iterable[_6046.ConceptGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear(
        self: "Self", design_entity: "_2587.FaceGear"
    ) -> "Iterable[_6068.FaceGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.FaceGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear_set(
        self: "Self", design_entity: "_2588.FaceGearSet"
    ) -> "Iterable[_6070.FaceGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.FaceGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear(
        self: "Self", design_entity: "_2572.AGMAGleasonConicalGear"
    ) -> "Iterable[_6019.AGMAGleasonConicalGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AGMAGleasonConicalGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_set(
        self: "Self", design_entity: "_2573.AGMAGleasonConicalGearSet"
    ) -> "Iterable[_6021.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear(
        self: "Self", design_entity: "_2574.BevelDifferentialGear"
    ) -> "Iterable[_6026.BevelDifferentialGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelDifferentialGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_set(
        self: "Self", design_entity: "_2575.BevelDifferentialGearSet"
    ) -> "Iterable[_6028.BevelDifferentialGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelDifferentialGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_planet_gear(
        self: "Self", design_entity: "_2576.BevelDifferentialPlanetGear"
    ) -> "Iterable[_6029.BevelDifferentialPlanetGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelDifferentialPlanetGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_sun_gear(
        self: "Self", design_entity: "_2577.BevelDifferentialSunGear"
    ) -> "Iterable[_6030.BevelDifferentialSunGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelDifferentialSunGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_SUN_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear(
        self: "Self", design_entity: "_2578.BevelGear"
    ) -> "Iterable[_6031.BevelGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear_set(
        self: "Self", design_entity: "_2579.BevelGearSet"
    ) -> "Iterable[_6033.BevelGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear(
        self: "Self", design_entity: "_2582.ConicalGear"
    ) -> "Iterable[_6047.ConicalGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear_set(
        self: "Self", design_entity: "_2583.ConicalGearSet"
    ) -> "Iterable[_6049.ConicalGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear(
        self: "Self", design_entity: "_2584.CylindricalGear"
    ) -> "Iterable[_6062.CylindricalGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CylindricalGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_set(
        self: "Self", design_entity: "_2585.CylindricalGearSet"
    ) -> "Iterable[_6064.CylindricalGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CylindricalGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_planet_gear(
        self: "Self", design_entity: "_2586.CylindricalPlanetGear"
    ) -> "Iterable[_6065.CylindricalPlanetGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CylindricalPlanetGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear(
        self: "Self", design_entity: "_2589.Gear"
    ) -> "Iterable[_6073.GearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.GearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear_set(
        self: "Self", design_entity: "_2591.GearSet"
    ) -> "Iterable[_6075.GearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.GearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear(
        self: "Self", design_entity: "_2593.HypoidGear"
    ) -> "Iterable[_6077.HypoidGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.HypoidGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_set(
        self: "Self", design_entity: "_2594.HypoidGearSet"
    ) -> "Iterable[_6079.HypoidGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.HypoidGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear(
        self: "Self", design_entity: "_2595.KlingelnbergCycloPalloidConicalGear"
    ) -> "Iterable[_6081.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(
        self: "Self", design_entity: "_2596.KlingelnbergCycloPalloidConicalGearSet"
    ) -> (
        "Iterable[_6083.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis]"
    ):
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(
        self: "Self", design_entity: "_2597.KlingelnbergCycloPalloidHypoidGear"
    ) -> "Iterable[_6084.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self", design_entity: "_2598.KlingelnbergCycloPalloidHypoidGearSet"
    ) -> (
        "Iterable[_6086.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]"
    ):
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "Self", design_entity: "_2599.KlingelnbergCycloPalloidSpiralBevelGear"
    ) -> "Iterable[_6087.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2600.KlingelnbergCycloPalloidSpiralBevelGearSet"
    ) -> "Iterable[_6089.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planetary_gear_set(
        self: "Self", design_entity: "_2601.PlanetaryGearSet"
    ) -> "Iterable[_6101.PlanetaryGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PlanetaryGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANETARY_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear(
        self: "Self", design_entity: "_2602.SpiralBevelGear"
    ) -> "Iterable[_6116.SpiralBevelGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpiralBevelGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_set(
        self: "Self", design_entity: "_2603.SpiralBevelGearSet"
    ) -> "Iterable[_6118.SpiralBevelGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpiralBevelGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear(
        self: "Self", design_entity: "_2604.StraightBevelDiffGear"
    ) -> "Iterable[_6122.StraightBevelDiffGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelDiffGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_set(
        self: "Self", design_entity: "_2605.StraightBevelDiffGearSet"
    ) -> "Iterable[_6124.StraightBevelDiffGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelDiffGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear(
        self: "Self", design_entity: "_2606.StraightBevelGear"
    ) -> "Iterable[_6125.StraightBevelGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_set(
        self: "Self", design_entity: "_2607.StraightBevelGearSet"
    ) -> "Iterable[_6127.StraightBevelGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_planet_gear(
        self: "Self", design_entity: "_2608.StraightBevelPlanetGear"
    ) -> "Iterable[_6128.StraightBevelPlanetGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelPlanetGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_PLANET_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_sun_gear(
        self: "Self", design_entity: "_2609.StraightBevelSunGear"
    ) -> "Iterable[_6129.StraightBevelSunGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelSunGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_SUN_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear(
        self: "Self", design_entity: "_2610.WormGear"
    ) -> "Iterable[_6140.WormGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.WormGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear_set(
        self: "Self", design_entity: "_2611.WormGearSet"
    ) -> "Iterable[_6142.WormGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.WormGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear(
        self: "Self", design_entity: "_2612.ZerolBevelGear"
    ) -> "Iterable[_6143.ZerolBevelGearCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ZerolBevelGearCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_set(
        self: "Self", design_entity: "_2613.ZerolBevelGearSet"
    ) -> "Iterable[_6145.ZerolBevelGearSetCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ZerolBevelGearSetCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR_SET],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_assembly(
        self: "Self", design_entity: "_2627.CycloidalAssembly"
    ) -> "Iterable[_6058.CycloidalAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CycloidalAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc(
        self: "Self", design_entity: "_2628.CycloidalDisc"
    ) -> "Iterable[_6060.CycloidalDiscCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CycloidalDiscCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_ring_pins(
        self: "Self", design_entity: "_2629.RingPins"
    ) -> "Iterable[_6106.RingPinsCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RingPinsCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_RING_PINS],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling(
        self: "Self", design_entity: "_2649.PartToPartShearCoupling"
    ) -> "Iterable[_6097.PartToPartShearCouplingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PartToPartShearCouplingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_half(
        self: "Self", design_entity: "_2650.PartToPartShearCouplingHalf"
    ) -> "Iterable[_6099.PartToPartShearCouplingHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PartToPartShearCouplingHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_belt_drive(
        self: "Self", design_entity: "_2636.BeltDrive"
    ) -> "Iterable[_6025.BeltDriveCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BeltDriveCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BELT_DRIVE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch(
        self: "Self", design_entity: "_2638.Clutch"
    ) -> "Iterable[_6036.ClutchCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ClutchCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch_half(
        self: "Self", design_entity: "_2639.ClutchHalf"
    ) -> "Iterable[_6038.ClutchHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ClutchHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_coupling(
        self: "Self", design_entity: "_2641.ConceptCoupling"
    ) -> "Iterable[_6041.ConceptCouplingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptCouplingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_coupling_half(
        self: "Self", design_entity: "_2642.ConceptCouplingHalf"
    ) -> "Iterable[_6043.ConceptCouplingHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptCouplingHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling(
        self: "Self", design_entity: "_2644.Coupling"
    ) -> "Iterable[_6052.CouplingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CouplingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coupling_half(
        self: "Self", design_entity: "_2645.CouplingHalf"
    ) -> "Iterable[_6054.CouplingHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CouplingHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COUPLING_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt(
        self: "Self", design_entity: "_2647.CVT"
    ) -> "Iterable[_6056.CVTCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CVTCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt_pulley(
        self: "Self", design_entity: "_2648.CVTPulley"
    ) -> "Iterable[_6057.CVTPulleyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CVTPulleyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT_PULLEY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_pulley(
        self: "Self", design_entity: "_2652.Pulley"
    ) -> "Iterable[_6105.PulleyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PulleyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PULLEY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft_hub_connection(
        self: "Self", design_entity: "_2660.ShaftHubConnection"
    ) -> "Iterable[_6113.ShaftHubConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ShaftHubConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT_HUB_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring(
        self: "Self", design_entity: "_2658.RollingRing"
    ) -> "Iterable[_6109.RollingRingCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RollingRingCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring_assembly(
        self: "Self", design_entity: "_2659.RollingRingAssembly"
    ) -> "Iterable[_6108.RollingRingAssemblyCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RollingRingAssemblyCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING_ASSEMBLY],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper(
        self: "Self", design_entity: "_2665.SpringDamper"
    ) -> "Iterable[_6119.SpringDamperCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpringDamperCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spring_damper_half(
        self: "Self", design_entity: "_2666.SpringDamperHalf"
    ) -> "Iterable[_6121.SpringDamperHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpringDamperHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPRING_DAMPER_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser(
        self: "Self", design_entity: "_2667.Synchroniser"
    ) -> "Iterable[_6130.SynchroniserCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SynchroniserCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_half(
        self: "Self", design_entity: "_2669.SynchroniserHalf"
    ) -> "Iterable[_6131.SynchroniserHalfCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SynchroniserHalfCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_HALF],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_part(
        self: "Self", design_entity: "_2670.SynchroniserPart"
    ) -> "Iterable[_6132.SynchroniserPartCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SynchroniserPartCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_PART],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_synchroniser_sleeve(
        self: "Self", design_entity: "_2671.SynchroniserSleeve"
    ) -> "Iterable[_6133.SynchroniserSleeveCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SynchroniserSleeveCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SYNCHRONISER_SLEEVE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter(
        self: "Self", design_entity: "_2672.TorqueConverter"
    ) -> "Iterable[_6134.TorqueConverterCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.TorqueConverterCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_pump(
        self: "Self", design_entity: "_2673.TorqueConverterPump"
    ) -> "Iterable[_6136.TorqueConverterPumpCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.TorqueConverterPumpCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_PUMP],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_torque_converter_turbine(
        self: "Self", design_entity: "_2675.TorqueConverterTurbine"
    ) -> "Iterable[_6137.TorqueConverterTurbineCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.TorqueConverterTurbineCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_TORQUE_CONVERTER_TURBINE],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2350.ShaftToMountableComponentConnection"
    ) -> "Iterable[_6114.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ShaftToMountableComponentConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cvt_belt_connection(
        self: "Self", design_entity: "_2328.CVTBeltConnection"
    ) -> "Iterable[_6055.CVTBeltConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CVTBeltConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CVT_BELT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_belt_connection(
        self: "Self", design_entity: "_2323.BeltConnection"
    ) -> "Iterable[_6024.BeltConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BeltConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BELT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_coaxial_connection(
        self: "Self", design_entity: "_2324.CoaxialConnection"
    ) -> "Iterable[_6039.CoaxialConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CoaxialConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_COAXIAL_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_connection(
        self: "Self", design_entity: "_2327.Connection"
    ) -> "Iterable[_6050.ConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_inter_mountable_component_connection(
        self: "Self", design_entity: "_2336.InterMountableComponentConnection"
    ) -> "Iterable[_6080.InterMountableComponentConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.InterMountableComponentConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_INTER_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_planetary_connection(
        self: "Self", design_entity: "_2342.PlanetaryConnection"
    ) -> "Iterable[_6100.PlanetaryConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PlanetaryConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PLANETARY_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_rolling_ring_connection(
        self: "Self", design_entity: "_2347.RollingRingConnection"
    ) -> "Iterable[_6110.RollingRingConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RollingRingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ROLLING_RING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_abstract_shaft_to_mountable_component_connection(
        self: "Self", design_entity: "_2320.AbstractShaftToMountableComponentConnection"
    ) -> "Iterable[_6018.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AbstractShaftToMountableComponentConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_differential_gear_mesh(
        self: "Self", design_entity: "_2356.BevelDifferentialGearMesh"
    ) -> "Iterable[_6027.BevelDifferentialGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelDifferentialGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_DIFFERENTIAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_concept_gear_mesh(
        self: "Self", design_entity: "_2360.ConceptGearMesh"
    ) -> "Iterable[_6045.ConceptGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConceptGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONCEPT_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_face_gear_mesh(
        self: "Self", design_entity: "_2366.FaceGearMesh"
    ) -> "Iterable[_6069.FaceGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.FaceGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_FACE_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_diff_gear_mesh(
        self: "Self", design_entity: "_2380.StraightBevelDiffGearMesh"
    ) -> "Iterable[_6123.StraightBevelDiffGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelDiffGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_DIFF_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_bevel_gear_mesh(
        self: "Self", design_entity: "_2358.BevelGearMesh"
    ) -> "Iterable[_6032.BevelGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.BevelGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_conical_gear_mesh(
        self: "Self", design_entity: "_2362.ConicalGearMesh"
    ) -> "Iterable[_6048.ConicalGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_agma_gleason_conical_gear_mesh(
        self: "Self", design_entity: "_2354.AGMAGleasonConicalGearMesh"
    ) -> "Iterable[_6020.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_AGMA_GLEASON_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cylindrical_gear_mesh(
        self: "Self", design_entity: "_2364.CylindricalGearMesh"
    ) -> "Iterable[_6063.CylindricalGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CylindricalGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYLINDRICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_hypoid_gear_mesh(
        self: "Self", design_entity: "_2370.HypoidGearMesh"
    ) -> "Iterable[_6078.HypoidGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.HypoidGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_HYPOID_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "Self", design_entity: "_2373.KlingelnbergCycloPalloidConicalGearMesh"
    ) -> "Iterable[_6082.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "Self", design_entity: "_2374.KlingelnbergCycloPalloidHypoidGearMesh"
    ) -> (
        "Iterable[_6085.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]"
    ):
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2375.KlingelnbergCycloPalloidSpiralBevelGearMesh"
    ) -> "Iterable[_6088.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_spiral_bevel_gear_mesh(
        self: "Self", design_entity: "_2378.SpiralBevelGearMesh"
    ) -> "Iterable[_6117.SpiralBevelGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.SpiralBevelGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_SPIRAL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_straight_bevel_gear_mesh(
        self: "Self", design_entity: "_2382.StraightBevelGearMesh"
    ) -> "Iterable[_6126.StraightBevelGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.StraightBevelGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_STRAIGHT_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_worm_gear_mesh(
        self: "Self", design_entity: "_2384.WormGearMesh"
    ) -> "Iterable[_6141.WormGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.WormGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_WORM_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_zerol_bevel_gear_mesh(
        self: "Self", design_entity: "_2386.ZerolBevelGearMesh"
    ) -> "Iterable[_6144.ZerolBevelGearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ZerolBevelGearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_ZEROL_BEVEL_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_gear_mesh(
        self: "Self", design_entity: "_2368.GearMesh"
    ) -> "Iterable[_6074.GearMeshCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.GearMeshCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_GEAR_MESH],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_central_bearing_connection(
        self: "Self", design_entity: "_2390.CycloidalDiscCentralBearingConnection"
    ) -> (
        "Iterable[_6059.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis]"
    ):
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CycloidalDiscCentralBearingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_cycloidal_disc_planetary_bearing_connection(
        self: "Self", design_entity: "_2393.CycloidalDiscPlanetaryBearingConnection"
    ) -> "Iterable[_6061.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.CycloidalDiscPlanetaryBearingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_ring_pins_to_disc_connection(
        self: "Self", design_entity: "_2396.RingPinsToDiscConnection"
    ) -> "Iterable[_6107.RingPinsToDiscConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.RingPinsToDiscConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_RING_PINS_TO_DISC_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_part_to_part_shear_coupling_connection(
        self: "Self", design_entity: "_2403.PartToPartShearCouplingConnection"
    ) -> "Iterable[_6098.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.PartToPartShearCouplingConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_PART_TO_PART_SHEAR_COUPLING_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @enforce_parameter_types
    def results_for_clutch_connection(
        self: "Self", design_entity: "_2397.ClutchConnection"
    ) -> "Iterable[_6037.ClutchConnectionCompoundHarmonicAnalysis]":
        """Iterable[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ClutchConnectionCompoundHarmonicAnalysis]

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)
        """
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call_overload(
                self.wrapped,
                "ResultsFor",
                [_CLUTCH_CONNECTION],
                design_entity.wrapped if design_entity else None,
            )
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CompoundHarmonicAnalysis
        """
        return _Cast_CompoundHarmonicAnalysis(self)
