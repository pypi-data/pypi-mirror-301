"""StraightBevelSunGear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2604

_STRAIGHT_BEVEL_SUN_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "StraightBevelSunGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2500, _2522, _2526
    from mastapy._private.system_model.part_model.gears import (
        _2572,
        _2578,
        _2582,
        _2589,
    )

    Self = TypeVar("Self", bound="StraightBevelSunGear")
    CastSelf = TypeVar(
        "CastSelf", bound="StraightBevelSunGear._Cast_StraightBevelSunGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGear:
    """Special nested class for casting StraightBevelSunGear to subclasses."""

    __parent__: "StraightBevelSunGear"

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2604.StraightBevelDiffGear":
        return self.__parent__._cast(_2604.StraightBevelDiffGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2578.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2578

        return self.__parent__._cast(_2578.BevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2572.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2572

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
    def straight_bevel_sun_gear(self: "CastSelf") -> "StraightBevelSunGear":
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
class StraightBevelSunGear(_2604.StraightBevelDiffGear):
    """StraightBevelSunGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_SUN_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelSunGear":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGear
        """
        return _Cast_StraightBevelSunGear(self)
