// The README's procedure as a Nextflow workflow. Each process names the files it reads, the files it writes and the command.
// Step 1: add a process COUNT and a process FIT in the same form, and call them in the workflow block.

process SUBSET {
    publishDir '.', mode: 'copy'

    input:
    path 'data/earthquakes.csv'
    path 'params.yaml'
    path 'subset.py'

    output:
    path 'results/subset.csv'

    script:
    "python subset.py"
}

workflow {
    subset = SUBSET(file('data/earthquakes.csv'), file('params.yaml'), file('subset.py'))
}
