# jsimIO

## JMT.jar executable

Downlad the [JMT standalone executable](http://sourceforge.net/projects/jmt/files/jmt/JMT-1.1.0/JMT-singlejar-1.1.0.jar/download), rename it `JMT.jar` and place it in `jsimIO` folder.
_See the `JMT.jar_GOES_HERE` placeholder_.

## Output files

Each simulation run creates automatically a folder in the script path used to run it (if no path is specified) named:

    /modelname_date_time/

And contains:

* `modename-input.jsimg`

  The generated simulation model file to be run by JMT.

* `modename-result.jsimg`

    The output file of JMT. It is basically the input `jsimg` file (some XML syntax could vary) with 2 additions:

    1. `jmodel` node as a sub-element of `archive` root node, containing information for displaying the model in the GUI. It is not guaranteed to work.
    2. `result` node as a sub-element of `sim` node. It is the result of the simulation, containing values for the requested performance indices.

* `Log_sourcestation@targetstation.txt`

  A `.txt` file for each logger station in the model. The name format includes the two _real_ stations connected by the logger.
