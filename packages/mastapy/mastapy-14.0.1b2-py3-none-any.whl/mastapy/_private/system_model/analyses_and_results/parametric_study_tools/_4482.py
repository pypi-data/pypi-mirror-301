"""KlingelnbergCycloPalloidConicalGearSetParametricStudyTool"""

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
    _4441,
)

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "KlingelnbergCycloPalloidConicalGearSetParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4407,
        _4474,
        _4480,
        _4481,
        _4485,
        _4488,
        _4506,
        _4525,
    )
    from mastapy._private.system_model.part_model.gears import _2596

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearSetParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetParametricStudyTool._Cast_KlingelnbergCycloPalloidConicalGearSetParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetParametricStudyTool:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetParametricStudyTool to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetParametricStudyTool"

    @property
    def conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4441.ConicalGearSetParametricStudyTool":
        return self.__parent__._cast(_4441.ConicalGearSetParametricStudyTool)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4485.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4485,
        )

        return self.__parent__._cast(
            _4485.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4488.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4488,
        )

        return self.__parent__._cast(
            _4488.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_parametric_study_tool(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
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
class KlingelnbergCycloPalloidConicalGearSetParametricStudyTool(
    _4441.ConicalGearSetParametricStudyTool
):
    """KlingelnbergCycloPalloidConicalGearSetParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_PARAMETRIC_STUDY_TOOL
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2596.KlingelnbergCycloPalloidConicalGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4481.KlingelnbergCycloPalloidConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_gears_parametric_study_tool(
        self: "Self",
    ) -> "List[_4481.KlingelnbergCycloPalloidConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalGearsParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4480.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesParametricStudyTool")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_meshes_parametric_study_tool(
        self: "Self",
    ) -> "List[_4480.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalMeshesParametricStudyTool"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSetParametricStudyTool(self)
