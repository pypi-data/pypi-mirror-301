"""CouplingStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3968

_COUPLING_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "CouplingStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3866,
        _3889,
        _3894,
        _3949,
        _3952,
        _3974,
        _3992,
    )
    from mastapy._private.system_model.part_model.couplings import _2644

    Self = TypeVar("Self", bound="CouplingStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="CouplingStabilityAnalysis._Cast_CouplingStabilityAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingStabilityAnalysis:
    """Special nested class for casting CouplingStabilityAnalysis to subclasses."""

    __parent__: "CouplingStabilityAnalysis"

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3968.SpecialisedAssemblyStabilityAnalysis":
        return self.__parent__._cast(_3968.SpecialisedAssemblyStabilityAnalysis)

    @property
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3866.AbstractAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3866,
        )

        return self.__parent__._cast(_3866.AbstractAssemblyStabilityAnalysis)

    @property
    def part_stability_analysis(self: "CastSelf") -> "_3949.PartStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3949,
        )

        return self.__parent__._cast(_3949.PartStabilityAnalysis)

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7720,
        )

        return self.__parent__._cast(_7720.PartStaticLoadAnalysisCase)

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
    def clutch_stability_analysis(self: "CastSelf") -> "_3889.ClutchStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3889,
        )

        return self.__parent__._cast(_3889.ClutchStabilityAnalysis)

    @property
    def concept_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3894.ConceptCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3894,
        )

        return self.__parent__._cast(_3894.ConceptCouplingStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3952.PartToPartShearCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3952,
        )

        return self.__parent__._cast(_3952.PartToPartShearCouplingStabilityAnalysis)

    @property
    def spring_damper_stability_analysis(
        self: "CastSelf",
    ) -> "_3974.SpringDamperStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3974,
        )

        return self.__parent__._cast(_3974.SpringDamperStabilityAnalysis)

    @property
    def torque_converter_stability_analysis(
        self: "CastSelf",
    ) -> "_3992.TorqueConverterStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3992,
        )

        return self.__parent__._cast(_3992.TorqueConverterStabilityAnalysis)

    @property
    def coupling_stability_analysis(self: "CastSelf") -> "CouplingStabilityAnalysis":
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
class CouplingStabilityAnalysis(_3968.SpecialisedAssemblyStabilityAnalysis):
    """CouplingStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2644.Coupling":
        """mastapy.system_model.part_model.couplings.Coupling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CouplingStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingStabilityAnalysis
        """
        return _Cast_CouplingStabilityAnalysis(self)
