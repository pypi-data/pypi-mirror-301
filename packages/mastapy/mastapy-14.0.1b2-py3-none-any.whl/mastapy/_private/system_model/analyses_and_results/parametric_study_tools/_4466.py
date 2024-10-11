"""ExternalCADModelParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4432,
)

_EXTERNAL_CAD_MODEL_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ExternalCADModelParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4506,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7034
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2839,
    )
    from mastapy._private.system_model.part_model import _2508

    Self = TypeVar("Self", bound="ExternalCADModelParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ExternalCADModelParametricStudyTool._Cast_ExternalCADModelParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalCADModelParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ExternalCADModelParametricStudyTool:
    """Special nested class for casting ExternalCADModelParametricStudyTool to subclasses."""

    __parent__: "ExternalCADModelParametricStudyTool"

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4432.ComponentParametricStudyTool":
        return self.__parent__._cast(_4432.ComponentParametricStudyTool)

    @property
    def part_parametric_study_tool(self: "CastSelf") -> "_4506.PartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4506,
        )

        return self.__parent__._cast(_4506.PartParametricStudyTool)

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
    def external_cad_model_parametric_study_tool(
        self: "CastSelf",
    ) -> "ExternalCADModelParametricStudyTool":
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
class ExternalCADModelParametricStudyTool(_4432.ComponentParametricStudyTool):
    """ExternalCADModelParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EXTERNAL_CAD_MODEL_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2508.ExternalCADModel":
        """mastapy.system_model.part_model.ExternalCADModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_load_case(self: "Self") -> "_7034.ExternalCADModelLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_system_deflection_results(
        self: "Self",
    ) -> "List[_2839.ExternalCADModelSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.ExternalCADModelSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ExternalCADModelParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ExternalCADModelParametricStudyTool
        """
        return _Cast_ExternalCADModelParametricStudyTool(self)
