"""CVTPulleyCompoundSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
    _3299,
)

_CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "CVTPulleyCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3115,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3234,
        _3248,
        _3288,
        _3290,
    )

    Self = TypeVar("Self", bound="CVTPulleyCompoundSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTPulleyCompoundSteadyStateSynchronousResponse._Cast_CVTPulleyCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting CVTPulleyCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "CVTPulleyCompoundSteadyStateSynchronousResponse"

    @property
    def pulley_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3299.PulleyCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(_3299.PulleyCompoundSteadyStateSynchronousResponse)

    @property
    def coupling_half_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3248.CouplingHalfCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3248,
        )

        return self.__parent__._cast(
            _3248.CouplingHalfCompoundSteadyStateSynchronousResponse
        )

    @property
    def mountable_component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3288.MountableComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3288,
        )

        return self.__parent__._cast(
            _3288.MountableComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def component_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3234.ComponentCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3234,
        )

        return self.__parent__._cast(
            _3234.ComponentCompoundSteadyStateSynchronousResponse
        )

    @property
    def part_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3290.PartCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3290,
        )

        return self.__parent__._cast(_3290.PartCompoundSteadyStateSynchronousResponse)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7715.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7715,
        )

        return self.__parent__._cast(_7715.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2738.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2738

        return self.__parent__._cast(_2738.DesignEntityAnalysis)

    @property
    def cvt_pulley_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "CVTPulleyCompoundSteadyStateSynchronousResponse":
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
class CVTPulleyCompoundSteadyStateSynchronousResponse(
    _3299.PulleyCompoundSteadyStateSynchronousResponse
):
    """CVTPulleyCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3115.CVTPulleySteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CVTPulleySteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3115.CVTPulleySteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.CVTPulleySteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CVTPulleyCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyCompoundSteadyStateSynchronousResponse
        """
        return _Cast_CVTPulleyCompoundSteadyStateSynchronousResponse(self)
