"""GearLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7077

_GEAR_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "GearLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6964,
        _6973,
        _6976,
        _6977,
        _6978,
        _6988,
        _6992,
        _6995,
        _7012,
        _7017,
        _7035,
        _7042,
        _7056,
        _7063,
        _7066,
        _7069,
        _7081,
        _7106,
        _7112,
        _7115,
        _7118,
        _7119,
        _7135,
        _7138,
    )
    from mastapy._private.system_model.part_model.gears import _2589

    Self = TypeVar("Self", bound="GearLoadCase")
    CastSelf = TypeVar("CastSelf", bound="GearLoadCase._Cast_GearLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("GearLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearLoadCase:
    """Special nested class for casting GearLoadCase to subclasses."""

    __parent__: "GearLoadCase"

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7077.MountableComponentLoadCase":
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
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6964.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6964,
        )

        return self.__parent__._cast(_6964.AGMAGleasonConicalGearLoadCase)

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
    def bevel_gear_load_case(self: "CastSelf") -> "_6978.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6978,
        )

        return self.__parent__._cast(_6978.BevelGearLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6992.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConceptGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6995.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6995,
        )

        return self.__parent__._cast(_6995.ConicalGearLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7012.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7012,
        )

        return self.__parent__._cast(_7012.CylindricalGearLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7017.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.CylindricalPlanetGearLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7035.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7035,
        )

        return self.__parent__._cast(_7035.FaceGearLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7056.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7056,
        )

        return self.__parent__._cast(_7056.HypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(_7066.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7069.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(
            _7069.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

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
    def worm_gear_load_case(self: "CastSelf") -> "_7135.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.WormGearLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7138.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7138,
        )

        return self.__parent__._cast(_7138.ZerolBevelGearLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "GearLoadCase":
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
class GearLoadCase(_7077.MountableComponentLoadCase):
    """GearLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def gear_temperature(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "GearTemperature")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gear_temperature.setter
    @enforce_parameter_types
    def gear_temperature(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GearTemperature", value)

    @property
    def component_design(self: "Self") -> "_2589.Gear":
        """mastapy.system_model.part_model.gears.Gear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_manufacture_errors(self: "Self") -> "_7042.GearManufactureError":
        """mastapy.system_model.analyses_and_results.static_loads.GearManufactureError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearManufactureErrors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearLoadCase":
        """Cast to another type.

        Returns:
            _Cast_GearLoadCase
        """
        return _Cast_GearLoadCase(self)
