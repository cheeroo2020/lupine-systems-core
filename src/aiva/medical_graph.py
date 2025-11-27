# src/aiva/medical_graph.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class PayloadSpec:
    """Configuration for a biological payload type."""
    time_limit_hours: float           # hard upper bound
    safe_temp_range_c: Tuple[float, float]  # (min, max) safe range in °C


class MedicalGraph:
    """
    Models medical viability based on:
    - payload type (Heart, Blood, Vaccine, etc.)
    - total transport duration in hours
    - container temperature in °C

    This is a simplified version of the thermal decay ideas in the Lupine book:
    - If duration exceeds the hard time limit → viability = 0.0
    - Otherwise, viability decays from 1.0 down towards 0.1
      as we approach the limit.
    - Temperature outside the safe band reduces viability further.
    """

    # Hard limits & safe temperature bands (simplified)
    _PAYLOAD_SPECS: Dict[str, PayloadSpec] = {
        "Heart": PayloadSpec(time_limit_hours=4.0, safe_temp_range_c=(2.0, 8.0)),
        "Blood": PayloadSpec(time_limit_hours=6.0, safe_temp_range_c=(2.0, 8.0)),
        "Vaccine": PayloadSpec(time_limit_hours=24.0, safe_temp_range_c=(2.0, 8.0)),
    }

    def _get_spec(self, payload_type: str) -> PayloadSpec:
        try:
            return self._PAYLOAD_SPECS[payload_type]
        except KeyError as exc:
            raise ValueError(f"Unknown payload_type: {payload_type!r}") from exc

    def calculate_viability(
        self,
        payload_type: str,
        duration_hours: float,
        temp_celsius: float,
    ) -> float:
        """
        Calculate viability score for a biological payload.

        Rules:
        - If duration_hours > hard limit → 0.0
        - Else base viability decays linearly from 1.0 (0h) to 0.1 (at limit)
        - Temperature outside the safe range applies an additional penalty.

        Returns
        -------
        float
            Viability score in [0.0, 1.0].
        """
        spec = self._get_spec(payload_type)

        if duration_hours >= spec.time_limit_hours:
            return 0.0

        if duration_hours <= 0:
            base_viability = 1.0
        else:
            # Linear decay: 0h → 1.0, limit → 0.1
            remaining_fraction = (spec.time_limit_hours - duration_hours) / spec.time_limit_hours
            base_viability = 0.1 + remaining_fraction * 0.9

        # Temperature penalty
        t_min, t_max = spec.safe_temp_range_c
        if t_min <= temp_celsius <= t_max:
            temp_factor = 1.0
        else:
            # Degrees outside safe band (simplified penalty, capped)
            if temp_celsius < t_min:
                delta = t_min - temp_celsius
            else:
                delta = temp_celsius - t_max
            delta_capped = min(delta, 10.0)
            # Each degree outside range reduces viability by 5%, up to 50%
            temp_factor = max(0.5, 1.0 - 0.05 * delta_capped)

        viability = base_viability * temp_factor
        # Clamp to [0, 1] and round slightly for nicer printing
        return max(0.0, min(1.0, round(viability, 3)))


if __name__ == "__main__":
    mg = MedicalGraph()
    print("Fast heart route:", mg.calculate_viability("Heart", 2.0, 4.0))
    print("Slow heart route:", mg.calculate_viability("Heart", 6.0, 4.0))

