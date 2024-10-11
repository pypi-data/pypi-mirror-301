"""AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"""

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
    _5275,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed",
        "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5264,
        _5284,
        _5286,
        _5326,
        _5340,
    )
    from mastapy._private.system_model.connections_and_sockets import _2320

    Self = TypeVar(
        "Self", bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed._Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed"

    @property
    def connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5275.ConnectionModalAnalysisAtASpeed":
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
    def coaxial_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5264.CoaxialConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5264,
        )

        return self.__parent__._cast(_5264.CoaxialConnectionModalAnalysisAtASpeed)

    @property
    def cycloidal_disc_central_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5284.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5284,
        )

        return self.__parent__._cast(
            _5284.CycloidalDiscCentralBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5286.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5286,
        )

        return self.__parent__._cast(
            _5286.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtASpeed
        )

    @property
    def planetary_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5326.PlanetaryConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5326,
        )

        return self.__parent__._cast(_5326.PlanetaryConnectionModalAnalysisAtASpeed)

    @property
    def shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5340.ShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
            _5340,
        )

        return self.__parent__._cast(
            _5340.ShaftToMountableComponentConnectionModalAnalysisAtASpeed
        )

    @property
    def abstract_shaft_to_mountable_component_connection_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
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
class AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed(
    _5275.ConnectionModalAnalysisAtASpeed
):
    """AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_MODAL_ANALYSIS_AT_A_SPEED
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(
        self: "Self",
    ) -> "_2320.AbstractShaftToMountableComponentConnection":
        """mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed
        """
        return _Cast_AbstractShaftToMountableComponentConnectionModalAnalysisAtASpeed(
            self
        )
