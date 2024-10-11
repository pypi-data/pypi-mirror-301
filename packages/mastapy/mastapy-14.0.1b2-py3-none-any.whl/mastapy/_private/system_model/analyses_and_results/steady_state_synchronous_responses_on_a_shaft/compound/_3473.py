"""AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
    _3474,
)

_ABSTRACT_SHAFT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft.Compound",
    "AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3342,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
        _3497,
        _3517,
        _3553,
        _3569,
    )

    Self = TypeVar(
        "Self", bound="AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft._Cast_AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft"

    @property
    def abstract_shaft_or_housing_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3474.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3474.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def component_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3497.ComponentCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3497,
        )

        return self.__parent__._cast(
            _3497.ComponentCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3553.PartCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3553,
        )

        return self.__parent__._cast(
            _3553.PartCompoundSteadyStateSynchronousResponseOnAShaft
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
    def cycloidal_disc_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3517.CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3517,
        )

        return self.__parent__._cast(
            _3517.CycloidalDiscCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3569.ShaftCompoundSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.compound import (
            _3569,
        )

        return self.__parent__._cast(
            _3569.ShaftCompoundSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def abstract_shaft_compound_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft":
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
class AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft(
    _3474.AbstractShaftOrHousingCompoundSteadyStateSynchronousResponseOnAShaft
):
    """AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_3342.AbstractShaftSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.AbstractShaftSteadyStateSynchronousResponseOnAShaft]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3342.AbstractShaftSteadyStateSynchronousResponseOnAShaft]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.AbstractShaftSteadyStateSynchronousResponseOnAShaft]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_AbstractShaftCompoundSteadyStateSynchronousResponseOnAShaft(self)
