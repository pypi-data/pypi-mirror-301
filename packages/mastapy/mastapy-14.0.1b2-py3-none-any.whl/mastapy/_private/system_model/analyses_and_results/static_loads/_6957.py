"""AbstractAssemblyLoadCase"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.static_loads import _7081

_ABSTRACT_ASSEMBLY_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AbstractAssemblyLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738, _2740, _2744
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _6966,
        _6969,
        _6972,
        _6975,
        _6980,
        _6981,
        _6985,
        _6991,
        _6994,
        _6999,
        _7004,
        _7006,
        _7008,
        _7016,
        _7037,
        _7039,
        _7046,
        _7058,
        _7065,
        _7068,
        _7071,
        _7075,
        _7084,
        _7086,
        _7098,
        _7101,
        _7105,
        _7108,
        _7111,
        _7114,
        _7117,
        _7121,
        _7126,
        _7137,
        _7140,
    )
    from mastapy._private.system_model.part_model import _2490

    Self = TypeVar("Self", bound="AbstractAssemblyLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractAssemblyLoadCase._Cast_AbstractAssemblyLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractAssemblyLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractAssemblyLoadCase:
    """Special nested class for casting AbstractAssemblyLoadCase to subclasses."""

    __parent__: "AbstractAssemblyLoadCase"

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
    def belt_drive_load_case(self: "CastSelf") -> "_6972.BeltDriveLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6972,
        )

        return self.__parent__._cast(_6972.BeltDriveLoadCase)

    @property
    def bevel_differential_gear_set_load_case(
        self: "CastSelf",
    ) -> "_6975.BevelDifferentialGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6975,
        )

        return self.__parent__._cast(_6975.BevelDifferentialGearSetLoadCase)

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
    def clutch_load_case(self: "CastSelf") -> "_6985.ClutchLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6985,
        )

        return self.__parent__._cast(_6985.ClutchLoadCase)

    @property
    def concept_coupling_load_case(self: "CastSelf") -> "_6991.ConceptCouplingLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6991,
        )

        return self.__parent__._cast(_6991.ConceptCouplingLoadCase)

    @property
    def concept_gear_set_load_case(self: "CastSelf") -> "_6994.ConceptGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6994,
        )

        return self.__parent__._cast(_6994.ConceptGearSetLoadCase)

    @property
    def conical_gear_set_load_case(self: "CastSelf") -> "_6999.ConicalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _6999,
        )

        return self.__parent__._cast(_6999.ConicalGearSetLoadCase)

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
    def cycloidal_assembly_load_case(
        self: "CastSelf",
    ) -> "_7008.CycloidalAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7008,
        )

        return self.__parent__._cast(_7008.CycloidalAssemblyLoadCase)

    @property
    def cylindrical_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7016.CylindricalGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7016,
        )

        return self.__parent__._cast(_7016.CylindricalGearSetLoadCase)

    @property
    def face_gear_set_load_case(self: "CastSelf") -> "_7037.FaceGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7037,
        )

        return self.__parent__._cast(_7037.FaceGearSetLoadCase)

    @property
    def flexible_pin_assembly_load_case(
        self: "CastSelf",
    ) -> "_7039.FlexiblePinAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7039,
        )

        return self.__parent__._cast(_7039.FlexiblePinAssemblyLoadCase)

    @property
    def gear_set_load_case(self: "CastSelf") -> "_7046.GearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7046,
        )

        return self.__parent__._cast(_7046.GearSetLoadCase)

    @property
    def hypoid_gear_set_load_case(self: "CastSelf") -> "_7058.HypoidGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7058,
        )

        return self.__parent__._cast(_7058.HypoidGearSetLoadCase)

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
    def microphone_array_load_case(self: "CastSelf") -> "_7075.MicrophoneArrayLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7075,
        )

        return self.__parent__._cast(_7075.MicrophoneArrayLoadCase)

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
    def rolling_ring_assembly_load_case(
        self: "CastSelf",
    ) -> "_7098.RollingRingAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7098,
        )

        return self.__parent__._cast(_7098.RollingRingAssemblyLoadCase)

    @property
    def root_assembly_load_case(self: "CastSelf") -> "_7101.RootAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7101,
        )

        return self.__parent__._cast(_7101.RootAssemblyLoadCase)

    @property
    def specialised_assembly_load_case(
        self: "CastSelf",
    ) -> "_7105.SpecialisedAssemblyLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7105,
        )

        return self.__parent__._cast(_7105.SpecialisedAssemblyLoadCase)

    @property
    def spiral_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7108.SpiralBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7108,
        )

        return self.__parent__._cast(_7108.SpiralBevelGearSetLoadCase)

    @property
    def spring_damper_load_case(self: "CastSelf") -> "_7111.SpringDamperLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7111,
        )

        return self.__parent__._cast(_7111.SpringDamperLoadCase)

    @property
    def straight_bevel_diff_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7114.StraightBevelDiffGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7114,
        )

        return self.__parent__._cast(_7114.StraightBevelDiffGearSetLoadCase)

    @property
    def straight_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7117.StraightBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7117,
        )

        return self.__parent__._cast(_7117.StraightBevelGearSetLoadCase)

    @property
    def synchroniser_load_case(self: "CastSelf") -> "_7121.SynchroniserLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7121,
        )

        return self.__parent__._cast(_7121.SynchroniserLoadCase)

    @property
    def torque_converter_load_case(self: "CastSelf") -> "_7126.TorqueConverterLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7126,
        )

        return self.__parent__._cast(_7126.TorqueConverterLoadCase)

    @property
    def worm_gear_set_load_case(self: "CastSelf") -> "_7137.WormGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7137,
        )

        return self.__parent__._cast(_7137.WormGearSetLoadCase)

    @property
    def zerol_bevel_gear_set_load_case(
        self: "CastSelf",
    ) -> "_7140.ZerolBevelGearSetLoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7140,
        )

        return self.__parent__._cast(_7140.ZerolBevelGearSetLoadCase)

    @property
    def abstract_assembly_load_case(self: "CastSelf") -> "AbstractAssemblyLoadCase":
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
class AbstractAssemblyLoadCase(_7081.PartLoadCase):
    """AbstractAssemblyLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_ASSEMBLY_LOAD_CASE

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
    def cast_to(self: "Self") -> "_Cast_AbstractAssemblyLoadCase":
        """Cast to another type.

        Returns:
            _Cast_AbstractAssemblyLoadCase
        """
        return _Cast_AbstractAssemblyLoadCase(self)
