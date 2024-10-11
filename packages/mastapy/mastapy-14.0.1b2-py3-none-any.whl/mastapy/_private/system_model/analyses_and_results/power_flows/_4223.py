"""PartPowerFlow"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7720

_PART_POWER_FLOW = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows", "PartPowerFlow"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.analysis_cases import _7717
    from mastapy._private.system_model.analyses_and_results.power_flows import (
        _4139,
        _4140,
        _4141,
        _4144,
        _4145,
        _4146,
        _4147,
        _4149,
        _4151,
        _4152,
        _4153,
        _4154,
        _4156,
        _4157,
        _4158,
        _4159,
        _4161,
        _4162,
        _4164,
        _4166,
        _4167,
        _4169,
        _4170,
        _4172,
        _4173,
        _4175,
        _4177,
        _4178,
        _4180,
        _4181,
        _4182,
        _4185,
        _4188,
        _4189,
        _4190,
        _4191,
        _4192,
        _4194,
        _4195,
        _4198,
        _4199,
        _4201,
        _4202,
        _4203,
        _4205,
        _4206,
        _4209,
        _4210,
        _4212,
        _4213,
        _4215,
        _4216,
        _4217,
        _4218,
        _4219,
        _4220,
        _4221,
        _4222,
        _4225,
        _4226,
        _4228,
        _4229,
        _4230,
        _4231,
        _4233,
        _4234,
        _4235,
        _4237,
        _4239,
        _4240,
        _4241,
        _4242,
        _4244,
        _4246,
        _4247,
        _4249,
        _4250,
        _4252,
        _4253,
        _4255,
        _4256,
        _4257,
        _4258,
        _4259,
        _4260,
        _4261,
        _4262,
        _4265,
        _4266,
        _4267,
        _4268,
        _4269,
        _4271,
        _4272,
        _4274,
        _4275,
    )
    from mastapy._private.system_model.drawing import _2309
    from mastapy._private.system_model.part_model import _2526

    Self = TypeVar("Self", bound="PartPowerFlow")
    CastSelf = TypeVar("CastSelf", bound="PartPowerFlow._Cast_PartPowerFlow")


__docformat__ = "restructuredtext en"
__all__ = ("PartPowerFlow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartPowerFlow:
    """Special nested class for casting PartPowerFlow to subclasses."""

    __parent__: "PartPowerFlow"

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7720.PartStaticLoadAnalysisCase":
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
    def abstract_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4139.AbstractAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4139

        return self.__parent__._cast(_4139.AbstractAssemblyPowerFlow)

    @property
    def abstract_shaft_or_housing_power_flow(
        self: "CastSelf",
    ) -> "_4140.AbstractShaftOrHousingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4140

        return self.__parent__._cast(_4140.AbstractShaftOrHousingPowerFlow)

    @property
    def abstract_shaft_power_flow(self: "CastSelf") -> "_4141.AbstractShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4141

        return self.__parent__._cast(_4141.AbstractShaftPowerFlow)

    @property
    def agma_gleason_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4144.AGMAGleasonConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4144

        return self.__parent__._cast(_4144.AGMAGleasonConicalGearPowerFlow)

    @property
    def agma_gleason_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4145.AGMAGleasonConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4145

        return self.__parent__._cast(_4145.AGMAGleasonConicalGearSetPowerFlow)

    @property
    def assembly_power_flow(self: "CastSelf") -> "_4146.AssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4146

        return self.__parent__._cast(_4146.AssemblyPowerFlow)

    @property
    def bearing_power_flow(self: "CastSelf") -> "_4147.BearingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4147

        return self.__parent__._cast(_4147.BearingPowerFlow)

    @property
    def belt_drive_power_flow(self: "CastSelf") -> "_4149.BeltDrivePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4149

        return self.__parent__._cast(_4149.BeltDrivePowerFlow)

    @property
    def bevel_differential_gear_power_flow(
        self: "CastSelf",
    ) -> "_4151.BevelDifferentialGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4151

        return self.__parent__._cast(_4151.BevelDifferentialGearPowerFlow)

    @property
    def bevel_differential_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4152.BevelDifferentialGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4152

        return self.__parent__._cast(_4152.BevelDifferentialGearSetPowerFlow)

    @property
    def bevel_differential_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4153.BevelDifferentialPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4153

        return self.__parent__._cast(_4153.BevelDifferentialPlanetGearPowerFlow)

    @property
    def bevel_differential_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4154.BevelDifferentialSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4154

        return self.__parent__._cast(_4154.BevelDifferentialSunGearPowerFlow)

    @property
    def bevel_gear_power_flow(self: "CastSelf") -> "_4156.BevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4156

        return self.__parent__._cast(_4156.BevelGearPowerFlow)

    @property
    def bevel_gear_set_power_flow(self: "CastSelf") -> "_4157.BevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4157

        return self.__parent__._cast(_4157.BevelGearSetPowerFlow)

    @property
    def bolted_joint_power_flow(self: "CastSelf") -> "_4158.BoltedJointPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4158

        return self.__parent__._cast(_4158.BoltedJointPowerFlow)

    @property
    def bolt_power_flow(self: "CastSelf") -> "_4159.BoltPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4159

        return self.__parent__._cast(_4159.BoltPowerFlow)

    @property
    def clutch_half_power_flow(self: "CastSelf") -> "_4161.ClutchHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4161

        return self.__parent__._cast(_4161.ClutchHalfPowerFlow)

    @property
    def clutch_power_flow(self: "CastSelf") -> "_4162.ClutchPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4162

        return self.__parent__._cast(_4162.ClutchPowerFlow)

    @property
    def component_power_flow(self: "CastSelf") -> "_4164.ComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4164

        return self.__parent__._cast(_4164.ComponentPowerFlow)

    @property
    def concept_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4166.ConceptCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4166

        return self.__parent__._cast(_4166.ConceptCouplingHalfPowerFlow)

    @property
    def concept_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4167.ConceptCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4167

        return self.__parent__._cast(_4167.ConceptCouplingPowerFlow)

    @property
    def concept_gear_power_flow(self: "CastSelf") -> "_4169.ConceptGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4169

        return self.__parent__._cast(_4169.ConceptGearPowerFlow)

    @property
    def concept_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4170.ConceptGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4170

        return self.__parent__._cast(_4170.ConceptGearSetPowerFlow)

    @property
    def conical_gear_power_flow(self: "CastSelf") -> "_4172.ConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4172

        return self.__parent__._cast(_4172.ConicalGearPowerFlow)

    @property
    def conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4173.ConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4173

        return self.__parent__._cast(_4173.ConicalGearSetPowerFlow)

    @property
    def connector_power_flow(self: "CastSelf") -> "_4175.ConnectorPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4175

        return self.__parent__._cast(_4175.ConnectorPowerFlow)

    @property
    def coupling_half_power_flow(self: "CastSelf") -> "_4177.CouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4177

        return self.__parent__._cast(_4177.CouplingHalfPowerFlow)

    @property
    def coupling_power_flow(self: "CastSelf") -> "_4178.CouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4178

        return self.__parent__._cast(_4178.CouplingPowerFlow)

    @property
    def cvt_power_flow(self: "CastSelf") -> "_4180.CVTPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4180

        return self.__parent__._cast(_4180.CVTPowerFlow)

    @property
    def cvt_pulley_power_flow(self: "CastSelf") -> "_4181.CVTPulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4181

        return self.__parent__._cast(_4181.CVTPulleyPowerFlow)

    @property
    def cycloidal_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4182.CycloidalAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4182

        return self.__parent__._cast(_4182.CycloidalAssemblyPowerFlow)

    @property
    def cycloidal_disc_power_flow(self: "CastSelf") -> "_4185.CycloidalDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4185

        return self.__parent__._cast(_4185.CycloidalDiscPowerFlow)

    @property
    def cylindrical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4188.CylindricalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4188

        return self.__parent__._cast(_4188.CylindricalGearPowerFlow)

    @property
    def cylindrical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4189.CylindricalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4189

        return self.__parent__._cast(_4189.CylindricalGearSetPowerFlow)

    @property
    def cylindrical_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4190.CylindricalPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4190

        return self.__parent__._cast(_4190.CylindricalPlanetGearPowerFlow)

    @property
    def datum_power_flow(self: "CastSelf") -> "_4191.DatumPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4191

        return self.__parent__._cast(_4191.DatumPowerFlow)

    @property
    def external_cad_model_power_flow(
        self: "CastSelf",
    ) -> "_4192.ExternalCADModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4192

        return self.__parent__._cast(_4192.ExternalCADModelPowerFlow)

    @property
    def face_gear_power_flow(self: "CastSelf") -> "_4194.FaceGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4194

        return self.__parent__._cast(_4194.FaceGearPowerFlow)

    @property
    def face_gear_set_power_flow(self: "CastSelf") -> "_4195.FaceGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4195

        return self.__parent__._cast(_4195.FaceGearSetPowerFlow)

    @property
    def fe_part_power_flow(self: "CastSelf") -> "_4198.FEPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4198

        return self.__parent__._cast(_4198.FEPartPowerFlow)

    @property
    def flexible_pin_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4199.FlexiblePinAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4199

        return self.__parent__._cast(_4199.FlexiblePinAssemblyPowerFlow)

    @property
    def gear_power_flow(self: "CastSelf") -> "_4201.GearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4201

        return self.__parent__._cast(_4201.GearPowerFlow)

    @property
    def gear_set_power_flow(self: "CastSelf") -> "_4202.GearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4202

        return self.__parent__._cast(_4202.GearSetPowerFlow)

    @property
    def guide_dxf_model_power_flow(self: "CastSelf") -> "_4203.GuideDxfModelPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4203

        return self.__parent__._cast(_4203.GuideDxfModelPowerFlow)

    @property
    def hypoid_gear_power_flow(self: "CastSelf") -> "_4205.HypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4205

        return self.__parent__._cast(_4205.HypoidGearPowerFlow)

    @property
    def hypoid_gear_set_power_flow(self: "CastSelf") -> "_4206.HypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4206

        return self.__parent__._cast(_4206.HypoidGearSetPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_power_flow(
        self: "CastSelf",
    ) -> "_4209.KlingelnbergCycloPalloidConicalGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4209

        return self.__parent__._cast(_4209.KlingelnbergCycloPalloidConicalGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4210.KlingelnbergCycloPalloidConicalGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4210

        return self.__parent__._cast(
            _4210.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_power_flow(
        self: "CastSelf",
    ) -> "_4212.KlingelnbergCycloPalloidHypoidGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4212

        return self.__parent__._cast(_4212.KlingelnbergCycloPalloidHypoidGearPowerFlow)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4213.KlingelnbergCycloPalloidHypoidGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4213

        return self.__parent__._cast(
            _4213.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4215.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4215

        return self.__parent__._cast(
            _4215.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4216.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4216

        return self.__parent__._cast(
            _4216.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        )

    @property
    def mass_disc_power_flow(self: "CastSelf") -> "_4217.MassDiscPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4217

        return self.__parent__._cast(_4217.MassDiscPowerFlow)

    @property
    def measurement_component_power_flow(
        self: "CastSelf",
    ) -> "_4218.MeasurementComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4218

        return self.__parent__._cast(_4218.MeasurementComponentPowerFlow)

    @property
    def microphone_array_power_flow(
        self: "CastSelf",
    ) -> "_4219.MicrophoneArrayPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4219

        return self.__parent__._cast(_4219.MicrophoneArrayPowerFlow)

    @property
    def microphone_power_flow(self: "CastSelf") -> "_4220.MicrophonePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4220

        return self.__parent__._cast(_4220.MicrophonePowerFlow)

    @property
    def mountable_component_power_flow(
        self: "CastSelf",
    ) -> "_4221.MountableComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4221

        return self.__parent__._cast(_4221.MountableComponentPowerFlow)

    @property
    def oil_seal_power_flow(self: "CastSelf") -> "_4222.OilSealPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4222

        return self.__parent__._cast(_4222.OilSealPowerFlow)

    @property
    def part_to_part_shear_coupling_half_power_flow(
        self: "CastSelf",
    ) -> "_4225.PartToPartShearCouplingHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4225

        return self.__parent__._cast(_4225.PartToPartShearCouplingHalfPowerFlow)

    @property
    def part_to_part_shear_coupling_power_flow(
        self: "CastSelf",
    ) -> "_4226.PartToPartShearCouplingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4226

        return self.__parent__._cast(_4226.PartToPartShearCouplingPowerFlow)

    @property
    def planetary_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4228.PlanetaryGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4228

        return self.__parent__._cast(_4228.PlanetaryGearSetPowerFlow)

    @property
    def planet_carrier_power_flow(self: "CastSelf") -> "_4229.PlanetCarrierPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4229

        return self.__parent__._cast(_4229.PlanetCarrierPowerFlow)

    @property
    def point_load_power_flow(self: "CastSelf") -> "_4230.PointLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4230

        return self.__parent__._cast(_4230.PointLoadPowerFlow)

    @property
    def power_load_power_flow(self: "CastSelf") -> "_4233.PowerLoadPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4233

        return self.__parent__._cast(_4233.PowerLoadPowerFlow)

    @property
    def pulley_power_flow(self: "CastSelf") -> "_4234.PulleyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4234

        return self.__parent__._cast(_4234.PulleyPowerFlow)

    @property
    def ring_pins_power_flow(self: "CastSelf") -> "_4235.RingPinsPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4235

        return self.__parent__._cast(_4235.RingPinsPowerFlow)

    @property
    def rolling_ring_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4237.RollingRingAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4237

        return self.__parent__._cast(_4237.RollingRingAssemblyPowerFlow)

    @property
    def rolling_ring_power_flow(self: "CastSelf") -> "_4239.RollingRingPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4239

        return self.__parent__._cast(_4239.RollingRingPowerFlow)

    @property
    def root_assembly_power_flow(self: "CastSelf") -> "_4240.RootAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4240

        return self.__parent__._cast(_4240.RootAssemblyPowerFlow)

    @property
    def shaft_hub_connection_power_flow(
        self: "CastSelf",
    ) -> "_4241.ShaftHubConnectionPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4241

        return self.__parent__._cast(_4241.ShaftHubConnectionPowerFlow)

    @property
    def shaft_power_flow(self: "CastSelf") -> "_4242.ShaftPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4242

        return self.__parent__._cast(_4242.ShaftPowerFlow)

    @property
    def specialised_assembly_power_flow(
        self: "CastSelf",
    ) -> "_4244.SpecialisedAssemblyPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4244

        return self.__parent__._cast(_4244.SpecialisedAssemblyPowerFlow)

    @property
    def spiral_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4246.SpiralBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4246

        return self.__parent__._cast(_4246.SpiralBevelGearPowerFlow)

    @property
    def spiral_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4247.SpiralBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4247

        return self.__parent__._cast(_4247.SpiralBevelGearSetPowerFlow)

    @property
    def spring_damper_half_power_flow(
        self: "CastSelf",
    ) -> "_4249.SpringDamperHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4249

        return self.__parent__._cast(_4249.SpringDamperHalfPowerFlow)

    @property
    def spring_damper_power_flow(self: "CastSelf") -> "_4250.SpringDamperPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4250

        return self.__parent__._cast(_4250.SpringDamperPowerFlow)

    @property
    def straight_bevel_diff_gear_power_flow(
        self: "CastSelf",
    ) -> "_4252.StraightBevelDiffGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4252

        return self.__parent__._cast(_4252.StraightBevelDiffGearPowerFlow)

    @property
    def straight_bevel_diff_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4253.StraightBevelDiffGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4253

        return self.__parent__._cast(_4253.StraightBevelDiffGearSetPowerFlow)

    @property
    def straight_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4255.StraightBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4255

        return self.__parent__._cast(_4255.StraightBevelGearPowerFlow)

    @property
    def straight_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4256.StraightBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4256

        return self.__parent__._cast(_4256.StraightBevelGearSetPowerFlow)

    @property
    def straight_bevel_planet_gear_power_flow(
        self: "CastSelf",
    ) -> "_4257.StraightBevelPlanetGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4257

        return self.__parent__._cast(_4257.StraightBevelPlanetGearPowerFlow)

    @property
    def straight_bevel_sun_gear_power_flow(
        self: "CastSelf",
    ) -> "_4258.StraightBevelSunGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4258

        return self.__parent__._cast(_4258.StraightBevelSunGearPowerFlow)

    @property
    def synchroniser_half_power_flow(
        self: "CastSelf",
    ) -> "_4259.SynchroniserHalfPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4259

        return self.__parent__._cast(_4259.SynchroniserHalfPowerFlow)

    @property
    def synchroniser_part_power_flow(
        self: "CastSelf",
    ) -> "_4260.SynchroniserPartPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4260

        return self.__parent__._cast(_4260.SynchroniserPartPowerFlow)

    @property
    def synchroniser_power_flow(self: "CastSelf") -> "_4261.SynchroniserPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4261

        return self.__parent__._cast(_4261.SynchroniserPowerFlow)

    @property
    def synchroniser_sleeve_power_flow(
        self: "CastSelf",
    ) -> "_4262.SynchroniserSleevePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4262

        return self.__parent__._cast(_4262.SynchroniserSleevePowerFlow)

    @property
    def torque_converter_power_flow(
        self: "CastSelf",
    ) -> "_4265.TorqueConverterPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4265

        return self.__parent__._cast(_4265.TorqueConverterPowerFlow)

    @property
    def torque_converter_pump_power_flow(
        self: "CastSelf",
    ) -> "_4266.TorqueConverterPumpPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4266

        return self.__parent__._cast(_4266.TorqueConverterPumpPowerFlow)

    @property
    def torque_converter_turbine_power_flow(
        self: "CastSelf",
    ) -> "_4267.TorqueConverterTurbinePowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4267

        return self.__parent__._cast(_4267.TorqueConverterTurbinePowerFlow)

    @property
    def unbalanced_mass_power_flow(self: "CastSelf") -> "_4268.UnbalancedMassPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4268

        return self.__parent__._cast(_4268.UnbalancedMassPowerFlow)

    @property
    def virtual_component_power_flow(
        self: "CastSelf",
    ) -> "_4269.VirtualComponentPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4269

        return self.__parent__._cast(_4269.VirtualComponentPowerFlow)

    @property
    def worm_gear_power_flow(self: "CastSelf") -> "_4271.WormGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4271

        return self.__parent__._cast(_4271.WormGearPowerFlow)

    @property
    def worm_gear_set_power_flow(self: "CastSelf") -> "_4272.WormGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4272

        return self.__parent__._cast(_4272.WormGearSetPowerFlow)

    @property
    def zerol_bevel_gear_power_flow(
        self: "CastSelf",
    ) -> "_4274.ZerolBevelGearPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4274

        return self.__parent__._cast(_4274.ZerolBevelGearPowerFlow)

    @property
    def zerol_bevel_gear_set_power_flow(
        self: "CastSelf",
    ) -> "_4275.ZerolBevelGearSetPowerFlow":
        from mastapy._private.system_model.analyses_and_results.power_flows import _4275

        return self.__parent__._cast(_4275.ZerolBevelGearSetPowerFlow)

    @property
    def part_power_flow(self: "CastSelf") -> "PartPowerFlow":
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
class PartPowerFlow(_7720.PartStaticLoadAnalysisCase):
    """PartPowerFlow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_POWER_FLOW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def two_d_drawing_showing_power_flow(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDDrawingShowingPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

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
    def power_flow(self: "Self") -> "_4231.PowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.PowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlow")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def create_viewable(self: "Self") -> "_2309.PowerFlowViewable":
        """mastapy.system_model.drawing.PowerFlowViewable"""
        method_result = pythonnet_method_call(self.wrapped, "CreateViewable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartPowerFlow":
        """Cast to another type.

        Returns:
            _Cast_PartPowerFlow
        """
        return _Cast_PartPowerFlow(self)
