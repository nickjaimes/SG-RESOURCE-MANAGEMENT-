This is the heart: it ties everything together.

from typing import Dict, Any
from .rg_state_model import ResourceState
from .rg_policies import determine_guardian_mode, summarize_risk


class ResourceGuardian:
    """
    SG RESOURCE GUARDIAN

    Orchestrates:
    - Thermal controller
    - Power controller
    - QNSF (memory/evolution)
    And produces:
    - Unified resource state
    - Actions and risk indices
    """

    def __init__(self, thermal_controller, power_controller, qnsf):
        """
        thermal_controller: instance of ThermalController
        power_controller: instance of PowerController
        qnsf: instance of QNSFCore
        """
        self.thermal = thermal_controller
        self.power = power_controller
        self.qnsf = qnsf

    def _build_thermal_event(self, current_temp, ambient_temp, workload_level) -> Dict[str, Any]:
        # simple example severity
        temp_excess = max(0.0, current_temp - self.thermal.target_temp)
        temp_span = max(1.0, self.thermal.max_safe_temp - self.thermal.target_temp)
        base_severity = min(1.0, temp_excess / temp_span)
        ambient_effect = max(0.0, (ambient_temp - 25.0) / 20.0)
        severity = min(1.0, 0.7 * base_severity + 0.3 * ambient_effect)

        return {
            "domain": "thermal",
            "temperature": current_temp,
            "severity": severity,
            "result": "stabilized",
            "action_taken": "cooling_adjusted",
            "ambient_temp": ambient_temp,
            "workload_level": workload_level,
        }

    def _build_power_event(self, current_load_kw) -> Dict[str, Any]:
        # small helper to compute severity
        from math import fabs

        max_cap = self.power.max_capacity_kw
        safe_limit = max_cap * (1.0 - self.power.safety_margin)

        if current_load_kw <= safe_limit:
            severity = 0.2
        elif current_load_kw >= max_cap:
            severity = 1.0
        else:
            overload_fraction = (current_load_kw - safe_limit) / max(
                max_cap - safe_limit, 0.0001
            )
            severity = min(1.0, 0.2 + 0.8 * overload_fraction)

        return {
            "domain": "power",
            "current_load_kw": current_load_kw,
            "severity": severity,
            "result": "stabilized",
            "action_taken": "shed_or_throttle",
        }

    def tick(
        self,
        current_temp: float,
        current_load_kw: float,
        ambient_temp: float,
        workload_level: float,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        One Resource Guardian cycle.

        Returns a snapshot dict ready for logging / dashboard / TRINITY.
        """

        context = context or {}

        # 1) Thermal decision
        cooling_level, thermal_emergency = self.thermal.compute_control_action(
            current_temp
        )
        thermal_decision = {
            "cooling_level": cooling_level,
            "emergency": thermal_emergency,
        }

        # 2) Power decision
        power_decision = self.power.compute_power_action(current_load_kw)

        # 3) Build QNSF events + absorb
        thermal_event = self._build_thermal_event(
            current_temp, ambient_temp, workload_level
        )
        power_event = self._build_power_event(current_load_kw)

        self.qnsf.absorb_event(thermal_event)
        self.qnsf.absorb_event(power_event)

        # 4) Compute combined risk
        combined_risk = summarize_risk(
            thermal_event["severity"], power_event["severity"]
        )
        qnsf_risk_index = self.qnsf.evaluate_risk_trajectory()

        # 5) Determine guardian mode (normal/preventive/emergency)
        mode = determine_guardian_mode(thermal_decision, power_decision)

        # 6) Build resource state
        state = ResourceState(
            temperature=current_temp,
            power_load_kw=current_load_kw,
            ambient_temp=ambient_temp,
            workload_level=workload_level,
            thermal_decision=thermal_decision,
            power_decision=power_decision,
            qnsf_risk_index=qnsf_risk_index,
            mode=mode,
        )

        # 7) Output snapshot
        return {
            "mode": state.mode,
            "temperature": state.temperature,
            "power_load_kw": state.power_load_kw,
            "thermal_decision": state.thermal_decision,
            "power_decision": state.power_decision,
            "qnsf_risk_index": state.qnsf_risk_index,
            "combined_risk_scalar": combined_risk,
            "context": context,
        } 

