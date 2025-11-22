High-level rules for combining thermal + power.

def determine_guardian_mode(thermal_decision, power_decision) -> str:
    """
    Decide global mode based on thermal & power conditions.
    """
    emergency_flags = [
        thermal_decision.get("emergency"),
        power_decision.get("emergency"),
    ]

    if any(emergency_flags):
        return "emergency"

    if thermal_decision.get("emergency") or power_decision.get("shed_non_critical"):
        return "preventive"

    return "normal"


def summarize_risk(thermal_severity: float, power_severity: float) -> float:
    """
    Combine thermal & power severity into one scalar (0-1).
    Very simple weighted average for now.
    """
    return min(1.0, max(0.0, 0.6 * thermal_severity + 0.4 * power_severity))

