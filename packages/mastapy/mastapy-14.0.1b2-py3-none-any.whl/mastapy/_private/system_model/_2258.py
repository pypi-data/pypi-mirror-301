"""DesignEntity"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DESIGN_ENTITY = python_net_import("SMT.MastaAPI.SystemModel", "DesignEntity")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2255
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
    from mastapy._private.utility.model_validation import _1844, _1845
    from mastapy._private.utility.scripting import _1792

    Self = TypeVar("Self", bound="DesignEntity")
    CastSelf = TypeVar("CastSelf", bound="DesignEntity._Cast_DesignEntity")


__docformat__ = "restructuredtext en"
__all__ = ("DesignEntity",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignEntity:
    """Special nested class for casting DesignEntity to subclasses."""

    __parent__: "DesignEntity"

    @property
    def abstract_shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2320.AbstractShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2320

        return self.__parent__._cast(_2320.AbstractShaftToMountableComponentConnection)

    @property
    def belt_connection(self: "CastSelf") -> "_2323.BeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2323

        return self.__parent__._cast(_2323.BeltConnection)

    @property
    def coaxial_connection(self: "CastSelf") -> "_2324.CoaxialConnection":
        from mastapy._private.system_model.connections_and_sockets import _2324

        return self.__parent__._cast(_2324.CoaxialConnection)

    @property
    def connection(self: "CastSelf") -> "_2327.Connection":
        from mastapy._private.system_model.connections_and_sockets import _2327

        return self.__parent__._cast(_2327.Connection)

    @property
    def cvt_belt_connection(self: "CastSelf") -> "_2328.CVTBeltConnection":
        from mastapy._private.system_model.connections_and_sockets import _2328

        return self.__parent__._cast(_2328.CVTBeltConnection)

    @property
    def inter_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2336.InterMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2336

        return self.__parent__._cast(_2336.InterMountableComponentConnection)

    @property
    def planetary_connection(self: "CastSelf") -> "_2342.PlanetaryConnection":
        from mastapy._private.system_model.connections_and_sockets import _2342

        return self.__parent__._cast(_2342.PlanetaryConnection)

    @property
    def rolling_ring_connection(self: "CastSelf") -> "_2347.RollingRingConnection":
        from mastapy._private.system_model.connections_and_sockets import _2347

        return self.__parent__._cast(_2347.RollingRingConnection)

    @property
    def shaft_to_mountable_component_connection(
        self: "CastSelf",
    ) -> "_2350.ShaftToMountableComponentConnection":
        from mastapy._private.system_model.connections_and_sockets import _2350

        return self.__parent__._cast(_2350.ShaftToMountableComponentConnection)

    @property
    def agma_gleason_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2354.AGMAGleasonConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2354

        return self.__parent__._cast(_2354.AGMAGleasonConicalGearMesh)

    @property
    def bevel_differential_gear_mesh(
        self: "CastSelf",
    ) -> "_2356.BevelDifferentialGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2356

        return self.__parent__._cast(_2356.BevelDifferentialGearMesh)

    @property
    def bevel_gear_mesh(self: "CastSelf") -> "_2358.BevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2358

        return self.__parent__._cast(_2358.BevelGearMesh)

    @property
    def concept_gear_mesh(self: "CastSelf") -> "_2360.ConceptGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2360

        return self.__parent__._cast(_2360.ConceptGearMesh)

    @property
    def conical_gear_mesh(self: "CastSelf") -> "_2362.ConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2362

        return self.__parent__._cast(_2362.ConicalGearMesh)

    @property
    def cylindrical_gear_mesh(self: "CastSelf") -> "_2364.CylindricalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2364

        return self.__parent__._cast(_2364.CylindricalGearMesh)

    @property
    def face_gear_mesh(self: "CastSelf") -> "_2366.FaceGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2366

        return self.__parent__._cast(_2366.FaceGearMesh)

    @property
    def gear_mesh(self: "CastSelf") -> "_2368.GearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2368

        return self.__parent__._cast(_2368.GearMesh)

    @property
    def hypoid_gear_mesh(self: "CastSelf") -> "_2370.HypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2370

        return self.__parent__._cast(_2370.HypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh(
        self: "CastSelf",
    ) -> "_2373.KlingelnbergCycloPalloidConicalGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2373

        return self.__parent__._cast(_2373.KlingelnbergCycloPalloidConicalGearMesh)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh(
        self: "CastSelf",
    ) -> "_2374.KlingelnbergCycloPalloidHypoidGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2374

        return self.__parent__._cast(_2374.KlingelnbergCycloPalloidHypoidGearMesh)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(
        self: "CastSelf",
    ) -> "_2375.KlingelnbergCycloPalloidSpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2375

        return self.__parent__._cast(_2375.KlingelnbergCycloPalloidSpiralBevelGearMesh)

    @property
    def spiral_bevel_gear_mesh(self: "CastSelf") -> "_2378.SpiralBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2378

        return self.__parent__._cast(_2378.SpiralBevelGearMesh)

    @property
    def straight_bevel_diff_gear_mesh(
        self: "CastSelf",
    ) -> "_2380.StraightBevelDiffGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2380

        return self.__parent__._cast(_2380.StraightBevelDiffGearMesh)

    @property
    def straight_bevel_gear_mesh(self: "CastSelf") -> "_2382.StraightBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2382

        return self.__parent__._cast(_2382.StraightBevelGearMesh)

    @property
    def worm_gear_mesh(self: "CastSelf") -> "_2384.WormGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2384

        return self.__parent__._cast(_2384.WormGearMesh)

    @property
    def zerol_bevel_gear_mesh(self: "CastSelf") -> "_2386.ZerolBevelGearMesh":
        from mastapy._private.system_model.connections_and_sockets.gears import _2386

        return self.__parent__._cast(_2386.ZerolBevelGearMesh)

    @property
    def cycloidal_disc_central_bearing_connection(
        self: "CastSelf",
    ) -> "_2390.CycloidalDiscCentralBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2390,
        )

        return self.__parent__._cast(_2390.CycloidalDiscCentralBearingConnection)

    @property
    def cycloidal_disc_planetary_bearing_connection(
        self: "CastSelf",
    ) -> "_2393.CycloidalDiscPlanetaryBearingConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2393,
        )

        return self.__parent__._cast(_2393.CycloidalDiscPlanetaryBearingConnection)

    @property
    def ring_pins_to_disc_connection(
        self: "CastSelf",
    ) -> "_2396.RingPinsToDiscConnection":
        from mastapy._private.system_model.connections_and_sockets.cycloidal import (
            _2396,
        )

        return self.__parent__._cast(_2396.RingPinsToDiscConnection)

    @property
    def clutch_connection(self: "CastSelf") -> "_2397.ClutchConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2397,
        )

        return self.__parent__._cast(_2397.ClutchConnection)

    @property
    def concept_coupling_connection(
        self: "CastSelf",
    ) -> "_2399.ConceptCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2399,
        )

        return self.__parent__._cast(_2399.ConceptCouplingConnection)

    @property
    def coupling_connection(self: "CastSelf") -> "_2401.CouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2401,
        )

        return self.__parent__._cast(_2401.CouplingConnection)

    @property
    def part_to_part_shear_coupling_connection(
        self: "CastSelf",
    ) -> "_2403.PartToPartShearCouplingConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2403,
        )

        return self.__parent__._cast(_2403.PartToPartShearCouplingConnection)

    @property
    def spring_damper_connection(self: "CastSelf") -> "_2405.SpringDamperConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2405,
        )

        return self.__parent__._cast(_2405.SpringDamperConnection)

    @property
    def torque_converter_connection(
        self: "CastSelf",
    ) -> "_2407.TorqueConverterConnection":
        from mastapy._private.system_model.connections_and_sockets.couplings import (
            _2407,
        )

        return self.__parent__._cast(_2407.TorqueConverterConnection)

    @property
    def assembly(self: "CastSelf") -> "_2489.Assembly":
        from mastapy._private.system_model.part_model import _2489

        return self.__parent__._cast(_2489.Assembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2490.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2490

        return self.__parent__._cast(_2490.AbstractAssembly)

    @property
    def abstract_shaft(self: "CastSelf") -> "_2491.AbstractShaft":
        from mastapy._private.system_model.part_model import _2491

        return self.__parent__._cast(_2491.AbstractShaft)

    @property
    def abstract_shaft_or_housing(self: "CastSelf") -> "_2492.AbstractShaftOrHousing":
        from mastapy._private.system_model.part_model import _2492

        return self.__parent__._cast(_2492.AbstractShaftOrHousing)

    @property
    def bearing(self: "CastSelf") -> "_2495.Bearing":
        from mastapy._private.system_model.part_model import _2495

        return self.__parent__._cast(_2495.Bearing)

    @property
    def bolt(self: "CastSelf") -> "_2498.Bolt":
        from mastapy._private.system_model.part_model import _2498

        return self.__parent__._cast(_2498.Bolt)

    @property
    def bolted_joint(self: "CastSelf") -> "_2499.BoltedJoint":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.BoltedJoint)

    @property
    def component(self: "CastSelf") -> "_2500.Component":
        from mastapy._private.system_model.part_model import _2500

        return self.__parent__._cast(_2500.Component)

    @property
    def connector(self: "CastSelf") -> "_2503.Connector":
        from mastapy._private.system_model.part_model import _2503

        return self.__parent__._cast(_2503.Connector)

    @property
    def datum(self: "CastSelf") -> "_2504.Datum":
        from mastapy._private.system_model.part_model import _2504

        return self.__parent__._cast(_2504.Datum)

    @property
    def external_cad_model(self: "CastSelf") -> "_2508.ExternalCADModel":
        from mastapy._private.system_model.part_model import _2508

        return self.__parent__._cast(_2508.ExternalCADModel)

    @property
    def fe_part(self: "CastSelf") -> "_2509.FEPart":
        from mastapy._private.system_model.part_model import _2509

        return self.__parent__._cast(_2509.FEPart)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2510.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2510

        return self.__parent__._cast(_2510.FlexiblePinAssembly)

    @property
    def guide_dxf_model(self: "CastSelf") -> "_2511.GuideDxfModel":
        from mastapy._private.system_model.part_model import _2511

        return self.__parent__._cast(_2511.GuideDxfModel)

    @property
    def mass_disc(self: "CastSelf") -> "_2518.MassDisc":
        from mastapy._private.system_model.part_model import _2518

        return self.__parent__._cast(_2518.MassDisc)

    @property
    def measurement_component(self: "CastSelf") -> "_2519.MeasurementComponent":
        from mastapy._private.system_model.part_model import _2519

        return self.__parent__._cast(_2519.MeasurementComponent)

    @property
    def microphone(self: "CastSelf") -> "_2520.Microphone":
        from mastapy._private.system_model.part_model import _2520

        return self.__parent__._cast(_2520.Microphone)

    @property
    def microphone_array(self: "CastSelf") -> "_2521.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MicrophoneArray)

    @property
    def mountable_component(self: "CastSelf") -> "_2522.MountableComponent":
        from mastapy._private.system_model.part_model import _2522

        return self.__parent__._cast(_2522.MountableComponent)

    @property
    def oil_seal(self: "CastSelf") -> "_2524.OilSeal":
        from mastapy._private.system_model.part_model import _2524

        return self.__parent__._cast(_2524.OilSeal)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def planet_carrier(self: "CastSelf") -> "_2527.PlanetCarrier":
        from mastapy._private.system_model.part_model import _2527

        return self.__parent__._cast(_2527.PlanetCarrier)

    @property
    def point_load(self: "CastSelf") -> "_2529.PointLoad":
        from mastapy._private.system_model.part_model import _2529

        return self.__parent__._cast(_2529.PointLoad)

    @property
    def power_load(self: "CastSelf") -> "_2530.PowerLoad":
        from mastapy._private.system_model.part_model import _2530

        return self.__parent__._cast(_2530.PowerLoad)

    @property
    def root_assembly(self: "CastSelf") -> "_2533.RootAssembly":
        from mastapy._private.system_model.part_model import _2533

        return self.__parent__._cast(_2533.RootAssembly)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2535.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.SpecialisedAssembly)

    @property
    def unbalanced_mass(self: "CastSelf") -> "_2536.UnbalancedMass":
        from mastapy._private.system_model.part_model import _2536

        return self.__parent__._cast(_2536.UnbalancedMass)

    @property
    def virtual_component(self: "CastSelf") -> "_2538.VirtualComponent":
        from mastapy._private.system_model.part_model import _2538

        return self.__parent__._cast(_2538.VirtualComponent)

    @property
    def shaft(self: "CastSelf") -> "_2541.Shaft":
        from mastapy._private.system_model.part_model.shaft_model import _2541

        return self.__parent__._cast(_2541.Shaft)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2572.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2572

        return self.__parent__._cast(_2572.AGMAGleasonConicalGear)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2573.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2574.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.BevelDifferentialGear)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2575.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.BevelDifferentialGearSet)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2576.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2576

        return self.__parent__._cast(_2576.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2577.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2577

        return self.__parent__._cast(_2577.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2578.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.BevelGear)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2579.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.BevelGearSet)

    @property
    def concept_gear(self: "CastSelf") -> "_2580.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2580

        return self.__parent__._cast(_2580.ConceptGear)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2581.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConceptGearSet)

    @property
    def conical_gear(self: "CastSelf") -> "_2582.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.ConicalGear)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2583.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConicalGearSet)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2584.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2584

        return self.__parent__._cast(_2584.CylindricalGear)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2585.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.CylindricalGearSet)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2586.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2586

        return self.__parent__._cast(_2586.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2587.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2587

        return self.__parent__._cast(_2587.FaceGear)

    @property
    def face_gear_set(self: "CastSelf") -> "_2588.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.FaceGearSet)

    @property
    def gear(self: "CastSelf") -> "_2589.Gear":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.Gear)

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.GearSet)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2593.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2593

        return self.__parent__._cast(_2593.HypoidGear)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2594.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2595.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2595

        return self.__parent__._cast(_2595.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2597.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2597

        return self.__parent__._cast(_2597.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2599.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2599

        return self.__parent__._cast(_2599.KlingelnbergCycloPalloidSpiralBevelGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2600.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2600

        return self.__parent__._cast(_2600.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2601.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2601

        return self.__parent__._cast(_2601.PlanetaryGearSet)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2602.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.SpiralBevelGear)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2603.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2604.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelDiffGear)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2605.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2606.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelGear)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2607.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelGearSet)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2608.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2609.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.StraightBevelSunGear)

    @property
    def worm_gear(self: "CastSelf") -> "_2610.WormGear":
        from mastapy._private.system_model.part_model.gears import _2610

        return self.__parent__._cast(_2610.WormGear)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2611.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.WormGearSet)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2612.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.ZerolBevelGear)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2613.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2627.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2627

        return self.__parent__._cast(_2627.CycloidalAssembly)

    @property
    def cycloidal_disc(self: "CastSelf") -> "_2628.CycloidalDisc":
        from mastapy._private.system_model.part_model.cycloidal import _2628

        return self.__parent__._cast(_2628.CycloidalDisc)

    @property
    def ring_pins(self: "CastSelf") -> "_2629.RingPins":
        from mastapy._private.system_model.part_model.cycloidal import _2629

        return self.__parent__._cast(_2629.RingPins)

    @property
    def belt_drive(self: "CastSelf") -> "_2636.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2636

        return self.__parent__._cast(_2636.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2638.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2638

        return self.__parent__._cast(_2638.Clutch)

    @property
    def clutch_half(self: "CastSelf") -> "_2639.ClutchHalf":
        from mastapy._private.system_model.part_model.couplings import _2639

        return self.__parent__._cast(_2639.ClutchHalf)

    @property
    def concept_coupling(self: "CastSelf") -> "_2641.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2641

        return self.__parent__._cast(_2641.ConceptCoupling)

    @property
    def concept_coupling_half(self: "CastSelf") -> "_2642.ConceptCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2642

        return self.__parent__._cast(_2642.ConceptCouplingHalf)

    @property
    def coupling(self: "CastSelf") -> "_2644.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2644

        return self.__parent__._cast(_2644.Coupling)

    @property
    def coupling_half(self: "CastSelf") -> "_2645.CouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2645

        return self.__parent__._cast(_2645.CouplingHalf)

    @property
    def cvt(self: "CastSelf") -> "_2647.CVT":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.CVT)

    @property
    def cvt_pulley(self: "CastSelf") -> "_2648.CVTPulley":
        from mastapy._private.system_model.part_model.couplings import _2648

        return self.__parent__._cast(_2648.CVTPulley)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2649.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.PartToPartShearCoupling)

    @property
    def part_to_part_shear_coupling_half(
        self: "CastSelf",
    ) -> "_2650.PartToPartShearCouplingHalf":
        from mastapy._private.system_model.part_model.couplings import _2650

        return self.__parent__._cast(_2650.PartToPartShearCouplingHalf)

    @property
    def pulley(self: "CastSelf") -> "_2652.Pulley":
        from mastapy._private.system_model.part_model.couplings import _2652

        return self.__parent__._cast(_2652.Pulley)

    @property
    def rolling_ring(self: "CastSelf") -> "_2658.RollingRing":
        from mastapy._private.system_model.part_model.couplings import _2658

        return self.__parent__._cast(_2658.RollingRing)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2659.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2659

        return self.__parent__._cast(_2659.RollingRingAssembly)

    @property
    def shaft_hub_connection(self: "CastSelf") -> "_2660.ShaftHubConnection":
        from mastapy._private.system_model.part_model.couplings import _2660

        return self.__parent__._cast(_2660.ShaftHubConnection)

    @property
    def spring_damper(self: "CastSelf") -> "_2665.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.SpringDamper)

    @property
    def spring_damper_half(self: "CastSelf") -> "_2666.SpringDamperHalf":
        from mastapy._private.system_model.part_model.couplings import _2666

        return self.__parent__._cast(_2666.SpringDamperHalf)

    @property
    def synchroniser(self: "CastSelf") -> "_2667.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.Synchroniser)

    @property
    def synchroniser_half(self: "CastSelf") -> "_2669.SynchroniserHalf":
        from mastapy._private.system_model.part_model.couplings import _2669

        return self.__parent__._cast(_2669.SynchroniserHalf)

    @property
    def synchroniser_part(self: "CastSelf") -> "_2670.SynchroniserPart":
        from mastapy._private.system_model.part_model.couplings import _2670

        return self.__parent__._cast(_2670.SynchroniserPart)

    @property
    def synchroniser_sleeve(self: "CastSelf") -> "_2671.SynchroniserSleeve":
        from mastapy._private.system_model.part_model.couplings import _2671

        return self.__parent__._cast(_2671.SynchroniserSleeve)

    @property
    def torque_converter(self: "CastSelf") -> "_2672.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2672

        return self.__parent__._cast(_2672.TorqueConverter)

    @property
    def torque_converter_pump(self: "CastSelf") -> "_2673.TorqueConverterPump":
        from mastapy._private.system_model.part_model.couplings import _2673

        return self.__parent__._cast(_2673.TorqueConverterPump)

    @property
    def torque_converter_turbine(self: "CastSelf") -> "_2675.TorqueConverterTurbine":
        from mastapy._private.system_model.part_model.couplings import _2675

        return self.__parent__._cast(_2675.TorqueConverterTurbine)

    @property
    def design_entity(self: "CastSelf") -> "DesignEntity":
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
class DesignEntity(_0.APIBase):
    """DesignEntity

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DESIGN_ENTITY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def full_name_without_root_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FullNameWithoutRootName")

        if temp is None:
            return ""

        return temp

    @property
    def id(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ID")

        if temp is None:
            return ""

        return temp

    @property
    def icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Icon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def small_icon(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmallIcon")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def unique_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UniqueName")

        if temp is None:
            return ""

        return temp

    @property
    def design_properties(self: "Self") -> "_2255.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def all_design_entities(self: "Self") -> "List[DesignEntity]":
        """List[mastapy.system_model.DesignEntity]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllDesignEntities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def all_status_errors(self: "Self") -> "List[_1845.StatusItem]":
        """List[mastapy.utility.model_validation.StatusItem]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllStatusErrors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def status(self: "Self") -> "_1844.Status":
        """mastapy.utility.model_validation.Status

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def user_specified_data(self: "Self") -> "_1792.UserSpecifiedData":
        """mastapy.utility.scripting.UserSpecifiedData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_DesignEntity":
        """Cast to another type.

        Returns:
            _Cast_DesignEntity
        """
        return _Cast_DesignEntity(self)
