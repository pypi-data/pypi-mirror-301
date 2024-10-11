"""AssemblyCompoundDynamicAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
    _6552,
)

_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound",
    "AssemblyCompoundDynamicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7715,
        _7718,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses import (
        _6426,
    )
    from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
        _6560,
        _6562,
        _6565,
        _6571,
        _6572,
        _6573,
        _6578,
        _6583,
        _6593,
        _6595,
        _6597,
        _6601,
        _6607,
        _6608,
        _6609,
        _6616,
        _6623,
        _6626,
        _6627,
        _6628,
        _6630,
        _6632,
        _6633,
        _6634,
        _6639,
        _6640,
        _6641,
        _6643,
        _6645,
        _6648,
        _6649,
        _6650,
        _6655,
        _6656,
        _6661,
        _6664,
        _6667,
        _6671,
        _6675,
        _6679,
        _6682,
    )
    from mastapy._private.system_model.part_model import _2489

    Self = TypeVar("Self", bound="AssemblyCompoundDynamicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AssemblyCompoundDynamicAnalysis._Cast_AssemblyCompoundDynamicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AssemblyCompoundDynamicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AssemblyCompoundDynamicAnalysis:
    """Special nested class for casting AssemblyCompoundDynamicAnalysis to subclasses."""

    __parent__: "AssemblyCompoundDynamicAnalysis"

    @property
    def abstract_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6552.AbstractAssemblyCompoundDynamicAnalysis":
        return self.__parent__._cast(_6552.AbstractAssemblyCompoundDynamicAnalysis)

    @property
    def part_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6633.PartCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6633,
        )

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
    def root_assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "_6648.RootAssemblyCompoundDynamicAnalysis":
        from mastapy._private.system_model.analyses_and_results.dynamic_analyses.compound import (
            _6648,
        )

        return self.__parent__._cast(_6648.RootAssemblyCompoundDynamicAnalysis)

    @property
    def assembly_compound_dynamic_analysis(
        self: "CastSelf",
    ) -> "AssemblyCompoundDynamicAnalysis":
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
class AssemblyCompoundDynamicAnalysis(_6552.AbstractAssemblyCompoundDynamicAnalysis):
    """AssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def component_design(self: "Self") -> "_2489.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_design(self: "Self") -> "_2489.Assembly":
        """mastapy.system_model.part_model.Assembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6426.AssemblyDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bearings(self: "Self") -> "List[_6560.BearingCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BearingCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def belt_drives(self: "Self") -> "List[_6562.BeltDriveCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltDriveCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeltDrives")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bevel_differential_gear_sets(
        self: "Self",
    ) -> "List[_6565.BevelDifferentialGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelDifferentialGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolted_joints(self: "Self") -> "List[_6572.BoltedJointCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltedJointCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoltedJoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def bolts(self: "Self") -> "List[_6571.BoltCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bolts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cv_ts(self: "Self") -> "List[_6593.CVTCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CVTs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def clutches(self: "Self") -> "List[_6573.ClutchCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clutches")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_couplings(
        self: "Self",
    ) -> "List[_6578.ConceptCouplingCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def concept_gear_sets(
        self: "Self",
    ) -> "List[_6583.ConceptGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConceptGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_assemblies(
        self: "Self",
    ) -> "List[_6595.CycloidalAssemblyCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CycloidalAssemblyCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cycloidal_discs(
        self: "Self",
    ) -> "List[_6597.CycloidalDiscCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CycloidalDiscCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CycloidalDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cylindrical_gear_sets(
        self: "Self",
    ) -> "List[_6601.CylindricalGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def fe_parts(self: "Self") -> "List[_6608.FEPartCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FEPartCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def face_gear_sets(
        self: "Self",
    ) -> "List[_6607.FaceGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def flexible_pin_assemblies(
        self: "Self",
    ) -> "List[_6609.FlexiblePinAssemblyCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FlexiblePinAssemblyCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlexiblePinAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def hypoid_gear_sets(
        self: "Self",
    ) -> "List[_6616.HypoidGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(
        self: "Self",
    ) -> "List[_6623.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(
        self: "Self",
    ) -> (
        "List[_6626.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]"
    ):
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidSpiralBevelGearSets"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def mass_discs(self: "Self") -> "List[_6627.MassDiscCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MassDiscCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassDiscs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def measurement_components(
        self: "Self",
    ) -> "List[_6628.MeasurementComponentCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MeasurementComponentCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeasurementComponents")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def microphones(self: "Self") -> "List[_6630.MicrophoneCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MicrophoneCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Microphones")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def oil_seals(self: "Self") -> "List[_6632.OilSealCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.OilSealCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSeals")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def part_to_part_shear_couplings(
        self: "Self",
    ) -> "List[_6634.PartToPartShearCouplingCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartToPartShearCouplings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def planet_carriers(
        self: "Self",
    ) -> "List[_6639.PlanetCarrierCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetCarrierCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetCarriers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def point_loads(self: "Self") -> "List[_6640.PointLoadCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PointLoadCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def power_loads(self: "Self") -> "List[_6641.PowerLoadCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PowerLoadCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLoads")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def ring_pins(self: "Self") -> "List[_6643.RingPinsCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RingPinsCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingPins")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def rolling_ring_assemblies(
        self: "Self",
    ) -> "List[_6645.RollingRingAssemblyCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingAssemblyCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingRingAssemblies")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shaft_hub_connections(
        self: "Self",
    ) -> "List[_6650.ShaftHubConnectionCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftHubConnectionCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftHubConnections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def shafts(self: "Self") -> "List[_6649.ShaftCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shafts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spiral_bevel_gear_sets(
        self: "Self",
    ) -> "List[_6655.SpiralBevelGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def spring_dampers(
        self: "Self",
    ) -> "List[_6656.SpringDamperCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDampers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_diff_gear_sets(
        self: "Self",
    ) -> "List[_6661.StraightBevelDiffGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelDiffGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def straight_bevel_gear_sets(
        self: "Self",
    ) -> "List[_6664.StraightBevelGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StraightBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def synchronisers(
        self: "Self",
    ) -> "List[_6667.SynchroniserCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Synchronisers")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def torque_converters(
        self: "Self",
    ) -> "List[_6671.TorqueConverterCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueConverters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def unbalanced_masses(
        self: "Self",
    ) -> "List[_6675.UnbalancedMassCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.UnbalancedMassCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnbalancedMasses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def worm_gear_sets(
        self: "Self",
    ) -> "List[_6679.WormGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def zerol_bevel_gear_sets(
        self: "Self",
    ) -> "List[_6682.ZerolBevelGearSetCompoundDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearSetCompoundDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def assembly_analysis_cases(self: "Self") -> "List[_6426.AssemblyDynamicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.dynamic_analyses.AssemblyDynamicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_AssemblyCompoundDynamicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_AssemblyCompoundDynamicAnalysis
        """
        return _Cast_AssemblyCompoundDynamicAnalysis(self)
