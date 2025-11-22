A simple container for current resource state.

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ResourceState:
    """
    Holds the current snapshot of resource conditions.
    """
    temperature: float
    power_load_kw: float
    ambient_temp: float
    workload_level: float

    thermal_decision: Dict[str, Any] = field(default_factory=dict)
    power_decision: Dict[str, Any] = field(default_factory=dict)
    qnsf_risk_index: float = 0.0
    mode: str = "normal"   # 'normal', 'preventive', 'emergency'

