"""AbstractAssemblyCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6096,
)

_ABSTRACT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "AbstractAssemblyCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5812,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6021,
        _6022,
        _6025,
        _6028,
        _6033,
        _6035,
        _6036,
        _6041,
        _6046,
        _6049,
        _6052,
        _6056,
        _6058,
        _6064,
        _6070,
        _6072,
        _6075,
        _6079,
        _6083,
        _6086,
        _6089,
        _6092,
        _6097,
        _6101,
        _6108,
        _6111,
        _6115,
        _6118,
        _6119,
        _6124,
        _6127,
        _6130,
        _6134,
        _6142,
        _6145,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundHarmonicAnalysis._Cast_AbstractAssemblyCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundHarmonicAnalysis:
    """Special nested class for casting AbstractAssemblyCompoundHarmonicAnalysis to subclasses."""

    __parent__: "AbstractAssemblyCompoundHarmonicAnalysis"

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6096.PartCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6096.PartCompoundHarmonicAnalysis)

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
    def agma_gleason_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6021.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6021,
        )

        return self.__parent__._cast(
            _6021.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6022.AssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6022,
        )

        return self.__parent__._cast(_6022.AssemblyCompoundHarmonicAnalysis)

    @property
    def belt_drive_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6025.BeltDriveCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6025,
        )

        return self.__parent__._cast(_6025.BeltDriveCompoundHarmonicAnalysis)

    @property
    def bevel_differential_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6028.BevelDifferentialGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6028,
        )

        return self.__parent__._cast(
            _6028.BevelDifferentialGearSetCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6033.BevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6033,
        )

        return self.__parent__._cast(_6033.BevelGearSetCompoundHarmonicAnalysis)

    @property
    def bolted_joint_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6035.BoltedJointCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6035,
        )

        return self.__parent__._cast(_6035.BoltedJointCompoundHarmonicAnalysis)

    @property
    def clutch_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6036.ClutchCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6036,
        )

        return self.__parent__._cast(_6036.ClutchCompoundHarmonicAnalysis)

    @property
    def concept_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6041.ConceptCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6041,
        )

        return self.__parent__._cast(_6041.ConceptCouplingCompoundHarmonicAnalysis)

    @property
    def concept_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6046.ConceptGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6046,
        )

        return self.__parent__._cast(_6046.ConceptGearSetCompoundHarmonicAnalysis)

    @property
    def conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6049.ConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6049,
        )

        return self.__parent__._cast(_6049.ConicalGearSetCompoundHarmonicAnalysis)

    @property
    def coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6052.CouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6052,
        )

        return self.__parent__._cast(_6052.CouplingCompoundHarmonicAnalysis)

    @property
    def cvt_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6056.CVTCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6056,
        )

        return self.__parent__._cast(_6056.CVTCompoundHarmonicAnalysis)

    @property
    def cycloidal_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6058.CycloidalAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6058,
        )

        return self.__parent__._cast(_6058.CycloidalAssemblyCompoundHarmonicAnalysis)

    @property
    def cylindrical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6064.CylindricalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6064,
        )

        return self.__parent__._cast(_6064.CylindricalGearSetCompoundHarmonicAnalysis)

    @property
    def face_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6070.FaceGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6070,
        )

        return self.__parent__._cast(_6070.FaceGearSetCompoundHarmonicAnalysis)

    @property
    def flexible_pin_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6072.FlexiblePinAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6072,
        )

        return self.__parent__._cast(_6072.FlexiblePinAssemblyCompoundHarmonicAnalysis)

    @property
    def gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6075.GearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6075,
        )

        return self.__parent__._cast(_6075.GearSetCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6079.HypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6079,
        )

        return self.__parent__._cast(_6079.HypoidGearSetCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6083.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6083,
        )

        return self.__parent__._cast(
            _6083.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6086.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6086,
        )

        return self.__parent__._cast(
            _6086.KlingelnbergCycloPalloidHypoidGearSetCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6089.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6089,
        )

        return self.__parent__._cast(
            _6089.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
        )

    @property
    def microphone_array_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6092.MicrophoneArrayCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6092,
        )

        return self.__parent__._cast(_6092.MicrophoneArrayCompoundHarmonicAnalysis)

    @property
    def part_to_part_shear_coupling_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6097.PartToPartShearCouplingCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6097,
        )

        return self.__parent__._cast(
            _6097.PartToPartShearCouplingCompoundHarmonicAnalysis
        )

    @property
    def planetary_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6101.PlanetaryGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6101,
        )

        return self.__parent__._cast(_6101.PlanetaryGearSetCompoundHarmonicAnalysis)

    @property
    def rolling_ring_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6108.RollingRingAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6108,
        )

        return self.__parent__._cast(_6108.RollingRingAssemblyCompoundHarmonicAnalysis)

    @property
    def root_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6111.RootAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6111,
        )

        return self.__parent__._cast(_6111.RootAssemblyCompoundHarmonicAnalysis)

    @property
    def specialised_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6115.SpecialisedAssemblyCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6115,
        )

        return self.__parent__._cast(_6115.SpecialisedAssemblyCompoundHarmonicAnalysis)

    @property
    def spiral_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6118.SpiralBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6118,
        )

        return self.__parent__._cast(_6118.SpiralBevelGearSetCompoundHarmonicAnalysis)

    @property
    def spring_damper_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6119.SpringDamperCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6119,
        )

        return self.__parent__._cast(_6119.SpringDamperCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6124.StraightBevelDiffGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6124,
        )

        return self.__parent__._cast(
            _6124.StraightBevelDiffGearSetCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6127.StraightBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6127,
        )

        return self.__parent__._cast(_6127.StraightBevelGearSetCompoundHarmonicAnalysis)

    @property
    def synchroniser_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6130.SynchroniserCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6130,
        )

        return self.__parent__._cast(_6130.SynchroniserCompoundHarmonicAnalysis)

    @property
    def torque_converter_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6134.TorqueConverterCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6134,
        )

        return self.__parent__._cast(_6134.TorqueConverterCompoundHarmonicAnalysis)

    @property
    def worm_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6142.WormGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6142,
        )

        return self.__parent__._cast(_6142.WormGearSetCompoundHarmonicAnalysis)

    @property
    def zerol_bevel_gear_set_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6145.ZerolBevelGearSetCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6145,
        )

        return self.__parent__._cast(_6145.ZerolBevelGearSetCompoundHarmonicAnalysis)

    @property
    def abstract_assembly_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundHarmonicAnalysis":
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
class AbstractAssemblyCompoundHarmonicAnalysis(_6096.PartCompoundHarmonicAnalysis):
    """AbstractAssemblyCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_5812.AbstractAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractAssemblyHarmonicAnalysis]

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
    ) -> "List[_5812.AbstractAssemblyHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.AbstractAssemblyHarmonicAnalysis]

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
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundHarmonicAnalysis
        """
        return _Cast_AbstractAssemblyCompoundHarmonicAnalysis(self)
