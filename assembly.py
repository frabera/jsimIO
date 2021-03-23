# %%
from jsimIO import *


# Create a Model instance
model = Model("Assembly")

# Create network nodes
source = Source(model, "Source")  # 1
m1 = Station(model, "M1")
m2 = Station(model, "M2")
m3 = Station(model, "M3")
sink = Sink(model, "Sink")  # 2
fork = Fork(model, "Fork", "Final Product")

# Define customer classes
final = OpenClass(model, "Final Product", source, Dist.Determ(1))
component_a = OpenClass(model, "Component A", fork, Dist.Determ(0.5))
component_b = OpenClass(model, "Component B", fork, Dist.Determ(0.8))
component_c = OpenClass(model, "Component C", fork, Dist.Determ(1.2))

join1 = Join(model, "Join 1", final, 2)
join2 = Join(model, "Join 2", final, 2)


# Set services
m1.set_service(component_a, Dist.Exp(1.1))
m2.set_service(final, Dist.Determ(1.2))
m3.set_service(final, Dist.Determ(1))

# routing
# part A
source.add_route(final, fork, 1)
fork.add_route(component_a, m1, 1)
fork.add_route(component_b, join1, 1)
fork.add_route(component_c, join2, 1)

m1.add_route(component_a, join1, 1)

join1.add_route(final, m2, 1)

m2.add_route(final, join2, 1)

join2.add_route(final, m3, 1)

m3.add_route(final, sink, 1)

model.add_measure()

# Export and run
# baked_model = bake(model)
# print(ET.tostring(baked_model._element, pretty_print=True).decode())

path = model.write_jsimg()
ret = model.solve_jsimg()
print(ret)

# %%
