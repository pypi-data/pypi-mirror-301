"""InterMountableComponentConnectionCompoundModalAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
    _4880,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound",
    "InterMountableComponentConnectionCompoundModalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4757
    from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
        _4850,
        _4854,
        _4857,
        _4862,
        _4867,
        _4872,
        _4875,
        _4878,
        _4883,
        _4885,
        _4893,
        _4899,
        _4904,
        _4908,
        _4912,
        _4915,
        _4918,
        _4928,
        _4937,
        _4940,
        _4947,
        _4950,
        _4953,
        _4956,
        _4965,
        _4971,
        _4974,
    )

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionCompoundModalAnalysis"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundModalAnalysis._Cast_InterMountableComponentConnectionCompoundModalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundModalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundModalAnalysis:
    """Special nested class for casting InterMountableComponentConnectionCompoundModalAnalysis to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundModalAnalysis"

    @property
    def connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4880.ConnectionCompoundModalAnalysis":
        return self.__parent__._cast(_4880.ConnectionCompoundModalAnalysis)

    @property
    def connection_compound_analysis(
        self: "CastSelf",
    ) -> "_7711.ConnectionCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7711,
        )

        return self.__parent__._cast(_7711.ConnectionCompoundAnalysis)

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
    def agma_gleason_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4850.AGMAGleasonConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4850,
        )

        return self.__parent__._cast(
            _4850.AGMAGleasonConicalGearMeshCompoundModalAnalysis
        )

    @property
    def belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4854.BeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4854,
        )

        return self.__parent__._cast(_4854.BeltConnectionCompoundModalAnalysis)

    @property
    def bevel_differential_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4857.BevelDifferentialGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4857,
        )

        return self.__parent__._cast(
            _4857.BevelDifferentialGearMeshCompoundModalAnalysis
        )

    @property
    def bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4862.BevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4862,
        )

        return self.__parent__._cast(_4862.BevelGearMeshCompoundModalAnalysis)

    @property
    def clutch_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4867.ClutchConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4867,
        )

        return self.__parent__._cast(_4867.ClutchConnectionCompoundModalAnalysis)

    @property
    def concept_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4872.ConceptCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4872,
        )

        return self.__parent__._cast(
            _4872.ConceptCouplingConnectionCompoundModalAnalysis
        )

    @property
    def concept_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4875.ConceptGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4875,
        )

        return self.__parent__._cast(_4875.ConceptGearMeshCompoundModalAnalysis)

    @property
    def conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4878.ConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4878,
        )

        return self.__parent__._cast(_4878.ConicalGearMeshCompoundModalAnalysis)

    @property
    def coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4883.CouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4883,
        )

        return self.__parent__._cast(_4883.CouplingConnectionCompoundModalAnalysis)

    @property
    def cvt_belt_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4885.CVTBeltConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4885,
        )

        return self.__parent__._cast(_4885.CVTBeltConnectionCompoundModalAnalysis)

    @property
    def cylindrical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4893.CylindricalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4893,
        )

        return self.__parent__._cast(_4893.CylindricalGearMeshCompoundModalAnalysis)

    @property
    def face_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4899.FaceGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4899,
        )

        return self.__parent__._cast(_4899.FaceGearMeshCompoundModalAnalysis)

    @property
    def gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4904.GearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4904,
        )

        return self.__parent__._cast(_4904.GearMeshCompoundModalAnalysis)

    @property
    def hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4908.HypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4908,
        )

        return self.__parent__._cast(_4908.HypoidGearMeshCompoundModalAnalysis)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4912.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4912,
        )

        return self.__parent__._cast(
            _4912.KlingelnbergCycloPalloidConicalGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4915.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4915,
        )

        return self.__parent__._cast(
            _4915.KlingelnbergCycloPalloidHypoidGearMeshCompoundModalAnalysis
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4918.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4918,
        )

        return self.__parent__._cast(
            _4918.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4928.PartToPartShearCouplingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4928,
        )

        return self.__parent__._cast(
            _4928.PartToPartShearCouplingConnectionCompoundModalAnalysis
        )

    @property
    def ring_pins_to_disc_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4937.RingPinsToDiscConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4937,
        )

        return self.__parent__._cast(
            _4937.RingPinsToDiscConnectionCompoundModalAnalysis
        )

    @property
    def rolling_ring_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4940.RollingRingConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4940,
        )

        return self.__parent__._cast(_4940.RollingRingConnectionCompoundModalAnalysis)

    @property
    def spiral_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4947.SpiralBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4947,
        )

        return self.__parent__._cast(_4947.SpiralBevelGearMeshCompoundModalAnalysis)

    @property
    def spring_damper_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4950.SpringDamperConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4950,
        )

        return self.__parent__._cast(_4950.SpringDamperConnectionCompoundModalAnalysis)

    @property
    def straight_bevel_diff_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4953.StraightBevelDiffGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4953,
        )

        return self.__parent__._cast(
            _4953.StraightBevelDiffGearMeshCompoundModalAnalysis
        )

    @property
    def straight_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4956.StraightBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4956,
        )

        return self.__parent__._cast(_4956.StraightBevelGearMeshCompoundModalAnalysis)

    @property
    def torque_converter_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4965.TorqueConverterConnectionCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4965,
        )

        return self.__parent__._cast(
            _4965.TorqueConverterConnectionCompoundModalAnalysis
        )

    @property
    def worm_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4971.WormGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4971,
        )

        return self.__parent__._cast(_4971.WormGearMeshCompoundModalAnalysis)

    @property
    def zerol_bevel_gear_mesh_compound_modal_analysis(
        self: "CastSelf",
    ) -> "_4974.ZerolBevelGearMeshCompoundModalAnalysis":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.compound import (
            _4974,
        )

        return self.__parent__._cast(_4974.ZerolBevelGearMeshCompoundModalAnalysis)

    @property
    def inter_mountable_component_connection_compound_modal_analysis(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundModalAnalysis":
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
class InterMountableComponentConnectionCompoundModalAnalysis(
    _4880.ConnectionCompoundModalAnalysis
):
    """InterMountableComponentConnectionCompoundModalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_MODAL_ANALYSIS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_4757.InterMountableComponentConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def connection_analysis_cases_ready(
        self: "Self",
    ) -> "List[_4757.InterMountableComponentConnectionModalAnalysis]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.InterMountableComponentConnectionModalAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_InterMountableComponentConnectionCompoundModalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundModalAnalysis
        """
        return _Cast_InterMountableComponentConnectionCompoundModalAnalysis(self)
