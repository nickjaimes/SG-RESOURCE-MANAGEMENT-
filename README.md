# 🛡 SG RESOURCE GUARDIAN  
**Unified Thermal + Power + QNSF Intelligence Layer**

> “When power, heat, and memory work together,  
> a system stops reacting… and starts *anticipating*.”

---

## 📌 Overview

**SG RESOURCE GUARDIAN** is the **unified orchestration layer** that combines:

- 🌡 **SG Thermal Control Algorithm**
- ⚡ **SG AI Power Management System**
- 🧠 **QNSF – Quantum Neuromorphic System Fabric**

into a single **AI resource guardian** that can:

- Protect systems from **overheating** and **overloading**
- Optimize **energy usage** and **cooling**
- Learn from all resource events over time (QNSF)
- Coordinate with:
  - **TRINITY AI** (global decision + optimization)
  - **EAGLE EYE** (anomaly detection)
  - **SG OS** (execution layer)
  - **SG Global Dashboard** (visualization)

Use cases:

- SG HIVE Data Centers  
- SG Rescue Pods / Safe Hubs  
- National Infrastructure Nodes  
- High-resilience facilities (hospitals, control centers)

---

## 🧬 Core Concept

The Resource Guardian:

- Reads **thermal + power + context signals**
- Applies **policy logic** (priority, mission state, safety)
- Invokes:
  - `ThermalController`
  - `PowerController`
  - `QNSFCore`
- Produces unified decisions:
  - Cooling levels  
  - Power shedding / throttling  
  - QNSF events + risk indices  
  - Signals to TRINITY & EAGLE

---

## 📂 Repository Layout

```text
resource_guardian/
  └── src/
      ├── rg_orchestrator.py   # Main orchestrator class
      ├── rg_policies.py       # Rule & mode definitions
      └── rg_state_model.py    # Resource state model
docs/
  ├── RESOURCE_GUARDIAN_OVERVIEW.md
  ├── ARCHITECTURE.md
  └── INTEGRATION_SG_OS_AND_GLOBAL.md
examples/
  ├── rg_datacenter_demo.py
  └── rg_rescue_pod_demo.py



⸻

🧪 Quick Example

from resource_guardian.src.rg_orchestrator import ResourceGuardian
from thermal_control.src.thermal_controller import ThermalController
from thermal_control.src.thermal_profiles import get_thermal_profile
from power_management.src.power_controller import PowerController
from power_management.src.power_profiles import get_power_profile
from qnsf.src.qnsf_core import QNSFCore

qnsf = QNSFCore()

thermal = ThermalController(**get_thermal_profile("balanced"))
power = PowerController(**get_power_profile("balanced"))

guardian = ResourceGuardian(thermal_controller=thermal,
                            power_controller=power,
                            qnsf=qnsf)

snapshot = guardian.tick(
    current_temp=68.0,
    current_load_kw=42.0,
    ambient_temp=30.0,
    workload_level=0.7,
    context={"mode": "datacenter"}
)

print(snapshot)


⸻

🧠 SG Ecosystem Integration
   •   TRINITY AI:
      •   Reads Guardian’s risk & status
      •   Changes policies (eco, resilience, emergency)
      •   Triggers power/thermal rituals
   •   EAGLE EYE:
      •   Monitors anomalies from Resource Guardian output
   •   QNSF:
      •   Learns long-term patterns:
         •   Repeated overloads
         •   Seasonal heat
         •   Facility-specific stress behavior

⸻

🖋 Author

Created by Nicolas E. Santiago
Safeway Guardian – Saitama, Japan – 2025
Powered by ChatGPT
