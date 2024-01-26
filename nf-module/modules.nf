process SPLITLETTERS {
    input:
    val x

    output:
    path 'chunk_*'

    script:
    """
    printf '$x' | split -b 6 - chunk_
    """
}

process CONVERTTOUPPER {
    input:
    val ready
    path y

    output:
    stdout emit: upper

    script:
    """
    cat $y | tr '[a-z]' '[A-Z]'
    """
}

process TIMESHIFT {

    input:
    val hours
    val minutes
    val percent_renewable
    val finish_time
    val area_code
    val authorization_header
    val logger
    path 'chunk_*'

    output:
    val true

    script:
    """
    sleep 120
    cli.py timeshift -s $hours -m $minutes -p $percent_renewable -f "$finish_time" -c "$area_code" -a "$authorization_header" --logging
    """
}

process UPLOAD_TRACEFILE{

}