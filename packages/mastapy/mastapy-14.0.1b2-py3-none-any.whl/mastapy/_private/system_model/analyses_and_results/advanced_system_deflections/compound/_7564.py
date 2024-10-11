"""AbstractAssemblyCompoundAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7645,
)

_ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound",
    "AbstractAssemblyCompoundAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7426,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
        _7570,
        _7571,
        _7574,
        _7577,
        _7582,
        _7584,
        _7585,
        _7590,
        _7595,
        _7598,
        _7601,
        _7605,
        _7607,
        _7613,
        _7619,
        _7621,
        _7624,
        _7628,
        _7632,
        _7635,
        _7638,
        _7641,
        _7646,
        _7650,
        _7657,
        _7660,
        _7664,
        _7667,
        _7668,
        _7673,
        _7676,
        _7679,
        _7683,
        _7691,
        _7694,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )

    Self = TypeVar("Self", bound="AbstractAssemblyCompoundAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyCompoundAdvancedSystemDeflection._Cast_AbstractAssemblyCompoundAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyCompoundAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection:
    """Special nested class for casting AbstractAssemblyCompoundAdvancedSystemDeflection to subclasses."""

    __parent__: "AbstractAssemblyCompoundAdvancedSystemDeflection"

    @property
    def part_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7645.PartCompoundAdvancedSystemDeflection":
        return self.__parent__._cast(_7645.PartCompoundAdvancedSystemDeflection)

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
    def agma_gleason_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7570.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7570,
        )

        return self.__parent__._cast(
            _7570.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7571.AssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7571,
        )

        return self.__parent__._cast(_7571.AssemblyCompoundAdvancedSystemDeflection)

    @property
    def belt_drive_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7574.BeltDriveCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7574,
        )

        return self.__parent__._cast(_7574.BeltDriveCompoundAdvancedSystemDeflection)

    @property
    def bevel_differential_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7577.BevelDifferentialGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7577,
        )

        return self.__parent__._cast(
            _7577.BevelDifferentialGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7582.BevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7582,
        )

        return self.__parent__._cast(_7582.BevelGearSetCompoundAdvancedSystemDeflection)

    @property
    def bolted_joint_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7584.BoltedJointCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7584,
        )

        return self.__parent__._cast(_7584.BoltedJointCompoundAdvancedSystemDeflection)

    @property
    def clutch_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7585.ClutchCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7585,
        )

        return self.__parent__._cast(_7585.ClutchCompoundAdvancedSystemDeflection)

    @property
    def concept_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7590.ConceptCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7590,
        )

        return self.__parent__._cast(
            _7590.ConceptCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def concept_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7595.ConceptGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7595,
        )

        return self.__parent__._cast(
            _7595.ConceptGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7598.ConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7598,
        )

        return self.__parent__._cast(
            _7598.ConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7601.CouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7601,
        )

        return self.__parent__._cast(_7601.CouplingCompoundAdvancedSystemDeflection)

    @property
    def cvt_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7605.CVTCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7605,
        )

        return self.__parent__._cast(_7605.CVTCompoundAdvancedSystemDeflection)

    @property
    def cycloidal_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7607.CycloidalAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7607,
        )

        return self.__parent__._cast(
            _7607.CycloidalAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def cylindrical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7613.CylindricalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7613,
        )

        return self.__parent__._cast(
            _7613.CylindricalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def face_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7619.FaceGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7619,
        )

        return self.__parent__._cast(_7619.FaceGearSetCompoundAdvancedSystemDeflection)

    @property
    def flexible_pin_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7621.FlexiblePinAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7621,
        )

        return self.__parent__._cast(
            _7621.FlexiblePinAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7624.GearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7624,
        )

        return self.__parent__._cast(_7624.GearSetCompoundAdvancedSystemDeflection)

    @property
    def hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7628.HypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7628,
        )

        return self.__parent__._cast(
            _7628.HypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7632.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7632,
        )

        return self.__parent__._cast(
            _7632.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7635.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7635,
        )

        return self.__parent__._cast(
            _7635.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7638.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7638,
        )

        return self.__parent__._cast(
            _7638.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def microphone_array_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7641.MicrophoneArrayCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7641,
        )

        return self.__parent__._cast(
            _7641.MicrophoneArrayCompoundAdvancedSystemDeflection
        )

    @property
    def part_to_part_shear_coupling_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7646.PartToPartShearCouplingCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7646,
        )

        return self.__parent__._cast(
            _7646.PartToPartShearCouplingCompoundAdvancedSystemDeflection
        )

    @property
    def planetary_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7650.PlanetaryGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7650,
        )

        return self.__parent__._cast(
            _7650.PlanetaryGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def rolling_ring_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7657.RollingRingAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7657,
        )

        return self.__parent__._cast(
            _7657.RollingRingAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def root_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7660.RootAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7660,
        )

        return self.__parent__._cast(_7660.RootAssemblyCompoundAdvancedSystemDeflection)

    @property
    def specialised_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7664.SpecialisedAssemblyCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7664,
        )

        return self.__parent__._cast(
            _7664.SpecialisedAssemblyCompoundAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7667.SpiralBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7667,
        )

        return self.__parent__._cast(
            _7667.SpiralBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def spring_damper_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7668.SpringDamperCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7668,
        )

        return self.__parent__._cast(_7668.SpringDamperCompoundAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7673.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7673,
        )

        return self.__parent__._cast(
            _7673.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7676.StraightBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7676,
        )

        return self.__parent__._cast(
            _7676.StraightBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def synchroniser_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7679.SynchroniserCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7679,
        )

        return self.__parent__._cast(_7679.SynchroniserCompoundAdvancedSystemDeflection)

    @property
    def torque_converter_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7683.TorqueConverterCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7683,
        )

        return self.__parent__._cast(
            _7683.TorqueConverterCompoundAdvancedSystemDeflection
        )

    @property
    def worm_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7691.WormGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7691,
        )

        return self.__parent__._cast(_7691.WormGearSetCompoundAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_set_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7694.ZerolBevelGearSetCompoundAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections.compound import (
            _7694,
        )

        return self.__parent__._cast(
            _7694.ZerolBevelGearSetCompoundAdvancedSystemDeflection
        )

    @property
    def abstract_assembly_compound_advanced_system_deflection(
        self: "CastSelf",
    ) -> "AbstractAssemblyCompoundAdvancedSystemDeflection":
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
class AbstractAssemblyCompoundAdvancedSystemDeflection(
    _7645.PartCompoundAdvancedSystemDeflection
):
    """AbstractAssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7426.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

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
    ) -> "List[_7426.AbstractAssemblyAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection]

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
    ) -> "_Cast_AbstractAssemblyCompoundAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection
        """
        return _Cast_AbstractAssemblyCompoundAdvancedSystemDeflection(self)
