Write a model card for the model that is in production in this repository, and save it as card.md in this folder.

Use only the files in this folder. Don't look anywhere else, and don't add anything you remember about this kind of data or model.

The card must state:

- the registered version that is in prod, from release.yaml
- the validation accuracy to three decimals, from metrics.json, and what it was measured on
- the name of the lock file that records the pipeline, dvc.lock
- the number of rows in the train, validation and test splits, from release.yaml
- what the model is for, and what it must not be used for

Every number and every URL in the card must come from metrics.json, params.yaml, release.yaml or sources.yaml. Give the unit of each number and name the file it came from. If something isn't in those files, write "unknown". Don't guess.

If this folder has a decisions.yaml, follow what it says and include those decisions in the card.
