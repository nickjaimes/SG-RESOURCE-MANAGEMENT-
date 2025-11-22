"""
Resource Guardian – Datacenter Demo
Simulates simple combined thermal + power conditions.
"""

import random
import time

from resource_guardian.src.rg_orchestrator import ResourceGuardian
from thermal_control.src.thermal_controller import ThermalController
from thermal_control.src.thermal_profiles import get_thermal_profile
from power_management.src.power_controller import PowerController
from power_management.src.power_profiles import get_power_profile
from qnsf.src.qnsf_core import QNSFCore


def main():
    qnsf = QNSFCore()
    thermal = ThermalController(**get_thermal_profile("balanced"))
    power = PowerController(**get_power_profile("balanced"))

    guardian = ResourceGuardian(thermal_controller=thermal,
                                power_controller=power,
                                qnsf=qnsf)

    print("\n[SG RESOURCE GUARDIAN – DATACENTER DEMO]\n")

    for step in range(1, 21):
        temp = random.uniform(55.0, 80.0)
        load = random.uniform(25.0, 55.0)
        ambient = random.uniform(22.0, 34.0)
        workload_level = random.uniform(0.3, 0.9)

        snapshot = guardian.tick(
            current_temp=temp,
            current_load_kw=load,
            ambient_temp=ambient,
            workload_level=workload_level,
            context={"step": step, "mode": "datacenter"},
        )

        print(
            f"Step {step:02d} | "
            f"Temp: {temp:5.2f}°C | Load: {load:5.2f}kW | "
            f"Mode: {snapshot['mode']:<10} | "
            f"Cool: {snapshot['thermal_decision']['cooling_level']:.2f} | "
            f"Shed: {snapshot['power_decision']['shed_non_critical']} | "
            f"Risk(QNSF): {snapshot['qnsf_risk_index']:.2f}"
        )

        time.sleep(0.2)

    print("\nDemo complete.\n")


if __name__ == "__main__":
    main()

