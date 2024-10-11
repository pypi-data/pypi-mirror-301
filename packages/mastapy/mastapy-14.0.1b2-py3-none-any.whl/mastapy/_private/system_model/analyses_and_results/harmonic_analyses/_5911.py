"""KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _5848

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5812,
        _5892,
        _5909,
        _5910,
        _5914,
        _5917,
        _5924,
        _5946,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2856,
    )
    from mastapy._private.system_model.part_model.gears import _2596

    Self = TypeVar(
        "Self", bound="KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis._Cast_KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis"

    @property
    def conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5848.ConicalGearSetHarmonicAnalysis":
        return self.__parent__._cast(_5848.ConicalGearSetHarmonicAnalysis)

    @property
    def gear_set_harmonic_analysis(self: "CastSelf") -> "_5892.GearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5892,
        )

        return self.__parent__._cast(_5892.GearSetHarmonicAnalysis)

    @property
    def specialised_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5946.SpecialisedAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5946,
        )

        return self.__parent__._cast(_5946.SpecialisedAssemblyHarmonicAnalysis)

    @property
    def abstract_assembly_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5812.AbstractAssemblyHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5812,
        )

        return self.__parent__._cast(_5812.AbstractAssemblyHarmonicAnalysis)

    @property
    def part_harmonic_analysis(self: "CastSelf") -> "_5924.PartHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5924,
        )

        return self.__parent__._cast(_5924.PartHarmonicAnalysis)

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
    def klingelnberg_cyclo_palloid_hypoid_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5914.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5914,
        )

        return self.__parent__._cast(
            _5914.KlingelnbergCycloPalloidHypoidGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "_5917.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _5917,
        )

        return self.__parent__._cast(
            _5917.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_harmonic_analysis(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis":
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
class KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis(
    _5848.ConicalGearSetHarmonicAnalysis
):
    """KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET_HARMONIC_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2596.KlingelnbergCycloPalloidConicalGearSet":
        """mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def conical_gears_harmonic_analysis(
        self: "Self",
    ) -> "List[_5909.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsHarmonicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_gears_harmonic_analysis(
        self: "Self",
    ) -> "List[_5909.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalGearsHarmonicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_harmonic_analysis(
        self: "Self",
    ) -> "List[_5910.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesHarmonicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_conical_meshes_harmonic_analysis(
        self: "Self",
    ) -> "List[_5910.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.KlingelnbergCycloPalloidConicalGearMeshHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidConicalMeshesHarmonicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2856.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.KlingelnbergCycloPalloidConicalGearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSetHarmonicAnalysis(self)
