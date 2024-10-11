"""FEAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7722

_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AnalysisCases", "FEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2737
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7432,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7707
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6471,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5866,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4740
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5028,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3919,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3126,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2914,
        _2921,
    )

    Self = TypeVar("Self", bound="FEAnalysis")
    CastSelf = TypeVar("CastSelf", bound="FEAnalysis._Cast_FEAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("FEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEAnalysis:
    """Special nested class for casting FEAnalysis to subclasses."""

    __parent__: "FEAnalysis"

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7722.StaticLoadAnalysisCase":
        return self.__parent__._cast(_7722.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7707.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7707,
        )

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
    def dynamic_model_for_stability_analysis(
        self: "CastSelf",
    ) -> "_3919.DynamicModelForStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3919,
        )

        return self.__parent__._cast(_3919.DynamicModelForStabilityAnalysis)

    @property
    def dynamic_model_for_modal_analysis(
        self: "CastSelf",
    ) -> "_4740.DynamicModelForModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4740,
        )

        return self.__parent__._cast(_4740.DynamicModelForModalAnalysis)

    @property
    def dynamic_model_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5028.DynamicModelAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
            _5028,
        )

        return self.__parent__._cast(_5028.DynamicModelAtAStiffness)

    @property
    def dynamic_model_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5866.DynamicModelForHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5866,
        )

        return self.__parent__._cast(_5866.DynamicModelForHarmonicAnalysis)

    @property
    def dynamic_analysis(self: "CastSelf") -> "_6471.DynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6471,
        )

        return self.__parent__._cast(_6471.DynamicAnalysis)

    @property
    def advanced_system_deflection_sub_analysis(
        self: "CastSelf",
    ) -> "_7432.AdvancedSystemDeflectionSubAnalysis":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7432,
        )

        return self.__parent__._cast(_7432.AdvancedSystemDeflectionSubAnalysis)

    @property
    def fe_analysis(self: "CastSelf") -> "FEAnalysis":
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
class FEAnalysis(_7722.StaticLoadAnalysisCase):
    """FEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def stiffness_with_respect_to_input_power_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StiffnessWithRespectToInputPowerLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_at_zero_displacement_for_input_power_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueAtZeroDisplacementForInputPowerLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def torque_ratio_to_output(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueRatioToOutput")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_FEAnalysis
        """
        return _Cast_FEAnalysis(self)
