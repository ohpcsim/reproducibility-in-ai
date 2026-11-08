// The penguin study as a Nextflow workflow. Each process names the files it reads, the files it writes and the command.
// It builds metrics.json. README.md also shows figures/body_mass.svg, which nothing builds yet.

process CLEAN {
    publishDir '.', mode: 'copy', overwrite: true

    input:
    path 'data/penguins.csv'
    path 'clean.py'

    output:
    path 'results/clean.csv'

    script:
    "python clean.py"
}

process VALIDATE {
    publishDir '.', mode: 'copy', overwrite: true

    input:
    path 'results/clean.csv'
    path 'validate.py'

    output:
    path 'results/validated.csv'

    script:
    "python validate.py"
}

process REPORT {
    publishDir '.', mode: 'copy', overwrite: true

    input:
    path 'results/validated.csv'
    path 'params.yaml'
    path 'report.py'

    output:
    path 'metrics.json'

    script:
    "python report.py"
}

workflow {
    clean = CLEAN(file('data/penguins.csv'), file('clean.py'))
    validated = VALIDATE(clean, file('validate.py'))
    REPORT(validated, file('params.yaml'), file('report.py'))
}
