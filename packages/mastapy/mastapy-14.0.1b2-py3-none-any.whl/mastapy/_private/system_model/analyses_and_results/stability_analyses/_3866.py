"""AbstractAssemblyStabilityAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.stability_analyses import _3949

_ABSTRACT_ASSEMBLY_STABILITY_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses",
    "AbstractAssemblyStabilityAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.stability_analyses import (
        _3871,
        _3873,
        _3876,
        _3878,
        _3883,
        _3885,
        _3889,
        _3894,
        _3896,
        _3899,
        _3905,
        _3909,
        _3910,
        _3915,
        _3922,
        _3925,
        _3927,
        _3931,
        _3935,
        _3938,
        _3941,
        _3945,
        _3952,
        _3954,
        _3961,
        _3964,
        _3968,
        _3970,
        _3974,
        _3979,
        _3982,
        _3989,
        _3992,
        _3997,
        _4000,
    )
    from mastapy._private.system_model.part_model import _2490

    Self = TypeVar("Self", bound="AbstractAssemblyStabilityAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractAssemblyStabilityAnalysis._Cast_AbstractAssemblyStabilityAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyStabilityAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyStabilityAnalysis:
    """Special nested class for casting AbstractAssemblyStabilityAnalysis to subclasses."""

    __parent__: "AbstractAssemblyStabilityAnalysis"

    @property
    def part_stability_analysis(self: "CastSelf") -> "_3949.PartStabilityAnalysis":
        return self.__parent__._cast(_3949.PartStabilityAnalysis)

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
    def agma_gleason_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3871.AGMAGleasonConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3871,
        )

        return self.__parent__._cast(_3871.AGMAGleasonConicalGearSetStabilityAnalysis)

    @property
    def assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3873.AssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3873,
        )

        return self.__parent__._cast(_3873.AssemblyStabilityAnalysis)

    @property
    def belt_drive_stability_analysis(
        self: "CastSelf",
    ) -> "_3876.BeltDriveStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3876,
        )

        return self.__parent__._cast(_3876.BeltDriveStabilityAnalysis)

    @property
    def bevel_differential_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3878.BevelDifferentialGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3878,
        )

        return self.__parent__._cast(_3878.BevelDifferentialGearSetStabilityAnalysis)

    @property
    def bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3883.BevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3883,
        )

        return self.__parent__._cast(_3883.BevelGearSetStabilityAnalysis)

    @property
    def bolted_joint_stability_analysis(
        self: "CastSelf",
    ) -> "_3885.BoltedJointStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3885,
        )

        return self.__parent__._cast(_3885.BoltedJointStabilityAnalysis)

    @property
    def clutch_stability_analysis(self: "CastSelf") -> "_3889.ClutchStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3889,
        )

        return self.__parent__._cast(_3889.ClutchStabilityAnalysis)

    @property
    def concept_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3894.ConceptCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3894,
        )

        return self.__parent__._cast(_3894.ConceptCouplingStabilityAnalysis)

    @property
    def concept_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3896.ConceptGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3896,
        )

        return self.__parent__._cast(_3896.ConceptGearSetStabilityAnalysis)

    @property
    def conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3899.ConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3899,
        )

        return self.__parent__._cast(_3899.ConicalGearSetStabilityAnalysis)

    @property
    def coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3905.CouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3905,
        )

        return self.__parent__._cast(_3905.CouplingStabilityAnalysis)

    @property
    def cvt_stability_analysis(self: "CastSelf") -> "_3909.CVTStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3909,
        )

        return self.__parent__._cast(_3909.CVTStabilityAnalysis)

    @property
    def cycloidal_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3910.CycloidalAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3910,
        )

        return self.__parent__._cast(_3910.CycloidalAssemblyStabilityAnalysis)

    @property
    def cylindrical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3915.CylindricalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3915,
        )

        return self.__parent__._cast(_3915.CylindricalGearSetStabilityAnalysis)

    @property
    def face_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3922.FaceGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3922,
        )

        return self.__parent__._cast(_3922.FaceGearSetStabilityAnalysis)

    @property
    def flexible_pin_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3925.FlexiblePinAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3925,
        )

        return self.__parent__._cast(_3925.FlexiblePinAssemblyStabilityAnalysis)

    @property
    def gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3927.GearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3927,
        )

        return self.__parent__._cast(_3927.GearSetStabilityAnalysis)

    @property
    def hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3931.HypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3931,
        )

        return self.__parent__._cast(_3931.HypoidGearSetStabilityAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3935.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3935,
        )

        return self.__parent__._cast(
            _3935.KlingelnbergCycloPalloidConicalGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3938.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3938,
        )

        return self.__parent__._cast(
            _3938.KlingelnbergCycloPalloidHypoidGearSetStabilityAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3941.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3941,
        )

        return self.__parent__._cast(
            _3941.KlingelnbergCycloPalloidSpiralBevelGearSetStabilityAnalysis
        )

    @property
    def microphone_array_stability_analysis(
        self: "CastSelf",
    ) -> "_3945.MicrophoneArrayStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3945,
        )

        return self.__parent__._cast(_3945.MicrophoneArrayStabilityAnalysis)

    @property
    def part_to_part_shear_coupling_stability_analysis(
        self: "CastSelf",
    ) -> "_3952.PartToPartShearCouplingStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3952,
        )

        return self.__parent__._cast(_3952.PartToPartShearCouplingStabilityAnalysis)

    @property
    def planetary_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3954.PlanetaryGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3954,
        )

        return self.__parent__._cast(_3954.PlanetaryGearSetStabilityAnalysis)

    @property
    def rolling_ring_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3961.RollingRingAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3961,
        )

        return self.__parent__._cast(_3961.RollingRingAssemblyStabilityAnalysis)

    @property
    def root_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3964.RootAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3964,
        )

        return self.__parent__._cast(_3964.RootAssemblyStabilityAnalysis)

    @property
    def specialised_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "_3968.SpecialisedAssemblyStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3968,
        )

        return self.__parent__._cast(_3968.SpecialisedAssemblyStabilityAnalysis)

    @property
    def spiral_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3970.SpiralBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3970,
        )

        return self.__parent__._cast(_3970.SpiralBevelGearSetStabilityAnalysis)

    @property
    def spring_damper_stability_analysis(
        self: "CastSelf",
    ) -> "_3974.SpringDamperStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3974,
        )

        return self.__parent__._cast(_3974.SpringDamperStabilityAnalysis)

    @property
    def straight_bevel_diff_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3979.StraightBevelDiffGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3979,
        )

        return self.__parent__._cast(_3979.StraightBevelDiffGearSetStabilityAnalysis)

    @property
    def straight_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3982.StraightBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3982,
        )

        return self.__parent__._cast(_3982.StraightBevelGearSetStabilityAnalysis)

    @property
    def synchroniser_stability_analysis(
        self: "CastSelf",
    ) -> "_3989.SynchroniserStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3989,
        )

        return self.__parent__._cast(_3989.SynchroniserStabilityAnalysis)

    @property
    def torque_converter_stability_analysis(
        self: "CastSelf",
    ) -> "_3992.TorqueConverterStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3992,
        )

        return self.__parent__._cast(_3992.TorqueConverterStabilityAnalysis)

    @property
    def worm_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_3997.WormGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _3997,
        )

        return self.__parent__._cast(_3997.WormGearSetStabilityAnalysis)

    @property
    def zerol_bevel_gear_set_stability_analysis(
        self: "CastSelf",
    ) -> "_4000.ZerolBevelGearSetStabilityAnalysis":
        from mastapy._private.system_model.analyses_and_results.stability_analyses import (
            _4000,
        )

        return self.__parent__._cast(_4000.ZerolBevelGearSetStabilityAnalysis)

    @property
    def abstract_assembly_stability_analysis(
        self: "CastSelf",
    ) -> "AbstractAssemblyStabilityAnalysis":
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
class AbstractAssemblyStabilityAnalysis(_3949.PartStabilityAnalysis):
    """AbstractAssemblyStabilityAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_STABILITY_ANALYSIS

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
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyStabilityAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyStabilityAnalysis
        """
        return _Cast_AbstractAssemblyStabilityAnalysis(self)
