# %%
from jsimIO import *

opzioni = Default.ModelOptions
opzioni["maxSamples"] = "100000"
opzioni["maxEvents"] = "100000"
opzioni["maxSimulated"] = "600"
opzioni["maxTime"] = "600"

# Create a Model instance

model = Model("HingeAssProva", opzioni)


# Create the network nodes

source = Source(model, "Source")
m1 = Station(model, "M1", buffer_size=1)
m2 = Station(model, "M2", buffer_size=1)
b1 = Station(model, "B1_1", buffer_size=1)
b2 = Station(model, "B1_2", buffer_size=1)
b3 = Station(model, "B1_3", buffer_size=1)
b4 = Station(model, "B1_4", buffer_size=1)
b5 = Station(model, "B1_5", buffer_size=1)
b6 = Station(model, "B1_6", buffer_size=1)
b7 = Station(model, "B1_7", buffer_size=1)
b8 = Station(model, "B1_8", buffer_size=1)
b9 = Station(model, "B1_9", buffer_size=1)
b10 = Station(model, "B1_10", buffer_size=1)
b11 = Station(model, "B1_11", buffer_size=1)
b12 = Station(model, "B1_12", buffer_size=1)
b13 = Station(model, "B1_13", buffer_size=1)
b14 = Station(model, "B1_14", buffer_size=1)

m3 = Station(model, "M3", buffer_size=1)
m4 = Station(model, "M4", buffer_size=1)
c1_1 = Station(model, "C1_1", buffer_size=1)
c1_2 = Station(model, "C1_2", buffer_size=1)
c1_3 = Station(model, "C1_3", buffer_size=1)
c1_4 = Station(model, "C1_4", buffer_size=1)
c1_5 = Station(model, "C1_5", buffer_size=1)
m5 = Station(model, "M5", buffer_size=1)
m6 = Station(model, "M6", buffer_size=1)

m7 = Station(model, "M7", buffer_size=1)
c2_1 = Station(model, "C2_1", buffer_size=1)
c2_2 = Station(model, "C2_2", buffer_size=1)
c2_3 = Station(model, "C2_3", buffer_size=1)
c2_4 = Station(model, "C2_4", buffer_size=1)
c2_5 = Station(model, "C2_5", buffer_size=1)
m8 = Station(model, "M8", buffer_size=1)
m9 = Station(model, "M9", buffer_size=1)
m10 = Station(model, "M10", buffer_size=1)
m11 = Station(model, "M11", buffer_size=1)
c3_1 = Station(model, "C3_1", buffer_size=1)
c3_2 = Station(model, "C3_2", buffer_size=1)
c3_3 = Station(model, "C3_3", buffer_size=1)
c3_4 = Station(model, "C3_4", buffer_size=1)
c3_5 = Station(model, "C3_5", buffer_size=1)
m12 = Station(model, "M12", buffer_size=1)

m13 = Station(model, "M13", buffer_size=1)
m14 = Station(model, "M14", buffer_size=1)
c4_1 = Station(model, "C4_1", buffer_size=1)
c4_2 = Station(model, "C4_2", buffer_size=1)
c4_3 = Station(model, "C4_3", buffer_size=1)
c4_4 = Station(model, "C4_4", buffer_size=1)
c4_5 = Station(model, "C4_5", buffer_size=1)
m15 = Station(model, "M15", buffer_size=1)

m16 = Station(model, "M16", buffer_size=1)
m17 = Station(model, "M17", buffer_size=1)
m18 = Station(model, "M18", buffer_size=1)
m19 = Station(model, "M19", buffer_size=1)

sink = Sink(model, "Sink")
fork = Fork(model, "Fork", "Final Product")

# Define the customer classes

