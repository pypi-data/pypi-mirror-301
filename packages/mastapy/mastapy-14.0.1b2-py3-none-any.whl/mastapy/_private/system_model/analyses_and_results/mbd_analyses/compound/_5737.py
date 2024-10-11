"""MeasurementComponentCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5785,
)

_MEASUREMENT_COMPONENT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "MeasurementComponentCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5591
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5686,
        _5740,
        _5742,
    )
    from mastapy._private.system_model.part_model import _2519

    Self = TypeVar(
        "Self", bound="MeasurementComponentCompoundMultibodyDynamicsAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="MeasurementComponentCompoundMultibodyDynamicsAnalysis._Cast_MeasurementComponentCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasurementComponentCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeasurementComponentCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting MeasurementComponentCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "MeasurementComponentCompoundMultibodyDynamicsAnalysis"

    @property
    def virtual_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5785.VirtualComponentCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5785.VirtualComponentCompoundMultibodyDynamicsAnalysis
        )

    @property
    def mountable_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5740.MountableComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5740,
        )

        return self.__parent__._cast(
            _5740.MountableComponentCompoundMultibodyDynamicsAnalysis
        )

    @property
    def component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5686.ComponentCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5686,
        )

        return self.__parent__._cast(_5686.ComponentCompoundMultibodyDynamicsAnalysis)

    @property
    def part_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5742.PartCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5742,
        )

        return self.__parent__._cast(_5742.PartCompoundMultibodyDynamicsAnalysis)

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
    def measurement_component_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "MeasurementComponentCompoundMultibodyDynamicsAnalysis":
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
class MeasurementComponentCompoundMultibodyDynamicsAnalysis(
    _5785.VirtualComponentCompoundMultibodyDynamicsAnalysis
):
    """MeasurementComponentCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MEASUREMENT_COMPONENT_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2519.MeasurementComponent":
        """mastapy.system_model.part_model.MeasurementComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5591.MeasurementComponentMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.MeasurementComponentMultibodyDynamicsAnalysis]

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
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_5591.MeasurementComponentMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.MeasurementComponentMultibodyDynamicsAnalysis]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_MeasurementComponentCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_MeasurementComponentCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_MeasurementComponentCompoundMultibodyDynamicsAnalysis(self)
