// The README's procedure as a Nextflow workflow. Each process names the files it reads, the files it writes and the command.
// Step 1: add a process VALIDATE and a process REPORT in the same form, and call them in the workflow block.

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

workflow {
    clean = CLEAN(file('data/penguins.csv'), file('clean.py'))
}
