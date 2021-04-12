class Default:
    ModelOptions = {
        "disableStatisticStop": "false",
        "logDecimalSeparator": ".",
        "logDelimiter": ",",
        "logReplaceMode": "0",
        "logPath": "",
        "maxEvents": "-1",
        "maxSamples": "1000000",
        "polling": "1.0",
        "maxSimulated": "-1",
        "maxTime": "-1"
    }

    SimulationOptions = {
        "-seed": 1,
        "-maxtime": 60
    }

    LoggerOptions = [
        {
            "classPath": "java.lang.String",
            "name": "logfileName",
            "value": "global.csv"
        },
        {
            "classPath": "java.lang.String",
            "name": "logfilePath",
            "value": "logfilePath"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logExecTimestamp",
            "value": "false"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logLoggerName",
            "value": "true"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logTimeStamp",
            "value": "true"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logJobID",
            "value": "true"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logJobClass",
            "value": "true"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logTimeSameClass",
            "value": "true"
        },
        {
            "classPath": "java.lang.Boolean",
            "name": "logTimeAnyClass",
            "value": "true"
        },
    ]

    MeasureOptions = {

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
