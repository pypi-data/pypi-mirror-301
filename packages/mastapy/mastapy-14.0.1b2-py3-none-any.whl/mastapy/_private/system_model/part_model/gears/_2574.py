"""BevelDifferentialGear"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2578

_BEVEL_DIFFERENTIAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "BevelDifferentialGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.bevel import _1220
    from mastapy._private.system_model import _2258
    from mastapy._private.system_model.part_model import _2500, _2522, _2526
    from mastapy._private.system_model.part_model.gears import (
        _2572,
        _2576,
        _2577,
        _2582,
        _2589,
    )

    Self = TypeVar("Self", bound="BevelDifferentialGear")
    CastSelf = TypeVar(
        "CastSelf", bound="BevelDifferentialGear._Cast_BevelDifferentialGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelDifferentialGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelDifferentialGear:
    """Special nested class for casting BevelDifferentialGear to subclasses."""

    __parent__: "BevelDifferentialGear"

    @property
    def bevel_gear(self: "CastSelf") -> "_2578.BevelGear":
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
    def bevel_differential_gear(self: "CastSelf") -> "BevelDifferentialGear":
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
class BevelDifferentialGear(_2578.BevelGear):
    """BevelDifferentialGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_DIFFERENTIAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_BevelDifferentialGear":
        """Cast to another type.

        Returns:
            _Cast_BevelDifferentialGear
        """
        return _Cast_BevelDifferentialGear(self)
