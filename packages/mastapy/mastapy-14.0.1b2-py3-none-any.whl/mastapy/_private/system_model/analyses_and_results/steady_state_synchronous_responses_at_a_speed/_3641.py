"""CouplingHalfSteadyStateSynchronousResponseAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _3682,
)

_COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed",
    "CouplingHalfSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3625,
        _3628,
        _3630,
        _3644,
        _3684,
        _3686,
        _3693,
        _3698,
        _3708,
        _3719,
        _3720,
        _3721,
        _3724,
        _3726,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CouplingHalfSteadyStateSynchronousResponseAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfSteadyStateSynchronousResponseAtASpeed._Cast_CouplingHalfSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfSteadyStateSynchronousResponseAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting CouplingHalfSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "CouplingHalfSteadyStateSynchronousResponseAtASpeed"

    @property
    def mountable_component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3682.MountableComponentSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3682.MountableComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def component_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3628.ComponentSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3628,
        )

        return self.__parent__._cast(
            _3628.ComponentSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3684.PartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3684,
        )

        return self.__parent__._cast(_3684.PartSteadyStateSynchronousResponseAtASpeed)

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
    def clutch_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3625.ClutchHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3625,
        )

        return self.__parent__._cast(
            _3625.ClutchHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3630.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3630,
        )

        return self.__parent__._cast(
            _3630.ConceptCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3644.CVTPulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3644,
        )

        return self.__parent__._cast(
            _3644.CVTPulleySteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3686.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3686,
        )

        return self.__parent__._cast(
            _3686.PartToPartShearCouplingHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def pulley_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3693.PulleySteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3693,
        )

        return self.__parent__._cast(_3693.PulleySteadyStateSynchronousResponseAtASpeed)

    @property
    def rolling_ring_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3698.RollingRingSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3698,
        )

        return self.__parent__._cast(
            _3698.RollingRingSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3708.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3708,
        )

        return self.__parent__._cast(
            _3708.SpringDamperHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3719.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3719,
        )

        return self.__parent__._cast(
            _3719.SynchroniserHalfSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3720.SynchroniserPartSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3720,
        )

        return self.__parent__._cast(
            _3720.SynchroniserPartSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3721.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3721,
        )

        return self.__parent__._cast(
            _3721.SynchroniserSleeveSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3724.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3724,
        )

        return self.__parent__._cast(
            _3724.TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3726.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
            _3726,
        )

        return self.__parent__._cast(
            _3726.TorqueConverterTurbineSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_half_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "CouplingHalfSteadyStateSynchronousResponseAtASpeed":
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
class CouplingHalfSteadyStateSynchronousResponseAtASpeed(
    _3682.MountableComponentSteadyStateSynchronousResponseAtASpeed
):
    """CouplingHalfSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2645.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CouplingHalfSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_CouplingHalfSteadyStateSynchronousResponseAtASpeed(self)
