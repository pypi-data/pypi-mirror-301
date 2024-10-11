"""CouplingConnectionCompoundMultibodyDynamicsAnalysis"""

from __future__ import annotations

from typing import ClassVar, TYPE_CHECKING

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.cast_exception import CastException
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
    _5726,
)

_COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound",
    "CouplingConnectionCompoundMultibodyDynamicsAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2738
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7711,
        _7715,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5544
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
        _5683,
        _5688,
        _5696,
        _5744,
        _5766,
        _5781,
    )

    Self = TypeVar("Self", bound="CouplingConnectionCompoundMultibodyDynamicsAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CouplingConnectionCompoundMultibodyDynamicsAnalysis._Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CouplingConnectionCompoundMultibodyDynamicsAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis:
    """Special nested class for casting CouplingConnectionCompoundMultibodyDynamicsAnalysis to subclasses."""

    __parent__: "CouplingConnectionCompoundMultibodyDynamicsAnalysis"

    @property
    def inter_mountable_component_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5726.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis":
        return self.__parent__._cast(
            _5726.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5696.ConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5696,
        )

        return self.__parent__._cast(_5696.ConnectionCompoundMultibodyDynamicsAnalysis)

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
    def clutch_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5683.ClutchConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5683,
        )

        return self.__parent__._cast(
            _5683.ClutchConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def concept_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5688.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5688,
        )

        return self.__parent__._cast(
            _5688.ConceptCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def part_to_part_shear_coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5744.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5744,
        )

        return self.__parent__._cast(
            _5744.PartToPartShearCouplingConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def spring_damper_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5766.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5766,
        )

        return self.__parent__._cast(
            _5766.SpringDamperConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def torque_converter_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "_5781.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis":
        from mastapy._private.system_model.analyses_and_results.mbd_analyses.compound import (
            _5781,
        )

        return self.__parent__._cast(
            _5781.TorqueConverterConnectionCompoundMultibodyDynamicsAnalysis
        )

    @property
    def coupling_connection_compound_multibody_dynamics_analysis(
        self: "CastSelf",
    ) -> "CouplingConnectionCompoundMultibodyDynamicsAnalysis":
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
class CouplingConnectionCompoundMultibodyDynamicsAnalysis(
    _5726.InterMountableComponentConnectionCompoundMultibodyDynamicsAnalysis
):
    """CouplingConnectionCompoundMultibodyDynamicsAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COUPLING_CONNECTION_COMPOUND_MULTIBODY_DYNAMICS_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def connection_analysis_cases(
        self: "Self",
    ) -> "List[_5544.CouplingConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis]

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
    ) -> "List[_5544.CouplingConnectionMultibodyDynamicsAnalysis]":
        """List[mastapy.system_model.analyses_and_results.mbd_analyses.CouplingConnectionMultibodyDynamicsAnalysis]

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
    ) -> "_Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis
        """
        return _Cast_CouplingConnectionCompoundMultibodyDynamicsAnalysis(self)