final = OpenClass(model, "Final Product", source, Dist.Determ(1))
component_a = OpenClass(model, "Component A", fork, Dist.Determ(0.5))
component_b = OpenClass(model, "Component B", fork, Dist.Determ(0.8))
component_c = OpenClass(model, "Component C", fork, Dist.Determ(1.2))
component_d = OpenClass(model, "Hinge Pin 1", fork, Dist.Determ(5))
component_e = OpenClass(model, "Hinge Connector 1", fork, Dist.Determ(5))
component_f = OpenClass(model, "Hinge Spring", fork, Dist.Determ(5))
component_g = OpenClass(model, "Hinge Pin 2", fork, Dist.Determ(5))
component_h = OpenClass(model, "Hinge Connector 2", fork, Dist.Determ(5))
component_i = OpenClass(model, "Hinge Pin 3", fork, Dist.Determ(5))
component_j = OpenClass(model, "Hinge Box", fork, Dist.Determ(5))
component_k = OpenClass(model, "Hinge Hook", fork, Dist.Determ(5))

# Create the network nodes

join1 = Join(model, "Join 1", final, 2)
join2 = Join(model, "Join 2", final, 2)
join3 = Join(model, "Join HP1", final, 2)
join4 = Join(model, "Join HC1", final, 2)
join5 = Join(model, "Join HS", final, 2)
join6 = Join(model, "Join HP2", final, 2)
join7 = Join(model, "Join HC2", final, 2)
join8 = Join(model, "Join HP3", final, 2)
join9 = Join(model, "Join HB", final, 2)
join10 = Join(model, "Join HH", final, 2)

# Set service times

m1.set_service(component_a, Dist.Determ(7))
b1.set_service(component_a, Dist.Determ(4))
b2.set_service(component_a, Dist.Determ(4))
b3.set_service(component_a, Dist.Determ(4))
b4.set_service(component_a, Dist.Determ(4))
b5.set_service(component_a, Dist.Determ(4))
m2.set_service(final, Dist.Determ(2))
b6.set_service(final, Dist.Determ(4))
b7.set_service(final, Dist.Determ(4))
b8.set_service(final, Dist.Determ(4))
b9.set_service(final, Dist.Determ(4))
b10.set_service(final, Dist.Determ(4))
b11.set_service(final, Dist.Determ(4))
b12.set_service(final, Dist.Determ(4))
b13.set_service(final, Dist.Determ(4))
b14.set_service(final, Dist.Determ(4))

m3.set_service(final, Dist.Determ(7))
m4.set_service(final, Dist.Determ(4))
c1_1.set_service(final, Dist.Determ(0.5))
c1_2.set_service(final, Dist.Determ(0.5))
c1_3.set_service(final, Dist.Determ(0.5))
c1_4.set_service(final, Dist.Determ(0.5))
c1_5.set_service(final, Dist.Determ(0.5))
m5.set_service(final, Dist.Determ(9))

m6.set_service(final, Dist.Determ(2))

m7.set_service(final, Dist.Determ(2))
c2_1.set_service(final, Dist.Determ(0.5))
c2_2.set_service(final, Dist.Determ(0.5))
c2_3.set_service(final, Dist.Determ(0.5))
c2_4.set_service(final, Dist.Determ(0.5))
c2_5.set_service(final, Dist.Determ(0.5))
m8.set_service(final, Dist.Determ(8))

m9.set_service(final, Dist.Determ(8))
m10.set_service(final, Dist.Determ(2))

m11.set_service(final, Dist.Determ(2))
c3_1.set_service(final, Dist.Determ(0.5))
c3_2.set_service(final, Dist.Determ(0.5))
c3_3.set_service(final, Dist.Determ(0.5))
c3_4.set_service(final, Dist.Determ(0.5))
c3_5.set_service(final, Dist.Determ(0.5))
m12.set_service(final, Dist.Determ(8))

m13.set_service(final, Dist.Determ(2))
m14.set_service(final, Dist.Determ(2))
c4_1.set_service(final, Dist.Determ(0.5))
c4_2.set_service(final, Dist.Determ(0.5))
c4_3.set_service(final, Dist.Determ(0.5))
c4_4.set_service(final, Dist.Determ(0.5))
c4_5.set_service(final, Dist.Determ(0.5))
m15.set_service(final, Dist.Determ(8))

