"""StraightBevelPlanetGearCompoundSystemDeflection"""

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
    _3049,
)

_STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "StraightBevelPlanetGearCompoundSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2908,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _2944,
        _2956,
        _2965,
        _2972,
        _2999,
        _3020,
        _3022,
    )

    Self = TypeVar("Self", bound="StraightBevelPlanetGearCompoundSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelPlanetGearCompoundSystemDeflection._Cast_StraightBevelPlanetGearCompoundSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelPlanetGearCompoundSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelPlanetGearCompoundSystemDeflection:
    """Special nested class for casting StraightBevelPlanetGearCompoundSystemDeflection to subclasses."""

    __parent__: "StraightBevelPlanetGearCompoundSystemDeflection"

    @property
    def straight_bevel_diff_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_3049.StraightBevelDiffGearCompoundSystemDeflection":
        return self.__parent__._cast(
            _3049.StraightBevelDiffGearCompoundSystemDeflection
        )

    @property
    def bevel_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2956.BevelGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2956,
        )

        return self.__parent__._cast(_2956.BevelGearCompoundSystemDeflection)

    @property
    def agma_gleason_conical_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2944.AGMAGleasonConicalGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2944,
        )

        return self.__parent__._cast(
            _2944.AGMAGleasonConicalGearCompoundSystemDeflection
        )

    @property
    def conical_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2972.ConicalGearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2972,
        )

        return self.__parent__._cast(_2972.ConicalGearCompoundSystemDeflection)

    @property
    def gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "_2999.GearCompoundSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
            _2999,
        )

        return self.__parent__._cast(_2999.GearCompoundSystemDeflection)

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
    def straight_bevel_planet_gear_compound_system_deflection(
        self: "CastSelf",
    ) -> "StraightBevelPlanetGearCompoundSystemDeflection":
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
class StraightBevelPlanetGearCompoundSystemDeflection(
    _3049.StraightBevelDiffGearCompoundSystemDeflection
):
    """StraightBevelPlanetGearCompoundSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_PLANET_GEAR_COMPOUND_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_2908.StraightBevelPlanetGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelPlanetGearSystemDeflection]

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
    ) -> "List[_2908.StraightBevelPlanetGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelPlanetGearSystemDeflection]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_StraightBevelPlanetGearCompoundSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelPlanetGearCompoundSystemDeflection
        """
        return _Cast_StraightBevelPlanetGearCompoundSystemDeflection(self)
