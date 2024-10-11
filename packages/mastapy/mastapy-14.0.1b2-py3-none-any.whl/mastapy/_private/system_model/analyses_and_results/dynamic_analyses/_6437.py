"""BevelGearSetDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6425

_BEVEL_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "BevelGearSetDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6419,
        _6432,
        _6435,
        _6436,
        _6453,
        _6481,
        _6502,
        _6521,
        _6524,
        _6530,
        _6533,
        _6551,
    )
    from mastapy._private.system_model.part_model.gears import _2579

    Self = TypeVar("Self", bound="BevelGearSetDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelGearSetDynamicAnalysis._Cast_BevelGearSetDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetDynamicAnalysis:
    """Special nested class for casting BevelGearSetDynamicAnalysis to subclasses."""

    __parent__: "BevelGearSetDynamicAnalysis"

    @property
    def agma_gleason_conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6425.AGMAGleasonConicalGearSetDynamicAnalysis":
        return self.__parent__._cast(_6425.AGMAGleasonConicalGearSetDynamicAnalysis)

    @property
    def conical_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6453.ConicalGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6453,
        )

        return self.__parent__._cast(_6453.ConicalGearSetDynamicAnalysis)

    @property
    def gear_set_dynamic_analysis(self: "CastSelf") -> "_6481.GearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6481,
        )

        return self.__parent__._cast(_6481.GearSetDynamicAnalysis)

    @property
    def specialised_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6521.SpecialisedAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6521,
        )

        return self.__parent__._cast(_6521.SpecialisedAssemblyDynamicAnalysis)

    @property
    def abstract_assembly_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6419.AbstractAssemblyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6419,
        )

        return self.__parent__._cast(_6419.AbstractAssemblyDynamicAnalysis)

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6502.PartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6502,
        )

        return self.__parent__._cast(_6502.PartDynamicAnalysis)

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
    def bevel_differential_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6432.BevelDifferentialGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6432,
        )

        return self.__parent__._cast(_6432.BevelDifferentialGearSetDynamicAnalysis)

    @property
    def spiral_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6524.SpiralBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6524,
        )

        return self.__parent__._cast(_6524.SpiralBevelGearSetDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6530.StraightBevelDiffGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6530,
        )

        return self.__parent__._cast(_6530.StraightBevelDiffGearSetDynamicAnalysis)

    @property
    def straight_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6533.StraightBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6533,
        )

        return self.__parent__._cast(_6533.StraightBevelGearSetDynamicAnalysis)

    @property
    def zerol_bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6551.ZerolBevelGearSetDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6551,
        )

        return self.__parent__._cast(_6551.ZerolBevelGearSetDynamicAnalysis)

    @property
    def bevel_gear_set_dynamic_analysis(
        self: "CastSelf",
    ) -> "BevelGearSetDynamicAnalysis":
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
class BevelGearSetDynamicAnalysis(_6425.AGMAGleasonConicalGearSetDynamicAnalysis):
    """BevelGearSetDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_DYNAMIC_ANALYSIS

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
    def agma_gleason_conical_gears_dynamic_analysis(
        self: "Self",
    ) -> "List[_6435.BevelGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalGearsDynamicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_gears_dynamic_analysis(
        self: "Self",
    ) -> "List[_6435.BevelGearDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearsDynamicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def agma_gleason_conical_meshes_dynamic_analysis(
        self: "Self",
    ) -> "List[_6436.BevelGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AGMAGleasonConicalMeshesDynamicAnalysis"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_meshes_dynamic_analysis(
        self: "Self",
    ) -> "List[_6436.BevelGearMeshDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.BevelGearMeshDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelMeshesDynamicAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSetDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetDynamicAnalysis
        """
        return _Cast_BevelGearSetDynamicAnalysis(self)
