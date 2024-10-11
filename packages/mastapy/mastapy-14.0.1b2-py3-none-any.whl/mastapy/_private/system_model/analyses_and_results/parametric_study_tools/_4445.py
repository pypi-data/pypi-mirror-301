"""CouplingHalfParametricStudyTool"""

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
    _4494,
)

_COUPLING_HALF_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "CouplingHalfParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4429,
        _4432,
        _4434,
        _4449,
        _4506,
        _4508,
        _4515,
        _4520,
        _4530,
        _4540,
        _4542,
        _4543,
        _4546,
        _4547,
    )
    from mastapy._private.system_model.part_model.couplings import _2645

    Self = TypeVar("Self", bound="CouplingHalfParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfParametricStudyTool._Cast_CouplingHalfParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfParametricStudyTool:
    """Special nested class for casting CouplingHalfParametricStudyTool to subclasses."""

    __parent__: "CouplingHalfParametricStudyTool"

    @property
    def mountable_component_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4494.MountableComponentParametricStudyTool":
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
    def clutch_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4429.ClutchHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4429,
        )

        return self.__parent__._cast(_4429.ClutchHalfParametricStudyTool)

    @property
    def concept_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4434.ConceptCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4434,
        )

        return self.__parent__._cast(_4434.ConceptCouplingHalfParametricStudyTool)

    @property
    def cvt_pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4449.CVTPulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4449,
        )

        return self.__parent__._cast(_4449.CVTPulleyParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4508.PartToPartShearCouplingHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4508,
        )

        return self.__parent__._cast(
            _4508.PartToPartShearCouplingHalfParametricStudyTool
        )

    @property
    def pulley_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4515.PulleyParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4515,
        )

        return self.__parent__._cast(_4515.PulleyParametricStudyTool)

    @property
    def rolling_ring_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4520.RollingRingParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4520,
        )

        return self.__parent__._cast(_4520.RollingRingParametricStudyTool)

    @property
    def spring_damper_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4530.SpringDamperHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4530,
        )

        return self.__parent__._cast(_4530.SpringDamperHalfParametricStudyTool)

    @property
    def synchroniser_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4540.SynchroniserHalfParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4540,
        )

        return self.__parent__._cast(_4540.SynchroniserHalfParametricStudyTool)

    @property
    def synchroniser_part_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4542.SynchroniserPartParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4542,
        )

        return self.__parent__._cast(_4542.SynchroniserPartParametricStudyTool)

    @property
    def synchroniser_sleeve_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4543.SynchroniserSleeveParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4543,
        )

        return self.__parent__._cast(_4543.SynchroniserSleeveParametricStudyTool)

    @property
    def torque_converter_pump_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4546.TorqueConverterPumpParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4546,
        )

        return self.__parent__._cast(_4546.TorqueConverterPumpParametricStudyTool)

    @property
    def torque_converter_turbine_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4547.TorqueConverterTurbineParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4547,
        )

        return self.__parent__._cast(_4547.TorqueConverterTurbineParametricStudyTool)

    @property
    def coupling_half_parametric_study_tool(
        self: "CastSelf",
    ) -> "CouplingHalfParametricStudyTool":
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
class CouplingHalfParametricStudyTool(_4494.MountableComponentParametricStudyTool):
    """CouplingHalfParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2645.CouplingHalf":
        """mastapy.system_model.part_model.couplings.CouplingHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingHalfParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfParametricStudyTool
        """
        return _Cast_CouplingHalfParametricStudyTool(self)
