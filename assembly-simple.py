# %%
from jsimIO import *


# Create a Model instance
model = Model("Assembly-simple")

# Create network nodes
source = Source(model, "Source")  # 1
m1 = Station(model, "M1")
sink = Sink(model, "Sink")  # 2
fork = Fork(model, "Fork", "Final Product")

# Define customer classes
final = OpenClass(model, "Final Product", source, Dist.Determ(1))
component_a = OpenClass(model, "Component A", fork, )
component_b = OpenClass(model, "Component B", fork, )

join1 = Join(model, "Join 1", final, 2)


# Set services
m1.set_service(component_a, Dist.Exp(1.1))

# routing
# part A
source.add_route(final, fork, 1)
fork.add_route(component_a, m1, 1)
fork.add_route(component_b, join1, 1)

m1.add_route(component_a, join1, 1)

join1.add_route(final, sink, 1)


model.add_measure()

# Export and run
# baked_model = bake(model)
# print(ET.tostring(baked_model._element, pretty_print=True).decode())

path = model.write_jsimg()
ret = model.solve_jsimg()
print(ret)

# %%
