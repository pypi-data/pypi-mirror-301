"""ConicalGearMeshCompoundHarmonicAnalysis"""

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
    _6074,
)

_CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "ConicalGearMeshCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _5847,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6020,
        _6027,
        _6032,
        _6050,
        _6078,
        _6080,
        _6082,
        _6085,
        _6088,
        _6117,
        _6123,
        _6126,
        _6144,
    )

    Self = TypeVar("Self", bound="ConicalGearMeshCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundHarmonicAnalysis._Cast_ConicalGearMeshCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundHarmonicAnalysis:
    """Special nested class for casting ConicalGearMeshCompoundHarmonicAnalysis to subclasses."""

    __parent__: "ConicalGearMeshCompoundHarmonicAnalysis"

    @property
    def gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6074.GearMeshCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6074.GearMeshCompoundHarmonicAnalysis)

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6080.InterMountableComponentConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6080,
        )

        return self.__parent__._cast(
            _6080.InterMountableComponentConnectionCompoundHarmonicAnalysis
        )

    @property
    def connection_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6050.ConnectionCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6050,
        )

        return self.__parent__._cast(_6050.ConnectionCompoundHarmonicAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6020.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6020,
        )

        return self.__parent__._cast(
            _6020.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_differential_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6027.BevelDifferentialGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6027,
        )

        return self.__parent__._cast(
            _6027.BevelDifferentialGearMeshCompoundHarmonicAnalysis
        )

    @property
    def bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6032.BevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6032,
        )

        return self.__parent__._cast(_6032.BevelGearMeshCompoundHarmonicAnalysis)

    @property
    def hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6078.HypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6078,
        )

        return self.__parent__._cast(_6078.HypoidGearMeshCompoundHarmonicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6082.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6082,
        )

        return self.__parent__._cast(
            _6082.KlingelnbergCycloPalloidConicalGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6085.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6085,
        )

        return self.__parent__._cast(
            _6085.KlingelnbergCycloPalloidHypoidGearMeshCompoundHarmonicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6088.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6088,
        )

        return self.__parent__._cast(
            _6088.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def spiral_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6117.SpiralBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6117,
        )

        return self.__parent__._cast(_6117.SpiralBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6123.StraightBevelDiffGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6123,
        )

        return self.__parent__._cast(
            _6123.StraightBevelDiffGearMeshCompoundHarmonicAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6126.StraightBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6126,
        )

        return self.__parent__._cast(
            _6126.StraightBevelGearMeshCompoundHarmonicAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6144.ZerolBevelGearMeshCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6144,
        )

        return self.__parent__._cast(_6144.ZerolBevelGearMeshCompoundHarmonicAnalysis)

    @property
    def conical_gear_mesh_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundHarmonicAnalysis":
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
class ConicalGearMeshCompoundHarmonicAnalysis(_6074.GearMeshCompoundHarmonicAnalysis):
    """ConicalGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(self: "Self") -> "List[ConicalGearMeshCompoundHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.compound.ConicalGearMeshCompoundHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5847.ConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearMeshHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_5847.ConicalGearMeshHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.ConicalGearMeshHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearMeshCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundHarmonicAnalysis
        """
        return _Cast_ConicalGearMeshCompoundHarmonicAnalysis(self)
