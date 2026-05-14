from dataclasses import dataclass


@dataclass(frozen=True)
class MitreTechnique:
    technique_id: str
    tactic: str
    name: str

    @property
    def url(self) -> str:
        return f"https://attack.mitre.org/techniques/{self.technique_id.replace('.', '/')}/"


class MitreEnrichmentService:
    TECHNIQUE_LOOKUP: dict[str, MitreTechnique] = {
        "brute_force": MitreTechnique("T1110", "Credential Access", "Brute Force"),
        "valid_accounts": MitreTechnique("T1078", "Defense Evasion", "Valid Accounts"),
        "phishing": MitreTechnique("T1566", "Initial Access", "Phishing"),
        "command_shell": MitreTechnique("T1059.003", "Execution", "Command and Scripting Interpreter: Windows Command Shell"),
        "powershell": MitreTechnique("T1059.001", "Execution", "Command and Scripting Interpreter: PowerShell"),
        "privilege_escalation": MitreTechnique("T1068", "Privilege Escalation", "Exploitation for Privilege Escalation"),
        "account_manipulation": MitreTechnique("T1098", "Persistence", "Account Manipulation"),
        "credential_dumping": MitreTechnique("T1003", "Credential Access", "OS Credential Dumping"),
        "network_scanning": MitreTechnique("T1046", "Discovery", "Network Service Discovery"),
        "remote_services": MitreTechnique("T1021", "Lateral Movement", "Remote Services"),
        "exfiltration": MitreTechnique("T1041", "Exfiltration", "Exfiltration Over C2 Channel"),
        "dns_tunneling": MitreTechnique("T1071.004", "Command and Control", "Application Layer Protocol: DNS"),
        "scheduled_task": MitreTechnique("T1053.005", "Execution", "Scheduled Task/Job: Scheduled Task"),
        "registry_run_key": MitreTechnique("T1547.001", "Persistence", "Registry Run Keys / Startup Folder"),
        "defense_evasion": MitreTechnique("T1562", "Defense Evasion", "Impair Defenses"),
        "data_staged": MitreTechnique("T1074", "Collection", "Data Staged"),
    }

    PATTERN_MAP: dict[str, str] = {
        "login_failed": "brute_force",
        "access_denied": "brute_force",
        "login_success": "valid_accounts",
        "privilege_change": "privilege_escalation",
        "role_update": "account_manipulation",
        "api_request": "network_scanning",
        "powershell": "powershell",
        "cmd.exe": "command_shell",
        "mimikatz": "credential_dumping",
        "nmap": "network_scanning",
        "rdp": "remote_services",
        "ssh": "remote_services",
        "dns": "dns_tunneling",
        "scheduled": "scheduled_task",
        "registry": "registry_run_key",
        "defender_disabled": "defense_evasion",
        "archive": "data_staged",
    }

    @classmethod
    def enrich(cls, *, event_type: str, message: str) -> MitreTechnique | None:
        content = f"{event_type} {message}".lower()
        for pattern, key in cls.PATTERN_MAP.items():
            if pattern in content:
                return cls.TECHNIQUE_LOOKUP[key]
        return None
