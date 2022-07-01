# Closed loop with pump problem

# #left leg He cooling jacket circuit
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Na","User")
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")
pipe1 = circuit1.add_pipe("pipe1",0.0174,2.5,"node1","node2",'DW',30.,5)
bc1 = comp.BC("bc1","node1",'P',5.E5)
# bc2 = comp.BC("bc2","node1",'T',533.)
# bc3 = comp.BC("bc3","node2",'msource',-1.6)

# circuit1 = comp.Circuit("circuit1")
# circuit1.assign_fluid("Na","User")
# node3 = circuit1.add_node("node3")
# node4 = circuit1.add_node("node4")
x = np.array([0.,0.0005,0.00186,0.0025,0.003])
y = np.array([150000.,147000.,132793.,80000.,0.])
pump1=circuit1.add_pump("pump1","node2","node1",x,y)
# bc4 = comp.BC("bc4","node3",'P',3.67207E5)
# bc5 = comp.BC("bc5","node3",'T',533.)
# bc6 = comp.BC("bc6","node4",'msource',-1.6)
# bc6 = comp.BC("bc6","node3",'P',5.E5)

# val1 = post.Monitor("node6","tpres_gues")
