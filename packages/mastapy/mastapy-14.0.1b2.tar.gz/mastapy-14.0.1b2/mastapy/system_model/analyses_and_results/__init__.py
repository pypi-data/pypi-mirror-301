"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results._2706 import (
        CompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2707 import SingleAnalysis
    from mastapy._private.system_model.analyses_and_results._2708 import (
        AdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2709 import (
        AdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2710 import (
        AdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2711 import (
        CompoundParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2712 import (
        CriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2713 import DynamicAnalysis
    from mastapy._private.system_model.analyses_and_results._2714 import (
        DynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2715 import (
        DynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2716 import (
        DynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2717 import (
        DynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2718 import (
        DynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2719 import (
        HarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2720 import (
        HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2721 import (
        HarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2722 import ModalAnalysis
    from mastapy._private.system_model.analyses_and_results._2723 import (
        ModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2724 import (
        ModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2725 import (
        ModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2726 import (
        MultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2727 import (
        ParametricStudyToolAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2728 import (
        PowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2729 import (
        StabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2730 import (
        SteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2731 import (
        SteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2732 import (
        SteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2733 import (
        SystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2734 import (
        TorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2735 import (
        AnalysisCaseVariable,
    )
    from mastapy._private.system_model.analyses_and_results._2736 import (
        ConnectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2737 import Context
    from mastapy._private.system_model.analyses_and_results._2738 import (
        DesignEntityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2739 import (
        DesignEntityGroupAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2740 import (
        DesignEntitySingleContextAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2744 import PartAnalysis
    from mastapy._private.system_model.analyses_and_results._2745 import (
        CompoundAdvancedSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2746 import (
        CompoundAdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2747 import (
        CompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2748 import (
        CompoundCriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2749 import (
        CompoundDynamicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2750 import (
        CompoundDynamicModelAtAStiffnessAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2751 import (
        CompoundDynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2752 import (
        CompoundDynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2753 import (
        CompoundDynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2754 import (
        CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2755 import (
        CompoundHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2756 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2757 import (
        CompoundHarmonicAnalysisOfSingleExcitationAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2758 import (
        CompoundModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2759 import (
        CompoundModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2760 import (
        CompoundModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2761 import (
        CompoundModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2762 import (
        CompoundMultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2763 import (
        CompoundPowerFlowAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2764 import (
        CompoundStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2765 import (
        CompoundSteadyStateSynchronousResponseAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2766 import (
        CompoundSteadyStateSynchronousResponseAtASpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2767 import (
        CompoundSteadyStateSynchronousResponseOnAShaftAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2768 import (
        CompoundSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2769 import (
        CompoundTorsionalSystemDeflectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2770 import (
        TESetUpForDynamicAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results._2771 import TimeOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results._2706": ["CompoundAnalysis"],
        "_private.system_model.analyses_and_results._2707": ["SingleAnalysis"],
        "_private.system_model.analyses_and_results._2708": [
            "AdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2709": [
            "AdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2710": [
            "AdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2711": [
            "CompoundParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2712": ["CriticalSpeedAnalysis"],
        "_private.system_model.analyses_and_results._2713": ["DynamicAnalysis"],
        "_private.system_model.analyses_and_results._2714": [
            "DynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2715": [
            "DynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2716": [
            "DynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2717": [
            "DynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2718": [
            "DynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2719": ["HarmonicAnalysis"],
        "_private.system_model.analyses_and_results._2720": [
            "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2721": [
            "HarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2722": ["ModalAnalysis"],
        "_private.system_model.analyses_and_results._2723": ["ModalAnalysisAtASpeed"],
        "_private.system_model.analyses_and_results._2724": [
            "ModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2725": [
            "ModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2726": [
            "MultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2727": [
            "ParametricStudyToolAnalysis"
        ],
        "_private.system_model.analyses_and_results._2728": ["PowerFlowAnalysis"],
        "_private.system_model.analyses_and_results._2729": ["StabilityAnalysis"],
        "_private.system_model.analyses_and_results._2730": [
            "SteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2731": [
            "SteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2732": [
            "SteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2733": [
            "SystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2734": [
            "TorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2735": ["AnalysisCaseVariable"],
        "_private.system_model.analyses_and_results._2736": ["ConnectionAnalysis"],
        "_private.system_model.analyses_and_results._2737": ["Context"],
        "_private.system_model.analyses_and_results._2738": ["DesignEntityAnalysis"],
        "_private.system_model.analyses_and_results._2739": [
            "DesignEntityGroupAnalysis"
        ],
        "_private.system_model.analyses_and_results._2740": [
            "DesignEntitySingleContextAnalysis"
        ],
        "_private.system_model.analyses_and_results._2744": ["PartAnalysis"],
        "_private.system_model.analyses_and_results._2745": [
            "CompoundAdvancedSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2746": [
            "CompoundAdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2747": [
            "CompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2748": [
            "CompoundCriticalSpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2749": ["CompoundDynamicAnalysis"],
        "_private.system_model.analyses_and_results._2750": [
            "CompoundDynamicModelAtAStiffnessAnalysis"
        ],
        "_private.system_model.analyses_and_results._2751": [
            "CompoundDynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2752": [
            "CompoundDynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2753": [
            "CompoundDynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2754": [
            "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2755": [
            "CompoundHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2756": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2757": [
            "CompoundHarmonicAnalysisOfSingleExcitationAnalysis"
        ],
        "_private.system_model.analyses_and_results._2758": ["CompoundModalAnalysis"],
        "_private.system_model.analyses_and_results._2759": [
            "CompoundModalAnalysisAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2760": [
            "CompoundModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2761": [
            "CompoundModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2762": [
            "CompoundMultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2763": [
            "CompoundPowerFlowAnalysis"
        ],
        "_private.system_model.analyses_and_results._2764": [
            "CompoundStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2765": [
            "CompoundSteadyStateSynchronousResponseAnalysis"
        ],
        "_private.system_model.analyses_and_results._2766": [
            "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2767": [
            "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis"
        ],
        "_private.system_model.analyses_and_results._2768": [
            "CompoundSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2769": [
            "CompoundTorsionalSystemDeflectionAnalysis"
        ],
        "_private.system_model.analyses_and_results._2770": [
            "TESetUpForDynamicAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results._2771": ["TimeOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "SingleAnalysis",
    "AdvancedSystemDeflectionAnalysis",
    "AdvancedSystemDeflectionSubAnalysis",
    "AdvancedTimeSteppingAnalysisForModulation",
    "CompoundParametricStudyToolAnalysis",
    "CriticalSpeedAnalysis",
    "DynamicAnalysis",
    "DynamicModelAtAStiffnessAnalysis",
    "DynamicModelForHarmonicAnalysis",
    "DynamicModelForModalAnalysis",
    "DynamicModelForStabilityAnalysis",
    "DynamicModelForSteadyStateSynchronousResponseAnalysis",
    "HarmonicAnalysis",
    "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "HarmonicAnalysisOfSingleExcitationAnalysis",
    "ModalAnalysis",
    "ModalAnalysisAtASpeed",
    "ModalAnalysisAtAStiffness",
    "ModalAnalysisForHarmonicAnalysis",
    "MultibodyDynamicsAnalysis",
    "ParametricStudyToolAnalysis",
    "PowerFlowAnalysis",
    "StabilityAnalysis",
    "SteadyStateSynchronousResponseAnalysis",
    "SteadyStateSynchronousResponseAtASpeedAnalysis",
    "SteadyStateSynchronousResponseOnAShaftAnalysis",
    "SystemDeflectionAnalysis",
    "TorsionalSystemDeflectionAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflectionAnalysis",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffnessAnalysis",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponseAnalysis",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitationAnalysis",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlowAnalysis",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponseAnalysis",
    "CompoundSteadyStateSynchronousResponseAtASpeedAnalysis",
    "CompoundSteadyStateSynchronousResponseOnAShaftAnalysis",
    "CompoundSystemDeflectionAnalysis",
    "CompoundTorsionalSystemDeflectionAnalysis",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)
