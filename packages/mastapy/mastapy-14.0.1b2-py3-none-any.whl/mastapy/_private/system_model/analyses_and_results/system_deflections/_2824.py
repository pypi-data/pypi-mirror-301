"""CycloidalDiscPlanetaryBearingConnectionSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _2775

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CycloidalDiscPlanetaryBearingConnectionSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7712,
        _7713,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4184
    from mastapy._private.system_model.analyses_and_results.static_loads import _7011
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2814,
    )
    from mastapy._private.system_model.connections_and_sockets.cycloidal import _2393

    Self = TypeVar(
        "Self", bound="CycloidalDiscPlanetaryBearingConnectionSystemDeflection"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscPlanetaryBearingConnectionSystemDeflection._Cast_CycloidalDiscPlanetaryBearingConnectionSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscPlanetaryBearingConnectionSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscPlanetaryBearingConnectionSystemDeflection:
    """Special nested class for casting CycloidalDiscPlanetaryBearingConnectionSystemDeflection to subclasses."""

    __parent__: "CycloidalDiscPlanetaryBearingConnectionSystemDeflection"

    @property
    def abstract_shaft_to_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_2775.AbstractShaftToMountableComponentConnectionSystemDeflection":
        return self.__parent__._cast(
            _2775.AbstractShaftToMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2814.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2814,
        )

        return self.__parent__._cast(_2814.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7712.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7712,
        )

        return self.__parent__._cast(_7712.ConnectionFEAnalysis)

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
    def cycloidal_disc_planetary_bearing_connection_system_deflection(
        self: "CastSelf",
    ) -> "CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
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
class CycloidalDiscPlanetaryBearingConnectionSystemDeflection(
    _2775.AbstractShaftToMountableComponentConnectionSystemDeflection
):
    """CycloidalDiscPlanetaryBearingConnectionSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_SYSTEM_DEFLECTION
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
    ) -> "_2393.CycloidalDiscPlanetaryBearingConnection":
        """mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(
        self: "Self",
    ) -> "_7011.CycloidalDiscPlanetaryBearingConnectionLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CycloidalDiscPlanetaryBearingConnectionLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def power_flow_results(
        self: "Self",
    ) -> "_4184.CycloidalDiscPlanetaryBearingConnectionPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CycloidalDiscPlanetaryBearingConnectionPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CycloidalDiscPlanetaryBearingConnectionSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscPlanetaryBearingConnectionSystemDeflection
        """
        return _Cast_CycloidalDiscPlanetaryBearingConnectionSystemDeflection(self)
