"""SpecialisedAssemblyCompoundModalAnalysisAtAStiffness"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
    _5109,
)

_SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound",
    "SpecialisedAssemblyCompoundModalAnalysisAtAStiffness",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
        _5078,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
        _5115,
        _5119,
        _5122,
        _5127,
        _5129,
        _5130,
        _5135,
        _5140,
        _5143,
        _5146,
        _5150,
        _5152,
        _5158,
        _5164,
        _5166,
        _5169,
        _5173,
        _5177,
        _5180,
        _5183,
        _5186,
        _5190,
        _5191,
        _5195,
        _5202,
        _5212,
        _5213,
        _5218,
        _5221,
        _5224,
        _5228,
        _5236,
        _5239,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundModalAnalysisAtAStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundModalAnalysisAtAStiffness._Cast_SpecialisedAssemblyCompoundModalAnalysisAtAStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundModalAnalysisAtAStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundModalAnalysisAtAStiffness:
    """Special nested class for casting SpecialisedAssemblyCompoundModalAnalysisAtAStiffness to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundModalAnalysisAtAStiffness"

    @property
    def abstract_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5109.AbstractAssemblyCompoundModalAnalysisAtAStiffness":
        return self.__parent__._cast(
            _5109.AbstractAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5190.PartCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5190,
        )

        return self.__parent__._cast(_5190.PartCompoundModalAnalysisAtAStiffness)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5115.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5115,
        )

        return self.__parent__._cast(
            _5115.AGMAGleasonConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def belt_drive_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5119.BeltDriveCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5119,
        )

        return self.__parent__._cast(_5119.BeltDriveCompoundModalAnalysisAtAStiffness)

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5122.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5122,
        )

        return self.__parent__._cast(
            _5122.BevelDifferentialGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5127.BevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5127,
        )

        return self.__parent__._cast(
            _5127.BevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def bolted_joint_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5129.BoltedJointCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5129,
        )

        return self.__parent__._cast(_5129.BoltedJointCompoundModalAnalysisAtAStiffness)

    @property
    def clutch_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5130.ClutchCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5130,
        )

        return self.__parent__._cast(_5130.ClutchCompoundModalAnalysisAtAStiffness)

    @property
    def concept_coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5135.ConceptCouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5135,
        )

        return self.__parent__._cast(
            _5135.ConceptCouplingCompoundModalAnalysisAtAStiffness
        )

    @property
    def concept_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5140.ConceptGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5140,
        )

        return self.__parent__._cast(
            _5140.ConceptGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5143.ConicalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5143,
        )

        return self.__parent__._cast(
            _5143.ConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5146.CouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5146,
        )

        return self.__parent__._cast(_5146.CouplingCompoundModalAnalysisAtAStiffness)

    @property
    def cvt_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5150.CVTCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5150,
        )

        return self.__parent__._cast(_5150.CVTCompoundModalAnalysisAtAStiffness)

    @property
    def cycloidal_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5152.CycloidalAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5152,
        )

        return self.__parent__._cast(
            _5152.CycloidalAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def cylindrical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5158.CylindricalGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5158,
        )

        return self.__parent__._cast(
            _5158.CylindricalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def face_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5164.FaceGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5164,
        )

        return self.__parent__._cast(_5164.FaceGearSetCompoundModalAnalysisAtAStiffness)

    @property
    def flexible_pin_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5166.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5166,
        )

        return self.__parent__._cast(
            _5166.FlexiblePinAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5169.GearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5169,
        )

        return self.__parent__._cast(_5169.GearSetCompoundModalAnalysisAtAStiffness)

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5173.HypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5173,
        )

        return self.__parent__._cast(
            _5173.HypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> (
        "_5177.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5177,
        )

        return self.__parent__._cast(
            _5177.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5180.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5180,
        )

        return self.__parent__._cast(
            _5180.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5183.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5183,
        )

        return self.__parent__._cast(
            _5183.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def microphone_array_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5186.MicrophoneArrayCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5186,
        )

        return self.__parent__._cast(
            _5186.MicrophoneArrayCompoundModalAnalysisAtAStiffness
        )

    @property
    def part_to_part_shear_coupling_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5191.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5191,
        )

        return self.__parent__._cast(
            _5191.PartToPartShearCouplingCompoundModalAnalysisAtAStiffness
        )

    @property
    def planetary_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5195.PlanetaryGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5195,
        )

        return self.__parent__._cast(
            _5195.PlanetaryGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def rolling_ring_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5202.RollingRingAssemblyCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5202,
        )

        return self.__parent__._cast(
            _5202.RollingRingAssemblyCompoundModalAnalysisAtAStiffness
        )

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5212.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5212,
        )

        return self.__parent__._cast(
            _5212.SpiralBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def spring_damper_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5213.SpringDamperCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5213,
        )

        return self.__parent__._cast(
            _5213.SpringDamperCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5218.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5218,
        )

        return self.__parent__._cast(
            _5218.StraightBevelDiffGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5221.StraightBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5221,
        )

        return self.__parent__._cast(
            _5221.StraightBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def synchroniser_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5224.SynchroniserCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5224,
        )

        return self.__parent__._cast(
            _5224.SynchroniserCompoundModalAnalysisAtAStiffness
        )

    @property
    def torque_converter_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5228.TorqueConverterCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5228,
        )

        return self.__parent__._cast(
            _5228.TorqueConverterCompoundModalAnalysisAtAStiffness
        )

    @property
    def worm_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5236.WormGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5236,
        )

        return self.__parent__._cast(_5236.WormGearSetCompoundModalAnalysisAtAStiffness)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "_5239.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import (
            _5239,
        )

        return self.__parent__._cast(
            _5239.ZerolBevelGearSetCompoundModalAnalysisAtAStiffness
        )

    @property
    def specialised_assembly_compound_modal_analysis_at_a_stiffness(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundModalAnalysisAtAStiffness":
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
class SpecialisedAssemblyCompoundModalAnalysisAtAStiffness(
    _5109.AbstractAssemblyCompoundModalAnalysisAtAStiffness
):
    """SpecialisedAssemblyCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5078.SpecialisedAssemblyModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.SpecialisedAssemblyModalAnalysisAtAStiffness]

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
    ) -> "List[_5078.SpecialisedAssemblyModalAnalysisAtAStiffness]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.SpecialisedAssemblyModalAnalysisAtAStiffness]

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
    ) -> "_Cast_SpecialisedAssemblyCompoundModalAnalysisAtAStiffness":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundModalAnalysisAtAStiffness
        """
        return _Cast_SpecialisedAssemblyCompoundModalAnalysisAtAStiffness(self)
