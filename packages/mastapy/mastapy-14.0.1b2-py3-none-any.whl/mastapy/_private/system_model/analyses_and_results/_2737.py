"""Context"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CONTEXT = python_net_import("SMT.MastaAPI.SystemModel.AnalysesAndResults", "Context")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model import _2255
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7430,
        _7432,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7162,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7707,
        _7709,
        _7716,
        _7722,
        _7723,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6729,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6471,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5866,
        _5895,
        _5899,
        _5904,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6208,
        _6226,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5595
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4740,
        _4771,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5319,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5028,
        _5056,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4500,
        _4501,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4231
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3919,
        _3975,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6954,
        _6955,
        _6956,
        _6962,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3126,
        _3182,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3710,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3447,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2914,
        _2921,
    )
    from mastapy._private.utility import _1632

    Self = TypeVar("Self", bound="Context")
    CastSelf = TypeVar("CastSelf", bound="Context._Cast_Context")


__docformat__ = "restructuredtext en"
__all__ = ("Context",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Context:
    """Special nested class for casting Context to subclasses."""

    __parent__: "Context"

    @property
    def system_deflection(self: "CastSelf") -> "_2914.SystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2914,
        )

        return self.__parent__._cast(_2914.SystemDeflection)

    @property
    def torsional_system_deflection(
        self: "CastSelf",
    ) -> "_2921.TorsionalSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2921,
        )

        return self.__parent__._cast(_2921.TorsionalSystemDeflection)

    @property
    def dynamic_model_for_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3126.DynamicModelForSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3126,
        )

        return self.__parent__._cast(
            _3126.DynamicModelForSteadyStateSynchronousResponse
        )

    @property
    def steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3182.SteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3182,
        )

        return self.__parent__._cast(_3182.SteadyStateSynchronousResponse)

    @property
    def steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3447.SteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3447,
        )

        return self.__parent__._cast(_3447.SteadyStateSynchronousResponseOnAShaft)

    @property
    def steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3710.SteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3710,
        )

        return self.__parent__._cast(_3710.SteadyStateSynchronousResponseAtASpeed)

    @property
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_3919.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3919,
        )

        return self.__parent__._cast(_3919.DynamicModelForStabilityAnalysis)

    @property
    def stability_analysis(self: "CastSelf") -> "_3975.StabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3975,
        )

        return self.__parent__._cast(_3975.StabilityAnalysis)

    @property
    def power_flow(self: "CastSelf") -> "_4231.PowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4231

        return self.__parent__._cast(_4231.PowerFlow)

    @property
    def parametric_study_static_load(
        self: "CastSelf",
    ) -> "_4500.ParametricStudyStaticLoad":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4500,
        )

        return self.__parent__._cast(_4500.ParametricStudyStaticLoad)

    @property
    def parametric_study_tool(self: "CastSelf") -> "_4501.ParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4501,
        )

        return self.__parent__._cast(_4501.ParametricStudyTool)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4740.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4740,
        )

        return self.__parent__._cast(_4740.DynamicModelForModalAnalysis)

    @property
    def modal_analysis(self: "CastSelf") -> "_4771.ModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4771,
        )

        return self.__parent__._cast(_4771.ModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5028.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5028,
        )

        return self.__parent__._cast(_5028.DynamicModelAtAStiffness)

    @property
    def modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5056.ModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5056,
        )

        return self.__parent__._cast(_5056.ModalAnalysisAtAStiffness)

    @property
    def modal_analysis_at_a_speed(self: "CastSelf") -> "_5319.ModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5319,
        )

        return self.__parent__._cast(_5319.ModalAnalysisAtASpeed)

    @property
    def multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5595.MultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5595,
        )

        return self.__parent__._cast(_5595.MultibodyDynamicsAnalysis)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5866.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5866,
        )

        return self.__parent__._cast(_5866.DynamicModelForHarmonicAnalysis)

    @property
    def harmonic_analysis(self: "CastSelf") -> "_5895.HarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5895,
        )

        return self.__parent__._cast(_5895.HarmonicAnalysis)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_5899.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5899,
        )

        return self.__parent__._cast(
            _5899.HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def harmonic_analysis_with_varying_stiffness_static_load_case(
        self: "CastSelf",
    ) -> "_5904.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5904,
        )

        return self.__parent__._cast(
            _5904.HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
        )

    @property
    def harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6208.HarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6208,
        )

        return self.__parent__._cast(_6208.HarmonicAnalysisOfSingleExcitation)

    @property
    def modal_analysis_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6226.ModalAnalysisForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
            _6226,
        )

        return self.__parent__._cast(_6226.ModalAnalysisForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6471.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6471,
        )

        return self.__parent__._cast(_6471.DynamicAnalysis)

    @property
    def critical_speed_analysis(self: "CastSelf") -> "_6729.CriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6729,
        )

        return self.__parent__._cast(_6729.CriticalSpeedAnalysis)

    @property
    def load_case(self: "CastSelf") -> "_6954.LoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6954,
        )

        return self.__parent__._cast(_6954.LoadCase)

    @property
    def static_load_case(self: "CastSelf") -> "_6955.StaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6955,
        )

        return self.__parent__._cast(_6955.StaticLoadCase)

    @property
    def time_series_load_case(self: "CastSelf") -> "_6956.TimeSeriesLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6956,
        )

        return self.__parent__._cast(_6956.TimeSeriesLoadCase)

    @property
    def advanced_time_stepping_analysis_for_modulation_static_load_case(
        self: "CastSelf",
    ) -> "_6962.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6962,
        )

        return self.__parent__._cast(
            _6962.AdvancedTimeSteppingAnalysisForModulationStaticLoadCase
        )

    @property
    def advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7162.AdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7162,
        )

        return self.__parent__._cast(_7162.AdvancedTimeSteppingAnalysisForModulation)

    @property
    def advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7430.AdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7430,
        )

        return self.__parent__._cast(_7430.AdvancedSystemDeflection)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7432.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7432,
        )

        return self.__parent__._cast(_7432.AdvancedSystemDeflectionSubAnalysis)

    @property
    def analysis_case(self: "CastSelf") -> "_7707.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

        return self.__parent__._cast(_7707.AnalysisCase)

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7709.CompoundAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7709,
        )

        return self.__parent__._cast(_7709.CompoundAnalysisCase)

    @property
    def fe_analysis(self: "CastSelf") -> "_7716.FEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7716,
        )

        return self.__parent__._cast(_7716.FEAnalysis)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7722.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7722,
        )

        return self.__parent__._cast(_7722.StaticLoadAnalysisCase)

    @property
    def time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7723.TimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7723,
        )

        return self.__parent__._cast(_7723.TimeSeriesLoadAnalysisCase)

    @property
    def context(self: "CastSelf") -> "Context":
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
class Context(_0.APIBase):
    """Context

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTEXT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def comment(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Comment")

        if temp is None:
            return ""

        return temp

    @comment.setter
    @enforce_parameter_types
    def comment(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Comment", str(value) if value is not None else ""
        )

    @property
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    def save_history_information(self: "Self") -> "_1632.FileHistoryItem":
        """mastapy.utility.FileHistoryItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SaveHistoryInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def design_properties(self: "Self") -> "_2255.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputDefaultReportTo", file_path if file_path else ""
        )

    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportTo", file_path if file_path else ""
        )

    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "str") -> None:
        """Method does not return.

        Args:
            file_path (str)
        """
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped, "OutputActiveReportAsTextTo", file_path if file_path else ""
        )

    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "str"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (str)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path if file_path else "",
        )

    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_Context":
        """Cast to another type.

        Returns:
            _Cast_Context
        """
        return _Cast_Context(self)
