# %%
from jsimIO import *


# Create a Model instance
model = Model("asd")

# Create network nodes
source = Source(model, "Source")  # 1
sink = Sink(model, "Sink")  # 2
queue1 = Station(model, "M1")  # 3

# Define customer classes
class1 = OpenClass(model, "Class1", source, Exp(0.4))
class2 = OpenClass(model, "Class2", source, Exp(0.9))

# Set services
queue1.set_service(class1, Exp(0.1))
queue1.set_service(class2, Normal(0, 1))

# Define routing (matrix)
# C = model.get_number_of_classes()
# M = model.get_number_of_nodes()

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

model.set_routing(routing_matrices)

# Export and run
# %%
print(ET.tostring(model._element, pretty_print=True).decode())

model.write_jsimg()

# %%
