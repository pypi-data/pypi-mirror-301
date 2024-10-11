"""KlingelnbergCycloPalloidConicalGearSet"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2583

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1009
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2490, _2526, _2535
    from mastapy._private.system_model.part_model.gears import _2591, _2598, _2600

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearSet")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSet._Cast_KlingelnbergCycloPalloidConicalGearSet",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSet:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSet to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSet"

    @property
    def conical_gear_set(self: "CastSelf") -> "_2583.ConicalGearSet":
        return self.__parent__._cast(_2583.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2591.GearSet":
        from mastapy._private.system_model.part_model.gears import _2591

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
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSet":
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
class KlingelnbergCycloPalloidConicalGearSet(_2583.ConicalGearSet):
    """KlingelnbergCycloPalloidConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_set_design(
        self: "Self",
    ) -> "_1009.KlingelnbergConicalGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def klingelnberg_conical_gear_set_design(
        self: "Self",
    ) -> "_1009.KlingelnbergConicalGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSet
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSet(self)
