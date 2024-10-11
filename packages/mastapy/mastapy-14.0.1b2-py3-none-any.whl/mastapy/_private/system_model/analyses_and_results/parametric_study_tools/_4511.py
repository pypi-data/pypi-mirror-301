"""PlanetaryGearSetParametricStudyTool"""

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
    _4456,
)

_PLANETARY_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "PlanetaryGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4407,
        _4474,
        _4506,
        _4525,
    )
    from mastapy._private.system_model.part_model.gears import _2601

    Self = TypeVar("Self", bound="PlanetaryGearSetParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetaryGearSetParametricStudyTool._Cast_PlanetaryGearSetParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryGearSetParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryGearSetParametricStudyTool:
    """Special nested class for casting PlanetaryGearSetParametricStudyTool to subclasses."""

    __parent__: "PlanetaryGearSetParametricStudyTool"

    @property
    def cylindrical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4456.CylindricalGearSetParametricStudyTool":
        return self.__parent__._cast(_4456.CylindricalGearSetParametricStudyTool)

    @property
    def gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4474.GearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4474,
        )

        return self.__parent__._cast(_4474.GearSetParametricStudyTool)

    @property
    def specialised_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4525.SpecialisedAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4525,
        )

        return self.__parent__._cast(_4525.SpecialisedAssemblyParametricStudyTool)

    @property
    def abstract_assembly_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4407.AbstractAssemblyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4407,
        )

        return self.__parent__._cast(_4407.AbstractAssemblyParametricStudyTool)

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
    def planetary_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "PlanetaryGearSetParametricStudyTool":
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
class PlanetaryGearSetParametricStudyTool(_4456.CylindricalGearSetParametricStudyTool):
    """PlanetaryGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_GEAR_SET_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2601.PlanetaryGearSet":
        """mastapy.system_model.part_model.gears.PlanetaryGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryGearSetParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryGearSetParametricStudyTool
        """
        return _Cast_PlanetaryGearSetParametricStudyTool(self)
