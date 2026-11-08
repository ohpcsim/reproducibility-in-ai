# Palmer penguin sex classifier

The workshop's exercises use one project, a study of Palmer penguins, and add a capability in each exercise.

- `dvc repro` runs clean, validate, report, split and train.
- `metrics.json` records male mean body mass minus female mean body mass, per species.
- `split.py` records 216 training rows from 2007 and 2008 and 117 validation rows from 2009.
- `train.py` standardizes four measurements and one-hot species columns, then fits logistic regression.
- `params.yaml` sets `train.C`. `model_metrics.json` records validation accuracy.
- Git holds the code, `params.yaml`, `dvc.yaml`, `dvc.lock`, `artifacts.yaml` and the data pointer.
- DVC stores the data, `splits.json`, `model.pkl` and both metrics files in `../osn-bucket`, a local stand-in for object storage.
- `gto show` lists registered versions and stages. Nothing is registered yet.

Data: palmerpenguins (Horst, Hill and Gorman 2020, doi:10.5281/zenodo.3960218), CC0, from Gorman, Williams and Fraser (2014), PLOS ONE 9(3): e90081. Collected by Palmer Station LTER with NSF support.
