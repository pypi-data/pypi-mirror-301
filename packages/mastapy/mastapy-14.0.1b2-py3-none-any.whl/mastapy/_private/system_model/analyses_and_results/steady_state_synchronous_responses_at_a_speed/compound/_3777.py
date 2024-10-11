"""CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _3825,
)

_CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3644,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3760,
        _3774,
        _3814,
        _3816,
    )

    Self = TypeVar(
        "Self", bound="CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed._Cast_CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def pulley_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3825.PulleyCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3825.PulleyCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_half_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3774.CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3774,
        )

        return self.__parent__._cast(
            _3774.CouplingHalfCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def mountable_component_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3814.MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3814,
        )

        return self.__parent__._cast(
            _3814.MountableComponentCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def component_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3760.ComponentCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3760,
        )

        return self.__parent__._cast(
            _3760.ComponentCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3816.PartCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3816,
        )

        return self.__parent__._cast(
            _3816.PartCompoundSteadyStateSynchronousResponseAtASpeed
        )

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
    def cvt_pulley_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed":
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
class CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed(
    _3825.PulleyCompoundSteadyStateSynchronousResponseAtASpeed
):
    """CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CVT_PULLEY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3644.CVTPulleySteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.CVTPulleySteadyStateSynchronousResponseAtASpeed]

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
    ) -> "List[_3644.CVTPulleySteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.CVTPulleySteadyStateSynchronousResponseAtASpeed]

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
    ) -> "_Cast_CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_CVTPulleyCompoundSteadyStateSynchronousResponseAtASpeed(self)
