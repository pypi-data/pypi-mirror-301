"""CouplingConnectionAdvancedSystemDeflection"""

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
    _7496,
)

_COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CouplingConnectionAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7451,
        _7456,
        _7464,
        _7515,
        _7537,
        _7552,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2401

    Self = TypeVar("Self", bound="CouplingConnectionAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionAdvancedSystemDeflection._Cast_CouplingConnectionAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionAdvancedSystemDeflection:
    """Special nested class for casting CouplingConnectionAdvancedSystemDeflection to subclasses."""

    __parent__: "CouplingConnectionAdvancedSystemDeflection"

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.InterMountableComponentConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7496.InterMountableComponentConnectionAdvancedSystemDeflection
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
    def clutch_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7451.ClutchConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7451,
        )

        return self.__parent__._cast(_7451.ClutchConnectionAdvancedSystemDeflection)

    @property
    def concept_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7456.ConceptCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7456,
        )

        return self.__parent__._cast(
            _7456.ConceptCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7515.PartToPartShearCouplingConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7515,
        )

        return self.__parent__._cast(
            _7515.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        )

    @property
    def spring_damper_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7537.SpringDamperConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7537,
        )

        return self.__parent__._cast(
            _7537.SpringDamperConnectionAdvancedSystemDeflection
        )

    @property
    def torque_converter_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7552.TorqueConverterConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7552,
        )

        return self.__parent__._cast(
            _7552.TorqueConverterConnectionAdvancedSystemDeflection
        )

    @property
    def coupling_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CouplingConnectionAdvancedSystemDeflection":
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
class CouplingConnectionAdvancedSystemDeflection(
    _7496.InterMountableComponentConnectionAdvancedSystemDeflection
):
    """CouplingConnectionAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2401.CouplingConnection":
        """mastapy.system_model.connections_and_sockets.couplings.CouplingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionAdvancedSystemDeflection
        """
        return _Cast_CouplingConnectionAdvancedSystemDeflection(self)
