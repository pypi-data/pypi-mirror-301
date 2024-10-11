"""GearMeshAdvancedSystemDeflection"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7496,
)

_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "GearMeshAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1561
    from mastapy._private.system_model.analyses_and_results import _2736, _2738, _2740
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7434,
        _7441,
        _7446,
        _7459,
        _7462,
        _7464,
        _7478,
        _7485,
        _7494,
        _7498,
        _7501,
        _7504,
        _7534,
        _7540,
        _7543,
        _7559,
        _7562,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7710,
        _7713,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2368

    Self = TypeVar("Self", bound="GearMeshAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshAdvancedSystemDeflection._Cast_GearMeshAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshAdvancedSystemDeflection:
    """Special nested class for casting GearMeshAdvancedSystemDeflection to subclasses."""

    __parent__: "GearMeshAdvancedSystemDeflection"

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7496.InterMountableComponentConnectionAdvancedSystemDeflection":
        return self.__parent__._cast(
            _7496.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7464.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7464,
        )

        return self.__parent__._cast(_7464.ConnectionAdvancedSystemDeflection)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7713.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7713,
        )

        return self.__parent__._cast(_7713.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7710.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7710,
        )

        return self.__parent__._cast(_7710.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2736.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2736

        return self.__parent__._cast(_2736.ConnectionAnalysis)

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
    def agma_gleason_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7434.AGMAGleasonConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7434,
        )

        return self.__parent__._cast(
            _7434.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def bevel_differential_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7441.BevelDifferentialGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7441,
        )

        return self.__parent__._cast(
            _7441.BevelDifferentialGearMeshAdvancedSystemDeflection
        )

    @property
    def bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7446.BevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7446,
        )

        return self.__parent__._cast(_7446.BevelGearMeshAdvancedSystemDeflection)

    @property
    def concept_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7459.ConceptGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7459,
        )

        return self.__parent__._cast(_7459.ConceptGearMeshAdvancedSystemDeflection)

    @property
    def conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7462.ConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7462,
        )

        return self.__parent__._cast(_7462.ConicalGearMeshAdvancedSystemDeflection)

    @property
    def cylindrical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7478.CylindricalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7478,
        )

        return self.__parent__._cast(_7478.CylindricalGearMeshAdvancedSystemDeflection)

    @property
    def face_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7485.FaceGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7485,
        )

        return self.__parent__._cast(_7485.FaceGearMeshAdvancedSystemDeflection)

    @property
    def hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7494.HypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7494,
        )

        return self.__parent__._cast(_7494.HypoidGearMeshAdvancedSystemDeflection)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7498.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7498,
        )

        return self.__parent__._cast(
            _7498.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7501.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7501,
        )

        return self.__parent__._cast(
            _7501.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7504.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7504,
        )

        return self.__parent__._cast(
            _7504.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def spiral_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7534.SpiralBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7534,
        )

        return self.__parent__._cast(_7534.SpiralBevelGearMeshAdvancedSystemDeflection)

    @property
    def straight_bevel_diff_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7540.StraightBevelDiffGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7540,
        )

        return self.__parent__._cast(
            _7540.StraightBevelDiffGearMeshAdvancedSystemDeflection
        )

    @property
    def straight_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7543.StraightBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7543,
        )

        return self.__parent__._cast(
            _7543.StraightBevelGearMeshAdvancedSystemDeflection
        )

    @property
    def worm_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7559.WormGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7559,
        )

        return self.__parent__._cast(_7559.WormGearMeshAdvancedSystemDeflection)

    @property
    def zerol_bevel_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7562.ZerolBevelGearMeshAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7562,
        )

        return self.__parent__._cast(_7562.ZerolBevelGearMeshAdvancedSystemDeflection)

    @property
    def gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "GearMeshAdvancedSystemDeflection":
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
class GearMeshAdvancedSystemDeflection(
    _7496.InterMountableComponentConnectionAdvancedSystemDeflection
):
    """GearMeshAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def mean_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def mean_moment_about_centre_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMomentAboutCentreFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_separation_left_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSeparationLeftFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    def minimum_separation_right_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSeparationRightFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    def number_of_teeth_passed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethPassed")

        if temp is None:
            return 0.0

        return temp

    @number_of_teeth_passed.setter
    @enforce_parameter_types
    def number_of_teeth_passed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethPassed",
            float(value) if value is not None else 0.0,
        )

    @property
    def operating_total_contact_ratio_for_first_tooth_passing_period(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OperatingTotalContactRatioForFirstToothPassingPeriod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_to_peak_moment_about_centre_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PeakToPeakMomentAboutCentreFromLTCA"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def peak_to_peak_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def signed_root_mean_square_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedRootMeanSquareMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    def connection_design(self: "Self") -> "_2368.GearMesh":
        """mastapy.system_model.connections_and_sockets.gears.GearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def misalignment_fourier_series_for_first_tooth_passing_period(
        self: "Self",
    ) -> "_1561.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MisalignmentFourierSeriesForFirstToothPassingPeriod"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_GearMeshAdvancedSystemDeflection
        """
        return _Cast_GearMeshAdvancedSystemDeflection(self)
