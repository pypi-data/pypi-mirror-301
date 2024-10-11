"""AbstractShaftToMountableComponentConnectionCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _2975,
)

_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
        "AbstractShaftToMountableComponentConnectionCompoundSystemDeflection",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2775,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2964,
        _2984,
        _2986,
        _3026,
        _3041,
    )

    Self = TypeVar(
        "Self",
        bound="AbstractShaftToMountableComponentConnectionCompoundSystemDeflection",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftToMountableComponentConnectionCompoundSystemDeflection._Cast_AbstractShaftToMountableComponentConnectionCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftToMountableComponentConnectionCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftToMountableComponentConnectionCompoundSystemDeflection:
    """Special nested class for casting AbstractShaftToMountableComponentConnectionCompoundSystemDeflection to subclasses."""

    __parent__: "AbstractShaftToMountableComponentConnectionCompoundSystemDeflection"

    @property
    def connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2975.ConnectionCompoundSystemDeflection":
        return self.__parent__._cast(_2975.ConnectionCompoundSystemDeflection)

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
    def coaxial_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2964.CoaxialConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2964,
        )

        return self.__parent__._cast(_2964.CoaxialConnectionCompoundSystemDeflection)

    @property
    def cycloidal_disc_central_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2984.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2984,
        )

        return self.__parent__._cast(
            _2984.CycloidalDiscCentralBearingConnectionCompoundSystemDeflection
        )

    @property
    def cycloidal_disc_planetary_bearing_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2986.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2986,
        )

        return self.__parent__._cast(
            _2986.CycloidalDiscPlanetaryBearingConnectionCompoundSystemDeflection
        )

    @property
    def planetary_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3026.PlanetaryConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3026,
        )

        return self.__parent__._cast(_3026.PlanetaryConnectionCompoundSystemDeflection)

    @property
    def shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3041.ShaftToMountableComponentConnectionCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3041,
        )

        return self.__parent__._cast(
            _3041.ShaftToMountableComponentConnectionCompoundSystemDeflection
        )

    @property
    def abstract_shaft_to_mountable_component_connection_compound_system_deflection(
        self: "CastSelf",
    ) -> "AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
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
class AbstractShaftToMountableComponentConnectionCompoundSystemDeflection(
    _2975.ConnectionCompoundSystemDeflection
):
    """AbstractShaftToMountableComponentConnectionCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_SYSTEM_DEFLECTION
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
    ) -> "List[_2775.AbstractShaftToMountableComponentConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftToMountableComponentConnectionSystemDeflection]

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
    ) -> "List[_2775.AbstractShaftToMountableComponentConnectionSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.AbstractShaftToMountableComponentConnectionSystemDeflection]

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
    ) -> "_Cast_AbstractShaftToMountableComponentConnectionCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftToMountableComponentConnectionCompoundSystemDeflection
        """
        return (
            _Cast_AbstractShaftToMountableComponentConnectionCompoundSystemDeflection(
                self
            )
        )
