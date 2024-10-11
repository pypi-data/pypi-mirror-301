"""BevelGearSetMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5509

_BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "BevelGearSetMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7721,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5503,
        _5519,
        _5522,
        _5523,
        _5541,
        _5568,
        _5597,
        _5619,
        _5622,
        _5629,
        _5632,
        _5653,
    )
    from mastapy._private.system_model.part_model.gears import _2579

    Self = TypeVar("Self", bound="BevelGearSetMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearSetMultibodyDynamicsAnalysis._Cast_BevelGearSetMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetMultibodyDynamicsAnalysis:
    """Special nested class for casting BevelGearSetMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "BevelGearSetMultibodyDynamicsAnalysis"

    @property
    def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5509.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5509.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5541.ConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5541,
        )

        return self.__parent__._cast(_5541.ConicalGearSetMultibodyDynamicsAnalysis)

    @property
    def gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5568.GearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5568,
        )

        return self.__parent__._cast(_5568.GearSetMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5619.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5619,
        )

        return self.__parent__._cast(_5619.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5503.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5503,
        )

        return self.__parent__._cast(_5503.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5597.PartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5597,
        )

        return self.__parent__._cast(_5597.PartMultibodyDynamicsAnalysis)

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7721.PartTimeSeriesLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7721,
        )

        return self.__parent__._cast(_7721.PartTimeSeriesLoadAnalysisCase)

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
    def bevel_differential_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5519.BevelDifferentialGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5519,
        )

        return self.__parent__._cast(
            _5519.BevelDifferentialGearSetMultibodyDynamicsAnalysis
        )

    @property
    def spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5622.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5622,
        )

        return self.__parent__._cast(_5622.SpiralBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5629.StraightBevelDiffGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5629,
        )

        return self.__parent__._cast(
            _5629.StraightBevelDiffGearSetMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5632.StraightBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5632,
        )

        return self.__parent__._cast(
            _5632.StraightBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def zerol_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5653.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5653,
        )

        return self.__parent__._cast(_5653.ZerolBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "BevelGearSetMultibodyDynamicsAnalysis":
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
class BevelGearSetMultibodyDynamicsAnalysis(
    _5509.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
):
    """BevelGearSetMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2579.BevelGearSet":
        """mastapy.system_model.part_model.gears.BevelGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def agma_gleason_conical_gears_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5523.BevelGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_gears_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5523.BevelGearMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelGearsMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5522.BevelGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMeshMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_multibody_dynamics_analysis(
        self: "Self",
    ) -> "List[_5522.BevelGearMeshMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.BevelGearMeshMultibodyDynamicsAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BevelMeshesMultibodyDynamicsAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSetMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetMultibodyDynamicsAnalysis
        """
        return _Cast_BevelGearSetMultibodyDynamicsAnalysis(self)