m16.set_service(final, Dist.Determ(2))
m17.set_service(final, Dist.Determ(2))
m18.set_service(final, Dist.Determ(4))
m19.set_service(final, Dist.Determ(5))

# Define the routings

source.add_route(final, fork, 1)
fork.add_route(component_a, m1, 1)
fork.add_route(component_b, join1, 1)
fork.add_route(component_c, join2, 1)
fork.add_route(component_d, join3, 1)
fork.add_route(component_e, join4, 1)
fork.add_route(component_f, join5, 1)
fork.add_route(component_g, join6, 1)
fork.add_route(component_h, join7, 1)
fork.add_route(component_i, join8, 1)
fork.add_route(component_j, join9, 1)
fork.add_route(component_k, join10, 1)

m1.add_route(component_a, b1, 1)
b1.add_route(component_a, b2, 1)
b2.add_route(component_a, b3, 1)
b3.add_route(component_a, b4, 1)
b4.add_route(component_a, b5, 1)
b5.add_route(component_a, join1, 1)

join1.add_route(final, m2, 1)

m2.add_route(final, b6, 1)
b6.add_route(final, b7, 1)
b7.add_route(final, b8, 1)
b8.add_route(final, b9, 1)
b9.add_route(final, b10, 1)
b10.add_route(final, b11, 1)
b11.add_route(final, b12, 1)
b12.add_route(final, b13, 1)
b13.add_route(final, b14, 1)
b14.add_route(final, m3, 1)
m3.add_route(final, m4, 1)
m4.add_route(final, c1_1, 1)
c1_1.add_route(final, c1_2, 1)
c1_2.add_route(final, c1_3, 1)
c1_3.add_route(final, c1_4, 1)
c1_4.add_route(final, c1_5, 1)
c1_5.add_route(final, join2, 1)
join2.add_route(final, m5, 1)

m5.add_route(final, join3, 1)

join3.add_route(final, m6, 1)

m6.add_route(final, m7, 1)

m7.add_route(final, c2_1, 1)
c2_1.add_route(final, c2_2, 1)
c2_2.add_route(final, c2_3, 1)
c2_3.add_route(final, c2_4, 1)
c2_4.add_route(final, c2_5, 1)
c2_5.add_route(final, join4, 1)
join4.add_route(final, m8, 1)

m8.add_route(final, join5, 1)

join5.add_route(final, m9, 1)

m9.add_route(final, join6, 1)
join6.add_route(final, m10, 1)

m10.add_route(final, m11, 1)

m11.add_route(final, c3_1, 1)
c3_1.add_route(final, c3_2, 1)
c3_2.add_route(final, c3_3, 1)
c3_3.add_route(final, c3_4, 1)
c3_4.add_route(final, c3_5, 1)
c3_5.add_route(final, join7, 1)
join7.add_route(final, m12, 1)

m12.add_route(final, join8, 1)

join8.add_route(final, m13, 1)

m13.add_route(final, m14, 1)
m14.add_route(final, c4_1, 1)
c4_1.add_route(final, c4_2, 1)
c4_2.add_route(final, c4_3, 1)
c4_3.add_route(final, c4_4, 1)
c4_4.add_route(final, c4_5, 1)
c4_5.add_route(final, join9, 1)
join9.add_route(final, m15, 1)

m15.add_route(final, join10, 1)

join10.add_route(final, m16, 1)

m16.add_route(final, m17, 1)
m17.add_route(final, m18, 1)
m18.add_route(final, m19, 1)
m19.add_route(final, sink, 1)

model.add_measure()

# Export and run

path = model.write_jsimg()
ret = model.solve_jsimg()
print(ret)

if ret.stderr:
    print(ret.stderr.decode())


# %%
