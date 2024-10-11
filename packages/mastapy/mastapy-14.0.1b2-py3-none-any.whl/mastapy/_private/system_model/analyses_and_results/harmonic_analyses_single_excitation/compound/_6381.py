"""SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6296,
)

_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6250,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6284,
        _6312,
        _6314,
        _6338,
        _6344,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2378

    Self = TypeVar(
        "Self", bound="SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation._Cast_SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6296.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6296.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def agma_gleason_conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6284.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6284,
        )

        return self.__parent__._cast(
            _6284.AGMAGleasonConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def conical_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6312.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6312,
        )

        return self.__parent__._cast(
            _6312.ConicalGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6338.GearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6338,
        )

        return self.__parent__._cast(
            _6338.GearMeshCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def inter_mountable_component_connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6344.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6344,
        )

        return self.__parent__._cast(
            _6344.InterMountableComponentConnectionCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def connection_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6314.ConnectionCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6314,
        )

        return self.__parent__._cast(
            _6314.ConnectionCompoundHarmonicAnalysisOfSingleExcitation
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
    def spiral_bevel_gear_mesh_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
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
class SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation(
    _6296.BevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
):
    """SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _SPIRAL_BEVEL_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2378.SpiralBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_design(self: "Self") -> "_2378.SpiralBevelGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6250.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]

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
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_6250.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.SpiralBevelGearMeshHarmonicAnalysisOfSingleExcitation]

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_SpiralBevelGearMeshCompoundHarmonicAnalysisOfSingleExcitation(self)
