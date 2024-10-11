"""StraightBevelDiffGearMeshParametricStudyTool"""

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
    _4423,
)

_STRAIGHT_BEVEL_DIFF_GEAR_MESH_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "StraightBevelDiffGearMeshParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7710
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4411,
        _4439,
        _4442,
        _4472,
        _4479,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7113
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2902,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2380

    Self = TypeVar("Self", bound="StraightBevelDiffGearMeshParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearMeshParametricStudyTool._Cast_StraightBevelDiffGearMeshParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearMeshParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearMeshParametricStudyTool:
    """Special nested class for casting StraightBevelDiffGearMeshParametricStudyTool to subclasses."""

    __parent__: "StraightBevelDiffGearMeshParametricStudyTool"

    @property
    def bevel_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4423.BevelGearMeshParametricStudyTool":
        return self.__parent__._cast(_4423.BevelGearMeshParametricStudyTool)

    @property
    def agma_gleason_conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4411.AGMAGleasonConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4411,
        )

        return self.__parent__._cast(
            _4411.AGMAGleasonConicalGearMeshParametricStudyTool
        )

    @property
    def conical_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4439.ConicalGearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4439,
        )

        return self.__parent__._cast(_4439.ConicalGearMeshParametricStudyTool)

    @property
    def gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4472.GearMeshParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4472,
        )

        return self.__parent__._cast(_4472.GearMeshParametricStudyTool)

    @property
    def inter_mountable_component_connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4479.InterMountableComponentConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4479,
        )

        return self.__parent__._cast(
            _4479.InterMountableComponentConnectionParametricStudyTool
        )

    @property
    def connection_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4442.ConnectionParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4442,
        )

        return self.__parent__._cast(_4442.ConnectionParametricStudyTool)

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
    def straight_bevel_diff_gear_mesh_parametric_study_tool(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearMeshParametricStudyTool":
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
class StraightBevelDiffGearMeshParametricStudyTool(
    _4423.BevelGearMeshParametricStudyTool
):
    """StraightBevelDiffGearMeshParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_MESH_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_design(self: "Self") -> "_2380.StraightBevelDiffGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_load_case(self: "Self") -> "_7113.StraightBevelDiffGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_system_deflection_results(
        self: "Self",
    ) -> "List[_2902.StraightBevelDiffGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.StraightBevelDiffGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSystemDeflectionResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearMeshParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearMeshParametricStudyTool
        """
        return _Cast_StraightBevelDiffGearMeshParametricStudyTool(self)
