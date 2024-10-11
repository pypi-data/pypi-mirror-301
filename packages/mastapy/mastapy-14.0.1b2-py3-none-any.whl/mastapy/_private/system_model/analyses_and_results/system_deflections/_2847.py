"""GearSetSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.system_deflections import _2895

_GEAR_SET_IMPLEMENTATION_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.Analysis", "GearSetImplementationDetail"
)
_GEAR_SET_MODES = python_net_import("SMT.MastaAPI.Gears", "GearSetModes")
_TASK_PROGRESS = python_net_import("SMT.MastaAPIUtility", "TaskProgress")
_BOOLEAN = python_net_import("System", "Boolean")
_GEAR_SET_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "GearSetSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7731
    from mastapy._private.gears import _341
    from mastapy._private.gears.analysis import _1268, _1271
    from mastapy._private.gears.rating import _376
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4202
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
        _2777,
        _2789,
        _2794,
        _2808,
        _2812,
        _2829,
        _2830,
        _2831,
        _2842,
        _2846,
        _2848,
        _2851,
        _2856,
        _2859,
        _2862,
        _2874,
        _2897,
        _2903,
        _2906,
        _2926,
        _2929,
    )
    from mastapy._private.system_model.part_model.gears import _2591

    Self = TypeVar("Self", bound="GearSetSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetSystemDeflection._Cast_GearSetSystemDeflection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetSystemDeflection:
    """Special nested class for casting GearSetSystemDeflection to subclasses."""

    __parent__: "GearSetSystemDeflection"

    @property
    def specialised_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2895.SpecialisedAssemblySystemDeflection":
        return self.__parent__._cast(_2895.SpecialisedAssemblySystemDeflection)

    @property
    def abstract_assembly_system_deflection(
        self: "CastSelf",
    ) -> "_2772.AbstractAssemblySystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2772,
        )

        return self.__parent__._cast(_2772.AbstractAssemblySystemDeflection)

    @property
    def part_system_deflection(self: "CastSelf") -> "_2874.PartSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2874,
        )

        return self.__parent__._cast(_2874.PartSystemDeflection)

    @property
    def part_fe_analysis(self: "CastSelf") -> "_7719.PartFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7719,
        )

        return self.__parent__._cast(_7719.PartFEAnalysis)

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
    def agma_gleason_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2777.AGMAGleasonConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2777,
        )

        return self.__parent__._cast(_2777.AGMAGleasonConicalGearSetSystemDeflection)

    @property
    def bevel_differential_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2789.BevelDifferentialGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2789,
        )

        return self.__parent__._cast(_2789.BevelDifferentialGearSetSystemDeflection)

    @property
    def bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2794.BevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2794,
        )

        return self.__parent__._cast(_2794.BevelGearSetSystemDeflection)

    @property
    def concept_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2808.ConceptGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2808,
        )

        return self.__parent__._cast(_2808.ConceptGearSetSystemDeflection)

    @property
    def conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2812.ConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2812,
        )

        return self.__parent__._cast(_2812.ConicalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2829.CylindricalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2829,
        )

        return self.__parent__._cast(_2829.CylindricalGearSetSystemDeflection)

    @property
    def cylindrical_gear_set_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2830.CylindricalGearSetSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2830,
        )

        return self.__parent__._cast(_2830.CylindricalGearSetSystemDeflectionTimestep)

    @property
    def cylindrical_gear_set_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2831.CylindricalGearSetSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2831,
        )

        return self.__parent__._cast(
            _2831.CylindricalGearSetSystemDeflectionWithLTCAResults
        )

    @property
    def face_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2842.FaceGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2842,
        )

        return self.__parent__._cast(_2842.FaceGearSetSystemDeflection)

    @property
    def hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2851.HypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2851,
        )

        return self.__parent__._cast(_2851.HypoidGearSetSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2856.KlingelnbergCycloPalloidConicalGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2856,
        )

        return self.__parent__._cast(
            _2856.KlingelnbergCycloPalloidConicalGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2859.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2859,
        )

        return self.__parent__._cast(
            _2859.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2862.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2862,
        )

        return self.__parent__._cast(
            _2862.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection
        )

    @property
    def spiral_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2897.SpiralBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2897,
        )

        return self.__parent__._cast(_2897.SpiralBevelGearSetSystemDeflection)

    @property
    def straight_bevel_diff_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2903.StraightBevelDiffGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2903,
        )

        return self.__parent__._cast(_2903.StraightBevelDiffGearSetSystemDeflection)

    @property
    def straight_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2906.StraightBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2906,
        )

        return self.__parent__._cast(_2906.StraightBevelGearSetSystemDeflection)

    @property
    def worm_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2926.WormGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2926,
        )

        return self.__parent__._cast(_2926.WormGearSetSystemDeflection)

    @property
    def zerol_bevel_gear_set_system_deflection(
        self: "CastSelf",
    ) -> "_2929.ZerolBevelGearSetSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2929,
        )

        return self.__parent__._cast(_2929.ZerolBevelGearSetSystemDeflection)

    @property
    def gear_set_system_deflection(self: "CastSelf") -> "GearSetSystemDeflection":
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
class GearSetSystemDeflection(_2895.SpecialisedAssemblySystemDeflection):
    """GearSetSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2591.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def rating(self: "Self") -> "_376.GearSetRating":
        """mastapy.gears.rating.GearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_system_deflection(self: "Self") -> "List[_2848.GearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_system_deflection(
        self: "Self",
    ) -> "List[_2846.GearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.GearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesSystemDeflection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_flow_results(self: "Self") -> "_4202.GearSetPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @enforce_parameter_types
    def analysis_for(
        self: "Self",
        gear_set_imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
    ) -> "_1268.GearSetImplementationAnalysis":
        """mastapy.gears.analysis.GearSetImplementationAnalysis

        Args:
            gear_set_imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "AnalysisFor",
            gear_set_imp_detail.wrapped if gear_set_imp_detail else None,
            gear_set_mode,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @enforce_parameter_types
    def implementation_detail_results_failed_for(
        self: "Self",
        gear_set_imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
    ) -> "bool":
        """bool

        Args:
            gear_set_imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "ImplementationDetailResultsFailedFor",
            gear_set_imp_detail.wrapped if gear_set_imp_detail else None,
            gear_set_mode,
        )
        return method_result

    @enforce_parameter_types
    def perform_implementation_detail_analysis_with_progress(
        self: "Self",
        imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
        progress: "_7731.TaskProgress",
        run_all_planetary_meshes: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
            progress (mastapy.TaskProgress)
            run_all_planetary_meshes (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [
                _GEAR_SET_IMPLEMENTATION_DETAIL,
                _GEAR_SET_MODES,
                _TASK_PROGRESS,
                _BOOLEAN,
            ],
            imp_detail.wrapped if imp_detail else None,
            gear_set_mode,
            progress.wrapped if progress else None,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @enforce_parameter_types
    def perform_implementation_detail_analysis(
        self: "Self",
        imp_detail: "_1271.GearSetImplementationDetail",
        gear_set_mode: "_341.GearSetModes",
        run_all_planetary_meshes: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            imp_detail (mastapy.gears.analysis.GearSetImplementationDetail)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [_GEAR_SET_IMPLEMENTATION_DETAIL, _GEAR_SET_MODES, _BOOLEAN],
            imp_detail.wrapped if imp_detail else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GearSetSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_GearSetSystemDeflection
        """
        return _Cast_GearSetSystemDeflection(self)
