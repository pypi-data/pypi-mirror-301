"""PlanetaryGearSetLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7016

_PLANETARY_GEAR_SET_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "PlanetaryGearSetLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6957,
        _7046,
        _7081,
        _7105,
    )
    from mastapy._private.system_model.part_model.gears import _2601
    from mastapy._private.utility import _1638

    Self = TypeVar("Self", bound="PlanetaryGearSetLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetaryGearSetLoadCase._Cast_PlanetaryGearSetLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSetLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSetLoadCase:
    """Special nested class for casting PlanetaryGearSetLoadCase to subclasses."""

    __parent__: "PlanetaryGearSetLoadCase"

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7016.CylindricalGearSetLoadCase":
        return self.__parent__._cast(_7016.CylindricalGearSetLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7046.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7046,
        )

        return self.__parent__._cast(_7046.GearSetLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7105.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpecialisedAssemblyLoadCase)

    @property
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6957.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6957,
        )

        return self.__parent__._cast(_6957.AbstractAssemblyLoadCase)

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
    def planetary_gear_set_load_case(self: "CastSelf") -> "PlanetaryGearSetLoadCase":
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
class PlanetaryGearSetLoadCase(_7016.CylindricalGearSetLoadCase):
    """PlanetaryGearSetLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def include_gear_blank_elastic_distortion(
        self: "Self",
    ) -> "_1638.LoadCaseOverrideOption":
        """mastapy.utility.LoadCaseOverrideOption"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGearBlankElasticDistortion")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility._1638", "LoadCaseOverrideOption"
        )(value)

    @include_gear_blank_elastic_distortion.setter
    @enforce_parameter_types
    def include_gear_blank_elastic_distortion(
        self: "Self", value: "_1638.LoadCaseOverrideOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.LoadCaseOverrideOption"
        )
        pythonnet_property_set(self.wrapped, "IncludeGearBlankElasticDistortion", value)

    @property
    def specify_separate_micro_geometry_for_each_planet_gear(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifySeparateMicroGeometryForEachPlanetGear"
        )

        if temp is None:
            return False

        return temp

    @specify_separate_micro_geometry_for_each_planet_gear.setter
    @enforce_parameter_types
    def specify_separate_micro_geometry_for_each_planet_gear(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifySeparateMicroGeometryForEachPlanetGear",
            bool(value) if value is not None else False,
        )

    @property
    def assembly_design(self: "Self") -> "_2601.PlanetaryGearSet":
        """mastapy.system_model.part_model.gears.PlanetaryGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSetLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSetLoadCase
        """
        return _Cast_PlanetaryGearSetLoadCase(self)
