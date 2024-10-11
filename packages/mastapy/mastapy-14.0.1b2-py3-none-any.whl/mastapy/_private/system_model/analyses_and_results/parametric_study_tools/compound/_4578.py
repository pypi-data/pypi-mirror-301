"""ClutchConnectionCompoundParametricStudyTool"""

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
    _4594,
)

_CLUTCH_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "ClutchConnectionCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4428,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4591,
        _4621,
    )
    from mastapy._private.system_model.connections_and_sockets.couplings import _2397

    Self = TypeVar("Self", bound="ClutchConnectionCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ClutchConnectionCompoundParametricStudyTool._Cast_ClutchConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchConnectionCompoundParametricStudyTool:
    """Special nested class for casting ClutchConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "ClutchConnectionCompoundParametricStudyTool"

    @property
    def coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4594.CouplingConnectionCompoundParametricStudyTool":
        return self.__parent__._cast(
            _4594.CouplingConnectionCompoundParametricStudyTool
        )

    @property
    def inter_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4621.InterMountableComponentConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4621,
        )

        return self.__parent__._cast(
            _4621.InterMountableComponentConnectionCompoundParametricStudyTool
        )

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4591.ConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4591,
        )

        return self.__parent__._cast(_4591.ConnectionCompoundParametricStudyTool)

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
    def clutch_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "ClutchConnectionCompoundParametricStudyTool":
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
class ClutchConnectionCompoundParametricStudyTool(
    _4594.CouplingConnectionCompoundParametricStudyTool
):
    """ClutchConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2397.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2397.ClutchConnection":
        """mastapy.system_model.connections_and_sockets.couplings.ClutchConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4428.ClutchConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4428.ClutchConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_ClutchConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ClutchConnectionCompoundParametricStudyTool
        """
        return _Cast_ClutchConnectionCompoundParametricStudyTool(self)
