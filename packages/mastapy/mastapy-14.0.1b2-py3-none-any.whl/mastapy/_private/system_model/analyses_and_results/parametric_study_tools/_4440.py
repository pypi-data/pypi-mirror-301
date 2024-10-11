"""ConicalGearParametricStudyTool"""

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
    _4473,
)

_CONICAL_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ConicalGearParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4412,
        _4419,
        _4421,
        _4422,
        _4424,
        _4432,
        _4477,
        _4481,
        _4484,
        _4487,
        _4494,
        _4506,
        _4527,
        _4533,
        _4536,
        _4538,
        _4539,
        _4554,
    )
    from mastapy._private.system_model.part_model.gears import _2582

    Self = TypeVar("Self", bound="ConicalGearParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearParametricStudyTool._Cast_ConicalGearParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearParametricStudyTool:
    """Special nested class for casting ConicalGearParametricStudyTool to subclasses."""

    __parent__: "ConicalGearParametricStudyTool"

    @property
    def gear_parametric_study_tool(self: "CastSelf") -> "_4473.GearParametricStudyTool":
        return self.__parent__._cast(_4473.GearParametricStudyTool)

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4494.MountableComponentParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4494,
        )

        return self.__parent__._cast(_4494.MountableComponentParametricStudyTool)

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
    def agma_gleason_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4412.AGMAGleasonConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4412,
        )

        return self.__parent__._cast(_4412.AGMAGleasonConicalGearParametricStudyTool)

    @property
    def bevel_differential_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4419.BevelDifferentialGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4419,
        )

        return self.__parent__._cast(_4419.BevelDifferentialGearParametricStudyTool)

    @property
    def bevel_differential_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4421.BevelDifferentialPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4421,
        )

        return self.__parent__._cast(
            _4421.BevelDifferentialPlanetGearParametricStudyTool
        )

    @property
    def bevel_differential_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4422.BevelDifferentialSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4422,
        )

        return self.__parent__._cast(_4422.BevelDifferentialSunGearParametricStudyTool)

    @property
    def bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4424.BevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4424,
        )

        return self.__parent__._cast(_4424.BevelGearParametricStudyTool)

    @property
    def hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4477.HypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4477,
        )

        return self.__parent__._cast(_4477.HypoidGearParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4481.KlingelnbergCycloPalloidConicalGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4481,
        )

        return self.__parent__._cast(
            _4481.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4484.KlingelnbergCycloPalloidHypoidGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4484,
        )

        return self.__parent__._cast(
            _4484.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4487.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4487,
        )

        return self.__parent__._cast(
            _4487.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        )

    @property
    def spiral_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4527.SpiralBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4527,
        )

        return self.__parent__._cast(_4527.SpiralBevelGearParametricStudyTool)

    @property
    def straight_bevel_diff_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4533.StraightBevelDiffGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4533,
        )

        return self.__parent__._cast(_4533.StraightBevelDiffGearParametricStudyTool)

    @property
    def straight_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4536.StraightBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4536,
        )

        return self.__parent__._cast(_4536.StraightBevelGearParametricStudyTool)

    @property
    def straight_bevel_planet_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4538.StraightBevelPlanetGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4538,
        )

        return self.__parent__._cast(_4538.StraightBevelPlanetGearParametricStudyTool)

    @property
    def straight_bevel_sun_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4539.StraightBevelSunGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4539,
        )

        return self.__parent__._cast(_4539.StraightBevelSunGearParametricStudyTool)

    @property
    def zerol_bevel_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4554.ZerolBevelGearParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4554,
        )

        return self.__parent__._cast(_4554.ZerolBevelGearParametricStudyTool)

    @property
    def conical_gear_parametric_study_tool(
        self: "CastSelf",
    ) -> "ConicalGearParametricStudyTool":
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
class ConicalGearParametricStudyTool(_4473.GearParametricStudyTool):
    """ConicalGearParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2582.ConicalGear":
        """mastapy.system_model.part_model.gears.ConicalGear

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def planetaries(self: "Self") -> "List[ConicalGearParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearParametricStudyTool
        """
        return _Cast_ConicalGearParametricStudyTool(self)
