"""Which polynomial degree predicts years the fit never saw?

Fits start_year to 2019, then scores 2020 to end_year. Prints one row per degree.
"""
import numpy as np
import yaml

import trend

params = yaml.safe_load(open("params.yaml"))
t, ppm = trend.load_table(open("data/co2_mm_mlo.csv", "rb").read())
train = (t >= params["start_year"]) & (t < 2020)
test = (t >= 2020) & (t < params["end_year"] + 1)

print("degree  fit RMSE (ppm)  holdout RMSE (ppm)")
for degree in range(1, 6):
    coef, center = trend.fit(t[train], ppm[train], degree)
    errors = [np.sqrt(np.mean((trend.predict(t[m], coef, center, degree) - ppm[m]) ** 2)) for m in (train, test)]
    print(f"{degree:6d}  {errors[0]:14.3f}  {errors[1]:18.3f}")
