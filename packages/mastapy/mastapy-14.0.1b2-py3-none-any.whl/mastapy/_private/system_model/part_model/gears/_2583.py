"""ConicalGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2591

_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "ConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1196
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2490, _2526, _2535
    from mastapy._private.system_model.part_model.gears import (
        _2573,
        _2575,
        _2579,
        _2582,
        _2594,
        _2596,
        _2598,
        _2600,
        _2603,
        _2605,
        _2607,
        _2613,
    )

    Self = TypeVar("Self", bound="ConicalGearSet")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearSet._Cast_ConicalGearSet")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSet:
    """Special nested class for casting ConicalGearSet to subclasses."""

    __parent__: "ConicalGearSet"

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
        return self.__parent__._cast(_2591.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2535.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2535

        return self.__parent__._cast(_2535.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2490.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2490

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
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2613.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2613

        return self.__parent__._cast(_2613.ZerolBevelGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "ConicalGearSet":
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
class ConicalGearSet(_2591.GearSet):
    """ConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def active_gear_set_design(self: "Self") -> "_1196.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gear_set_design(self: "Self") -> "_1196.ConicalGearSetDesign":
        """mastapy.gears.gear_designs.conical.ConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears(self: "Self") -> "List[_2582.ConicalGear]":
        """List[mastapy.system_model.part_model.gears.ConicalGear]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSet
        """
        return _Cast_ConicalGearSet(self)
