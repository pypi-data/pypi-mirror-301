"""StraightBevelSunGearCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4663,
)

_STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "StraightBevelSunGearCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4539,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4560,
        _4572,
        _4581,
        _4588,
        _4614,
        _4635,
        _4637,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7119

    Self = TypeVar("Self", bound="StraightBevelSunGearCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelSunGearCompoundParametricStudyTool._Cast_StraightBevelSunGearCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelSunGearCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelSunGearCompoundParametricStudyTool:
    """Special nested class for casting StraightBevelSunGearCompoundParametricStudyTool to subclasses."""

    __parent__: "StraightBevelSunGearCompoundParametricStudyTool"

    @property
    def straight_bevel_diff_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4663.StraightBevelDiffGearCompoundParametricStudyTool":
        return self.__parent__._cast(
            _4663.StraightBevelDiffGearCompoundParametricStudyTool
        )

    @property
    def bevel_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4572.BevelGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4572,
        )

        return self.__parent__._cast(_4572.BevelGearCompoundParametricStudyTool)

    @property
    def agma_gleason_conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4560.AGMAGleasonConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4560,
        )

        return self.__parent__._cast(
            _4560.AGMAGleasonConicalGearCompoundParametricStudyTool
        )

    @property
    def conical_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4588.ConicalGearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4588,
        )

        return self.__parent__._cast(_4588.ConicalGearCompoundParametricStudyTool)

    @property
    def gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4614.GearCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4614,
        )

        return self.__parent__._cast(_4614.GearCompoundParametricStudyTool)

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4635.MountableComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4635,
        )

        return self.__parent__._cast(
            _4635.MountableComponentCompoundParametricStudyTool
        )

    @property
    def component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4581.ComponentCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4581,
        )

        return self.__parent__._cast(_4581.ComponentCompoundParametricStudyTool)

    @property
    def part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4637.PartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4637,
        )

        return self.__parent__._cast(_4637.PartCompoundParametricStudyTool)

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
    def straight_bevel_sun_gear_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "StraightBevelSunGearCompoundParametricStudyTool":
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
class StraightBevelSunGearCompoundParametricStudyTool(
    _4663.StraightBevelDiffGearCompoundParametricStudyTool
):
    """StraightBevelSunGearCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_SUN_GEAR_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def properties_changing_all_load_cases(
        self: "Self",
    ) -> "_7119.StraightBevelSunGearLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertiesChangingAllLoadCases")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4539.StraightBevelSunGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool]

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
    ) -> "List[_4539.StraightBevelSunGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool]

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
    ) -> "_Cast_StraightBevelSunGearCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelSunGearCompoundParametricStudyTool
        """
        return _Cast_StraightBevelSunGearCompoundParametricStudyTool(self)
