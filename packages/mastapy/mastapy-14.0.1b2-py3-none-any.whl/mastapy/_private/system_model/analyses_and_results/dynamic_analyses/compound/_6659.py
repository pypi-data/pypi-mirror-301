"""StraightBevelDiffGearCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6568,
)

_STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "StraightBevelDiffGearCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6528,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6556,
        _6577,
        _6584,
        _6610,
        _6631,
        _6633,
        _6665,
        _6666,
    )
    from mastapy._private.system_model.part_model.gears import _2604

    Self = TypeVar("Self", bound="StraightBevelDiffGearCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearCompoundDynamicAnalysis._Cast_StraightBevelDiffGearCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearCompoundDynamicAnalysis:
    """Special nested class for casting StraightBevelDiffGearCompoundDynamicAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearCompoundDynamicAnalysis"

    @property
    def bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.BevelGearCompoundDynamicAnalysis":
        return self.__parent__._cast(_6568.BevelGearCompoundDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6556.AGMAGleasonConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6556,
        )

        return self.__parent__._cast(
            _6556.AGMAGleasonConicalGearCompoundDynamicAnalysis
        )

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConicalGearCompoundDynamicAnalysis)

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
    def straight_bevel_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.StraightBevelPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6665,
        )

        return self.__parent__._cast(
            _6665.StraightBevelPlanetGearCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6666.StraightBevelSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6666,
        )

        return self.__parent__._cast(_6666.StraightBevelSunGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearCompoundDynamicAnalysis":
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
class StraightBevelDiffGearCompoundDynamicAnalysis(
    _6568.BevelGearCompoundDynamicAnalysis
):
    """StraightBevelDiffGearCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2604.StraightBevelDiffGear":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGear

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
    ) -> "List[_6528.StraightBevelDiffGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis]

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
    ) -> "List[_6528.StraightBevelDiffGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.StraightBevelDiffGearDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearCompoundDynamicAnalysis
        """
        return _Cast_StraightBevelDiffGearCompoundDynamicAnalysis(self)
