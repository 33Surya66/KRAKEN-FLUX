from enum import Enum
from typing import Dict, List, Set

class AgentType(str, Enum):
    MONITORING = "monitoring"
    FORENSICS = "forensics"
    RESPONSE = "response"
    COMPLIANCE = "compliance"
    SIMULATION = "simulation"

class AgentCapability(str, Enum):
    # Monitoring capabilities
    SYSTEM_MONITORING = "system_monitoring"
    NETWORK_MONITORING = "network_monitoring"
    LOG_MONITORING = "log_monitoring"
    THREAT_DETECTION = "threat_detection"

    # Forensics capabilities
    EVIDENCE_COLLECTION = "evidence_collection"
    MEMORY_ANALYSIS = "memory_analysis"
    DISK_ANALYSIS = "disk_analysis"
    NETWORK_ANALYSIS = "network_analysis"

    # Response capabilities
    INCIDENT_RESPONSE = "incident_response"
    THREAT_CONTAINMENT = "threat_containment"
    SYSTEM_RECOVERY = "system_recovery"
    AUTOMATED_REMEDIATION = "automated_remediation"

    # Compliance capabilities
    POLICY_ENFORCEMENT = "policy_enforcement"
    COMPLIANCE_CHECKING = "compliance_checking"
    AUDIT_LOGGING = "audit_logging"
    REPORT_GENERATION = "report_generation"

    # Simulation capabilities
    THREAT_SIMULATION = "threat_simulation"
    RESPONSE_SIMULATION = "response_simulation"
    SCENARIO_TESTING = "scenario_testing"
    PERFORMANCE_TESTING = "performance_testing"

# Define which capabilities are available for each agent type
AGENT_TYPE_CAPABILITIES: Dict[AgentType, Set[AgentCapability]] = {
    AgentType.MONITORING: {
        AgentCapability.SYSTEM_MONITORING,
        AgentCapability.NETWORK_MONITORING,
        AgentCapability.LOG_MONITORING,
        AgentCapability.THREAT_DETECTION
    },
    AgentType.FORENSICS: {
        AgentCapability.EVIDENCE_COLLECTION,
        AgentCapability.MEMORY_ANALYSIS,
        AgentCapability.DISK_ANALYSIS,
        AgentCapability.NETWORK_ANALYSIS
    },
    AgentType.RESPONSE: {
        AgentCapability.INCIDENT_RESPONSE,
        AgentCapability.THREAT_CONTAINMENT,
        AgentCapability.SYSTEM_RECOVERY,
        AgentCapability.AUTOMATED_REMEDIATION
    },
    AgentType.COMPLIANCE: {
        AgentCapability.POLICY_ENFORCEMENT,
        AgentCapability.COMPLIANCE_CHECKING,
        AgentCapability.AUDIT_LOGGING,
        AgentCapability.REPORT_GENERATION
    },
    AgentType.SIMULATION: {
        AgentCapability.THREAT_SIMULATION,
        AgentCapability.RESPONSE_SIMULATION,
        AgentCapability.SCENARIO_TESTING,
        AgentCapability.PERFORMANCE_TESTING
    }
}

# Define default configurations for each agent type
AGENT_TYPE_CONFIGS: Dict[AgentType, Dict] = {
    AgentType.MONITORING: {
        "interval": 30,  # seconds
        "batch_size": 100,
        "alert_threshold": 0.8
    },
    AgentType.FORENSICS: {
        "interval": 60,  # seconds
        "evidence_retention": 30,  # days
        "compression_enabled": True
    },
    AgentType.RESPONSE: {
        "interval": 15,  # seconds
        "max_concurrent_actions": 5,
        "retry_attempts": 3
    },
    AgentType.COMPLIANCE: {
        "interval": 3600,  # seconds
        "report_frequency": "daily",
        "notification_enabled": True
    },
    AgentType.SIMULATION: {
        "interval": 300,  # seconds
        "max_simulations": 10,
        "data_retention": 7  # days
    }
} 