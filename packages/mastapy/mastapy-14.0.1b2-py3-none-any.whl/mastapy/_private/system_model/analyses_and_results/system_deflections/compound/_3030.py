"""PowerLoadCompoundSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
    _3066,
)

_POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "PowerLoadCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2881,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2965,
        _3020,
        _3022,
    )
    from mastapy._private.system_model.part_model import _2530

    Self = TypeVar("Self", bound="PowerLoadCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerLoadCompoundSystemDeflection._Cast_PowerLoadCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoadCompoundSystemDeflection:
    """Special nested class for casting PowerLoadCompoundSystemDeflection to subclasses."""

    __parent__: "PowerLoadCompoundSystemDeflection"

    @property
    def virtual_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3066.VirtualComponentCompoundSystemDeflection":
        return self.__parent__._cast(_3066.VirtualComponentCompoundSystemDeflection)

    @property
    def mountable_component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3020.MountableComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3020,
        )

        return self.__parent__._cast(_3020.MountableComponentCompoundSystemDeflection)

    @property
    def component_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2965.ComponentCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2965,
        )

        return self.__parent__._cast(_2965.ComponentCompoundSystemDeflection)

    @property
    def part_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3022.PartCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _3022,
        )

        return self.__parent__._cast(_3022.PartCompoundSystemDeflection)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

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
    def power_load_compound_system_deflection(
        self: "CastSelf",
    ) -> "PowerLoadCompoundSystemDeflection":
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
class PowerLoadCompoundSystemDeflection(_3066.VirtualComponentCompoundSystemDeflection):
    """PowerLoadCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOAD_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2530.PowerLoad":
        """mastapy.system_model.part_model.PowerLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2881.PowerLoadSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_2881.PowerLoadSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.PowerLoadSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoadCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_PowerLoadCompoundSystemDeflection
        """
        return _Cast_PowerLoadCompoundSystemDeflection(self)
