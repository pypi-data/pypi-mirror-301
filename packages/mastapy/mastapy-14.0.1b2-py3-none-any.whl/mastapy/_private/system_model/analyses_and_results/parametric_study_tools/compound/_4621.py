"""InterMountableComponentConnectionCompoundParametricStudyTool"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
    _4591,
)

_INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound",
        "InterMountableComponentConnectionCompoundParametricStudyTool",
    )
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4479,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
        _4561,
        _4565,
        _4568,
        _4573,
        _4578,
        _4583,
        _4586,
        _4589,
        _4594,
        _4596,
        _4604,
        _4610,
        _4615,
        _4619,
        _4623,
        _4626,
        _4629,
        _4639,
        _4648,
        _4651,
        _4658,
        _4661,
        _4664,
        _4667,
        _4676,
        _4682,
        _4685,
    )

    Self = TypeVar(
        "Self", bound="InterMountableComponentConnectionCompoundParametricStudyTool"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="InterMountableComponentConnectionCompoundParametricStudyTool._Cast_InterMountableComponentConnectionCompoundParametricStudyTool",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InterMountableComponentConnectionCompoundParametricStudyTool",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InterMountableComponentConnectionCompoundParametricStudyTool:
    """Special nested class for casting InterMountableComponentConnectionCompoundParametricStudyTool to subclasses."""

    __parent__: "InterMountableComponentConnectionCompoundParametricStudyTool"

    @property
    def connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4591.ConnectionCompoundParametricStudyTool":
        return self.__parent__._cast(_4591.ConnectionCompoundParametricStudyTool)

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
    def agma_gleason_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4561.AGMAGleasonConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4561,
        )

        return self.__parent__._cast(
            _4561.AGMAGleasonConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4565.BeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4565,
        )

        return self.__parent__._cast(_4565.BeltConnectionCompoundParametricStudyTool)

    @property
    def bevel_differential_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4568.BevelDifferentialGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4568,
        )

        return self.__parent__._cast(
            _4568.BevelDifferentialGearMeshCompoundParametricStudyTool
        )

    @property
    def bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4573.BevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4573,
        )

        return self.__parent__._cast(_4573.BevelGearMeshCompoundParametricStudyTool)

    @property
    def clutch_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4578.ClutchConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4578,
        )

        return self.__parent__._cast(_4578.ClutchConnectionCompoundParametricStudyTool)

    @property
    def concept_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4583.ConceptCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4583,
        )

        return self.__parent__._cast(
            _4583.ConceptCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def concept_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4586.ConceptGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4586,
        )

        return self.__parent__._cast(_4586.ConceptGearMeshCompoundParametricStudyTool)

    @property
    def conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4589.ConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4589,
        )

        return self.__parent__._cast(_4589.ConicalGearMeshCompoundParametricStudyTool)

    @property
    def coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4594.CouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4594,
        )

        return self.__parent__._cast(
            _4594.CouplingConnectionCompoundParametricStudyTool
        )

    @property
    def cvt_belt_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4596.CVTBeltConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4596,
        )

        return self.__parent__._cast(_4596.CVTBeltConnectionCompoundParametricStudyTool)

    @property
    def cylindrical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4604.CylindricalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4604,
        )

        return self.__parent__._cast(
            _4604.CylindricalGearMeshCompoundParametricStudyTool
        )

    @property
    def face_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4610.FaceGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4610,
        )

        return self.__parent__._cast(_4610.FaceGearMeshCompoundParametricStudyTool)

    @property
    def gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4615.GearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4615,
        )

        return self.__parent__._cast(_4615.GearMeshCompoundParametricStudyTool)

    @property
    def hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4619.HypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4619,
        )

        return self.__parent__._cast(_4619.HypoidGearMeshCompoundParametricStudyTool)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4623.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4623,
        )

        return self.__parent__._cast(
            _4623.KlingelnbergCycloPalloidConicalGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4626.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4626,
        )

        return self.__parent__._cast(
            _4626.KlingelnbergCycloPalloidHypoidGearMeshCompoundParametricStudyTool
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4629.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4629,
        )

        return self.__parent__._cast(
            _4629.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def part_to_part_shear_coupling_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4639.PartToPartShearCouplingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4639,
        )

        return self.__parent__._cast(
            _4639.PartToPartShearCouplingConnectionCompoundParametricStudyTool
        )

    @property
    def ring_pins_to_disc_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4648.RingPinsToDiscConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4648,
        )

        return self.__parent__._cast(
            _4648.RingPinsToDiscConnectionCompoundParametricStudyTool
        )

    @property
    def rolling_ring_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4651.RollingRingConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4651,
        )

        return self.__parent__._cast(
            _4651.RollingRingConnectionCompoundParametricStudyTool
        )

    @property
    def spiral_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4658.SpiralBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4658,
        )

        return self.__parent__._cast(
            _4658.SpiralBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def spring_damper_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4661.SpringDamperConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4661,
        )

        return self.__parent__._cast(
            _4661.SpringDamperConnectionCompoundParametricStudyTool
        )

    @property
    def straight_bevel_diff_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4664.StraightBevelDiffGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4664,
        )

        return self.__parent__._cast(
            _4664.StraightBevelDiffGearMeshCompoundParametricStudyTool
        )

    @property
    def straight_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4667.StraightBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4667,
        )

        return self.__parent__._cast(
            _4667.StraightBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def torque_converter_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4676.TorqueConverterConnectionCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4676,
        )

        return self.__parent__._cast(
            _4676.TorqueConverterConnectionCompoundParametricStudyTool
        )

    @property
    def worm_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4682.WormGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4682,
        )

        return self.__parent__._cast(_4682.WormGearMeshCompoundParametricStudyTool)

    @property
    def zerol_bevel_gear_mesh_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "_4685.ZerolBevelGearMeshCompoundParametricStudyTool":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools.compound import (
            _4685,
        )

        return self.__parent__._cast(
            _4685.ZerolBevelGearMeshCompoundParametricStudyTool
        )

    @property
    def inter_mountable_component_connection_compound_parametric_study_tool(
        self: "CastSelf",
    ) -> "InterMountableComponentConnectionCompoundParametricStudyTool":
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
class InterMountableComponentConnectionCompoundParametricStudyTool(
    _4591.ConnectionCompoundParametricStudyTool
):
    """InterMountableComponentConnectionCompoundParametricStudyTool

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _INTER_MOUNTABLE_COMPONENT_CONNECTION_COMPOUND_PARAMETRIC_STUDY_TOOL
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
    ) -> "List[_4479.InterMountableComponentConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool]

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
    ) -> "List[_4479.InterMountableComponentConnectionParametricStudyTool]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool]

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
    ) -> "_Cast_InterMountableComponentConnectionCompoundParametricStudyTool":
        """Cast to another type.

        Returns:
            _Cast_InterMountableComponentConnectionCompoundParametricStudyTool
        """
        return _Cast_InterMountableComponentConnectionCompoundParametricStudyTool(self)
