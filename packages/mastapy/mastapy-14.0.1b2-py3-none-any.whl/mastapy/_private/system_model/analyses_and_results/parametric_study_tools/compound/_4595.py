"""CouplingHalfCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4635,
)

_COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
    "CouplingHalfCompoundParametricStudyTool",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4445,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4579,
        _4581,
        _4584,
        _4598,
        _4637,
        _4640,
        _4646,
        _4650,
        _4662,
        _4672,
        _4673,
        _4674,
        _4677,
        _4678,
    )

    Self = TypeVar("Self", bound="CouplingHalfCompoundParametricStudyTool")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingHalfCompoundParametricStudyTool._Cast_CouplingHalfCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingHalfCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingHalfCompoundParametricStudyTool:
    """Special nested class for casting CouplingHalfCompoundParametricStudyTool to subclasses."""

    __parent__: "CouplingHalfCompoundParametricStudyTool"

    @property
    def mountable_component_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4635.MountableComponentCompoundParametricStudyTool":
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
    def clutch_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4579.ClutchHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4579,
        )

        return self.__parent__._cast(_4579.ClutchHalfCompoundParametricStudyTool)

    @property
    def concept_coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4584.ConceptCouplingHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4584,
        )

        return self.__parent__._cast(
            _4584.ConceptCouplingHalfCompoundParametricStudyTool
        )

    @property
    def cvt_pulley_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4598.CVTPulleyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4598,
        )

        return self.__parent__._cast(_4598.CVTPulleyCompoundParametricStudyTool)

    @property
    def part_to_part_shear_coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4640.PartToPartShearCouplingHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4640,
        )

        return self.__parent__._cast(
            _4640.PartToPartShearCouplingHalfCompoundParametricStudyTool
        )

    @property
    def pulley_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4646.PulleyCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4646,
        )

        return self.__parent__._cast(_4646.PulleyCompoundParametricStudyTool)

    @property
    def rolling_ring_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4650.RollingRingCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4650,
        )

        return self.__parent__._cast(_4650.RollingRingCompoundParametricStudyTool)

    @property
    def spring_damper_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4662.SpringDamperHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4662,
        )

        return self.__parent__._cast(_4662.SpringDamperHalfCompoundParametricStudyTool)

    @property
    def synchroniser_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4672.SynchroniserHalfCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4672,
        )

        return self.__parent__._cast(_4672.SynchroniserHalfCompoundParametricStudyTool)

    @property
    def synchroniser_part_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4673.SynchroniserPartCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4673,
        )

        return self.__parent__._cast(_4673.SynchroniserPartCompoundParametricStudyTool)

    @property
    def synchroniser_sleeve_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4674.SynchroniserSleeveCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4674,
        )

        return self.__parent__._cast(
            _4674.SynchroniserSleeveCompoundParametricStudyTool
        )

    @property
    def torque_converter_pump_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4677.TorqueConverterPumpCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4677,
        )

        return self.__parent__._cast(
            _4677.TorqueConverterPumpCompoundParametricStudyTool
        )

    @property
    def torque_converter_turbine_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4678.TorqueConverterTurbineCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4678,
        )

        return self.__parent__._cast(
            _4678.TorqueConverterTurbineCompoundParametricStudyTool
        )

    @property
    def coupling_half_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "CouplingHalfCompoundParametricStudyTool":
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
class CouplingHalfCompoundParametricStudyTool(
    _4635.MountableComponentCompoundParametricStudyTool
):
    """CouplingHalfCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_HALF_COMPOUND_PARAMETRIC_STUDY_TOOL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4445.CouplingHalfParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool]

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
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4445.CouplingHalfParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool]

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
    def cast_to(self: "Self") -> "_Cast_CouplingHalfCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_CouplingHalfCompoundParametricStudyTool
        """
        return _Cast_CouplingHalfCompoundParametricStudyTool(self)
