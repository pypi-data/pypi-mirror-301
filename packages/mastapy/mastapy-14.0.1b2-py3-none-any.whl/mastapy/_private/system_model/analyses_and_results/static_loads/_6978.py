"""BevelGearLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6964

_BEVEL_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "BevelGearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6973,
        _6976,
        _6977,
        _6988,
        _6995,
        _7041,
        _7077,
        _7081,
        _7106,
        _7112,
        _7115,
        _7118,
        _7119,
        _7138,
    )
    from mastapy._private.system_model.part_model.gears import _2578

    Self = TypeVar("Self", bound="BevelGearLoadCase")
    CastSelf = TypeVar("CastSelf", bound="BevelGearLoadCase._Cast_BevelGearLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearLoadCase:
    """Special nested class for casting BevelGearLoadCase to subclasses."""

    __parent__: "BevelGearLoadCase"

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6964.AGMAGleasonConicalGearLoadCase":
        return self.__parent__._cast(_6964.AGMAGleasonConicalGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6995.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6995,
        )

        return self.__parent__._cast(_6995.ConicalGearLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7041.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7041,
        )

        return self.__parent__._cast(_7041.GearLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7077.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7077,
        )

        return self.__parent__._cast(_7077.MountableComponentLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6988.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ComponentLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "_7081.PartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7081,
        )

        return self.__parent__._cast(_7081.PartLoadCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2740.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2740

        return self.__parent__._cast(_2740.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6976.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6976,
        )

        return self.__parent__._cast(_6976.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6977.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelDifferentialSunGearLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7106.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7106,
        )

        return self.__parent__._cast(_7106.SpiralBevelGearLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelGearLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7118.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7119.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.StraightBevelSunGearLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7138.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7138,
        )

        return self.__parent__._cast(_7138.ZerolBevelGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "BevelGearLoadCase":
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
class BevelGearLoadCase(_6964.AGMAGleasonConicalGearLoadCase):
    """BevelGearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2578.BevelGear":
        """mastapy.system_model.part_model.gears.BevelGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_BevelGearLoadCase
        """
        return _Cast_BevelGearLoadCase(self)
