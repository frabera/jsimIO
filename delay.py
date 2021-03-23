# %%
from jsimIO import *


# Create a Model instance
model = Model("Delay")

# Create network nodes
source = Source(model, "Source")  # 1


sink = Sink(model, "Sink")  # 2
delay = Delay(model, "M1")  # 3

# Define customer classes
class1 = OpenClass(model, "Class1", source, Dist.Exp(0.4))
class2 = OpenClass(model, "Class2", source, Dist.Determ(0.9))

# Set services
delay.set_service(class1, Dist.Exp(0.1))
delay.set_service(class2, Dist.Determ(0.1))

routing_matrices = [
    [  # class 1
        [0, 0, 1],
        [0, 0, 0],
        [0, 1, 0]
    ],
    [  # class 2
        [0, 0, 1],
        [0, 0, 0],
        [0, 1, 0]
    ]
]

model.set_routing_matrices(routing_matrices)

model.add_measure()

# Export and run
# baked_model = bake(model, fill_loggers=True)

path = model.write_jsimg()
ret = model.solve_jsimg(path)
print(ret)


# %%
