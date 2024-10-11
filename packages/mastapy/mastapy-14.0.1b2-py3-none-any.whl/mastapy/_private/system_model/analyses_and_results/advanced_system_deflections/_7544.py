"""StraightBevelGearSetAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7447,
)

_STRAIGHT_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "StraightBevelGearSetAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.straight_bevel import _410
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7426,
        _7435,
        _7463,
        _7491,
        _7513,
        _7532,
        _7542,
        _7543,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7117
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2906,
    )
    from mastapy._private.system_model.part_model.gears import _2607

    Self = TypeVar("Self", bound="StraightBevelGearSetAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearSetAdvancedSystemDeflection._Cast_StraightBevelGearSetAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearSetAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearSetAdvancedSystemDeflection:
    """Special nested class for casting StraightBevelGearSetAdvancedSystemDeflection to subclasses."""

    __parent__: "StraightBevelGearSetAdvancedSystemDeflection"

    @property
    def bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7447.BevelGearSetAdvancedSystemDeflection":
        return self.__parent__._cast(_7447.BevelGearSetAdvancedSystemDeflection)

    @property
    def agma_gleason_conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7435.AGMAGleasonConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7435,
        )

        return self.__parent__._cast(
            _7435.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7463.ConicalGearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7463,
        )

        return self.__parent__._cast(_7463.ConicalGearSetAdvancedSystemDeflection)

    @property
    def gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7491.GearSetAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7491,
        )

        return self.__parent__._cast(_7491.GearSetAdvancedSystemDeflection)

    @property
    def specialised_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7532.SpecialisedAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7532,
        )

        return self.__parent__._cast(_7532.SpecialisedAssemblyAdvancedSystemDeflection)

    @property
    def abstract_assembly_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7426.AbstractAssemblyAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7426,
        )

        return self.__parent__._cast(_7426.AbstractAssemblyAdvancedSystemDeflection)

    @property
    def part_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7513.PartAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7513,
        )

        return self.__parent__._cast(_7513.PartAdvancedSystemDeflection)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

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
    def straight_bevel_gear_set_advanced_system_deflection(
        self: "CastSelf",
    ) -> "StraightBevelGearSetAdvancedSystemDeflection":
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
class StraightBevelGearSetAdvancedSystemDeflection(
    _7447.BevelGearSetAdvancedSystemDeflection
):
    """StraightBevelGearSetAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2607.StraightBevelGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7117.StraightBevelGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_410.StraightBevelGearSetRating":
        """mastapy.gears.rating.straight_bevel.StraightBevelGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_detailed_analysis(self: "Self") -> "_410.StraightBevelGearSetRating":
        """mastapy.gears.rating.straight_bevel.StraightBevelGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_system_deflection_results(
        self: "Self",
    ) -> "List[_2906.StraightBevelGearSetSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelGearSetSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblySystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_gears_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7542.StraightBevelGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_gears_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7542.StraightBevelGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelGearsAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7543.StraightBevelGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_meshes_advanced_system_deflection(
        self: "Self",
    ) -> "List[_7543.StraightBevelGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelMeshesAdvancedSystemDeflection"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearSetAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearSetAdvancedSystemDeflection
        """
        return _Cast_StraightBevelGearSetAdvancedSystemDeflection(self)
