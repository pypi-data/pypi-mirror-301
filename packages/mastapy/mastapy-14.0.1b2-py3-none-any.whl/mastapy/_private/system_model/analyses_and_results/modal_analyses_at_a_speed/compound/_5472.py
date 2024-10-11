"""SpecialisedAssemblyCompoundModalAnalysisAtASpeed"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _5372,
)

_SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound",
    "SpecialisedAssemblyCompoundModalAnalysisAtASpeed",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed import (
        _5341,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
        _5378,
        _5382,
        _5385,
        _5390,
        _5392,
        _5393,
        _5398,
        _5403,
        _5406,
        _5409,
        _5413,
        _5415,
        _5421,
        _5427,
        _5429,
        _5432,
        _5436,
        _5440,
        _5443,
        _5446,
        _5449,
        _5453,
        _5454,
        _5458,
        _5465,
        _5475,
        _5476,
        _5481,
        _5484,
        _5487,
        _5491,
        _5499,
        _5502,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundModalAnalysisAtASpeed")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundModalAnalysisAtASpeed._Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundModalAnalysisAtASpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed:
    """Special nested class for casting SpecialisedAssemblyCompoundModalAnalysisAtASpeed to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundModalAnalysisAtASpeed"

    @property
    def abstract_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5372.AbstractAssemblyCompoundModalAnalysisAtASpeed":
        return self.__parent__._cast(
            _5372.AbstractAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def part_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5453.PartCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5453,
        )

        return self.__parent__._cast(_5453.PartCompoundModalAnalysisAtASpeed)

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
    def agma_gleason_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5378.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5378,
        )

        return self.__parent__._cast(
            _5378.AGMAGleasonConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def belt_drive_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5382.BeltDriveCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5382,
        )

        return self.__parent__._cast(_5382.BeltDriveCompoundModalAnalysisAtASpeed)

    @property
    def bevel_differential_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5385.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5385,
        )

        return self.__parent__._cast(
            _5385.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5390.BevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5390,
        )

        return self.__parent__._cast(_5390.BevelGearSetCompoundModalAnalysisAtASpeed)

    @property
    def bolted_joint_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5392.BoltedJointCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5392,
        )

        return self.__parent__._cast(_5392.BoltedJointCompoundModalAnalysisAtASpeed)

    @property
    def clutch_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5393.ClutchCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5393,
        )

        return self.__parent__._cast(_5393.ClutchCompoundModalAnalysisAtASpeed)

    @property
    def concept_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5398.ConceptCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5398,
        )

        return self.__parent__._cast(_5398.ConceptCouplingCompoundModalAnalysisAtASpeed)

    @property
    def concept_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5403.ConceptGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5403,
        )

        return self.__parent__._cast(_5403.ConceptGearSetCompoundModalAnalysisAtASpeed)

    @property
    def conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5406.ConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5406,
        )

        return self.__parent__._cast(_5406.ConicalGearSetCompoundModalAnalysisAtASpeed)

    @property
    def coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5409.CouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5409,
        )

        return self.__parent__._cast(_5409.CouplingCompoundModalAnalysisAtASpeed)

    @property
    def cvt_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5413.CVTCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5413,
        )

        return self.__parent__._cast(_5413.CVTCompoundModalAnalysisAtASpeed)

    @property
    def cycloidal_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5415.CycloidalAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5415,
        )

        return self.__parent__._cast(
            _5415.CycloidalAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def cylindrical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5421.CylindricalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5421,
        )

        return self.__parent__._cast(
            _5421.CylindricalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def face_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5427.FaceGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5427,
        )

        return self.__parent__._cast(_5427.FaceGearSetCompoundModalAnalysisAtASpeed)

    @property
    def flexible_pin_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5429.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5429,
        )

        return self.__parent__._cast(
            _5429.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5432.GearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5432,
        )

        return self.__parent__._cast(_5432.GearSetCompoundModalAnalysisAtASpeed)

    @property
    def hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5436.HypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5436,
        )

        return self.__parent__._cast(_5436.HypoidGearSetCompoundModalAnalysisAtASpeed)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5440.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5440,
        )

        return self.__parent__._cast(
            _5440.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5443.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5443,
        )

        return self.__parent__._cast(
            _5443.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> (
        "_5446.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed"
    ):
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5446,
        )

        return self.__parent__._cast(
            _5446.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def microphone_array_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5449.MicrophoneArrayCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5449,
        )

        return self.__parent__._cast(_5449.MicrophoneArrayCompoundModalAnalysisAtASpeed)

    @property
    def part_to_part_shear_coupling_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5454.PartToPartShearCouplingCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5454,
        )

        return self.__parent__._cast(
            _5454.PartToPartShearCouplingCompoundModalAnalysisAtASpeed
        )

    @property
    def planetary_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5458.PlanetaryGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5458,
        )

        return self.__parent__._cast(
            _5458.PlanetaryGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def rolling_ring_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5465.RollingRingAssemblyCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5465,
        )

        return self.__parent__._cast(
            _5465.RollingRingAssemblyCompoundModalAnalysisAtASpeed
        )

    @property
    def spiral_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5475.SpiralBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5475,
        )

        return self.__parent__._cast(
            _5475.SpiralBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def spring_damper_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5476.SpringDamperCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5476,
        )

        return self.__parent__._cast(_5476.SpringDamperCompoundModalAnalysisAtASpeed)

    @property
    def straight_bevel_diff_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5481.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5481,
        )

        return self.__parent__._cast(
            _5481.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def straight_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5484.StraightBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5484,
        )

        return self.__parent__._cast(
            _5484.StraightBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def synchroniser_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5487.SynchroniserCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5487,
        )

        return self.__parent__._cast(_5487.SynchroniserCompoundModalAnalysisAtASpeed)

    @property
    def torque_converter_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5491.TorqueConverterCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5491,
        )

        return self.__parent__._cast(_5491.TorqueConverterCompoundModalAnalysisAtASpeed)

    @property
    def worm_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5499.WormGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5499,
        )

        return self.__parent__._cast(_5499.WormGearSetCompoundModalAnalysisAtASpeed)

    @property
    def zerol_bevel_gear_set_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "_5502.ZerolBevelGearSetCompoundModalAnalysisAtASpeed":
        from mastapy._private.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
            _5502,
        )

        return self.__parent__._cast(
            _5502.ZerolBevelGearSetCompoundModalAnalysisAtASpeed
        )

    @property
    def specialised_assembly_compound_modal_analysis_at_a_speed(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
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
class SpecialisedAssemblyCompoundModalAnalysisAtASpeed(
    _5372.AbstractAssemblyCompoundModalAnalysisAtASpeed
):
    """SpecialisedAssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5341.SpecialisedAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpecialisedAssemblyModalAnalysisAtASpeed]

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
    ) -> "List[_5341.SpecialisedAssemblyModalAnalysisAtASpeed]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.SpecialisedAssemblyModalAnalysisAtASpeed]

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
    ) -> "_Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed
        """
        return _Cast_SpecialisedAssemblyCompoundModalAnalysisAtASpeed(self)
