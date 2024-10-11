"""ConicalGearSetCompoundSteadyStateSynchronousResponse"""

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
    _3269,
)

_CONICAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses.Compound",
    "ConicalGearSetCompoundSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3107,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
        _3209,
        _3215,
        _3222,
        _3227,
        _3273,
        _3277,
        _3280,
        _3283,
        _3290,
        _3309,
        _3312,
        _3318,
        _3321,
        _3339,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundSteadyStateSynchronousResponse._Cast_ConicalGearSetCompoundSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundSteadyStateSynchronousResponse:
    """Special nested class for casting ConicalGearSetCompoundSteadyStateSynchronousResponse to subclasses."""

    __parent__: "ConicalGearSetCompoundSteadyStateSynchronousResponse"

    @property
    def gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3269.GearSetCompoundSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3269.GearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def specialised_assembly_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3309.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3309,
        )

        return self.__parent__._cast(
            _3309.SpecialisedAssemblyCompoundSteadyStateSynchronousResponse
        )

    @property
    def abstract_assembly_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3209.AbstractAssemblyCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3209,
        )

        return self.__parent__._cast(
            _3209.AbstractAssemblyCompoundSteadyStateSynchronousResponse
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
    def agma_gleason_conical_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3215.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3215,
        )

        return self.__parent__._cast(
            _3215.AGMAGleasonConicalGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3222.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3222,
        )

        return self.__parent__._cast(
            _3222.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3227.BevelGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3227,
        )

        return self.__parent__._cast(
            _3227.BevelGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def hypoid_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3273.HypoidGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3273,
        )

        return self.__parent__._cast(
            _3273.HypoidGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3277.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3277,
        )

        return self.__parent__._cast(
            _3277.KlingelnbergCycloPalloidConicalGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3280.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3280,
        )

        return self.__parent__._cast(
            _3280.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3283.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3283,
        )

        return self.__parent__._cast(
            _3283.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3312.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3312,
        )

        return self.__parent__._cast(
            _3312.SpiralBevelGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3318.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3318,
        )

        return self.__parent__._cast(
            _3318.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3321.StraightBevelGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3321,
        )

        return self.__parent__._cast(
            _3321.StraightBevelGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def zerol_bevel_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3339.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses.compound import (
            _3339,
        )

        return self.__parent__._cast(
            _3339.ZerolBevelGearSetCompoundSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_set_compound_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundSteadyStateSynchronousResponse":
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
class ConicalGearSetCompoundSteadyStateSynchronousResponse(
    _3269.GearSetCompoundSteadyStateSynchronousResponse
):
    """ConicalGearSetCompoundSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CONICAL_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_3107.ConicalGearSetSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearSetSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3107.ConicalGearSetSteadyStateSynchronousResponse]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses.ConicalGearSetSteadyStateSynchronousResponse]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConicalGearSetCompoundSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundSteadyStateSynchronousResponse
        """
        return _Cast_ConicalGearSetCompoundSteadyStateSynchronousResponse(self)
