"""Fit a polynomial trend plus a seasonal cycle to monthly CO2 at Mauna Loa."""
import numpy as np

SEASONAL_HARMONICS = 2


def load_table(raw):
    """Return decimal year and monthly mean CO2 (ppm) from the bytes of the NOAA CSV."""
    rows = [line for line in raw.splitlines() if not line.startswith(b"#")]
    table = np.genfromtxt(rows, delimiter=",", names=True)
    return table["decimal_date"], table["average"]


def _design(t, center, degree):
    columns = [(t - center) ** k for k in range(degree + 1)]
    for h in range(1, SEASONAL_HARMONICS + 1):
        columns += [np.cos(2 * np.pi * h * t), np.sin(2 * np.pi * h * t)]
    return np.column_stack(columns)


def fit(t, ppm, degree):
    """Least-squares fit. Returns (coefficients, center year)."""
    center = t.mean()
    coef, *_ = np.linalg.lstsq(_design(t, center, degree), ppm, rcond=None)
    return coef, center


def predict(t, coef, center, degree):
    return _design(t, center, degree) @ coef


def summarize(t, ppm, params):
    """Fit the years in params and return the numbers the group publishes."""
    start, end, degree = params["start_year"], params["end_year"], params["degree"]
    keep = (t >= start) & (t < end + 1)
    t, ppm = t[keep], ppm[keep]
    coef, center = fit(t, ppm, degree)
    # Growth rate is the slope of the trend at the middle of the last year.
    at = end + 0.5 - center
    growth = sum(k * coef[k] * at ** (k - 1) for k in range(1, degree + 1))
    rmse = np.sqrt(np.mean((predict(t, coef, center, degree) - ppm) ** 2))
    year = np.linspace(2000, 2001, 365)
    seasonal = _design(year, 0.0, degree)[:, degree + 1 :] @ coef[degree + 1 :]
    return {
        "growth_rate_ppm_per_year": round(float(growth), 3),
        "rmse_ppm": round(float(rmse), 3),
        "seasonal_amplitude_ppm": round(float(seasonal.max() - seasonal.min()), 3),
    }
