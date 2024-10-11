"""PartLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results import _2744
from mastapy._private.system_model.analyses_and_results.static_loads import _6955, _7048

_PART_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PartLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1428
    from mastapy._private.system_model.analyses_and_results import _2738, _2740
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6956,
        _6957,
        _6958,
        _6959,
        _6964,
        _6966,
        _6969,
        _6970,
        _6972,
        _6973,
        _6975,
        _6976,
        _6977,
        _6978,
        _6980,
        _6981,
        _6982,
        _6984,
        _6985,
        _6988,
        _6990,
        _6991,
        _6992,
        _6994,
        _6995,
        _6999,
        _7001,
        _7003,
        _7004,
        _7006,
        _7007,
        _7008,
        _7010,
        _7012,
        _7016,
        _7017,
        _7020,
        _7034,
        _7035,
        _7037,
        _7038,
        _7039,
        _7041,
        _7046,
        _7047,
        _7056,
        _7058,
        _7063,
        _7065,
        _7066,
        _7068,
        _7069,
        _7071,
        _7072,
        _7073,
        _7075,
        _7076,
        _7077,
        _7079,
        _7083,
        _7084,
        _7086,
        _7088,
        _7091,
        _7092,
        _7093,
        _7096,
        _7098,
        _7100,
        _7101,
        _7102,
        _7103,
        _7105,
        _7106,
        _7108,
        _7110,
        _7111,
        _7112,
        _7114,
        _7115,
        _7117,
        _7118,
        _7119,
        _7120,
        _7121,
        _7122,
        _7123,
        _7126,
        _7127,
        _7128,
        _7133,
        _7134,
        _7135,
        _7137,
        _7138,
        _7140,
    )
    from mastapy._private.system_model.part_model import _2526

    Self = TypeVar("Self", bound="PartLoadCase")
    CastSelf = TypeVar("CastSelf", bound="PartLoadCase._Cast_PartLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("PartLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartLoadCase:
    """Special nested class for casting PartLoadCase to subclasses."""

    __parent__: "PartLoadCase"

    @property
    def part_analysis(self: "CastSelf") -> "_2744.PartAnalysis":
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
    def abstract_assembly_load_case(
        self: "CastSelf",
    ) -> "_6957.AbstractAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6957,
        )

        return self.__parent__._cast(_6957.AbstractAssemblyLoadCase)

    @property
    def abstract_shaft_load_case(self: "CastSelf") -> "_6958.AbstractShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6958,
        )

        return self.__parent__._cast(_6958.AbstractShaftLoadCase)

    @property
    def abstract_shaft_or_housing_load_case(
        self: "CastSelf",
    ) -> "_6959.AbstractShaftOrHousingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6959,
        )

        return self.__parent__._cast(_6959.AbstractShaftOrHousingLoadCase)

    @property
    def agma_gleason_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_6964.AGMAGleasonConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6964,
        )

        return self.__parent__._cast(_6964.AGMAGleasonConicalGearLoadCase)

    @property
    def agma_gleason_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6966.AGMAGleasonConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6966,
        )

        return self.__parent__._cast(_6966.AGMAGleasonConicalGearSetLoadCase)

    @property
    def assembly_load_case(self: "CastSelf") -> "_6969.AssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6969,
        )

        return self.__parent__._cast(_6969.AssemblyLoadCase)

    @property
    def bearing_load_case(self: "CastSelf") -> "_6970.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6970,
        )

        return self.__parent__._cast(_6970.BearingLoadCase)

    @property
    def belt_drive_load_case(self: "CastSelf") -> "_6972.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialGearLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6975.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelDifferentialGearSetLoadCase)

    @property
    def bevel_differential_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_6976.BevelDifferentialPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6976,
        )

        return self.__parent__._cast(_6976.BevelDifferentialPlanetGearLoadCase)

    @property
    def bevel_differential_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_6977.BevelDifferentialSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6977,
        )

        return self.__parent__._cast(_6977.BevelDifferentialSunGearLoadCase)

    @property
    def bevel_gear_load_case(self: "CastSelf") -> "_6978.BevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6978,
        )

        return self.__parent__._cast(_6978.BevelGearLoadCase)

    @property
    def bevel_gear_set_load_case(self: "CastSelf") -> "_6980.BevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6980,
        )

        return self.__parent__._cast(_6980.BevelGearSetLoadCase)

    @property
    def bolted_joint_load_case(self: "CastSelf") -> "_6981.BoltedJointLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6981,
        )

        return self.__parent__._cast(_6981.BoltedJointLoadCase)

    @property
    def bolt_load_case(self: "CastSelf") -> "_6982.BoltLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6982,
        )

        return self.__parent__._cast(_6982.BoltLoadCase)

    @property
    def clutch_half_load_case(self: "CastSelf") -> "_6984.ClutchHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6984,
        )

        return self.__parent__._cast(_6984.ClutchHalfLoadCase)

    @property
    def clutch_load_case(self: "CastSelf") -> "_6985.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ClutchLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "_6988.ComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6988,
        )

        return self.__parent__._cast(_6988.ComponentLoadCase)

    @property
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6990.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ConceptCouplingHalfLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6991.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptCouplingLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6992.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConceptGearLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6994.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6994,
        )

        return self.__parent__._cast(_6994.ConceptGearSetLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6995.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6995,
        )

        return self.__parent__._cast(_6995.ConicalGearLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6999.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6999,
        )

        return self.__parent__._cast(_6999.ConicalGearSetLoadCase)

    @property
    def connector_load_case(self: "CastSelf") -> "_7001.ConnectorLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7001,
        )

        return self.__parent__._cast(_7001.ConnectorLoadCase)

    @property
    def coupling_half_load_case(self: "CastSelf") -> "_7003.CouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7003,
        )

        return self.__parent__._cast(_7003.CouplingHalfLoadCase)

    @property
    def coupling_load_case(self: "CastSelf") -> "_7004.CouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7004,
        )

        return self.__parent__._cast(_7004.CouplingLoadCase)

    @property
    def cvt_load_case(self: "CastSelf") -> "_7006.CVTLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7006,
        )

        return self.__parent__._cast(_7006.CVTLoadCase)

    @property
    def cvt_pulley_load_case(self: "CastSelf") -> "_7007.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CVTPulleyLoadCase)

    @property
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7008.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7008,
        )

        return self.__parent__._cast(_7008.CycloidalAssemblyLoadCase)

    @property
    def cycloidal_disc_load_case(self: "CastSelf") -> "_7010.CycloidalDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7010,
        )

        return self.__parent__._cast(_7010.CycloidalDiscLoadCase)

    @property
    def cylindrical_gear_load_case(self: "CastSelf") -> "_7012.CylindricalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7012,
        )

        return self.__parent__._cast(_7012.CylindricalGearLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7016.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7016,
        )

        return self.__parent__._cast(_7016.CylindricalGearSetLoadCase)

    @property
    def cylindrical_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7017.CylindricalPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7017,
        )

        return self.__parent__._cast(_7017.CylindricalPlanetGearLoadCase)

    @property
    def datum_load_case(self: "CastSelf") -> "_7020.DatumLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7020,
        )

        return self.__parent__._cast(_7020.DatumLoadCase)

    @property
    def external_cad_model_load_case(
        self: "CastSelf",
    ) -> "_7034.ExternalCADModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7034,
        )

        return self.__parent__._cast(_7034.ExternalCADModelLoadCase)

    @property
    def face_gear_load_case(self: "CastSelf") -> "_7035.FaceGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7035,
        )

        return self.__parent__._cast(_7035.FaceGearLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7037.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7037,
        )

        return self.__parent__._cast(_7037.FaceGearSetLoadCase)

    @property
    def fe_part_load_case(self: "CastSelf") -> "_7038.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.FEPartLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7039.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7039,
        )

        return self.__parent__._cast(_7039.FlexiblePinAssemblyLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7041.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7041,
        )

        return self.__parent__._cast(_7041.GearLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7046.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7046,
        )

        return self.__parent__._cast(_7046.GearSetLoadCase)

    @property
    def guide_dxf_model_load_case(self: "CastSelf") -> "_7047.GuideDxfModelLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7047,
        )

        return self.__parent__._cast(_7047.GuideDxfModelLoadCase)

    @property
    def hypoid_gear_load_case(self: "CastSelf") -> "_7056.HypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7056,
        )

        return self.__parent__._cast(_7056.HypoidGearLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7058.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7058,
        )

        return self.__parent__._cast(_7058.HypoidGearSetLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7065.KlingelnbergCycloPalloidConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7065,
        )

        return self.__parent__._cast(
            _7065.KlingelnbergCycloPalloidConicalGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(_7066.KlingelnbergCycloPalloidHypoidGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7068.KlingelnbergCycloPalloidHypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7068,
        )

        return self.__parent__._cast(
            _7068.KlingelnbergCycloPalloidHypoidGearSetLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7069.KlingelnbergCycloPalloidSpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7069,
        )

        return self.__parent__._cast(
            _7069.KlingelnbergCycloPalloidSpiralBevelGearLoadCase
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7071.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7071,
        )

        return self.__parent__._cast(
            _7071.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase
        )

    @property
    def mass_disc_load_case(self: "CastSelf") -> "_7072.MassDiscLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7072,
        )

        return self.__parent__._cast(_7072.MassDiscLoadCase)

    @property
    def measurement_component_load_case(
        self: "CastSelf",
    ) -> "_7073.MeasurementComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7073,
        )

        return self.__parent__._cast(_7073.MeasurementComponentLoadCase)

    @property
    def microphone_array_load_case(self: "CastSelf") -> "_7075.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7075,
        )

        return self.__parent__._cast(_7075.MicrophoneArrayLoadCase)

    @property
    def microphone_load_case(self: "CastSelf") -> "_7076.MicrophoneLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7076,
        )

        return self.__parent__._cast(_7076.MicrophoneLoadCase)

    @property
    def mountable_component_load_case(
        self: "CastSelf",
    ) -> "_7077.MountableComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7077,
        )

        return self.__parent__._cast(_7077.MountableComponentLoadCase)

    @property
    def oil_seal_load_case(self: "CastSelf") -> "_7079.OilSealLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7079,
        )

        return self.__parent__._cast(_7079.OilSealLoadCase)

    @property
    def part_to_part_shear_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_7083.PartToPartShearCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7083,
        )

        return self.__parent__._cast(_7083.PartToPartShearCouplingHalfLoadCase)

    @property
    def part_to_part_shear_coupling_load_case(
        self: "CastSelf",
    ) -> "_7084.PartToPartShearCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7084,
        )

        return self.__parent__._cast(_7084.PartToPartShearCouplingLoadCase)

    @property
    def planetary_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7086.PlanetaryGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7086,
        )

        return self.__parent__._cast(_7086.PlanetaryGearSetLoadCase)

    @property
    def planet_carrier_load_case(self: "CastSelf") -> "_7088.PlanetCarrierLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7088,
        )

        return self.__parent__._cast(_7088.PlanetCarrierLoadCase)

    @property
    def point_load_load_case(self: "CastSelf") -> "_7091.PointLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7091,
        )

        return self.__parent__._cast(_7091.PointLoadLoadCase)

    @property
    def power_load_load_case(self: "CastSelf") -> "_7092.PowerLoadLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7092,
        )

        return self.__parent__._cast(_7092.PowerLoadLoadCase)

    @property
    def pulley_load_case(self: "CastSelf") -> "_7093.PulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7093,
        )

        return self.__parent__._cast(_7093.PulleyLoadCase)

    @property
    def ring_pins_load_case(self: "CastSelf") -> "_7096.RingPinsLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7096,
        )

        return self.__parent__._cast(_7096.RingPinsLoadCase)

    @property
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7098.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7098,
        )

        return self.__parent__._cast(_7098.RollingRingAssemblyLoadCase)

    @property
    def rolling_ring_load_case(self: "CastSelf") -> "_7100.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.RollingRingLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7101.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7101,
        )

        return self.__parent__._cast(_7101.RootAssemblyLoadCase)

    @property
    def shaft_hub_connection_load_case(
        self: "CastSelf",
    ) -> "_7102.ShaftHubConnectionLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7102,
        )

        return self.__parent__._cast(_7102.ShaftHubConnectionLoadCase)

    @property
    def shaft_load_case(self: "CastSelf") -> "_7103.ShaftLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7103,
        )

        return self.__parent__._cast(_7103.ShaftLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7105.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7106.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7106,
        )

        return self.__parent__._cast(_7106.SpiralBevelGearLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7108.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7110.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.SpringDamperHalfLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7111.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelGearLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7117.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.StraightBevelGearSetLoadCase)

    @property
    def straight_bevel_planet_gear_load_case(
        self: "CastSelf",
    ) -> "_7118.StraightBevelPlanetGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7118,
        )

        return self.__parent__._cast(_7118.StraightBevelPlanetGearLoadCase)

    @property
    def straight_bevel_sun_gear_load_case(
        self: "CastSelf",
    ) -> "_7119.StraightBevelSunGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7119,
        )

        return self.__parent__._cast(_7119.StraightBevelSunGearLoadCase)

    @property
    def synchroniser_half_load_case(
        self: "CastSelf",
    ) -> "_7120.SynchroniserHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7120,
        )

        return self.__parent__._cast(_7120.SynchroniserHalfLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7121.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7121,
        )

        return self.__parent__._cast(_7121.SynchroniserLoadCase)

    @property
    def synchroniser_part_load_case(
        self: "CastSelf",
    ) -> "_7122.SynchroniserPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7122,
        )

        return self.__parent__._cast(_7122.SynchroniserPartLoadCase)

    @property
    def synchroniser_sleeve_load_case(
        self: "CastSelf",
    ) -> "_7123.SynchroniserSleeveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7123,
        )

        return self.__parent__._cast(_7123.SynchroniserSleeveLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7126.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7126,
        )

        return self.__parent__._cast(_7126.TorqueConverterLoadCase)

    @property
    def torque_converter_pump_load_case(
        self: "CastSelf",
    ) -> "_7127.TorqueConverterPumpLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7127,
        )

        return self.__parent__._cast(_7127.TorqueConverterPumpLoadCase)

    @property
    def torque_converter_turbine_load_case(
        self: "CastSelf",
    ) -> "_7128.TorqueConverterTurbineLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7128,
        )

        return self.__parent__._cast(_7128.TorqueConverterTurbineLoadCase)

    @property
    def unbalanced_mass_load_case(self: "CastSelf") -> "_7133.UnbalancedMassLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7133,
        )

        return self.__parent__._cast(_7133.UnbalancedMassLoadCase)

    @property
    def virtual_component_load_case(
        self: "CastSelf",
    ) -> "_7134.VirtualComponentLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7134,
        )

        return self.__parent__._cast(_7134.VirtualComponentLoadCase)

    @property
    def worm_gear_load_case(self: "CastSelf") -> "_7135.WormGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7135,
        )

        return self.__parent__._cast(_7135.WormGearLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7137.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7138.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7138,
        )

        return self.__parent__._cast(_7138.ZerolBevelGearLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7140.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7140,
        )

        return self.__parent__._cast(_7140.ZerolBevelGearSetLoadCase)

    @property
    def part_load_case(self: "CastSelf") -> "PartLoadCase":
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
class PartLoadCase(_2744.PartAnalysis):
    """PartLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def excitation_data_is_up_to_date(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationDataIsUpToDate")

        if temp is None:
            return False

        return temp

    @property
    def harmonic_excitation_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]"""
        temp = pythonnet_property_get(self.wrapped, "HarmonicExcitationType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @harmonic_excitation_type.setter
    @enforce_parameter_types
    def harmonic_excitation_type(
        self: "Self", value: "_7048.HarmonicExcitationType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicExcitationType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "HarmonicExcitationType", value)

    @property
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def load_case_for_harmonic_excitation_type_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "_6955.StaticLoadCase"
    ) -> None:
        wrapper_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.wrapper_type()
        )
        enclosed_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = wrapper_type[enclosed_type](
            value.wrapped if value is not None else None
        )
        pythonnet_property_set(
            self.wrapped,
            "LoadCaseForHarmonicExcitationTypeAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            value,
        )

    @property
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_advanced_system_deflection_current_load_case_set_up.setter
    @enforce_parameter_types
    def use_this_load_case_for_advanced_system_deflection_current_load_case_set_up(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseThisLoadCaseForAdvancedSystemDeflectionCurrentLoadCaseSetUp",
            bool(value) if value is not None else False,
        )

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
    def static_load_case(self: "Self") -> "_6955.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def time_series_load_case(self: "Self") -> "_6956.TimeSeriesLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.TimeSeriesLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeSeriesLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    def clear_user_specified_excitation_data_for_this_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ClearUserSpecifiedExcitationDataForThisLoadCase"
        )

    def get_harmonic_load_data_for_import(self: "Self") -> "_1428.HarmonicLoadDataBase":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataBase"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetHarmonicLoadDataForImport"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PartLoadCase":
        """Cast to another type.

        Returns:
            _Cast_PartLoadCase
        """
        return _Cast_PartLoadCase(self)
