"""ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7354,
)

_CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7196,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7300,
        _7307,
        _7312,
        _7330,
        _7358,
        _7360,
        _7362,
        _7365,
        _7368,
        _7397,
        _7403,
        _7406,
        _7424,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )

    Self = TypeVar(
        "Self", bound="ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7354.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7354.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def inter_mountable_component_connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7360.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7360,
        )

        return self.__parent__._cast(
            _7360.InterMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def connection_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7330.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7330,
        )

        return self.__parent__._cast(
            _7330.ConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
        )

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
    def agma_gleason_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7300.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7300,
        )

        return self.__parent__._cast(
            _7300.AGMAGleasonConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_differential_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7307.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7307,
        )

        return self.__parent__._cast(
            _7307.BevelDifferentialGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7312.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7312,
        )

        return self.__parent__._cast(
            _7312.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7358.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7358,
        )

        return self.__parent__._cast(
            _7358.HypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7362.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7362,
        )

        return self.__parent__._cast(
            _7362.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7365.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7365,
        )

        return self.__parent__._cast(
            _7365.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7368.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7368,
        )

        return self.__parent__._cast(
            _7368.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def spiral_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7397.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7397,
        )

        return self.__parent__._cast(
            _7397.SpiralBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7403.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7403,
        )

        return self.__parent__._cast(
            _7403.StraightBevelDiffGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def straight_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7406.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7406,
        )

        return self.__parent__._cast(
            _7406.StraightBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def zerol_bevel_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7424.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7424,
        )

        return self.__parent__._cast(
            _7424.ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def conical_gear_mesh_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7354.GearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CONICAL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def planetaries(
        self: "Self",
    ) -> "List[ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound.ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7196.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation]

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
    ) -> "List[_7196.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.ConicalGearMeshAdvancedTimeSteppingAnalysisForModulation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_ConicalGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(
            self
        )
