"""CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6713,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6692,
        _6724,
        _6791,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2390

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis._Cast_CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis"

    @property
    def coaxial_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6713.CoaxialConnectionCriticalSpeedAnalysis":
        return self.__parent__._cast(_6713.CoaxialConnectionCriticalSpeedAnalysis)

    @property
    def shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6791.ShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6791,
        )

        return self.__parent__._cast(
            _6791.ShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def abstract_shaft_to_mountable_component_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6692.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6692,
        )

        return self.__parent__._cast(
            _6692.AbstractShaftToMountableComponentConnectionCriticalSpeedAnalysis
        )

    @property
    def connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6724.ConnectionCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6724,
        )

        return self.__parent__._cast(_6724.ConnectionCriticalSpeedAnalysis)

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
    def cycloidal_disc_central_bearing_connection_critical_speed_analysis(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis":
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
class CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis(
    _6713.CoaxialConnectionCriticalSpeedAnalysis
):
    """CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_CRITICAL_SPEED_ANALYSIS
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
    ) -> "_2390.CycloidalDiscCentralBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection

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
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis
        """
        return _Cast_CycloidalDiscCentralBearingConnectionCriticalSpeedAnalysis(self)
