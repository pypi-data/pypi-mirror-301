"""InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed"""

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
    _3770,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound",
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
        _3668,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
        _3740,
        _3744,
        _3747,
        _3752,
        _3757,
        _3762,
        _3765,
        _3768,
        _3773,
        _3775,
        _3783,
        _3789,
        _3794,
        _3798,
        _3802,
        _3805,
        _3808,
        _3818,
        _3827,
        _3830,
        _3837,
        _3840,
        _3843,
        _3846,
        _3855,
        _3861,
        _3864,
    )

    Self = TypeVar(
        "Self",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed._Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = (
    "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed",
)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed:
    """Special nested class for casting InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed"

    @property
    def connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3770.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        return self.__parent__._cast(
            _3770.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3740.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3740,
        )

        return self.__parent__._cast(
            _3740.AGMAGleasonConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def belt_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3744.BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3744,
        )

        return self.__parent__._cast(
            _3744.BeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_differential_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3747.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3747,
        )

        return self.__parent__._cast(
            _3747.BevelDifferentialGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3752.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3752,
        )

        return self.__parent__._cast(
            _3752.BevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def clutch_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3757.ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3757,
        )

        return self.__parent__._cast(
            _3757.ClutchConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3762.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3762,
        )

        return self.__parent__._cast(
            _3762.ConceptCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def concept_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3765.ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3765,
        )

        return self.__parent__._cast(
            _3765.ConceptGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3768.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3768,
        )

        return self.__parent__._cast(
            _3768.ConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3773.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3773,
        )

        return self.__parent__._cast(
            _3773.CouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cvt_belt_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3775.CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3775,
        )

        return self.__parent__._cast(
            _3775.CVTBeltConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def cylindrical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3783.CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3783,
        )

        return self.__parent__._cast(
            _3783.CylindricalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def face_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3789.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3789,
        )

        return self.__parent__._cast(
            _3789.FaceGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3794.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3794,
        )

        return self.__parent__._cast(
            _3794.GearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def hypoid_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3798.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3798,
        )

        return self.__parent__._cast(
            _3798.HypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3802.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3802,
        )

        return self.__parent__._cast(
            _3802.KlingelnbergCycloPalloidConicalGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3805.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3805,
        )

        return self.__parent__._cast(
            _3805.KlingelnbergCycloPalloidHypoidGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3808.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3808,
        )

        return self.__parent__._cast(
            _3808.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def part_to_part_shear_coupling_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3818.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3818,
        )

        return self.__parent__._cast(
            _3818.PartToPartShearCouplingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def ring_pins_to_disc_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3827.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3827,
        )

        return self.__parent__._cast(
            _3827.RingPinsToDiscConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def rolling_ring_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3830.RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3830,
        )

        return self.__parent__._cast(
            _3830.RollingRingConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spiral_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3837.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3837,
        )

        return self.__parent__._cast(
            _3837.SpiralBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def spring_damper_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3840.SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3840,
        )

        return self.__parent__._cast(
            _3840.SpringDamperConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3843.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3843,
        )

        return self.__parent__._cast(
            _3843.StraightBevelDiffGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def straight_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3846.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3846,
        )

        return self.__parent__._cast(
            _3846.StraightBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def torque_converter_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_3855.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3855,
        )

        return self.__parent__._cast(
            _3855.TorqueConverterConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def worm_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3861.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3861,
        )

        return self.__parent__._cast(
            _3861.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def zerol_bevel_gear_mesh_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "_3864.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
            _3864,
        )

        return self.__parent__._cast(
            _3864.ZerolBevelGearMeshCompoundSteadyStateSynchronousResponseAtASpeed
        )

    @property
    def inter_mountable_component_connection_compound_steady_state_synchronous_response_at_a_speed(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
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
class InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed(
    _3770.ConnectionCompoundSteadyStateSynchronousResponseAtASpeed
):
    """InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3668.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_3668.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.InterMountableComponentConnectionSteadyStateSynchronousResponseAtASpeed]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed
        """
        return _Cast_InterMountableComponentConnectionCompoundSteadyStateSynchronousResponseAtASpeed(
            self
        )
