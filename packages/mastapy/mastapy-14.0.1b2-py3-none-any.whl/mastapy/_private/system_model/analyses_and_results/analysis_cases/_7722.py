"""StaticLoadAnalysisCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707

_STATIC_LOAD_ANALYSIS_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases",
    "StaticLoadAnalysisCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7430,
        _7432,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7162,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7709,
        _7716,
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
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6208,
        _6226,
    )
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
    from mastapy._private.system_model.analyses_and_results.power_flows import _4231
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3919,
        _3975,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _6955
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

    Self = TypeVar("Self", bound="StaticLoadAnalysisCase")
    CastSelf = TypeVar(
        "CastSelf", bound="StaticLoadAnalysisCase._Cast_StaticLoadAnalysisCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StaticLoadAnalysisCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StaticLoadAnalysisCase:
    """Special nested class for casting StaticLoadAnalysisCase to subclasses."""

    __parent__: "StaticLoadAnalysisCase"

    @property
    def analysis_case(self: "CastSelf") -> "_7707.AnalysisCase":
        return self.__parent__._cast(_7707.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2737.Context":
        from mastapy._private.system_model.analyses_and_results import _2737

        return self.__parent__._cast(_2737.Context)

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
    def static_load_analysis_case(self: "CastSelf") -> "StaticLoadAnalysisCase":
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
class StaticLoadAnalysisCase(_7707.AnalysisCase):
    """StaticLoadAnalysisCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATIC_LOAD_ANALYSIS_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def load_case(self: "Self") -> "_6955.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StaticLoadAnalysisCase":
        """Cast to another type.

        Returns:
            _Cast_StaticLoadAnalysisCase
        """
        return _Cast_StaticLoadAnalysisCase(self)
