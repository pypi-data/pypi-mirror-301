"""ConnectionSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7713

_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "ConnectionSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3343,
        _3344,
        _3349,
        _3351,
        _3356,
        _3361,
        _3364,
        _3366,
        _3369,
        _3372,
        _3377,
        _3380,
        _3384,
        _3385,
        _3387,
        _3393,
        _3398,
        _3402,
        _3405,
        _3406,
        _3409,
        _3412,
        _3422,
        _3425,
        _3432,
        _3434,
        _3439,
        _3441,
        _3444,
        _3447,
        _3448,
        _3451,
        _3460,
        _3466,
        _3469,
    )
    from mastapy._private.system_model.connections_and_sockets import _2327

    Self = TypeVar("Self", bound="ConnectionSteadyStateSynchronousResponseOnAShaft")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConnectionSteadyStateSynchronousResponseOnAShaft._Cast_ConnectionSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConnectionSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting ConnectionSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "ConnectionSteadyStateSynchronousResponseOnAShaft"

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
        return self.__parent__._cast(_7713.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7710.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2736.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.ConnectionAnalysis)

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
    def abstract_shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3343.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3343,
        )

        return self.__parent__._cast(
            _3343.AbstractShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3344.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3344,
        )

        return self.__parent__._cast(
            _3344.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3349.BeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3349,
        )

        return self.__parent__._cast(
            _3349.BeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3351.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3351,
        )

        return self.__parent__._cast(
            _3351.BevelDifferentialGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3356.BevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3356,
        )

        return self.__parent__._cast(
            _3356.BevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3361.ClutchConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3361,
        )

        return self.__parent__._cast(
            _3361.ClutchConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coaxial_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3364.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3364,
        )

        return self.__parent__._cast(
            _3364.CoaxialConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3366.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3366,
        )

        return self.__parent__._cast(
            _3366.ConceptCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3369.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3369,
        )

        return self.__parent__._cast(
            _3369.ConceptGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3372.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3372,
        )

        return self.__parent__._cast(
            _3372.ConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3377.CouplingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3377,
        )

        return self.__parent__._cast(
            _3377.CouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_belt_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3380.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3380,
        )

        return self.__parent__._cast(
            _3380.CVTBeltConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_central_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3384.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3384,
        )

        return self.__parent__._cast(
            _3384.CycloidalDiscCentralBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3385.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3385,
        )

        return self.__parent__._cast(
            _3385.CycloidalDiscPlanetaryBearingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3387.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3387,
        )

        return self.__parent__._cast(
            _3387.CylindricalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3393.FaceGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3393,
        )

        return self.__parent__._cast(
            _3393.FaceGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3398.GearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3398,
        )

        return self.__parent__._cast(
            _3398.GearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3402.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3402,
        )

        return self.__parent__._cast(
            _3402.HypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3405.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3405,
        )

        return self.__parent__._cast(
            _3405.InterMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3406.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3406,
        )

        return self.__parent__._cast(
            _3406.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3409.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3409,
        )

        return self.__parent__._cast(
            _3409.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3412.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3412,
        )

        return self.__parent__._cast(
            _3412.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3422.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3422,
        )

        return self.__parent__._cast(
            _3422.PartToPartShearCouplingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planetary_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3425.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3425,
        )

        return self.__parent__._cast(
            _3425.PlanetaryConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def ring_pins_to_disc_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3432.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3432,
        )

        return self.__parent__._cast(
            _3432.RingPinsToDiscConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3434.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3434,
        )

        return self.__parent__._cast(
            _3434.RollingRingConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_to_mountable_component_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3439.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3439,
        )

        return self.__parent__._cast(
            _3439.ShaftToMountableComponentConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3441.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3441,
        )

        return self.__parent__._cast(
            _3441.SpiralBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3444.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3444,
        )

        return self.__parent__._cast(
            _3444.SpringDamperConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3448.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3448,
        )

        return self.__parent__._cast(
            _3448.StraightBevelDiffGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3451.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3451,
        )

        return self.__parent__._cast(
            _3451.StraightBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3460.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3460,
        )

        return self.__parent__._cast(
            _3460.TorqueConverterConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3466.WormGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3466,
        )

        return self.__parent__._cast(
            _3466.WormGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3469.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3469,
        )

        return self.__parent__._cast(
            _3469.ZerolBevelGearMeshSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "ConnectionSteadyStateSynchronousResponseOnAShaft":
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
class ConnectionSteadyStateSynchronousResponseOnAShaft(
    _7713.ConnectionStaticLoadAnalysisCase
):
    """ConnectionSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2327.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2327.Connection":
        """mastapy.system_model.connections_and_sockets.Connection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def steady_state_synchronous_response_on_a_shaft(
        self: "Self",
    ) -> "_3447.SteadyStateSynchronousResponseOnAShaft":
        """mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft.SteadyStateSynchronousResponseOnAShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SteadyStateSynchronousResponseOnAShaft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConnectionSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_ConnectionSteadyStateSynchronousResponseOnAShaft(self)
