"""BevelGear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2572

_BEVEL_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelGear")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1220
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2500, _2522, _2526
    from mastapy._private.system_model.part_model.gears import (
        _2574,
        _2576,
        _2577,
        _2582,
        _2589,
        _2602,
        _2604,
        _2606,
        _2608,
        _2609,
        _2612,
    )

    Self = TypeVar("Self", bound="BevelGear")
    CastSelf = TypeVar("CastSelf", bound="BevelGear._Cast_BevelGear")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGear:
    """Special nested class for casting BevelGear to subclasses."""

    __parent__: "BevelGear"

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2572.AGMAGleasonConicalGear":
        return self.__parent__._cast(_2572.AGMAGleasonConicalGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2582.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2582

        return self.__parent__._cast(_2582.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2589.Gear":
        from mastapy._private.system_model.part_model.gears import _2589

        return self.__parent__._cast(_2589.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2522.MountableComponent":
        from mastapy._private.system_model.part_model import _2522

        return self.__parent__._cast(_2522.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2500.Component":
        from mastapy._private.system_model.part_model import _2500

        return self.__parent__._cast(_2500.Component)

    @property
    def part(self: "CastSelf") -> "_2526.Part":
        from mastapy._private.system_model.part_model import _2526

        return self.__parent__._cast(_2526.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2258.DesignEntity":
        from mastapy._private.system_model import _2258

        return self.__parent__._cast(_2258.DesignEntity)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2574.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2574

        return self.__parent__._cast(_2574.BevelDifferentialGear)

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
    def spiral_bevel_gear(self: "CastSelf") -> "_2602.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2602

        return self.__parent__._cast(_2602.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2604.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2604

        return self.__parent__._cast(_2604.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2606.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2606

        return self.__parent__._cast(_2606.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2608.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2608

        return self.__parent__._cast(_2608.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2609.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2609

        return self.__parent__._cast(_2609.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2612.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2612

        return self.__parent__._cast(_2612.ZerolBevelGear)

    @property
    def bevel_gear(self: "CastSelf") -> "BevelGear":
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
class BevelGear(_2572.AGMAGleasonConicalGear):
    """BevelGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def conical_gear_design(self: "Self") -> "_1220.BevelGearDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gear_design(self: "Self") -> "_1220.BevelGearDesign":
        """mastapy.gears.gear_designs.bevel.BevelGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGear":
        """Cast to another type.

        Returns:
            _Cast_BevelGear
        """
        return _Cast_BevelGear(self)
