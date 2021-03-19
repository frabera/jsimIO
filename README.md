# jsimIO

## JMT.jar executable

Downlad the [JMT standalone executable](http://sourceforge.net/projects/jmt/files/jmt/JMT-1.1.0/JMT-singlejar-1.1.0.jar/download), rename it `JMT.jar` and place it in `jsimIO` folder _(Check the `JMT.jar_GOES_HERE` placeholder)_.

> Currently it is already in the repository, there is no need to download the jar file.

## Output files

Each simulation run creates automatically a folder in the script path used to run it ~~(if no path is specified)~~ named:

    modelname_date_time/

And contains:

* `modelname-input.jsimg`

  The generated simulation model file to be run by JMT.

* `modelname-input.jsimg-result.jsimg`

    The output file of JMT. It contains just the simulation results (the values of the requested measures).

* Log file: `global.csv`

  A `.csv` file containing the logs of all the logger stations in the model. The name format includes the real station related to the logger (each logger precedes its related station).

## Examples

In the root folder there are some examples:

1. **example1.py**
  Simple open system with one station. Open the jsimg file in _Example1_ folder with JMT to visualize it.
2. **job_shop.py**
  Sample job-shop system. Open its jsimg file in the related folder for further details.
  Model of the system: [Gitbook Link](https://virtualfactory.gitbook.io/virtual-learning-factory-toolkit/use-cases/job-shop/job-shop-ontogui)
3. **hybrid_flowshop.py**
  Sample hybrid flow-shop system. Open its jsimg file in the related folder for further details.
  Model of the system: [Gitbook Link](https://virtualfactory.gitbook.io/virtual-learning-factory-toolkit/use-cases/hybrid-flow-shop/hybrid-flow-shop-ontogui)

## Routing

There are two ways to define routing inside the system:

1. **Routing Matrix**
  List of matrices, passed with `model.set_routing(matrices)`. One matrix per userclass, each row and column index is related to a node, in order of declaration. It is used in all the examples except for `job_shop_noroutematrix.py`
2. **Node class method**
  A more explicit way, but it is needed to set each route, for each node, for each class. The node method `node.add_route(class, target_station, probability)`. It is used in `job_shop_noroutematrix.py` example.

In both cases the probabilities are normalized (per row).
