"""StraightBevelGearMeshModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
    _5256,
)

_STRAIGHT_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
    "StraightBevelGearMeshModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5244,
        _5272,
        _5275,
        _5298,
        _5305,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7116
    from mastapy._private.system_model.connections_and_sockets.gears import _2382

    Self = TypeVar("Self", bound="StraightBevelGearMeshModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelGearMeshModalAnalysisAtASpeed._Cast_StraightBevelGearMeshModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelGearMeshModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelGearMeshModalAnalysisAtASpeed:
    """Special nested class for casting StraightBevelGearMeshModalAnalysisAtASpeed to subclasses."""

    __parent__: "StraightBevelGearMeshModalAnalysisAtASpeed"

    @property
    def bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5256.BevelGearMeshModalAnalysisAtASpeed":
        return self.__parent__._cast(_5256.BevelGearMeshModalAnalysisAtASpeed)

    @property
    def agma_gleason_conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5244.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5244,
        )

        return self.__parent__._cast(
            _5244.AGMAGleasonConicalGearMeshModalAnalysisAtASpeed
        )

    @property
    def conical_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5272.ConicalGearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5272,
        )

        return self.__parent__._cast(_5272.ConicalGearMeshModalAnalysisAtASpeed)

    @property
    def gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5298.GearMeshModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5298,
        )

        return self.__parent__._cast(_5298.GearMeshModalAnalysisAtASpeed)

    @property
    def inter_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5305.InterMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5305,
        )

        return self.__parent__._cast(
            _5305.InterMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5275.ConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5275,
        )

        return self.__parent__._cast(_5275.ConnectionModalAnalysisAtASpeed)

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
    def straight_bevel_gear_mesh_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "StraightBevelGearMeshModalAnalysisAtASpeed":
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
class StraightBevelGearMeshModalAnalysisAtASpeed(
    _5256.BevelGearMeshModalAnalysisAtASpeed
):
    """StraightBevelGearMeshModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_GEAR_MESH_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2382.StraightBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7116.StraightBevelGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelGearMeshModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelGearMeshModalAnalysisAtASpeed
        """
        return _Cast_StraightBevelGearMeshModalAnalysisAtASpeed(self)
