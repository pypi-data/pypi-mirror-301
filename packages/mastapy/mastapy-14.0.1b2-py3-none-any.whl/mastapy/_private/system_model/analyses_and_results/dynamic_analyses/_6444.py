"""ComponentDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses import _6502

_COMPONENT_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses",
    "ComponentDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7719,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6420,
        _6421,
        _6423,
        _6427,
        _6430,
        _6433,
        _6434,
        _6435,
        _6438,
        _6442,
        _6447,
        _6448,
        _6451,
        _6455,
        _6458,
        _6461,
        _6464,
        _6466,
        _6469,
        _6470,
        _6473,
        _6474,
        _6477,
        _6479,
        _6482,
        _6483,
        _6487,
        _6490,
        _6493,
        _6496,
        _6497,
        _6499,
        _6500,
        _6501,
        _6505,
        _6508,
        _6509,
        _6510,
        _6511,
        _6512,
        _6516,
        _6518,
        _6519,
        _6522,
        _6527,
        _6528,
        _6531,
        _6534,
        _6535,
        _6537,
        _6538,
        _6539,
        _6542,
        _6543,
        _6544,
        _6545,
        _6546,
        _6549,
    )
    from mastapy._private.system_model.part_model import _2500

    Self = TypeVar("Self", bound="ComponentDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ComponentDynamicAnalysis._Cast_ComponentDynamicAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentDynamicAnalysis:
    """Special nested class for casting ComponentDynamicAnalysis to subclasses."""

    __parent__: "ComponentDynamicAnalysis"

    @property
    def part_dynamic_analysis(self: "CastSelf") -> "_6502.PartDynamicAnalysis":
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
    def abstract_shaft_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6420.AbstractShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6420,
        )

        return self.__parent__._cast(_6420.AbstractShaftDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6421.AbstractShaftOrHousingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6421,
        )

        return self.__parent__._cast(_6421.AbstractShaftOrHousingDynamicAnalysis)

    @property
    def agma_gleason_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6423.AGMAGleasonConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6423,
        )

        return self.__parent__._cast(_6423.AGMAGleasonConicalGearDynamicAnalysis)

    @property
    def bearing_dynamic_analysis(self: "CastSelf") -> "_6427.BearingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6427,
        )

        return self.__parent__._cast(_6427.BearingDynamicAnalysis)

    @property
    def bevel_differential_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6430.BevelDifferentialGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6430,
        )

        return self.__parent__._cast(_6430.BevelDifferentialGearDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6433.BevelDifferentialPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6433,
        )

        return self.__parent__._cast(_6433.BevelDifferentialPlanetGearDynamicAnalysis)

    @property
    def bevel_differential_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6434.BevelDifferentialSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6434,
        )

        return self.__parent__._cast(_6434.BevelDifferentialSunGearDynamicAnalysis)

    @property
    def bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6435.BevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6435,
        )

        return self.__parent__._cast(_6435.BevelGearDynamicAnalysis)

    @property
    def bolt_dynamic_analysis(self: "CastSelf") -> "_6438.BoltDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6438,
        )

        return self.__parent__._cast(_6438.BoltDynamicAnalysis)

    @property
    def clutch_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6442.ClutchHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6442,
        )

        return self.__parent__._cast(_6442.ClutchHalfDynamicAnalysis)

    @property
    def concept_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6447.ConceptCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6447,
        )

        return self.__parent__._cast(_6447.ConceptCouplingHalfDynamicAnalysis)

    @property
    def concept_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6448.ConceptGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6448,
        )

        return self.__parent__._cast(_6448.ConceptGearDynamicAnalysis)

    @property
    def conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6451.ConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6451,
        )

        return self.__parent__._cast(_6451.ConicalGearDynamicAnalysis)

    @property
    def connector_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6455.ConnectorDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6455,
        )

        return self.__parent__._cast(_6455.ConnectorDynamicAnalysis)

    @property
    def coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6458.CouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6458,
        )

        return self.__parent__._cast(_6458.CouplingHalfDynamicAnalysis)

    @property
    def cvt_pulley_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6461.CVTPulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6461,
        )

        return self.__parent__._cast(_6461.CVTPulleyDynamicAnalysis)

    @property
    def cycloidal_disc_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6464.CycloidalDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6464,
        )

        return self.__parent__._cast(_6464.CycloidalDiscDynamicAnalysis)

    @property
    def cylindrical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6466.CylindricalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6466,
        )

        return self.__parent__._cast(_6466.CylindricalGearDynamicAnalysis)

    @property
    def cylindrical_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6469.CylindricalPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6469,
        )

        return self.__parent__._cast(_6469.CylindricalPlanetGearDynamicAnalysis)

    @property
    def datum_dynamic_analysis(self: "CastSelf") -> "_6470.DatumDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6470,
        )

        return self.__parent__._cast(_6470.DatumDynamicAnalysis)

    @property
    def external_cad_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6473.ExternalCADModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6473,
        )

        return self.__parent__._cast(_6473.ExternalCADModelDynamicAnalysis)

    @property
    def face_gear_dynamic_analysis(self: "CastSelf") -> "_6474.FaceGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6474,
        )

        return self.__parent__._cast(_6474.FaceGearDynamicAnalysis)

    @property
    def fe_part_dynamic_analysis(self: "CastSelf") -> "_6477.FEPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6477,
        )

        return self.__parent__._cast(_6477.FEPartDynamicAnalysis)

    @property
    def gear_dynamic_analysis(self: "CastSelf") -> "_6479.GearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6479,
        )

        return self.__parent__._cast(_6479.GearDynamicAnalysis)

    @property
    def guide_dxf_model_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6482.GuideDxfModelDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6482,
        )

        return self.__parent__._cast(_6482.GuideDxfModelDynamicAnalysis)

    @property
    def hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6483.HypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6483,
        )

        return self.__parent__._cast(_6483.HypoidGearDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6487.KlingelnbergCycloPalloidConicalGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6487,
        )

        return self.__parent__._cast(
            _6487.KlingelnbergCycloPalloidConicalGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6490.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6490,
        )

        return self.__parent__._cast(
            _6490.KlingelnbergCycloPalloidHypoidGearDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6493.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6493,
        )

        return self.__parent__._cast(
            _6493.KlingelnbergCycloPalloidSpiralBevelGearDynamicAnalysis
        )

    @property
    def mass_disc_dynamic_analysis(self: "CastSelf") -> "_6496.MassDiscDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6496,
        )

        return self.__parent__._cast(_6496.MassDiscDynamicAnalysis)

    @property
    def measurement_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6497.MeasurementComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6497,
        )

        return self.__parent__._cast(_6497.MeasurementComponentDynamicAnalysis)

    @property
    def microphone_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6499.MicrophoneDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6499,
        )

        return self.__parent__._cast(_6499.MicrophoneDynamicAnalysis)

    @property
    def mountable_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6500.MountableComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6500,
        )

        return self.__parent__._cast(_6500.MountableComponentDynamicAnalysis)

    @property
    def oil_seal_dynamic_analysis(self: "CastSelf") -> "_6501.OilSealDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6501,
        )

        return self.__parent__._cast(_6501.OilSealDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6505.PartToPartShearCouplingHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6505,
        )

        return self.__parent__._cast(_6505.PartToPartShearCouplingHalfDynamicAnalysis)

    @property
    def planet_carrier_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6508.PlanetCarrierDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6508,
        )

        return self.__parent__._cast(_6508.PlanetCarrierDynamicAnalysis)

    @property
    def point_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6509.PointLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6509,
        )

        return self.__parent__._cast(_6509.PointLoadDynamicAnalysis)

    @property
    def power_load_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6510.PowerLoadDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6510,
        )

        return self.__parent__._cast(_6510.PowerLoadDynamicAnalysis)

    @property
    def pulley_dynamic_analysis(self: "CastSelf") -> "_6511.PulleyDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6511,
        )

        return self.__parent__._cast(_6511.PulleyDynamicAnalysis)

    @property
    def ring_pins_dynamic_analysis(self: "CastSelf") -> "_6512.RingPinsDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6512,
        )

        return self.__parent__._cast(_6512.RingPinsDynamicAnalysis)

    @property
    def rolling_ring_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6516.RollingRingDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6516,
        )

        return self.__parent__._cast(_6516.RollingRingDynamicAnalysis)

    @property
    def shaft_dynamic_analysis(self: "CastSelf") -> "_6518.ShaftDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6518,
        )

        return self.__parent__._cast(_6518.ShaftDynamicAnalysis)

    @property
    def shaft_hub_connection_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6519.ShaftHubConnectionDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6519,
        )

        return self.__parent__._cast(_6519.ShaftHubConnectionDynamicAnalysis)

    @property
    def spiral_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6522.SpiralBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6522,
        )

        return self.__parent__._cast(_6522.SpiralBevelGearDynamicAnalysis)

    @property
    def spring_damper_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6527.SpringDamperHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6527,
        )

        return self.__parent__._cast(_6527.SpringDamperHalfDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6528.StraightBevelDiffGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6528,
        )

        return self.__parent__._cast(_6528.StraightBevelDiffGearDynamicAnalysis)

    @property
    def straight_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6531.StraightBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6531,
        )

        return self.__parent__._cast(_6531.StraightBevelGearDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6534.StraightBevelPlanetGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6534,
        )

        return self.__parent__._cast(_6534.StraightBevelPlanetGearDynamicAnalysis)

    @property
    def straight_bevel_sun_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6535.StraightBevelSunGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6535,
        )

        return self.__parent__._cast(_6535.StraightBevelSunGearDynamicAnalysis)

    @property
    def synchroniser_half_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6537.SynchroniserHalfDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6537,
        )

        return self.__parent__._cast(_6537.SynchroniserHalfDynamicAnalysis)

    @property
    def synchroniser_part_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6538.SynchroniserPartDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6538,
        )

        return self.__parent__._cast(_6538.SynchroniserPartDynamicAnalysis)

    @property
    def synchroniser_sleeve_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6539.SynchroniserSleeveDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6539,
        )

        return self.__parent__._cast(_6539.SynchroniserSleeveDynamicAnalysis)

    @property
    def torque_converter_pump_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6542.TorqueConverterPumpDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6542,
        )

        return self.__parent__._cast(_6542.TorqueConverterPumpDynamicAnalysis)

    @property
    def torque_converter_turbine_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6543.TorqueConverterTurbineDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6543,
        )

        return self.__parent__._cast(_6543.TorqueConverterTurbineDynamicAnalysis)

    @property
    def unbalanced_mass_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6544.UnbalancedMassDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6544,
        )

        return self.__parent__._cast(_6544.UnbalancedMassDynamicAnalysis)

    @property
    def virtual_component_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6545.VirtualComponentDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6545,
        )

        return self.__parent__._cast(_6545.VirtualComponentDynamicAnalysis)

    @property
    def worm_gear_dynamic_analysis(self: "CastSelf") -> "_6546.WormGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6546,
        )

        return self.__parent__._cast(_6546.WormGearDynamicAnalysis)

    @property
    def zerol_bevel_gear_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6549.ZerolBevelGearDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
            _6549,
        )

        return self.__parent__._cast(_6549.ZerolBevelGearDynamicAnalysis)

    @property
    def component_dynamic_analysis(self: "CastSelf") -> "ComponentDynamicAnalysis":
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
class ComponentDynamicAnalysis(_6502.PartDynamicAnalysis):
    """ComponentDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2500.Component":
        """mastapy.system_model.part_model.Component

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ComponentDynamicAnalysis
        """
        return _Cast_ComponentDynamicAnalysis(self)
