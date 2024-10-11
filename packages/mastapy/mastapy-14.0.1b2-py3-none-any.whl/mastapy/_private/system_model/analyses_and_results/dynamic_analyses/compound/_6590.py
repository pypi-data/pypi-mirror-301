"""CouplingConnectionCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6617,
)

_COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "CouplingConnectionCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6456,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6574,
        _6579,
        _6587,
        _6635,
        _6657,
        _6672,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundDynamicAnalysis._Cast_CouplingConnectionCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundDynamicAnalysis:
    """Special nested class for casting CouplingConnectionCompoundDynamicAnalysis to subclasses."""

    __parent__: "CouplingConnectionCompoundDynamicAnalysis"

    @property
    def inter_mountable_component_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6617.InterMountableComponentConnectionCompoundDynamicAnalysis":
        return self.__parent__._cast(
            _6617.InterMountableComponentConnectionCompoundDynamicAnalysis
        )

    @property
    def connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6587.ConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6587,
        )

        return self.__parent__._cast(_6587.ConnectionCompoundDynamicAnalysis)

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
    def clutch_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6574.ClutchConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6574,
        )

        return self.__parent__._cast(_6574.ClutchConnectionCompoundDynamicAnalysis)

    @property
    def concept_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6579.ConceptCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6579,
        )

        return self.__parent__._cast(
            _6579.ConceptCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6635.PartToPartShearCouplingConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6635,
        )

        return self.__parent__._cast(
            _6635.PartToPartShearCouplingConnectionCompoundDynamicAnalysis
        )

    @property
    def spring_damper_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6657.SpringDamperConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6657,
        )

        return self.__parent__._cast(
            _6657.SpringDamperConnectionCompoundDynamicAnalysis
        )

    @property
    def torque_converter_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6672.TorqueConverterConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6672,
        )

        return self.__parent__._cast(
            _6672.TorqueConverterConnectionCompoundDynamicAnalysis
        )

    @property
    def coupling_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundDynamicAnalysis":
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
class CouplingConnectionCompoundDynamicAnalysis(
    _6617.InterMountableComponentConnectionCompoundDynamicAnalysis
):
    """CouplingConnectionCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6456.CouplingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis]

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
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6456.CouplingConnectionDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.CouplingConnectionDynamicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_CouplingConnectionCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundDynamicAnalysis
        """
        return _Cast_CouplingConnectionCompoundDynamicAnalysis(self)
