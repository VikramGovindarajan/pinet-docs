# simple NC problem U section (open loop) for validation

#circuit inputs
circuit1 = comp.Circuit("circuit1",solveSS=True)
circuit1.assign_fluid("Water","CoolProp",incomp=True)

#node inputs
node1 = circuit1.add_node("node1",elevation=0.2)
node2 = circuit1.add_node("node2",elevation=0.)
node3 = circuit1.add_node("node3",elevation=0.,ttemp_old=289.)
node4 = circuit1.add_node("node4",elevation=0.2,ttemp_old=289.)

#pipe inputs
pipe1=circuit1.add_pipe(identifier="pipe1",diameter=0.1,length=0.2,unode="node1",dnode="node2",fricopt=0.05,roughness=30.E-6,ncell=10)
pipe2=circuit1.add_pipe(identifier="pipe2",diameter=0.1,length=0.2,unode="node2",dnode="node3",fricopt=0.05,roughness=30.E-6,ncell=10,heat_input=2.E4)
pipe3=circuit1.add_pipe(identifier="pipe3",diameter=0.1,length=0.2,unode="node3",dnode="node4",fricopt=0.05,roughness=30.E-6,ncell=10)


#boundary conditions
bc1 = comp.BC("bc1","node1",'P',1.E5)
bc2 = comp.BC("bc2","node1",'T',288.)
bc3 = comp.BC("bc3","node4",'P',1.E5)
# bc4 = comp.BC("bc4","node4",'T',289.)


import solver_settings
solver_settings.temp_solve = True
solver_settings.conv_crit_temp_SS = 1.E-7
solver_settings.conv_crit_flow = 1.E-7
