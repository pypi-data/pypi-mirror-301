"""VirtualComponentAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7243,
)

_VIRTUAL_COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "VirtualComponentAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7188,
        _7239,
        _7240,
        _7245,
        _7252,
        _7253,
        _7287,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2924,
    )
    from mastapy._private.system_model.part_model import _2538

    Self = TypeVar(
        "Self", bound="VirtualComponentAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentAdvancedTimeSteppingAnalysisForModulation._Cast_VirtualComponentAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting VirtualComponentAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "VirtualComponentAdvancedTimeSteppingAnalysisForModulation"

    @property
    def mountable_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7243.MountableComponentAdvancedTimeSteppingAnalysisForModulation":
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
    ) -> "_7239.MassDiscAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7239,
        )

        return self.__parent__._cast(
            _7239.MassDiscAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def measurement_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7240.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7240,
        )

        return self.__parent__._cast(
            _7240.MeasurementComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def point_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7252.PointLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7252,
        )

        return self.__parent__._cast(
            _7252.PointLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def power_load_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7253.PowerLoadAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7253,
        )

        return self.__parent__._cast(
            _7253.PowerLoadAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def unbalanced_mass_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7287.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7287,
        )

        return self.__parent__._cast(
            _7287.UnbalancedMassAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def virtual_component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
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
class VirtualComponentAdvancedTimeSteppingAnalysisForModulation(
    _7243.MountableComponentAdvancedTimeSteppingAnalysisForModulation
):
    """VirtualComponentAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _VIRTUAL_COMPONENT_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2538.VirtualComponent":
        """mastapy.system_model.part_model.VirtualComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2924.VirtualComponentSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.VirtualComponentSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_VirtualComponentAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_VirtualComponentAdvancedTimeSteppingAnalysisForModulation(self)
