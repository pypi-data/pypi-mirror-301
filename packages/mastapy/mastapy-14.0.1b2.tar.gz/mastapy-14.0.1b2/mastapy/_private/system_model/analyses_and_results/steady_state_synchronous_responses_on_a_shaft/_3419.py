"""MountableComponentSteadyStateSynchronousResponseOnAShaft"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _3365,
)

_MOUNTABLE_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft",
    "MountableComponentSteadyStateSynchronousResponseOnAShaft",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7717,
        _7720,
    )
    from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
        _3346,
        _3348,
        _3353,
        _3354,
        _3355,
        _3358,
        _3362,
        _3367,
        _3371,
        _3374,
        _3376,
        _3378,
        _3381,
        _3389,
        _3390,
        _3395,
        _3400,
        _3404,
        _3408,
        _3411,
        _3414,
        _3415,
        _3416,
        _3420,
        _3421,
        _3423,
        _3427,
        _3428,
        _3429,
        _3430,
        _3431,
        _3435,
        _3437,
        _3443,
        _3445,
        _3450,
        _3453,
        _3454,
        _3455,
        _3456,
        _3457,
        _3458,
        _3461,
        _3463,
        _3464,
        _3465,
        _3468,
        _3471,
    )
    from mastapy._private.system_model.part_model import _2522

    Self = TypeVar(
        "Self", bound="MountableComponentSteadyStateSynchronousResponseOnAShaft"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountableComponentSteadyStateSynchronousResponseOnAShaft._Cast_MountableComponentSteadyStateSynchronousResponseOnAShaft",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountableComponentSteadyStateSynchronousResponseOnAShaft",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountableComponentSteadyStateSynchronousResponseOnAShaft:
    """Special nested class for casting MountableComponentSteadyStateSynchronousResponseOnAShaft to subclasses."""

    __parent__: "MountableComponentSteadyStateSynchronousResponseOnAShaft"

    @property
    def component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3365.ComponentSteadyStateSynchronousResponseOnAShaft":
        return self.__parent__._cast(
            _3365.ComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3421.PartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3421,
        )

        return self.__parent__._cast(_3421.PartSteadyStateSynchronousResponseOnAShaft)

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
    def agma_gleason_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3346.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3346,
        )

        return self.__parent__._cast(
            _3346.AGMAGleasonConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bearing_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3348.BearingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3348,
        )

        return self.__parent__._cast(
            _3348.BearingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3353.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3353,
        )

        return self.__parent__._cast(
            _3353.BevelDifferentialGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3354.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3354,
        )

        return self.__parent__._cast(
            _3354.BevelDifferentialPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_differential_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3355.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3355,
        )

        return self.__parent__._cast(
            _3355.BevelDifferentialSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3358.BevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3358,
        )

        return self.__parent__._cast(
            _3358.BevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def clutch_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3362.ClutchHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3362,
        )

        return self.__parent__._cast(
            _3362.ClutchHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3367.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3367,
        )

        return self.__parent__._cast(
            _3367.ConceptCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def concept_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3371.ConceptGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3371,
        )

        return self.__parent__._cast(
            _3371.ConceptGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3374.ConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3374,
        )

        return self.__parent__._cast(
            _3374.ConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def connector_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3376.ConnectorSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3376,
        )

        return self.__parent__._cast(
            _3376.ConnectorSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3378.CouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3378,
        )

        return self.__parent__._cast(
            _3378.CouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cvt_pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3381.CVTPulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3381,
        )

        return self.__parent__._cast(
            _3381.CVTPulleySteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3389.CylindricalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3389,
        )

        return self.__parent__._cast(
            _3389.CylindricalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def cylindrical_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3390.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3390,
        )

        return self.__parent__._cast(
            _3390.CylindricalPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def face_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3395.FaceGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3395,
        )

        return self.__parent__._cast(
            _3395.FaceGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3400.GearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3400,
        )

        return self.__parent__._cast(_3400.GearSteadyStateSynchronousResponseOnAShaft)

    @property
    def hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3404.HypoidGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3404,
        )

        return self.__parent__._cast(
            _3404.HypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_conical_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3408.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3408,
        )

        return self.__parent__._cast(
            _3408.KlingelnbergCycloPalloidConicalGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> (
        "_3411.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft"
    ):
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3411,
        )

        return self.__parent__._cast(
            _3411.KlingelnbergCycloPalloidHypoidGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3414.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3414,
        )

        return self.__parent__._cast(
            _3414.KlingelnbergCycloPalloidSpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mass_disc_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3415.MassDiscSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3415,
        )

        return self.__parent__._cast(
            _3415.MassDiscSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def measurement_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3416.MeasurementComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3416,
        )

        return self.__parent__._cast(
            _3416.MeasurementComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def oil_seal_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3420.OilSealSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3420,
        )

        return self.__parent__._cast(
            _3420.OilSealSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def part_to_part_shear_coupling_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3423.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3423,
        )

        return self.__parent__._cast(
            _3423.PartToPartShearCouplingHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def planet_carrier_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3427.PlanetCarrierSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3427,
        )

        return self.__parent__._cast(
            _3427.PlanetCarrierSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def point_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3428.PointLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3428,
        )

        return self.__parent__._cast(
            _3428.PointLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def power_load_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3429.PowerLoadSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3429,
        )

        return self.__parent__._cast(
            _3429.PowerLoadSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def pulley_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3430.PulleySteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3430,
        )

        return self.__parent__._cast(_3430.PulleySteadyStateSynchronousResponseOnAShaft)

    @property
    def ring_pins_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3431.RingPinsSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3431,
        )

        return self.__parent__._cast(
            _3431.RingPinsSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def rolling_ring_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3435.RollingRingSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3435,
        )

        return self.__parent__._cast(
            _3435.RollingRingSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def shaft_hub_connection_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3437.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3437,
        )

        return self.__parent__._cast(
            _3437.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spiral_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3443.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3443,
        )

        return self.__parent__._cast(
            _3443.SpiralBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def spring_damper_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3445.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3445,
        )

        return self.__parent__._cast(
            _3445.SpringDamperHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_diff_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3450.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3450,
        )

        return self.__parent__._cast(
            _3450.StraightBevelDiffGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3453.StraightBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3453,
        )

        return self.__parent__._cast(
            _3453.StraightBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_planet_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3454.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3454,
        )

        return self.__parent__._cast(
            _3454.StraightBevelPlanetGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def straight_bevel_sun_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3455.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3455,
        )

        return self.__parent__._cast(
            _3455.StraightBevelSunGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_half_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3456.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3456,
        )

        return self.__parent__._cast(
            _3456.SynchroniserHalfSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_part_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3457.SynchroniserPartSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3457,
        )

        return self.__parent__._cast(
            _3457.SynchroniserPartSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def synchroniser_sleeve_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3458.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3458,
        )

        return self.__parent__._cast(
            _3458.SynchroniserSleeveSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_pump_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3461.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3461,
        )

        return self.__parent__._cast(
            _3461.TorqueConverterPumpSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def torque_converter_turbine_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3463.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3463,
        )

        return self.__parent__._cast(
            _3463.TorqueConverterTurbineSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def unbalanced_mass_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3464.UnbalancedMassSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3464,
        )

        return self.__parent__._cast(
            _3464.UnbalancedMassSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def virtual_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3465.VirtualComponentSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3465,
        )

        return self.__parent__._cast(
            _3465.VirtualComponentSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def worm_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3468.WormGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3468,
        )

        return self.__parent__._cast(
            _3468.WormGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def zerol_bevel_gear_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "_3471.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft":
        from mastapy._private.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
            _3471,
        )

        return self.__parent__._cast(
            _3471.ZerolBevelGearSteadyStateSynchronousResponseOnAShaft
        )

    @property
    def mountable_component_steady_state_synchronous_response_on_a_shaft(
        self: "CastSelf",
    ) -> "MountableComponentSteadyStateSynchronousResponseOnAShaft":
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
class MountableComponentSteadyStateSynchronousResponseOnAShaft(
    _3365.ComponentSteadyStateSynchronousResponseOnAShaft
):
    """MountableComponentSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _MOUNTABLE_COMPONENT_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2522.MountableComponent":
        """mastapy.system_model.part_model.MountableComponent

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_MountableComponentSteadyStateSynchronousResponseOnAShaft":
        """Cast to another type.

        Returns:
            _Cast_MountableComponentSteadyStateSynchronousResponseOnAShaft
        """
        return _Cast_MountableComponentSteadyStateSynchronousResponseOnAShaft(self)
