"""MassDiscAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7288,
)

_MASS_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "MassDiscAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7188,
        _7243,
        _7245,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7072
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2866,
    )
    from mastapy._private.system_model.part_model import _2518

    Self = TypeVar("Self", bound="MassDiscAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MassDiscAdvancedTimeSteppingAnalysisForModulation._Cast_MassDiscAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MassDiscAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MassDiscAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting MassDiscAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "MassDiscAdvancedTimeSteppingAnalysisForModulation"

    @property
    def virtual_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7288.VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7288.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7243.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7243,
        )

        return self.__parent__._cast(
            _7243.MountableComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7188.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7188,
        )

        return self.__parent__._cast(
            _7188.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7245.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7245,
        )

        return self.__parent__._cast(
            _7245.PartAdvancedTimeSteppingAnalysisForModulation
        )

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
    def mass_disc_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "MassDiscAdvancedTimeSteppingAnalysisForModulation":
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
class MassDiscAdvancedTimeSteppingAnalysisForModulation(
    _7288.VirtualComponentAdvancedTimeSteppingAnalysisForModulation
):
    """MassDiscAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASS_DISC_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2518.MassDisc":
        """mastapy.system_model.part_model.MassDisc

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7072.MassDiscLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(self: "Self") -> "_2866.MassDiscSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.MassDiscSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(
        self: "Self",
    ) -> "List[MassDiscAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.MassDiscAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_MassDiscAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_MassDiscAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_MassDiscAdvancedTimeSteppingAnalysisForModulation(self)
