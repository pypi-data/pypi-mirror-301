"""CouplingConnectionCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7629,
)

_COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "CouplingConnectionCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7468,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7586,
        _7591,
        _7599,
        _7647,
        _7669,
        _7684,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundAdvancedSystemDeflection._Cast_CouplingConnectionCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundAdvancedSystemDeflection:
    """Special nested class for casting CouplingConnectionCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "CouplingConnectionCompoundAdvancedSystemDeflection"

    @property
    def inter_mountable_component_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7629.InterMountableComponentConnectionCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7629.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7599.ConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7599,
        )

        return self.__parent__._cast(_7599.ConnectionCompoundAdvancedSystemDeflection)

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
    def clutch_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7586.ClutchConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7586,
        )

        return self.__parent__._cast(
            _7586.ClutchConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def concept_coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7591.ConceptCouplingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7591,
        )

        return self.__parent__._cast(
            _7591.ConceptCouplingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7647.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7647,
        )

        return self.__parent__._cast(
            _7647.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def spring_damper_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7669.SpringDamperConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7669,
        )

        return self.__parent__._cast(
            _7669.SpringDamperConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7684.TorqueConverterConnectionCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7684,
        )

        return self.__parent__._cast(
            _7684.TorqueConverterConnectionCompoundAdvancedSystemDeflection
        )

    @property
    def coupling_connection_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundAdvancedSystemDeflection":
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
class CouplingConnectionCompoundAdvancedSystemDeflection(
    _7629.InterMountableComponentConnectionCompoundAdvancedSystemDeflection
):
    """CouplingConnectionCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_7468.CouplingConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection]

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
    ) -> "List[_7468.CouplingConnectionAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection]

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
    ) -> "_Cast_CouplingConnectionCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundAdvancedSystemDeflection
        """
        return _Cast_CouplingConnectionCompoundAdvancedSystemDeflection(self)
