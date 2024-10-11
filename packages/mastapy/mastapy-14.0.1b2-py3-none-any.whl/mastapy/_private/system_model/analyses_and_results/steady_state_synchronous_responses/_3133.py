"""GearMeshSteadyStateSynchronousResponse"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
    _3140,
)

_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses",
    "GearMeshSteadyStateSynchronousResponse",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
        _3078,
        _3085,
        _3090,
        _3103,
        _3106,
        _3109,
        _3121,
        _3128,
        _3137,
        _3141,
        _3144,
        _3147,
        _3176,
        _3185,
        _3188,
        _3203,
        _3206,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2368

    Self = TypeVar("Self", bound="GearMeshSteadyStateSynchronousResponse")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshSteadyStateSynchronousResponse._Cast_GearMeshSteadyStateSynchronousResponse",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshSteadyStateSynchronousResponse",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshSteadyStateSynchronousResponse:
    """Special nested class for casting GearMeshSteadyStateSynchronousResponse to subclasses."""

    __parent__: "GearMeshSteadyStateSynchronousResponse"

    @property
    def inter_mountable_component_connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3140.InterMountableComponentConnectionSteadyStateSynchronousResponse":
        return self.__parent__._cast(
            _3140.InterMountableComponentConnectionSteadyStateSynchronousResponse
        )

    @property
    def connection_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3109.ConnectionSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3109,
        )

        return self.__parent__._cast(_3109.ConnectionSteadyStateSynchronousResponse)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

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
    def agma_gleason_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3078.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3078,
        )

        return self.__parent__._cast(
            _3078.AGMAGleasonConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def bevel_differential_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3085.BevelDifferentialGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3085,
        )

        return self.__parent__._cast(
            _3085.BevelDifferentialGearMeshSteadyStateSynchronousResponse
        )

    @property
    def bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3090.BevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3090,
        )

        return self.__parent__._cast(_3090.BevelGearMeshSteadyStateSynchronousResponse)

    @property
    def concept_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3103.ConceptGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3103,
        )

        return self.__parent__._cast(
            _3103.ConceptGearMeshSteadyStateSynchronousResponse
        )

    @property
    def conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3106.ConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3106,
        )

        return self.__parent__._cast(
            _3106.ConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def cylindrical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3121.CylindricalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3121,
        )

        return self.__parent__._cast(
            _3121.CylindricalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def face_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3128.FaceGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3128,
        )

        return self.__parent__._cast(_3128.FaceGearMeshSteadyStateSynchronousResponse)

    @property
    def hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3137.HypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3137,
        )

        return self.__parent__._cast(_3137.HypoidGearMeshSteadyStateSynchronousResponse)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3141.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3141,
        )

        return self.__parent__._cast(
            _3141.KlingelnbergCycloPalloidConicalGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3144.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3144,
        )

        return self.__parent__._cast(
            _3144.KlingelnbergCycloPalloidHypoidGearMeshSteadyStateSynchronousResponse
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3147.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3147,
        )

        return self.__parent__._cast(
            _3147.KlingelnbergCycloPalloidSpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def spiral_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3176.SpiralBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3176,
        )

        return self.__parent__._cast(
            _3176.SpiralBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_diff_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3185.StraightBevelDiffGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3185,
        )

        return self.__parent__._cast(
            _3185.StraightBevelDiffGearMeshSteadyStateSynchronousResponse
        )

    @property
    def straight_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3188.StraightBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3188,
        )

        return self.__parent__._cast(
            _3188.StraightBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def worm_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3203.WormGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3203,
        )

        return self.__parent__._cast(_3203.WormGearMeshSteadyStateSynchronousResponse)

    @property
    def zerol_bevel_gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "_3206.ZerolBevelGearMeshSteadyStateSynchronousResponse":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses import (
            _3206,
        )

        return self.__parent__._cast(
            _3206.ZerolBevelGearMeshSteadyStateSynchronousResponse
        )

    @property
    def gear_mesh_steady_state_synchronous_response(
        self: "CastSelf",
    ) -> "GearMeshSteadyStateSynchronousResponse":
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
class GearMeshSteadyStateSynchronousResponse(
    _3140.InterMountableComponentConnectionSteadyStateSynchronousResponse
):
    """GearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2368.GearMesh":
        """mastapy.system_model.connections_and_sockets.gears.GearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshSteadyStateSynchronousResponse":
        """Cast to another type.

        Returns:
            _Cast_GearMeshSteadyStateSynchronousResponse
        """
        return _Cast_GearMeshSteadyStateSynchronousResponse(self)
