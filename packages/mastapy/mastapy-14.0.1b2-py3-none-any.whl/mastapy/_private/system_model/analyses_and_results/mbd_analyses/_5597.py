"""PartMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7721

_PART_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "PartMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility.convergence import _1624
    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5503,
        _5504,
        _5505,
        _5508,
        _5509,
        _5511,
        _5513,
        _5516,
        _5518,
        _5519,
        _5520,
        _5521,
        _5523,
        _5524,
        _5525,
        _5526,
        _5528,
        _5529,
        _5532,
        _5534,
        _5535,
        _5537,
        _5538,
        _5540,
        _5541,
        _5543,
        _5545,
        _5546,
        _5548,
        _5549,
        _5550,
        _5552,
        _5555,
        _5556,
        _5557,
        _5558,
        _5559,
        _5561,
        _5562,
        _5563,
        _5564,
        _5567,
        _5568,
        _5569,
        _5571,
        _5572,
        _5579,
        _5580,
        _5582,
        _5583,
        _5585,
        _5586,
        _5587,
        _5591,
        _5592,
        _5593,
        _5594,
        _5595,
        _5596,
        _5599,
        _5600,
        _5602,
        _5603,
        _5604,
        _5605,
        _5606,
        _5607,
        _5609,
        _5611,
        _5612,
        _5615,
        _5616,
        _5619,
        _5621,
        _5622,
        _5625,
        _5626,
        _5628,
        _5629,
        _5631,
        _5632,
        _5633,
        _5634,
        _5635,
        _5636,
        _5637,
        _5638,
        _5641,
        _5642,
        _5644,
        _5645,
        _5646,
        _5649,
        _5650,
        _5652,
        _5653,
    )
    from mastapy._private.system_model.drawing import _2305
    from mastapy._private.system_model.part_model import _2526

    Self = TypeVar("Self", bound="PartMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartMultibodyDynamicsAnalysis._Cast_PartMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartMultibodyDynamicsAnalysis:
    """Special nested class for casting PartMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "PartMultibodyDynamicsAnalysis"

    @property
    def part_time_series_load_analysis_case(
        self: "CastSelf",
    ) -> "_7721.PartTimeSeriesLoadAnalysisCase":
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
    def abstract_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5503.AbstractAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5503,
        )

        return self.__parent__._cast(_5503.AbstractAssemblyMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5504.AbstractShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5504,
        )

        return self.__parent__._cast(_5504.AbstractShaftMultibodyDynamicsAnalysis)

    @property
    def abstract_shaft_or_housing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5505.AbstractShaftOrHousingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5505,
        )

        return self.__parent__._cast(
            _5505.AbstractShaftOrHousingMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5508.AGMAGleasonConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5508,
        )

        return self.__parent__._cast(
            _5508.AGMAGleasonConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def agma_gleason_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5509.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5509,
        )

        return self.__parent__._cast(
            _5509.AGMAGleasonConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5511.AssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5511,
        )

        return self.__parent__._cast(_5511.AssemblyMultibodyDynamicsAnalysis)

    @property
    def bearing_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5513.BearingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5513,
        )

        return self.__parent__._cast(_5513.BearingMultibodyDynamicsAnalysis)

    @property
    def belt_drive_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5516.BeltDriveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5516,
        )

        return self.__parent__._cast(_5516.BeltDriveMultibodyDynamicsAnalysis)

    @property
    def bevel_differential_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5518.BevelDifferentialGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5518,
        )

        return self.__parent__._cast(
            _5518.BevelDifferentialGearMultibodyDynamicsAnalysis
        )

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
    def bevel_differential_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5520.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5520,
        )

        return self.__parent__._cast(
            _5520.BevelDifferentialPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_differential_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5521.BevelDifferentialSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5521,
        )

        return self.__parent__._cast(
            _5521.BevelDifferentialSunGearMultibodyDynamicsAnalysis
        )

    @property
    def bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5523.BevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5523,
        )

        return self.__parent__._cast(_5523.BevelGearMultibodyDynamicsAnalysis)

    @property
    def bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5524.BevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5524,
        )

        return self.__parent__._cast(_5524.BevelGearSetMultibodyDynamicsAnalysis)

    @property
    def bolted_joint_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5525.BoltedJointMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5525,
        )

        return self.__parent__._cast(_5525.BoltedJointMultibodyDynamicsAnalysis)

    @property
    def bolt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5526.BoltMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5526,
        )

        return self.__parent__._cast(_5526.BoltMultibodyDynamicsAnalysis)

    @property
    def clutch_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5528.ClutchHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5528,
        )

        return self.__parent__._cast(_5528.ClutchHalfMultibodyDynamicsAnalysis)

    @property
    def clutch_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5529.ClutchMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5529,
        )

        return self.__parent__._cast(_5529.ClutchMultibodyDynamicsAnalysis)

    @property
    def component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5532.ComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5532,
        )

        return self.__parent__._cast(_5532.ComponentMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5534.ConceptCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5534,
        )

        return self.__parent__._cast(_5534.ConceptCouplingHalfMultibodyDynamicsAnalysis)

    @property
    def concept_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5535.ConceptCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5535,
        )

        return self.__parent__._cast(_5535.ConceptCouplingMultibodyDynamicsAnalysis)

    @property
    def concept_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5537.ConceptGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5537,
        )

        return self.__parent__._cast(_5537.ConceptGearMultibodyDynamicsAnalysis)

    @property
    def concept_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5538.ConceptGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5538,
        )

        return self.__parent__._cast(_5538.ConceptGearSetMultibodyDynamicsAnalysis)

    @property
    def conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5540.ConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5540,
        )

        return self.__parent__._cast(_5540.ConicalGearMultibodyDynamicsAnalysis)

    @property
    def conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5541.ConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5541,
        )

        return self.__parent__._cast(_5541.ConicalGearSetMultibodyDynamicsAnalysis)

    @property
    def connector_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5543.ConnectorMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5543,
        )

        return self.__parent__._cast(_5543.ConnectorMultibodyDynamicsAnalysis)

    @property
    def coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5545.CouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5545,
        )

        return self.__parent__._cast(_5545.CouplingHalfMultibodyDynamicsAnalysis)

    @property
    def coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5546.CouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5546,
        )

        return self.__parent__._cast(_5546.CouplingMultibodyDynamicsAnalysis)

    @property
    def cvt_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5548.CVTMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5548,
        )

        return self.__parent__._cast(_5548.CVTMultibodyDynamicsAnalysis)

    @property
    def cvt_pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5549.CVTPulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5549,
        )

        return self.__parent__._cast(_5549.CVTPulleyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5550.CycloidalAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5550,
        )

        return self.__parent__._cast(_5550.CycloidalAssemblyMultibodyDynamicsAnalysis)

    @property
    def cycloidal_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5552.CycloidalDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5552,
        )

        return self.__parent__._cast(_5552.CycloidalDiscMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5555.CylindricalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5555,
        )

        return self.__parent__._cast(_5555.CylindricalGearMultibodyDynamicsAnalysis)

    @property
    def cylindrical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5556.CylindricalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5556,
        )

        return self.__parent__._cast(_5556.CylindricalGearSetMultibodyDynamicsAnalysis)

    @property
    def cylindrical_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5557.CylindricalPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5557,
        )

        return self.__parent__._cast(
            _5557.CylindricalPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def datum_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5558.DatumMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5558,
        )

        return self.__parent__._cast(_5558.DatumMultibodyDynamicsAnalysis)

    @property
    def external_cad_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5559.ExternalCADModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5559,
        )

        return self.__parent__._cast(_5559.ExternalCADModelMultibodyDynamicsAnalysis)

    @property
    def face_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5561.FaceGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5561,
        )

        return self.__parent__._cast(_5561.FaceGearMultibodyDynamicsAnalysis)

    @property
    def face_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5562.FaceGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5562,
        )

        return self.__parent__._cast(_5562.FaceGearSetMultibodyDynamicsAnalysis)

    @property
    def fe_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5563.FEPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5563,
        )

        return self.__parent__._cast(_5563.FEPartMultibodyDynamicsAnalysis)

    @property
    def flexible_pin_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5564.FlexiblePinAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5564,
        )

        return self.__parent__._cast(_5564.FlexiblePinAssemblyMultibodyDynamicsAnalysis)

    @property
    def gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5567.GearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5567,
        )

        return self.__parent__._cast(_5567.GearMultibodyDynamicsAnalysis)

    @property
    def gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5568.GearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5568,
        )

        return self.__parent__._cast(_5568.GearSetMultibodyDynamicsAnalysis)

    @property
    def guide_dxf_model_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5569.GuideDxfModelMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5569,
        )

        return self.__parent__._cast(_5569.GuideDxfModelMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5571.HypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5571,
        )

        return self.__parent__._cast(_5571.HypoidGearMultibodyDynamicsAnalysis)

    @property
    def hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5572.HypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5572,
        )

        return self.__parent__._cast(_5572.HypoidGearSetMultibodyDynamicsAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5579.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5579,
        )

        return self.__parent__._cast(
            _5579.KlingelnbergCycloPalloidConicalGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5580.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5580,
        )

        return self.__parent__._cast(
            _5580.KlingelnbergCycloPalloidConicalGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5582.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5582,
        )

        return self.__parent__._cast(
            _5582.KlingelnbergCycloPalloidHypoidGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5583.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5583,
        )

        return self.__parent__._cast(
            _5583.KlingelnbergCycloPalloidHypoidGearSetMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5585.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5585,
        )

        return self.__parent__._cast(
            _5585.KlingelnbergCycloPalloidSpiralBevelGearMultibodyDynamicsAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5586.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5586,
        )

        return self.__parent__._cast(
            _5586.KlingelnbergCycloPalloidSpiralBevelGearSetMultibodyDynamicsAnalysis
        )

    @property
    def mass_disc_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5587.MassDiscMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5587,
        )

        return self.__parent__._cast(_5587.MassDiscMultibodyDynamicsAnalysis)

    @property
    def measurement_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5591.MeasurementComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5591,
        )

        return self.__parent__._cast(
            _5591.MeasurementComponentMultibodyDynamicsAnalysis
        )

    @property
    def microphone_array_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5592.MicrophoneArrayMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5592,
        )

        return self.__parent__._cast(_5592.MicrophoneArrayMultibodyDynamicsAnalysis)

    @property
    def microphone_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5593.MicrophoneMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5593,
        )

        return self.__parent__._cast(_5593.MicrophoneMultibodyDynamicsAnalysis)

    @property
    def mountable_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5594.MountableComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5594,
        )

        return self.__parent__._cast(_5594.MountableComponentMultibodyDynamicsAnalysis)

    @property
    def oil_seal_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5596.OilSealMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5596,
        )

        return self.__parent__._cast(_5596.OilSealMultibodyDynamicsAnalysis)

    @property
    def part_to_part_shear_coupling_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5599.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5599,
        )

        return self.__parent__._cast(
            _5599.PartToPartShearCouplingHalfMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5600.PartToPartShearCouplingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5600,
        )

        return self.__parent__._cast(
            _5600.PartToPartShearCouplingMultibodyDynamicsAnalysis
        )

    @property
    def planetary_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5602.PlanetaryGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5602,
        )

        return self.__parent__._cast(_5602.PlanetaryGearSetMultibodyDynamicsAnalysis)

    @property
    def planet_carrier_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5603.PlanetCarrierMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5603,
        )

        return self.__parent__._cast(_5603.PlanetCarrierMultibodyDynamicsAnalysis)

    @property
    def point_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5604.PointLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5604,
        )

        return self.__parent__._cast(_5604.PointLoadMultibodyDynamicsAnalysis)

    @property
    def power_load_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5605.PowerLoadMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5605,
        )

        return self.__parent__._cast(_5605.PowerLoadMultibodyDynamicsAnalysis)

    @property
    def pulley_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5606.PulleyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5606,
        )

        return self.__parent__._cast(_5606.PulleyMultibodyDynamicsAnalysis)

    @property
    def ring_pins_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5607.RingPinsMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5607,
        )

        return self.__parent__._cast(_5607.RingPinsMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5609.RollingRingAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5609,
        )

        return self.__parent__._cast(_5609.RollingRingAssemblyMultibodyDynamicsAnalysis)

    @property
    def rolling_ring_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5611.RollingRingMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5611,
        )

        return self.__parent__._cast(_5611.RollingRingMultibodyDynamicsAnalysis)

    @property
    def root_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5612.RootAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5612,
        )

        return self.__parent__._cast(_5612.RootAssemblyMultibodyDynamicsAnalysis)

    @property
    def shaft_hub_connection_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5615.ShaftHubConnectionMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5615,
        )

        return self.__parent__._cast(_5615.ShaftHubConnectionMultibodyDynamicsAnalysis)

    @property
    def shaft_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5616.ShaftMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5616,
        )

        return self.__parent__._cast(_5616.ShaftMultibodyDynamicsAnalysis)

    @property
    def specialised_assembly_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5619.SpecialisedAssemblyMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5619,
        )

        return self.__parent__._cast(_5619.SpecialisedAssemblyMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5621.SpiralBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5621,
        )

        return self.__parent__._cast(_5621.SpiralBevelGearMultibodyDynamicsAnalysis)

    @property
    def spiral_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5622.SpiralBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5622,
        )

        return self.__parent__._cast(_5622.SpiralBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def spring_damper_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5625.SpringDamperHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5625,
        )

        return self.__parent__._cast(_5625.SpringDamperHalfMultibodyDynamicsAnalysis)

    @property
    def spring_damper_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5626.SpringDamperMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5626,
        )

        return self.__parent__._cast(_5626.SpringDamperMultibodyDynamicsAnalysis)

    @property
    def straight_bevel_diff_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5628.StraightBevelDiffGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5628,
        )

        return self.__parent__._cast(
            _5628.StraightBevelDiffGearMultibodyDynamicsAnalysis
        )

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
    def straight_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5631.StraightBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5631,
        )

        return self.__parent__._cast(_5631.StraightBevelGearMultibodyDynamicsAnalysis)

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
    def straight_bevel_planet_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5633.StraightBevelPlanetGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5633,
        )

        return self.__parent__._cast(
            _5633.StraightBevelPlanetGearMultibodyDynamicsAnalysis
        )

    @property
    def straight_bevel_sun_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5634.StraightBevelSunGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5634,
        )

        return self.__parent__._cast(
            _5634.StraightBevelSunGearMultibodyDynamicsAnalysis
        )

    @property
    def synchroniser_half_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5635.SynchroniserHalfMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5635,
        )

        return self.__parent__._cast(_5635.SynchroniserHalfMultibodyDynamicsAnalysis)

    @property
    def synchroniser_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5636.SynchroniserMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5636,
        )

        return self.__parent__._cast(_5636.SynchroniserMultibodyDynamicsAnalysis)

    @property
    def synchroniser_part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5637.SynchroniserPartMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5637,
        )

        return self.__parent__._cast(_5637.SynchroniserPartMultibodyDynamicsAnalysis)

    @property
    def synchroniser_sleeve_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5638.SynchroniserSleeveMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5638,
        )

        return self.__parent__._cast(_5638.SynchroniserSleeveMultibodyDynamicsAnalysis)

    @property
    def torque_converter_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5641.TorqueConverterMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5641,
        )

        return self.__parent__._cast(_5641.TorqueConverterMultibodyDynamicsAnalysis)

    @property
    def torque_converter_pump_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5642.TorqueConverterPumpMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5642,
        )

        return self.__parent__._cast(_5642.TorqueConverterPumpMultibodyDynamicsAnalysis)

    @property
    def torque_converter_turbine_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5644.TorqueConverterTurbineMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5644,
        )

        return self.__parent__._cast(
            _5644.TorqueConverterTurbineMultibodyDynamicsAnalysis
        )

    @property
    def unbalanced_mass_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5645.UnbalancedMassMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5645,
        )

        return self.__parent__._cast(_5645.UnbalancedMassMultibodyDynamicsAnalysis)

    @property
    def virtual_component_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5646.VirtualComponentMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5646,
        )

        return self.__parent__._cast(_5646.VirtualComponentMultibodyDynamicsAnalysis)

    @property
    def worm_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5649.WormGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5649,
        )

        return self.__parent__._cast(_5649.WormGearMultibodyDynamicsAnalysis)

    @property
    def worm_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5650.WormGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5650,
        )

        return self.__parent__._cast(_5650.WormGearSetMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5652.ZerolBevelGearMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5652,
        )

        return self.__parent__._cast(_5652.ZerolBevelGearMultibodyDynamicsAnalysis)

    @property
    def zerol_bevel_gear_set_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5653.ZerolBevelGearSetMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
            _5653,
        )

        return self.__parent__._cast(_5653.ZerolBevelGearSetMultibodyDynamicsAnalysis)

    @property
    def part_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "PartMultibodyDynamicsAnalysis":
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
class PartMultibodyDynamicsAnalysis(_7721.PartTimeSeriesLoadAnalysisCase):
    """PartMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2526.Part":
        """mastapy.system_model.part_model.Part

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def multibody_dynamics_analysis(self: "Self") -> "_5595.MultibodyDynamicsAnalysis":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MultibodyDynamicsAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MultibodyDynamicsAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def data_logger(self: "Self") -> "_1624.DataLogger":
        """mastapy.math_utility.convergence.DataLogger

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataLogger")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def create_viewable(self: "Self") -> "_2305.MBDAnalysisViewable":
        """mastapy.system_model.drawing.MBDAnalysisViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_PartMultibodyDynamicsAnalysis
        """
        return _Cast_PartMultibodyDynamicsAnalysis(self)
