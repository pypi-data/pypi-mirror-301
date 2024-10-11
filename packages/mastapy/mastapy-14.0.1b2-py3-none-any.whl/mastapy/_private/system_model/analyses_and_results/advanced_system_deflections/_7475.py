"""CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7453,
)

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
        "CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7429,
        _7464,
        _7531,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2390

    Self = TypeVar(
        "Self", bound="CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection._Cast_CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection:
    """Special nested class for casting CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection to subclasses."""

    __parent__: "CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection"

    @property
    def coaxial_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7453.CoaxialConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(_7453.CoaxialConnectionAdvancedSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7531.ShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7531,
        )

        return self.__parent__._cast(
            _7531.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def abstract_shaft_to_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7429.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7429,
        )

        return self.__parent__._cast(
            _7429.AbstractShaftToMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7464.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7464,
        )

        return self.__parent__._cast(_7464.ConnectionAdvancedSystemDeflection)

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
    def cycloidal_disc_central_bearing_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection":
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
class CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection(
    _7453.CoaxialConnectionAdvancedSystemDeflection
):
    """CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION
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
    ) -> "_Cast_CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection
        """
        return _Cast_CycloidalDiscCentralBearingConnectionAdvancedSystemDeflection(self)
