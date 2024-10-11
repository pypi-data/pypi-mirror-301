"""StraightBevelDiffGearSetCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
    _6707,
)

_STRAIGHT_BEVEL_DIFF_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses",
    "StraightBevelDiffGearSetCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6689,
        _6695,
        _6723,
        _6752,
        _6773,
        _6792,
        _6799,
        _6800,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7114
    from mastapy._private.system_model.part_model.gears import _2605

    Self = TypeVar("Self", bound="StraightBevelDiffGearSetCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearSetCriticalSpeedAnalysis._Cast_StraightBevelDiffGearSetCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearSetCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearSetCriticalSpeedAnalysis:
    """Special nested class for casting StraightBevelDiffGearSetCriticalSpeedAnalysis to subclasses."""

    __parent__: "StraightBevelDiffGearSetCriticalSpeedAnalysis"

    @property
    def bevel_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6707.BevelGearSetCriticalSpeedAnalysis":
        return self.__parent__._cast(_6707.BevelGearSetCriticalSpeedAnalysis)

    @property
    def agma_gleason_conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6695.AGMAGleasonConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6695,
        )

        return self.__parent__._cast(
            _6695.AGMAGleasonConicalGearSetCriticalSpeedAnalysis
        )

    @property
    def conical_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6723.ConicalGearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6723,
        )

        return self.__parent__._cast(_6723.ConicalGearSetCriticalSpeedAnalysis)

    @property
    def gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6752.GearSetCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6752,
        )

        return self.__parent__._cast(_6752.GearSetCriticalSpeedAnalysis)

    @property
    def specialised_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6792.SpecialisedAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6792,
        )

        return self.__parent__._cast(_6792.SpecialisedAssemblyCriticalSpeedAnalysis)

    @property
    def abstract_assembly_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6689.AbstractAssemblyCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6689,
        )

        return self.__parent__._cast(_6689.AbstractAssemblyCriticalSpeedAnalysis)

    @property
    def part_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6773.PartCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
            _6773,
        )

        return self.__parent__._cast(_6773.PartCriticalSpeedAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7717.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7717,
        )

        return self.__parent__._cast(_7717.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2744

        return self.__parent__._cast(_2744.PartAnalysis)

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
    def straight_bevel_diff_gear_set_critical_speed_analysis(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearSetCriticalSpeedAnalysis":
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
class StraightBevelDiffGearSetCriticalSpeedAnalysis(
    _6707.BevelGearSetCriticalSpeedAnalysis
):
    """StraightBevelDiffGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2605.StraightBevelDiffGearSet":
        """mastapy.system_model.part_model.gears.StraightBevelDiffGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_load_case(self: "Self") -> "_7114.StraightBevelDiffGearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def bevel_gears_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6799.StraightBevelDiffGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsCriticalSpeedAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_gears_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6799.StraightBevelDiffGearCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffGearsCriticalSpeedAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6800.StraightBevelDiffGearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearMeshCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesCriticalSpeedAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_meshes_critical_speed_analysis(
        self: "Self",
    ) -> "List[_6800.StraightBevelDiffGearMeshCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.StraightBevelDiffGearMeshCriticalSpeedAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StraightBevelDiffMeshesCriticalSpeedAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearSetCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearSetCriticalSpeedAnalysis
        """
        return _Cast_StraightBevelDiffGearSetCriticalSpeedAnalysis(self)
