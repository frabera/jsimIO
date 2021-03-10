# %%
from jsimIO import *


# Create a Model instance
model = Model("HybridFlowShop")

# Create network nodes
source = Source(model, "Source")  # 1
# buffer size + 1, servers count as one buffer place
m1 = Station(model, "M1", buffer_size=11)
m2 = Station(model, "M2", buffer_size=8)
m3 = Station(model, "M3", buffer_size=9)
m4 = Station(model, "M4", buffer_size=13)
m5 = Station(model, "M5", buffer_size=10)
sink = Sink(model, "Sink")  # 2

# Define customer classes
part_a = OpenClass(model, "Part A", source, Determ(1))
part_b = OpenClass(model, "Part B", source, Determ(0.5))
part_c = OpenClass(model, "Part C", source, Determ(0.8))

# Set services
m1.set_service(part_a, Determ(1.1))
m1.set_service(part_b, Determ(1.3))
m1.set_service(part_c, Determ(1))
m2.set_service(part_a, Determ(0.9))
m2.set_service(part_c, Determ(1.1))
m3.set_service(part_b, Determ(2.1))
m4.set_service(part_a, Determ(1.5))
m4.set_service(part_b, Determ(1.2))
m4.set_service(part_c, Determ(0.7))
m5.set_service(part_a, Determ(0.7))
m5.set_service(part_b, Determ(0.8))
m5.set_service(part_c, Determ(0.5))


routing_matrices = [
    [  # part A
        [0, 1, 0, 0, 0, 0, 0],  # source
        [0, 0, 1, 0, 0, 0, 0],  # m1
        [0, 0, 0, 0, 1, 0, 0],  # m2
        [0, 0, 0, 0, 0, 0, 0],  # m3
        [0, 0, 0, 0, 0, 1, 0],  # m4
        [0, 0, 0, 0, 0, 0, 1],  # m5
        [0, 0, 0, 0, 0, 0, 0]   # sink
    ],
    [  # part B
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0]
    ],
    [  # part C
        [0, 1, 0, 0, 0, 0, 0],  # source
        [0, 0, 1, 0, 0, 0, 0],  # m1
        [0, 0, 0, 0, 1, 0, 0],  # m2
        [0, 0, 0, 0, 0, 0, 0],  # m3
        [0, 0, 0, 0, 0, 1, 0],  # m4
        [0, 0, 0, 0, 0, 0, 1],  # m5
        [0, 0, 0, 0, 0, 0, 0]   # sink
    ]
]

model.set_routing(routing_matrices)

# Export and run
baked_model = bake(model)
print(ET.tostring(baked_model._element, pretty_print=True).decode())

path = baked_model.write_jsimg()
ret = baked_model.solve_jsimg(path)
print(ret)