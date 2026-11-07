"""Plant a signal we know, and make the fit find it."""
import numpy as np

import trend


def test_fit_recovers_a_planted_growth_rate():
    t = 2000 + np.arange(25 * 12) / 12
    ppm = 370 + 2.0 * (t - 2000) + 3 * np.sin(2 * np.pi * t)
    params = {"start_year": 2000, "end_year": 2024, "degree": 2}
    assert abs(trend.summarize(t, ppm, params)["growth_rate_ppm_per_year"] - 2.0) < 0.01


def test_seasonal_amplitude_is_peak_to_trough():
    t = 2000 + np.arange(25 * 12) / 12
    ppm = 370 + 2.0 * (t - 2000) + 3 * np.sin(2 * np.pi * t)
    params = {"start_year": 2000, "end_year": 2024, "degree": 2}
    assert abs(trend.summarize(t, ppm, params)["seasonal_amplitude_ppm"] - 6.0) < 0.05
