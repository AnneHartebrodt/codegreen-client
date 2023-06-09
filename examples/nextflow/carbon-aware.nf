#!/usr/bin/env nextflow
nextflow.enable.dsl=2 

process longAndIntensiveComputation {
  input: 
    val x
  output:
    stdout
  script:
    """
    
    echo '$x world!'
    """
}

workflow {
  Channel.of('Bonjour', 'Ciao', 'Hello', 'Hola') | sayHello | view
}