"""Part"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model import _2258

_PART = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "Part")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.math_utility import _1566
    from mastapy._private.system_model.connections_and_sockets import _2327
    from mastapy._private.system_model.import_export import _2297
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

    Self = TypeVar("Self", bound="Part")
    CastSelf = TypeVar("CastSelf", bound="Part._Cast_Part")


__docformat__ = "restructuredtext en"
__all__ = ("Part",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Part:
    """Special nested class for casting Part to subclasses."""

    __parent__: "Part"

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def assembly(self: "CastSelf") -> "_2489.Assembly":
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
    def part(self: "CastSelf") -> "Part":
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
class Part(_2258.DesignEntity):
    """Part

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def two_d_drawing_full_model(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingFullModel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_isometric_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDIsometricView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThreeDView")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xy_plane_with_z_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXyPlaneWithZAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_xz_plane_with_y_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInXzPlaneWithYAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_into_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingIntoTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def three_d_view_orientated_in_yz_plane_with_x_axis_pointing_out_of_the_screen(
        self: "Self",
    ) -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThreeDViewOrientatedInYzPlaneWithXAxisPointingOutOfTheScreen"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    def drawing_number(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DrawingNumber")

        if temp is None:
            return ""

        return temp

    @drawing_number.setter
    @enforce_parameter_types
    def drawing_number(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawingNumber", str(value) if value is not None else ""
        )

    @property
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
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
    def mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mass.setter
    @enforce_parameter_types
    def mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Mass", value)

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
    def mass_properties_from_design(self: "Self") -> "_1566.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassPropertiesFromDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def mass_properties_from_design_including_planetary_duplicates(
        self: "Self",
    ) -> "_1566.MassProperties":
        """mastapy.math_utility.MassProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MassPropertiesFromDesignIncludingPlanetaryDuplicates"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connections(self: "Self") -> "List[_2327.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Connections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def local_connections(self: "Self") -> "List[_2327.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def connections_to(self: "Self", part: "Part") -> "List[_2327.Connection]":
        """List[mastapy.system_model.connections_and_sockets.Connection]

        Args:
            part (mastapy.system_model.part_model.Part)
        """
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ConnectionsTo", part.wrapped if part else None
            )
        )

    @enforce_parameter_types
    def copy_to(self: "Self", container: "_2489.Assembly") -> "Part":
        """mastapy.system_model.part_model.Part

        Args:
            container (mastapy.system_model.part_model.Assembly)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CopyTo", container.wrapped if container else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def create_geometry_export_options(self: "Self") -> "_2297.GeometryExportOptions":
        """mastapy.system_model.import_export.GeometryExportOptions"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryExportOptions"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    def delete_connections(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteConnections")

    @property
    def cast_to(self: "Self") -> "_Cast_Part":
        """Cast to another type.

        Returns:
            _Cast_Part
        """
        return _Cast_Part(self)
