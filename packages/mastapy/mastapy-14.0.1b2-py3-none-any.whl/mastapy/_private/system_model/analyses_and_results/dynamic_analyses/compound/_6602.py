"""CylindricalPlanetGearCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6599,
)

_CYLINDRICAL_PLANET_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CylindricalPlanetGearCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6469,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6577,
        _6610,
        _6631,
        _6633,
    )

    Self = TypeVar("Self", bound="CylindricalPlanetGearCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalPlanetGearCompoundDynamicAnalysis._Cast_CylindricalPlanetGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalPlanetGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalPlanetGearCompoundDynamicAnalysis:
    """Special nested class for casting CylindricalPlanetGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "CylindricalPlanetGearCompoundDynamicAnalysis"

    @property
    def cylindrical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.CylindricalGearCompoundDynamicAnalysis":
        return self.__parent__._cast(_6599.CylindricalGearCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6610,
        )

        return self.__parent__._cast(_6610.GearCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6631.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6631,
        )

        return self.__parent__._cast(_6631.MountableComponentCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6577.ComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6577,
        )

        return self.__parent__._cast(_6577.ComponentCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6633,
        )

        return self.__parent__._cast(_6633.PartCompoundDynamicAnalysis)

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
    def cylindrical_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CylindricalPlanetGearCompoundDynamicAnalysis":
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
class CylindricalPlanetGearCompoundDynamicAnalysis(
    _6599.CylindricalGearCompoundDynamicAnalysis
):
    """CylindricalPlanetGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_PLANET_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6469.CylindricalPlanetGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis]

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
    ) -> "List[_6469.CylindricalPlanetGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CylindricalPlanetGearDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CylindricalPlanetGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CylindricalPlanetGearCompoundDynamicAnalysis
        """
        return _Cast_CylindricalPlanetGearCompoundDynamicAnalysis(self)
