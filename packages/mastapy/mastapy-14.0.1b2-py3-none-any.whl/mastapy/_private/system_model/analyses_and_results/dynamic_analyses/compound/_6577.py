"""ComponentCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6633,
)

_COMPONENT_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "ComponentCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6444,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6553,
        _6554,
        _6556,
        _6560,
        _6563,
        _6566,
        _6567,
        _6568,
        _6571,
        _6575,
        _6580,
        _6581,
        _6584,
        _6588,
        _6591,
        _6594,
        _6597,
        _6599,
        _6602,
        _6603,
        _6604,
        _6605,
        _6608,
        _6610,
        _6613,
        _6614,
        _6618,
        _6621,
        _6624,
        _6627,
        _6628,
        _6630,
        _6631,
        _6632,
        _6636,
        _6639,
        _6640,
        _6641,
        _6642,
        _6643,
        _6646,
        _6649,
        _6650,
        _6653,
        _6658,
        _6659,
        _6662,
        _6665,
        _6666,
        _6668,
        _6669,
        _6670,
        _6673,
        _6674,
        _6675,
        _6676,
        _6677,
        _6680,
    )

    Self = TypeVar("Self", bound="ComponentCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ComponentCompoundDynamicAnalysis._Cast_ComponentCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComponentCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentCompoundDynamicAnalysis:
    """Special nested class for casting ComponentCompoundDynamicAnalysis to subclasses."""

    __parent__: "ComponentCompoundDynamicAnalysis"

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.PartCompoundDynamicAnalysis":
        return self.__parent__._cast(_6633.PartCompoundDynamicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7718.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7718,
        )

        return self.__parent__._cast(_7718.PartCompoundAnalysis)

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
    def abstract_shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6553.AbstractShaftCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6553,
        )

        return self.__parent__._cast(_6553.AbstractShaftCompoundDynamicAnalysis)

    @property
    def abstract_shaft_or_housing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6554.AbstractShaftOrHousingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6554,
        )

        return self.__parent__._cast(
            _6554.AbstractShaftOrHousingCompoundDynamicAnalysis
        )

    @property
    def agma_gleason_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6556.AGMAGleasonConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6556,
        )

        return self.__parent__._cast(
            _6556.AGMAGleasonConicalGearCompoundDynamicAnalysis
        )

    @property
    def bearing_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6560.BearingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6560,
        )

        return self.__parent__._cast(_6560.BearingCompoundDynamicAnalysis)

    @property
    def bevel_differential_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6563.BevelDifferentialGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6563,
        )

        return self.__parent__._cast(_6563.BevelDifferentialGearCompoundDynamicAnalysis)

    @property
    def bevel_differential_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6566.BevelDifferentialPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6566,
        )

        return self.__parent__._cast(
            _6566.BevelDifferentialPlanetGearCompoundDynamicAnalysis
        )

    @property
    def bevel_differential_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6567.BevelDifferentialSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6567,
        )

        return self.__parent__._cast(
            _6567.BevelDifferentialSunGearCompoundDynamicAnalysis
        )

    @property
    def bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6568.BevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6568,
        )

        return self.__parent__._cast(_6568.BevelGearCompoundDynamicAnalysis)

    @property
    def bolt_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6571.BoltCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6571,
        )

        return self.__parent__._cast(_6571.BoltCompoundDynamicAnalysis)

    @property
    def clutch_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6575.ClutchHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6575,
        )

        return self.__parent__._cast(_6575.ClutchHalfCompoundDynamicAnalysis)

    @property
    def concept_coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6580.ConceptCouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6580,
        )

        return self.__parent__._cast(_6580.ConceptCouplingHalfCompoundDynamicAnalysis)

    @property
    def concept_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6581.ConceptGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6581,
        )

        return self.__parent__._cast(_6581.ConceptGearCompoundDynamicAnalysis)

    @property
    def conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6584.ConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6584,
        )

        return self.__parent__._cast(_6584.ConicalGearCompoundDynamicAnalysis)

    @property
    def connector_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6588.ConnectorCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6588,
        )

        return self.__parent__._cast(_6588.ConnectorCompoundDynamicAnalysis)

    @property
    def coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6591.CouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6591,
        )

        return self.__parent__._cast(_6591.CouplingHalfCompoundDynamicAnalysis)

    @property
    def cvt_pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6594.CVTPulleyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6594,
        )

        return self.__parent__._cast(_6594.CVTPulleyCompoundDynamicAnalysis)

    @property
    def cycloidal_disc_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6597.CycloidalDiscCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6597,
        )

        return self.__parent__._cast(_6597.CycloidalDiscCompoundDynamicAnalysis)

    @property
    def cylindrical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6599.CylindricalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6599,
        )

        return self.__parent__._cast(_6599.CylindricalGearCompoundDynamicAnalysis)

    @property
    def cylindrical_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6602.CylindricalPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6602,
        )

        return self.__parent__._cast(_6602.CylindricalPlanetGearCompoundDynamicAnalysis)

    @property
    def datum_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6603.DatumCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6603,
        )

        return self.__parent__._cast(_6603.DatumCompoundDynamicAnalysis)

    @property
    def external_cad_model_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6604.ExternalCADModelCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6604,
        )

        return self.__parent__._cast(_6604.ExternalCADModelCompoundDynamicAnalysis)

    @property
    def face_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6605.FaceGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6605,
        )

        return self.__parent__._cast(_6605.FaceGearCompoundDynamicAnalysis)

    @property
    def fe_part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6608.FEPartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6608,
        )

        return self.__parent__._cast(_6608.FEPartCompoundDynamicAnalysis)

    @property
    def gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6610.GearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6610,
        )

        return self.__parent__._cast(_6610.GearCompoundDynamicAnalysis)

    @property
    def guide_dxf_model_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6613.GuideDxfModelCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6613,
        )

        return self.__parent__._cast(_6613.GuideDxfModelCompoundDynamicAnalysis)

    @property
    def hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6614.HypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6614,
        )

        return self.__parent__._cast(_6614.HypoidGearCompoundDynamicAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6618.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6618,
        )

        return self.__parent__._cast(
            _6618.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6621.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6621,
        )

        return self.__parent__._cast(
            _6621.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6624.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6624,
        )

        return self.__parent__._cast(
            _6624.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis
        )

    @property
    def mass_disc_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6627.MassDiscCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6627,
        )

        return self.__parent__._cast(_6627.MassDiscCompoundDynamicAnalysis)

    @property
    def measurement_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6628.MeasurementComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6628,
        )

        return self.__parent__._cast(_6628.MeasurementComponentCompoundDynamicAnalysis)

    @property
    def microphone_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6630.MicrophoneCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6630,
        )

        return self.__parent__._cast(_6630.MicrophoneCompoundDynamicAnalysis)

    @property
    def mountable_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6631.MountableComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6631,
        )

        return self.__parent__._cast(_6631.MountableComponentCompoundDynamicAnalysis)

    @property
    def oil_seal_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6632.OilSealCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6632,
        )

        return self.__parent__._cast(_6632.OilSealCompoundDynamicAnalysis)

    @property
    def part_to_part_shear_coupling_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6636.PartToPartShearCouplingHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6636,
        )

        return self.__parent__._cast(
            _6636.PartToPartShearCouplingHalfCompoundDynamicAnalysis
        )

    @property
    def planet_carrier_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6639.PlanetCarrierCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6639,
        )

        return self.__parent__._cast(_6639.PlanetCarrierCompoundDynamicAnalysis)

    @property
    def point_load_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6640.PointLoadCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6640,
        )

        return self.__parent__._cast(_6640.PointLoadCompoundDynamicAnalysis)

    @property
    def power_load_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6641.PowerLoadCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6641,
        )

        return self.__parent__._cast(_6641.PowerLoadCompoundDynamicAnalysis)

    @property
    def pulley_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6642.PulleyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6642,
        )

        return self.__parent__._cast(_6642.PulleyCompoundDynamicAnalysis)

    @property
    def ring_pins_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6643.RingPinsCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6643,
        )

        return self.__parent__._cast(_6643.RingPinsCompoundDynamicAnalysis)

    @property
    def rolling_ring_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6646.RollingRingCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6646,
        )

        return self.__parent__._cast(_6646.RollingRingCompoundDynamicAnalysis)

    @property
    def shaft_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6649.ShaftCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6649,
        )

        return self.__parent__._cast(_6649.ShaftCompoundDynamicAnalysis)

    @property
    def shaft_hub_connection_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6650.ShaftHubConnectionCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6650,
        )

        return self.__parent__._cast(_6650.ShaftHubConnectionCompoundDynamicAnalysis)

    @property
    def spiral_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6653.SpiralBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6653,
        )

        return self.__parent__._cast(_6653.SpiralBevelGearCompoundDynamicAnalysis)

    @property
    def spring_damper_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6658.SpringDamperHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6658,
        )

        return self.__parent__._cast(_6658.SpringDamperHalfCompoundDynamicAnalysis)

    @property
    def straight_bevel_diff_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6659.StraightBevelDiffGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6659,
        )

        return self.__parent__._cast(_6659.StraightBevelDiffGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6662.StraightBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6662,
        )

        return self.__parent__._cast(_6662.StraightBevelGearCompoundDynamicAnalysis)

    @property
    def straight_bevel_planet_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6665.StraightBevelPlanetGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6665,
        )

        return self.__parent__._cast(
            _6665.StraightBevelPlanetGearCompoundDynamicAnalysis
        )

    @property
    def straight_bevel_sun_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6666.StraightBevelSunGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6666,
        )

        return self.__parent__._cast(_6666.StraightBevelSunGearCompoundDynamicAnalysis)

    @property
    def synchroniser_half_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6668.SynchroniserHalfCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6668,
        )

        return self.__parent__._cast(_6668.SynchroniserHalfCompoundDynamicAnalysis)

    @property
    def synchroniser_part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6669.SynchroniserPartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6669,
        )

        return self.__parent__._cast(_6669.SynchroniserPartCompoundDynamicAnalysis)

    @property
    def synchroniser_sleeve_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6670.SynchroniserSleeveCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6670,
        )

        return self.__parent__._cast(_6670.SynchroniserSleeveCompoundDynamicAnalysis)

    @property
    def torque_converter_pump_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6673.TorqueConverterPumpCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6673,
        )

        return self.__parent__._cast(_6673.TorqueConverterPumpCompoundDynamicAnalysis)

    @property
    def torque_converter_turbine_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6674.TorqueConverterTurbineCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6674,
        )

        return self.__parent__._cast(
            _6674.TorqueConverterTurbineCompoundDynamicAnalysis
        )

    @property
    def unbalanced_mass_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6675.UnbalancedMassCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6675,
        )

        return self.__parent__._cast(_6675.UnbalancedMassCompoundDynamicAnalysis)

    @property
    def virtual_component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6676.VirtualComponentCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6676,
        )

        return self.__parent__._cast(_6676.VirtualComponentCompoundDynamicAnalysis)

    @property
    def worm_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6677.WormGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6677,
        )

        return self.__parent__._cast(_6677.WormGearCompoundDynamicAnalysis)

    @property
    def zerol_bevel_gear_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6680.ZerolBevelGearCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6680,
        )

        return self.__parent__._cast(_6680.ZerolBevelGearCompoundDynamicAnalysis)

    @property
    def component_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "ComponentCompoundDynamicAnalysis":
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
class ComponentCompoundDynamicAnalysis(_6633.PartCompoundDynamicAnalysis):
    """ComponentCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6444.ComponentDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6444.ComponentDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.ComponentDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ComponentCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ComponentCompoundDynamicAnalysis
        """
        return _Cast_ComponentCompoundDynamicAnalysis(self)
