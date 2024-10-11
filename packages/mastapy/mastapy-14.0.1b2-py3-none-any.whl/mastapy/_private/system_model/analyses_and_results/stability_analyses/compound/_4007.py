"""AGMAGleasonConicalGearMeshCompoundStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
    _4035,
)

_AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound",
    "AGMAGleasonConicalGearMeshCompoundStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3870,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
        _4014,
        _4019,
        _4037,
        _4061,
        _4065,
        _4067,
        _4104,
        _4110,
        _4113,
        _4131,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearMeshCompoundStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMAGleasonConicalGearMeshCompoundStabilityAnalysis._Cast_AGMAGleasonConicalGearMeshCompoundStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearMeshCompoundStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearMeshCompoundStabilityAnalysis:
    """Special nested class for casting AGMAGleasonConicalGearMeshCompoundStabilityAnalysis to subclasses."""

    __parent__: "AGMAGleasonConicalGearMeshCompoundStabilityAnalysis"

    @property
    def conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4035.ConicalGearMeshCompoundStabilityAnalysis":
        return self.__parent__._cast(_4035.ConicalGearMeshCompoundStabilityAnalysis)

    @property
    def gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4061.GearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4061,
        )

        return self.__parent__._cast(_4061.GearMeshCompoundStabilityAnalysis)

    @property
    def inter_mountable_component_connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4067.InterMountableComponentConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4067,
        )

        return self.__parent__._cast(
            _4067.InterMountableComponentConnectionCompoundStabilityAnalysis
        )

    @property
    def connection_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4037.ConnectionCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4037,
        )

        return self.__parent__._cast(_4037.ConnectionCompoundStabilityAnalysis)

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
    def bevel_differential_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4014.BevelDifferentialGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4014,
        )

        return self.__parent__._cast(
            _4014.BevelDifferentialGearMeshCompoundStabilityAnalysis
        )

    @property
    def bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4019.BevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4019,
        )

        return self.__parent__._cast(_4019.BevelGearMeshCompoundStabilityAnalysis)

    @property
    def hypoid_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4065.HypoidGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4065,
        )

        return self.__parent__._cast(_4065.HypoidGearMeshCompoundStabilityAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4104.SpiralBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4104,
        )

        return self.__parent__._cast(_4104.SpiralBevelGearMeshCompoundStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4110.StraightBevelDiffGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4110,
        )

        return self.__parent__._cast(
            _4110.StraightBevelDiffGearMeshCompoundStabilityAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4113.StraightBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4113,
        )

        return self.__parent__._cast(
            _4113.StraightBevelGearMeshCompoundStabilityAnalysis
        )

    @property
    def zerol_bevel_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "_4131.ZerolBevelGearMeshCompoundStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses.compound import (
            _4131,
        )

        return self.__parent__._cast(_4131.ZerolBevelGearMeshCompoundStabilityAnalysis)

    @property
    def agma_gleason_conical_gear_mesh_compound_stability_analysis(
        self: "CastSelf",
    ) -> "AGMAGleasonConicalGearMeshCompoundStabilityAnalysis":
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
class AGMAGleasonConicalGearMeshCompoundStabilityAnalysis(
    _4035.ConicalGearMeshCompoundStabilityAnalysis
):
    """AGMAGleasonConicalGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_3870.AGMAGleasonConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearMeshStabilityAnalysis]

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
    ) -> "List[_3870.AGMAGleasonConicalGearMeshStabilityAnalysis]":
        """List[mastapy.system_model.analyses_and_results.stability_analyses.AGMAGleasonConicalGearMeshStabilityAnalysis]

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
    ) -> "_Cast_AGMAGleasonConicalGearMeshCompoundStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearMeshCompoundStabilityAnalysis
        """
        return _Cast_AGMAGleasonConicalGearMeshCompoundStabilityAnalysis(self)
