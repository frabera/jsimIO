# %%
from jsimIO import *


# Create a Model instance
model = Model("JobShop_noroutematrix")

# Create network nodes
source = Source(model, "Source")  # 1
# buffer size + 1, servers count as one buffer place
m1 = Station(model, "M1", buffer_size=11)
m2 = Station(model, "M2", buffer_size=8)
m3 = Station(model, "M3", buffer_size=10)
m4 = Station(model, "M4", buffer_size=5)
m5 = Station(model, "M5", buffer_size=13)
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
m2.set_service(part_b, Determ(1.2))
m3.set_service(part_b, Determ(1))
m3.set_service(part_c, Determ(3))
m4.set_service(part_a, Determ(1.5))
m5.set_service(part_a, Determ(0.7))
m5.set_service(part_b, Determ(0.8))
m5.set_service(part_c, Determ(0.5))

# routing
# part A
source.add_route(part_a, m1, 1)
m1.add_route(part_a, m2, 1)
m2.add_route(part_a, m4, 1)
m4.add_route(part_a, m5, 1)
m5.add_route(part_a, sink, 1)

# part B
source.add_route(part_b, m1, 1)
m1.add_route(part_b, m2, 1)
m2.add_route(part_b, m3, 1)
m3.add_route(part_b, m5, 1)
m5.add_route(part_b, sink, 1)

# part C
source.add_route(part_c, m1, 1)
m1.add_route(part_c, m3, 1)
m3.add_route(part_c, m5, 1)
m5.add_route(part_c, sink, 1)

model.set_routing()

# Export and run
baked_model = bake(model)
print(ET.tostring(baked_model._element, pretty_print=True).decode())

path = baked_model.write_jsimg()
ret = baked_model.solve_jsimg(path)
print(ret)

# %%
