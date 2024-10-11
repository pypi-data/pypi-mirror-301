"""AbstractShaftParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4408,
)

_ABSTRACT_SHAFT_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "AbstractShaftParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4432,
        _4452,
        _4506,
        _4523,
    )
    from mastapy._private.system_model.part_model import _2491

    Self = TypeVar("Self", bound="AbstractShaftParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractShaftParametricStudyTool._Cast_AbstractShaftParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractShaftParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractShaftParametricStudyTool:
    """Special nested class for casting AbstractShaftParametricStudyTool to subclasses."""

    __parent__: "AbstractShaftParametricStudyTool"

    @property
    def abstract_shaft_or_housing_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4408.AbstractShaftOrHousingParametricStudyTool":
        return self.__parent__._cast(_4408.AbstractShaftOrHousingParametricStudyTool)

    @property
    def component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4432.ComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4432,
        )

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
    def cycloidal_disc_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4452.CycloidalDiscParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4452,
        )

        return self.__parent__._cast(_4452.CycloidalDiscParametricStudyTool)

    @property
    def shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4523.ShaftParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4523,
        )

        return self.__parent__._cast(_4523.ShaftParametricStudyTool)

    @property
    def abstract_shaft_parametric_study_tool(
        self: "CastSelf",
    ) -> "AbstractShaftParametricStudyTool":
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
class AbstractShaftParametricStudyTool(_4408.AbstractShaftOrHousingParametricStudyTool):
    """AbstractShaftParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SHAFT_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2491.AbstractShaft":
        """mastapy.system_model.part_model.AbstractShaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractShaftParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_AbstractShaftParametricStudyTool
        """
        return _Cast_AbstractShaftParametricStudyTool(self)
