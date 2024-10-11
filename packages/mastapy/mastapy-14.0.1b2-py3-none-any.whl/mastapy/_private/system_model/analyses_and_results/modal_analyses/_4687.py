"""AbstractAssemblyModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4779

_ABSTRACT_ASSEMBLY_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "AbstractAssemblyModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4693,
        _4694,
        _4697,
        _4700,
        _4705,
        _4706,
        _4710,
        _4712,
        _4715,
        _4718,
        _4721,
        _4727,
        _4729,
        _4731,
        _4737,
        _4746,
        _4748,
        _4750,
        _4752,
        _4756,
        _4760,
        _4763,
        _4766,
        _4769,
        _4782,
        _4784,
        _4791,
        _4794,
        _4799,
        _4802,
        _4805,
        _4808,
        _4811,
        _4815,
        _4819,
        _4829,
        _4832,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2772,
    )
    from mastapy._private.system_model.part_model import _2490

    Self = TypeVar("Self", bound="AbstractAssemblyModalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyModalAnalysis._Cast_AbstractAssemblyModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyModalAnalysis:
    """Special nested class for casting AbstractAssemblyModalAnalysis to subclasses."""

    __parent__: "AbstractAssemblyModalAnalysis"

    @property
    def part_modal_analysis(self: "CastSelf") -> "_4779.PartModalAnalysis":
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
    def assembly_modal_analysis(self: "CastSelf") -> "_4694.AssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4694,
        )

        return self.__parent__._cast(_4694.AssemblyModalAnalysis)

    @property
    def belt_drive_modal_analysis(self: "CastSelf") -> "_4697.BeltDriveModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4697,
        )

        return self.__parent__._cast(_4697.BeltDriveModalAnalysis)

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
    def bolted_joint_modal_analysis(
        self: "CastSelf",
    ) -> "_4706.BoltedJointModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4706,
        )

        return self.__parent__._cast(_4706.BoltedJointModalAnalysis)

    @property
    def clutch_modal_analysis(self: "CastSelf") -> "_4710.ClutchModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4710,
        )

        return self.__parent__._cast(_4710.ClutchModalAnalysis)

    @property
    def concept_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4715.ConceptCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4715,
        )

        return self.__parent__._cast(_4715.ConceptCouplingModalAnalysis)

    @property
    def concept_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4718.ConceptGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4718,
        )

        return self.__parent__._cast(_4718.ConceptGearSetModalAnalysis)

    @property
    def conical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4721.ConicalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4721,
        )

        return self.__parent__._cast(_4721.ConicalGearSetModalAnalysis)

    @property
    def coupling_modal_analysis(self: "CastSelf") -> "_4727.CouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4727,
        )

        return self.__parent__._cast(_4727.CouplingModalAnalysis)

    @property
    def cvt_modal_analysis(self: "CastSelf") -> "_4729.CVTModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4729,
        )

        return self.__parent__._cast(_4729.CVTModalAnalysis)

    @property
    def cycloidal_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4731.CycloidalAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4731,
        )

        return self.__parent__._cast(_4731.CycloidalAssemblyModalAnalysis)

    @property
    def cylindrical_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4737.CylindricalGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4737,
        )

        return self.__parent__._cast(_4737.CylindricalGearSetModalAnalysis)

    @property
    def face_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4746.FaceGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4746,
        )

        return self.__parent__._cast(_4746.FaceGearSetModalAnalysis)

    @property
    def flexible_pin_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4748.FlexiblePinAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4748,
        )

        return self.__parent__._cast(_4748.FlexiblePinAssemblyModalAnalysis)

    @property
    def gear_set_modal_analysis(self: "CastSelf") -> "_4752.GearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4752,
        )

        return self.__parent__._cast(_4752.GearSetModalAnalysis)

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
    def microphone_array_modal_analysis(
        self: "CastSelf",
    ) -> "_4769.MicrophoneArrayModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4769,
        )

        return self.__parent__._cast(_4769.MicrophoneArrayModalAnalysis)

    @property
    def part_to_part_shear_coupling_modal_analysis(
        self: "CastSelf",
    ) -> "_4782.PartToPartShearCouplingModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4782,
        )

        return self.__parent__._cast(_4782.PartToPartShearCouplingModalAnalysis)

    @property
    def planetary_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4784.PlanetaryGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4784,
        )

        return self.__parent__._cast(_4784.PlanetaryGearSetModalAnalysis)

    @property
    def rolling_ring_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4791.RollingRingAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4791,
        )

        return self.__parent__._cast(_4791.RollingRingAssemblyModalAnalysis)

    @property
    def root_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4794.RootAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4794,
        )

        return self.__parent__._cast(_4794.RootAssemblyModalAnalysis)

    @property
    def specialised_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "_4799.SpecialisedAssemblyModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4799,
        )

        return self.__parent__._cast(_4799.SpecialisedAssemblyModalAnalysis)

    @property
    def spiral_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4802.SpiralBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4802,
        )

        return self.__parent__._cast(_4802.SpiralBevelGearSetModalAnalysis)

    @property
    def spring_damper_modal_analysis(
        self: "CastSelf",
    ) -> "_4805.SpringDamperModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4805,
        )

        return self.__parent__._cast(_4805.SpringDamperModalAnalysis)

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
    def synchroniser_modal_analysis(
        self: "CastSelf",
    ) -> "_4815.SynchroniserModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4815,
        )

        return self.__parent__._cast(_4815.SynchroniserModalAnalysis)

    @property
    def torque_converter_modal_analysis(
        self: "CastSelf",
    ) -> "_4819.TorqueConverterModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4819,
        )

        return self.__parent__._cast(_4819.TorqueConverterModalAnalysis)

    @property
    def worm_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4829.WormGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4829,
        )

        return self.__parent__._cast(_4829.WormGearSetModalAnalysis)

    @property
    def zerol_bevel_gear_set_modal_analysis(
        self: "CastSelf",
    ) -> "_4832.ZerolBevelGearSetModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4832,
        )

        return self.__parent__._cast(_4832.ZerolBevelGearSetModalAnalysis)

    @property
    def abstract_assembly_modal_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyModalAnalysis":
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
class AbstractAssemblyModalAnalysis(_4779.PartModalAnalysis):
    """AbstractAssemblyModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_MODAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2490.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2490.AbstractAssembly":
        """mastapy.system_model.part_model.AbstractAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def gear_meshes(self: "Self") -> "List[_4750.GearMeshModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.GearMeshModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rigidly_connected_groups(self: "Self") -> "List[_4712.ComponentModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.ComponentModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidlyConnectedGroups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def system_deflection_results(
        self: "Self",
    ) -> "_2772.AbstractAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.AbstractAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyModalAnalysis
        """
        return _Cast_AbstractAssemblyModalAnalysis(self)
