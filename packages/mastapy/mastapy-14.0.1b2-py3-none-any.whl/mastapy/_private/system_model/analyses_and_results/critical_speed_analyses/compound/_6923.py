"""SpecialisedAssemblyCompoundCriticalSpeedAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
    _6823,
)

_SPECIALISED_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound",
    "SpecialisedAssemblyCompoundCriticalSpeedAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses import (
        _6792,
    )
    from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
        _6829,
        _6833,
        _6836,
        _6841,
        _6843,
        _6844,
        _6849,
        _6854,
        _6857,
        _6860,
        _6864,
        _6866,
        _6872,
        _6878,
        _6880,
        _6883,
        _6887,
        _6891,
        _6894,
        _6897,
        _6900,
        _6904,
        _6905,
        _6909,
        _6916,
        _6926,
        _6927,
        _6932,
        _6935,
        _6938,
        _6942,
        _6950,
        _6953,
    )

    Self = TypeVar("Self", bound="SpecialisedAssemblyCompoundCriticalSpeedAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpecialisedAssemblyCompoundCriticalSpeedAnalysis._Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssemblyCompoundCriticalSpeedAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis:
    """Special nested class for casting SpecialisedAssemblyCompoundCriticalSpeedAnalysis to subclasses."""

    __parent__: "SpecialisedAssemblyCompoundCriticalSpeedAnalysis"

    @property
    def abstract_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6823.AbstractAssemblyCompoundCriticalSpeedAnalysis":
        return self.__parent__._cast(
            _6823.AbstractAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def part_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6904.PartCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6904,
        )

        return self.__parent__._cast(_6904.PartCompoundCriticalSpeedAnalysis)

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
    def agma_gleason_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6829.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6829,
        )

        return self.__parent__._cast(
            _6829.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def belt_drive_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6833.BeltDriveCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6833,
        )

        return self.__parent__._cast(_6833.BeltDriveCompoundCriticalSpeedAnalysis)

    @property
    def bevel_differential_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6836.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6836,
        )

        return self.__parent__._cast(
            _6836.BevelDifferentialGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6841.BevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6841,
        )

        return self.__parent__._cast(_6841.BevelGearSetCompoundCriticalSpeedAnalysis)

    @property
    def bolted_joint_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6843.BoltedJointCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6843,
        )

        return self.__parent__._cast(_6843.BoltedJointCompoundCriticalSpeedAnalysis)

    @property
    def clutch_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6844.ClutchCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6844,
        )

        return self.__parent__._cast(_6844.ClutchCompoundCriticalSpeedAnalysis)

    @property
    def concept_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6849.ConceptCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6849,
        )

        return self.__parent__._cast(_6849.ConceptCouplingCompoundCriticalSpeedAnalysis)

    @property
    def concept_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6854.ConceptGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6854,
        )

        return self.__parent__._cast(_6854.ConceptGearSetCompoundCriticalSpeedAnalysis)

    @property
    def conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6857.ConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6857,
        )

        return self.__parent__._cast(_6857.ConicalGearSetCompoundCriticalSpeedAnalysis)

    @property
    def coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6860.CouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6860,
        )

        return self.__parent__._cast(_6860.CouplingCompoundCriticalSpeedAnalysis)

    @property
    def cvt_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6864.CVTCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6864,
        )

        return self.__parent__._cast(_6864.CVTCompoundCriticalSpeedAnalysis)

    @property
    def cycloidal_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6866.CycloidalAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6866,
        )

        return self.__parent__._cast(
            _6866.CycloidalAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def cylindrical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6872.CylindricalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6872,
        )

        return self.__parent__._cast(
            _6872.CylindricalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def face_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6878.FaceGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6878,
        )

        return self.__parent__._cast(_6878.FaceGearSetCompoundCriticalSpeedAnalysis)

    @property
    def flexible_pin_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6880.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6880,
        )

        return self.__parent__._cast(
            _6880.FlexiblePinAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6883.GearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6883,
        )

        return self.__parent__._cast(_6883.GearSetCompoundCriticalSpeedAnalysis)

    @property
    def hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6887.HypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6887,
        )

        return self.__parent__._cast(_6887.HypoidGearSetCompoundCriticalSpeedAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6891.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6891,
        )

        return self.__parent__._cast(
            _6891.KlingelnbergCycloPalloidConicalGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6894.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6894,
        )

        return self.__parent__._cast(
            _6894.KlingelnbergCycloPalloidHypoidGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> (
        "_6897.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis"
    ):
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6897,
        )

        return self.__parent__._cast(
            _6897.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def microphone_array_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6900.MicrophoneArrayCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6900,
        )

        return self.__parent__._cast(_6900.MicrophoneArrayCompoundCriticalSpeedAnalysis)

    @property
    def part_to_part_shear_coupling_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6905.PartToPartShearCouplingCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6905,
        )

        return self.__parent__._cast(
            _6905.PartToPartShearCouplingCompoundCriticalSpeedAnalysis
        )

    @property
    def planetary_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6909.PlanetaryGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6909,
        )

        return self.__parent__._cast(
            _6909.PlanetaryGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def rolling_ring_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6916.RollingRingAssemblyCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6916,
        )

        return self.__parent__._cast(
            _6916.RollingRingAssemblyCompoundCriticalSpeedAnalysis
        )

    @property
    def spiral_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6926.SpiralBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6926,
        )

        return self.__parent__._cast(
            _6926.SpiralBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def spring_damper_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6927.SpringDamperCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6927,
        )

        return self.__parent__._cast(_6927.SpringDamperCompoundCriticalSpeedAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6932.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6932,
        )

        return self.__parent__._cast(
            _6932.StraightBevelDiffGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6935.StraightBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6935,
        )

        return self.__parent__._cast(
            _6935.StraightBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def synchroniser_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6938.SynchroniserCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6938,
        )

        return self.__parent__._cast(_6938.SynchroniserCompoundCriticalSpeedAnalysis)

    @property
    def torque_converter_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6942.TorqueConverterCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6942,
        )

        return self.__parent__._cast(_6942.TorqueConverterCompoundCriticalSpeedAnalysis)

    @property
    def worm_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6950.WormGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6950,
        )

        return self.__parent__._cast(_6950.WormGearSetCompoundCriticalSpeedAnalysis)

    @property
    def zerol_bevel_gear_set_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "_6953.ZerolBevelGearSetCompoundCriticalSpeedAnalysis":
        from mastapy._private.system_model.analyses_and_results.critical_speed_analyses.compound import (
            _6953,
        )

        return self.__parent__._cast(
            _6953.ZerolBevelGearSetCompoundCriticalSpeedAnalysis
        )

    @property
    def specialised_assembly_compound_critical_speed_analysis(
        self: "CastSelf",
    ) -> "SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
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
class SpecialisedAssemblyCompoundCriticalSpeedAnalysis(
    _6823.AbstractAssemblyCompoundCriticalSpeedAnalysis
):
    """SpecialisedAssemblyCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY_COMPOUND_CRITICAL_SPEED_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6792.SpecialisedAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SpecialisedAssemblyCriticalSpeedAnalysis]

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
    ) -> "List[_6792.SpecialisedAssemblyCriticalSpeedAnalysis]":
        """List[mastapy.system_model.analyses_and_results.critical_speed_analyses.SpecialisedAssemblyCriticalSpeedAnalysis]

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
    ) -> "_Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis
        """
        return _Cast_SpecialisedAssemblyCompoundCriticalSpeedAnalysis(self)
