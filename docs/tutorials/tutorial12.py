# 2 phase NC problem (SS flow rate)

#circuit inputs
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Water","CoolProp",incomp=True)

#node inputs
node1 = circuit1.add_node("node1",elevation=2.445)
node2 = circuit1.add_node("node2",elevation=0.)
node3 = circuit1.add_node("node3",elevation=0.)
node4 = circuit1.add_node("node4",elevation=0.575)
node5 = circuit1.add_node("node5",elevation=2.21)
node6 = circuit1.add_node("node6",elevation=2.445,ttemp_old=555.)

#pipe inputs
pipe1=circuit1.add_pipe("pipe1",0.0199,2.445,"node1","node2",'BL',30.E-6,10)
pipe2=circuit1.add_pipe("pipe2",0.0199,2.02,"node2","node3",'BL',30.E-6,10)
pipe3=circuit1.add_pipe("pipe3",0.0199,0.575,"node3","node4",'BL',30.E-6,10,heat_input=25000.)
pipe4=circuit1.add_pipe(identifier="pipe4",diameter=0.0199,length=1.635,unode="node4",dnode="node5",fricopt='BL',roughness=30.E-6,ncell=10)
pipe5=circuit1.add_pipe("pipe5",0.0199,2.036,"node5","node6",'BL',30.E-6,10)

#boundary conditions
bc1 = comp.BC("bc1","node1",'P',70.E5)
bc2 = comp.BC("bc2","node1",'T',549.)
bc3 = comp.BC("bc3","node6",'P',70.E5) #69.35
# bc3 = comp.BC("bc3","node6",'msource',-0.026975 )

import solver_settings
solver_settings.conv_crit_temp_SS = 1.E-7
solver_settings.conv_crit_flow = 1.E-7
