# jsimIO Manual

## Model class

```python
Model(str: name,
      dict: options=Default.ModelOptions)
```

### Model methods

```python
Model.set_routing_matrices(list: routing_matrices)
Model.add_measure()
Model.write_jsimg()
Model.solve_jsimg()
```

## Nodes

Each node in jsimIO is implemented as a child-class of an internal `_Node` class. Below each available node is presented, types and default values of instantiation arguments are reported.

#### Node methods

```python
_Node.add_route(_UserClass: userclass,
                _Node: target,
                int: probability)
```

### Source

```python
Source(Model: model, str: name)
```

### Sink

```python
Sink(Model: model, str: name)
```

### Station

```python
Station(Model: model,
        str: name,
        SchedStrategy: scheduling_strategy=SchedStrategy.FCFS,
        int: buffer_size=-1,
        int: max_jobs=1,
        DropStrategy: drop_strategy.BAS_BLOCKING)
```

The default value for the scheduling strategy is First Come First Served (FCFS) and the default Drop Strategy is BAS_BLOCKING.
The default value for buffer size is -1 (infinite) and the default number of servers (max_jobs) is 1.

#### Station methods

```python
Station.set_service(_UserClass: userclass,
                    Dist._Distribution: distribution)
```

### Fork

```python
Fork(Model: model,
     str: name,
     str: forked_class_NameString
     SchedStrategy; scheduling_strategy=SchedStrategy.FCFS,
     int: buffer_size=-1,
     DropStrategy: drop_strategy.BAS_BLOCKING)
```

**Note**: Please mind that in the fork instantiation it is required, differently from the other classes, to input the forked userclass variable with its *string name* and **not with the variable itself**. This is required since during the fork instantiation the forked user class is not yet defined (refer to the objects definition sequence).

### Join

```python
Join(Model: model,
     str: name,
     _UserClass: output
     int: number_of_class_inputs)
```

### Delay

```python
Delay(Model: model, str: name)
```

### Logger

```python
Logger(Model: model, str: name)
```

## User classes

Each class type is implemented as a child-class of an internal class `_UserClass`:

### Open class

```python
OpenClass(Model: model,
          str: name,
          _Node: reference_station,
          Dist._Distribution: distribution,
          int: priority=0)
```

### Closed class

```python
ClosedClass(Model: model,
            str: name,
            _Node: reference_station,
            int: customers,
            int: priority=0)
```
