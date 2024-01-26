#!/usr/bin/env nextflow

params.greeting = 'Hello world!'
greeting_ch = Channel.of(params.greeting)

include { SPLITLETTERS as SPLITLETTERS_one } from './modules.nf'
include { SPLITLETTERS as SPLITLETTERS_two } from './modules.nf'

include { CONVERTTOUPPER as CONVERTTOUPPER_one } from './modules.nf'
include { CONVERTTOUPPER as CONVERTTOUPPER_two } from './modules.nf'


include { TIMESHIFT as TIMESHIFT_one } from './modules.nf'
include { TIMESHIFT as TIMESHIFT_two } from './modules.nf'


workflow {
    letters_ch1 = SPLITLETTERS_one(greeting_ch)
    time_out = TIMESHIFT_one(1, 20, 30, "2023-06-12 18:00" ,'DE-9', 'gallo', 'True',  letters_ch1.flatten())

    time_out.view()
    letters_ch1.flatten().view()
    results_ch1 = CONVERTTOUPPER_one(time_out, letters_ch1.flatten())
    results_ch1.view { it }

    letters_ch2 = SPLITLETTERS_two(greeting_ch)
    time_out_2 = TIMESHIFT_two(1, 20, 30, "2023-06-12 18:00" , 'DE-9', 'gallo', 'True', letters_ch2.flatten())

    results_ch2 = CONVERTTOUPPER_two(time_out_2, letters_ch2.flatten())
    results_ch2.view { it }
}
