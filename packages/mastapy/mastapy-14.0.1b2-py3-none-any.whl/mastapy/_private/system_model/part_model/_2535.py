"""SpecialisedAssembly"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2490

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2499, _2510, _2521, _2526
    from mastapy._private.system_model.part_model.couplings import (
        _2636,
        _2638,
        _2641,
        _2644,
        _2647,
        _2649,
        _2659,
        _2665,
        _2667,
        _2672,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2627
    from mastapy._private.system_model.part_model.gears import (
        _2573,
        _2575,
        _2579,
        _2581,
        _2583,
        _2585,
        _2588,
        _2591,
        _2594,
        _2596,
        _2598,
        _2600,
        _2601,
        _2603,
        _2605,
        _2607,
        _2611,
        _2613,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2490.AbstractAssembly":
        return self.__parent__._cast(_2490.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def bolted_joint(self: "CastSelf") -> "_2499.BoltedJoint":
        from mastapy._private.system_model.part_model import _2499

        return self.__parent__._cast(_2499.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2510.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2510

        return self.__parent__._cast(_2510.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2521.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2521

        return self.__parent__._cast(_2521.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2573.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2573

        return self.__parent__._cast(_2573.AGMAGleasonConicalGearSet)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2575.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2575

        return self.__parent__._cast(_2575.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2579.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2579

        return self.__parent__._cast(_2579.BevelGearSet)

    @property
    def concept_gear_set(self: "CastSelf") -> "_2581.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2581

        return self.__parent__._cast(_2581.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2583.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2583

        return self.__parent__._cast(_2583.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2585.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2585

        return self.__parent__._cast(_2585.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2588.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2588

        return self.__parent__._cast(_2588.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
        from mastapy._private.system_model.part_model.gears import _2591

        return self.__parent__._cast(_2591.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2594.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2594

        return self.__parent__._cast(_2594.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2596.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2596

        return self.__parent__._cast(_2596.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2598.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2598

        return self.__parent__._cast(_2598.KlingelnbergCycloPalloidHypoidGearSet)

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
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2603.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2603

        return self.__parent__._cast(_2603.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2605.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2605

        return self.__parent__._cast(_2605.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2607.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2607

        return self.__parent__._cast(_2607.StraightBevelGearSet)

    @property
    def worm_gear_set(self: "CastSelf") -> "_2611.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2611

        return self.__parent__._cast(_2611.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2613.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2627.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2627

        return self.__parent__._cast(_2627.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2636.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2636

        return self.__parent__._cast(_2636.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2638.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2638

        return self.__parent__._cast(_2638.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2641.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2641

        return self.__parent__._cast(_2641.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2644.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2644

        return self.__parent__._cast(_2644.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2647.CVT":
        from mastapy._private.system_model.part_model.couplings import _2647

        return self.__parent__._cast(_2647.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2649.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2649

        return self.__parent__._cast(_2649.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2659.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2659

        return self.__parent__._cast(_2659.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2665.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2665

        return self.__parent__._cast(_2665.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2667.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2667

        return self.__parent__._cast(_2667.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2672.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2672

        return self.__parent__._cast(_2672.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2490.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
