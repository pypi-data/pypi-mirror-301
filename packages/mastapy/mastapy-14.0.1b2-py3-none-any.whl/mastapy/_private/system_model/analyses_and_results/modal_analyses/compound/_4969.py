"""VirtualComponentCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4924,
)

_VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "VirtualComponentCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4823
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4870,
        _4920,
        _4921,
        _4926,
        _4933,
        _4934,
        _4968,
    )

    Self = TypeVar("Self", bound="VirtualComponentCompoundModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualComponentCompoundModalAnalysis._Cast_VirtualComponentCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualComponentCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualComponentCompoundModalAnalysis:
    """Special nested class for casting VirtualComponentCompoundModalAnalysis to subclasses."""

    __parent__: "VirtualComponentCompoundModalAnalysis"

    @property
    def mountable_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4924.MountableComponentCompoundModalAnalysis":
        return self.__parent__._cast(_4924.MountableComponentCompoundModalAnalysis)

    @property
    def component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4870.ComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4870,
        )

        return self.__parent__._cast(_4870.ComponentCompoundModalAnalysis)

    @property
    def part_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4926.PartCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4926,
        )

        return self.__parent__._cast(_4926.PartCompoundModalAnalysis)

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
    def mass_disc_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4920.MassDiscCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4920,
        )

        return self.__parent__._cast(_4920.MassDiscCompoundModalAnalysis)

    @property
    def measurement_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4921.MeasurementComponentCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4921,
        )

        return self.__parent__._cast(_4921.MeasurementComponentCompoundModalAnalysis)

    @property
    def point_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4933.PointLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4933,
        )

        return self.__parent__._cast(_4933.PointLoadCompoundModalAnalysis)

    @property
    def power_load_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4934.PowerLoadCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4934,
        )

        return self.__parent__._cast(_4934.PowerLoadCompoundModalAnalysis)

    @property
    def unbalanced_mass_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4968.UnbalancedMassCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4968,
        )

        return self.__parent__._cast(_4968.UnbalancedMassCompoundModalAnalysis)

    @property
    def virtual_component_compound_modal_analysis(
        self: "CastSelf",
    ) -> "VirtualComponentCompoundModalAnalysis":
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
class VirtualComponentCompoundModalAnalysis(
    _4924.MountableComponentCompoundModalAnalysis
):
    """VirtualComponentCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_COMPONENT_COMPOUND_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_4823.VirtualComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis]

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
    ) -> "List[_4823.VirtualComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.VirtualComponentModalAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_VirtualComponentCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_VirtualComponentCompoundModalAnalysis
        """
        return _Cast_VirtualComponentCompoundModalAnalysis(self)
