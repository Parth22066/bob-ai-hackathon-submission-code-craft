"""GridGuard AI risk scoring example module."""


def calculate_risk(load_pct: float, temperature_c: float, vibration_mm_s: float) -> float:
    """Return a normalized risk score between 0 and 100."""
    weighted = (0.45 * load_pct) + (0.30 * temperature_c) + (0.25 * vibration_mm_s)
    return max(0.0, min(100.0, weighted))


if __name__ == "__main__":
    score = calculate_risk(load_pct=72.0, temperature_c=58.0, vibration_mm_s=40.0)
    print(f"GridGuard sample risk score: {score:.2f}")
