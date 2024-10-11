"""CycloidalDiscCentralBearingConnectionLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _6987

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "CycloidalDiscCentralBearingConnectionLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6960,
        _7000,
        _7104,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2390

    Self = TypeVar("Self", bound="CycloidalDiscCentralBearingConnectionLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionLoadCase._Cast_CycloidalDiscCentralBearingConnectionLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionLoadCase:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionLoadCase to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionLoadCase"

    @property
    def coaxial_connection_load_case(
        self: "CastSelf",
    ) -> "_6987.CoaxialConnectionLoadCase":
        return self.__parent__._cast(_6987.CoaxialConnectionLoadCase)

    @property
    def shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_7104.ShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7104,
        )

        return self.__parent__._cast(_7104.ShaftToMountableComponentConnectionLoadCase)

    @property
    def abstract_shaft_to_mountable_component_connection_load_case(
        self: "CastSelf",
    ) -> "_6960.AbstractShaftToMountableComponentConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6960,
        )

        return self.__parent__._cast(
            _6960.AbstractShaftToMountableComponentConnectionLoadCase
        )

    @property
    def connection_load_case(self: "CastSelf") -> "_7000.ConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7000,
        )

        return self.__parent__._cast(_7000.ConnectionLoadCase)

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
    def cycloidal_disc_central_bearing_connection_load_case(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionLoadCase":
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
class CycloidalDiscCentralBearingConnectionLoadCase(_6987.CoaxialConnectionLoadCase):
    """CycloidalDiscCentralBearingConnectionLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_LOAD_CASE

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
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscCentralBearingConnectionLoadCase":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionLoadCase
        """
        return _Cast_CycloidalDiscCentralBearingConnectionLoadCase(self)
