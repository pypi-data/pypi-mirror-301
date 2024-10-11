"""ConicalGearSetCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5721,
)

_CONICAL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "ConicalGearSetCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5541
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5661,
        _5667,
        _5674,
        _5679,
        _5725,
        _5729,
        _5732,
        _5735,
        _5742,
        _5761,
        _5764,
        _5770,
        _5773,
        _5791,
    )

    Self = TypeVar("Self", bound="ConicalGearSetCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetCompoundMultibodyDynamicsAnalysis._Cast_ConicalGearSetCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting ConicalGearSetCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "ConicalGearSetCompoundMultibodyDynamicsAnalysis"

    @property
    def gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5721.GearSetCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(_5721.GearSetCompoundMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5761.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5761,
        )

        return self.__parent__._cast(
            _5761.SpecialisedAssemblyCompoundMultibodyDynamicsAnalysis
        )

    @property
    def abstract_assembly_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5661.AbstractAssemblyCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5661,
        )

        return self.__parent__._cast(
            _5661.AbstractAssemblyCompoundMultibodyDynamicsAnalysis
        )

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
    def agma_gleason_conical_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5667.AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5667,
        )

        return self.__parent__._cast(
            _5667.AGMAGleasonConicalGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5674.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5674,
        )

        return self.__parent__._cast(
            _5674.BevelDifferentialGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5679.BevelGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5679,
        )

        return self.__parent__._cast(
            _5679.BevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def hypoid_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5725.HypoidGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5725,
        )

        return self.__parent__._cast(
            _5725.HypoidGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> (
        "_5729.KlingelnbergCycloPalloidConicalGearSetCompoundMultibodyDynamicsAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5729,
        )

        return self.__parent__._cast(
            _5729.KlingelnbergCycloPalloidConicalGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5732.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5732,
        )

        return self.__parent__._cast(
            _5732.KlingelnbergCycloPalloidHypoidGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5735.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5735,
        )

        return self.__parent__._cast(
            _5735.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5764.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5764,
        )

        return self.__parent__._cast(
            _5764.SpiralBevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_diff_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5770.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5770,
        )

        return self.__parent__._cast(
            _5770.StraightBevelDiffGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5773.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5773,
        )

        return self.__parent__._cast(
            _5773.StraightBevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def zerol_bevel_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5791.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5791,
        )

        return self.__parent__._cast(
            _5791.ZerolBevelGearSetCompoundMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_set_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "ConicalGearSetCompoundMultibodyDynamicsAnalysis":
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
class ConicalGearSetCompoundMultibodyDynamicsAnalysis(
    _5721.GearSetCompoundMultibodyDynamicsAnalysis
):
    """ConicalGearSetCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5541.ConicalGearSetMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearSetMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5541.ConicalGearSetMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.ConicalGearSetMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConicalGearSetCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_ConicalGearSetCompoundMultibodyDynamicsAnalysis(self)
