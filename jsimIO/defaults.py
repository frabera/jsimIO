class Default:
    ModelOptions = {
        "disableStatisticStop": "false",
        "logDecimalSeparator": ".",
        "logDelimiter": ",",
        "logReplaceMode": "0",
        "logpath": "",
        "maxEvents": "-1",
        "maxSamples": "1000000",
        "polling": "1.0"
    }

    SimulationOptions = {
        "-seed": 1,
        "-maxtime": 60
    }


class Id:
    class Station:
        Queue = 0
        Server = 1
        Router = 2
    
    class Source:
        RandomSource = 0
        ServiceTunnel = 1
        Router = 2
