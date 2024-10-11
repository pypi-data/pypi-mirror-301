"""ComponentLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7081

_COMPONENT_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "ComponentLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6958,
        _6959,
        _6964,
        _6970,
        _6973,
        _6976,
        _6977,
        _6978,
        _6982,
        _6984,
        _6990,
        _6992,
        _6995,
        _7001,
        _7003,
        _7007,
        _7010,
        _7012,
        _7017,
        _7020,
        _7034,
        _7035,
        _7038,
        _7041,
        _7047,
        _7056,
        _7063,
        _7066,
        _7069,
        _7072,
        _7073,
        _7076,
        _7077,
        _7079,
        _7083,
        _7088,
        _7091,
        _7092,
        _7093,
        _7096,
        _7100,
        _7102,
        _7103,
        _7106,
        _7110,
        _7112,
        _7115,
        _7118,
        _7119,
        _7120,
        _7122,
        _7123,
        _7127,
        _7128,
        _7133,
        _7134,
        _7135,
        _7138,
    )
    from mastapy._private.system_model.part_model import _2500

    Self = TypeVar("Self", bound="ComponentLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ComponentLoadCase._Cast_ComponentLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ComponentLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ComponentLoadCase:
    """Special nested class for casting ComponentLoadCase to subclasses."""

    __parent__: "ComponentLoadCase"

    @property
    def part_load_case(self: "CastSelf") -> "_7081.PartLoadCase":
        return self.__parent__._cast(_7081.PartLoadCase)

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
    def bearing_load_case(self: "CastSelf") -> "_6970.BearingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6970,
        )

        return self.__parent__._cast(_6970.BearingLoadCase)

    @property
    def bevel_differential_gear_load_case(
        self: "CastSelf",
    ) -> "_6973.BevelDifferentialGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6973,
        )

        return self.__parent__._cast(_6973.BevelDifferentialGearLoadCase)

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
    def concept_coupling_half_load_case(
        self: "CastSelf",
    ) -> "_6990.ConceptCouplingHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6990,
        )

        return self.__parent__._cast(_6990.ConceptCouplingHalfLoadCase)

    @property
    def concept_gear_load_case(self: "CastSelf") -> "_6992.ConceptGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6992,
        )

        return self.__parent__._cast(_6992.ConceptGearLoadCase)

    @property
    def conical_gear_load_case(self: "CastSelf") -> "_6995.ConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6995,
        )

        return self.__parent__._cast(_6995.ConicalGearLoadCase)

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
    def cvt_pulley_load_case(self: "CastSelf") -> "_7007.CVTPulleyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7007,
        )

        return self.__parent__._cast(_7007.CVTPulleyLoadCase)

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
    def fe_part_load_case(self: "CastSelf") -> "_7038.FEPartLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7038,
        )

        return self.__parent__._cast(_7038.FEPartLoadCase)

    @property
    def gear_load_case(self: "CastSelf") -> "_7041.GearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7041,
        )

        return self.__parent__._cast(_7041.GearLoadCase)

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
    def klingelnberg_cyclo_palloid_conical_gear_load_case(
        self: "CastSelf",
    ) -> "_7063.KlingelnbergCycloPalloidConicalGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7063,
        )

        return self.__parent__._cast(_7063.KlingelnbergCycloPalloidConicalGearLoadCase)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_load_case(
        self: "CastSelf",
    ) -> "_7066.KlingelnbergCycloPalloidHypoidGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7066,
        )

        return self.__parent__._cast(_7066.KlingelnbergCycloPalloidHypoidGearLoadCase)

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
    def rolling_ring_load_case(self: "CastSelf") -> "_7100.RollingRingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7100,
        )

        return self.__parent__._cast(_7100.RollingRingLoadCase)

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
    def spiral_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7106.SpiralBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7106,
        )

        return self.__parent__._cast(_7106.SpiralBevelGearLoadCase)

    @property
    def spring_damper_half_load_case(
        self: "CastSelf",
    ) -> "_7110.SpringDamperHalfLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7110,
        )

        return self.__parent__._cast(_7110.SpringDamperHalfLoadCase)

    @property
    def straight_bevel_diff_gear_load_case(
        self: "CastSelf",
    ) -> "_7112.StraightBevelDiffGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7112,
        )

        return self.__parent__._cast(_7112.StraightBevelDiffGearLoadCase)

    @property
    def straight_bevel_gear_load_case(
        self: "CastSelf",
    ) -> "_7115.StraightBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7115,
        )

        return self.__parent__._cast(_7115.StraightBevelGearLoadCase)

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
    def zerol_bevel_gear_load_case(self: "CastSelf") -> "_7138.ZerolBevelGearLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7138,
        )

        return self.__parent__._cast(_7138.ZerolBevelGearLoadCase)

    @property
    def component_load_case(self: "CastSelf") -> "ComponentLoadCase":
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
class ComponentLoadCase(_7081.PartLoadCase):
    """ComponentLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COMPONENT_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def additional_modal_damping_ratio(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AdditionalModalDampingRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @additional_modal_damping_ratio.setter
    @enforce_parameter_types
    def additional_modal_damping_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AdditionalModalDampingRatio", value)

    @property
    def is_connected_to_ground(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsConnectedToGround")

        if temp is None:
            return False

        return temp

    @property
    def is_torsionally_free(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsTorsionallyFree")

        if temp is None:
            return False

        return temp

    @property
    def magnitude_of_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnitudeOfRotation")

        if temp is None:
            return 0.0

        return temp

    @magnitude_of_rotation.setter
    @enforce_parameter_types
    def magnitude_of_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnitudeOfRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    def rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rayleigh_damping_beta.setter
    @enforce_parameter_types
    def rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RayleighDampingBeta", value)

    @property
    def rotation_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotationAngle")

        if temp is None:
            return 0.0

        return temp

    @rotation_angle.setter
    @enforce_parameter_types
    def rotation_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RotationAngle", float(value) if value is not None else 0.0
        )

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
    def cast_to(self: "Self") -> "_Cast_ComponentLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ComponentLoadCase
        """
        return _Cast_ComponentLoadCase(self)
