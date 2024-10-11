"""ConicalGearSetModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4752

_CONICAL_GEAR_SET_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ConicalGearSetModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4687,
        _4693,
        _4700,
        _4705,
        _4719,
        _4720,
        _4756,
        _4760,
        _4763,
        _4766,
        _4779,
        _4799,
        _4802,
        _4808,
        _4811,
        _4832,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2812,
    )
    from mastapy._private.system_model.part_model.gears import _2583

    Self = TypeVar("Self", bound="ConicalGearSetModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearSetModalAnalysis._Cast_ConicalGearSetModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearSetModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearSetModalAnalysis:
    """Special nested class for casting ConicalGearSetModalAnalysis to subclasses."""

    __parent__: "ConicalGearSetModalAnalysis"

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4752.GearSetModalAnalysis":
        return self.__parent__._cast(_4752.GearSetModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4799.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4799,
        )

        return self.__parent__._cast(_4799.SpecialisedAssemblyModalAnalysis)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4687.AbstractAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4687,
        )

        return self.__parent__._cast(_4687.AbstractAssemblyModalAnalysis)

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4779.PartModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4779,
        )

        return self.__parent__._cast(_4779.PartModalAnalysis)

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
    def agma_gleason_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4693.AGMAGleasonConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4693,
        )

        return self.__parent__._cast(_4693.AGMAGleasonConicalGearSetModalAnalysis)

    @property
    def bevel_differential_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4700.BevelDifferentialGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4700,
        )

        return self.__parent__._cast(_4700.BevelDifferentialGearSetModalAnalysis)

    @property
    def bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4705.BevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4705,
        )

        return self.__parent__._cast(_4705.BevelGearSetModalAnalysis)

    @property
    def hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4756.HypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4756,
        )

        return self.__parent__._cast(_4756.HypoidGearSetModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4760,
        )

        return self.__parent__._cast(
            _4760.KlingelnbergCycloPalloidConicalGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4763,
        )

        return self.__parent__._cast(
            _4763.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4766,
        )

        return self.__parent__._cast(
            _4766.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis
        )

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpiralBevelGearSetModalAnalysis)

    @property
    def straight_bevel_diff_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4808.StraightBevelDiffGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4808,
        )

        return self.__parent__._cast(_4808.StraightBevelDiffGearSetModalAnalysis)

    @property
    def straight_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4811.StraightBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4811,
        )

        return self.__parent__._cast(_4811.StraightBevelGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4832.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4832,
        )

        return self.__parent__._cast(_4832.ZerolBevelGearSetModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "ConicalGearSetModalAnalysis":
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
class ConicalGearSetModalAnalysis(_4752.GearSetModalAnalysis):
    """ConicalGearSetModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_SET_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def assembly_design(self: "Self") -> "_2583.ConicalGearSet":
        """mastapy.system_model.part_model.gears.ConicalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gears_modal_analysis(self: "Self") -> "List[_4720.ConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearsModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_gears_modal_analysis(
        self: "Self",
    ) -> "List[_4720.ConicalGearModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearsModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def meshes_modal_analysis(
        self: "Self",
    ) -> "List[_4719.ConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshesModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def conical_meshes_modal_analysis(
        self: "Self",
    ) -> "List[_4719.ConicalGearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ConicalGearMeshModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalMeshesModalAnalysis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2812.ConicalGearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.ConicalGearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearSetModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearSetModalAnalysis
        """
        return _Cast_ConicalGearSetModalAnalysis(self)
