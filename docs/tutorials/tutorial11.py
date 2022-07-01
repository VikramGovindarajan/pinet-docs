# simple NC problem HHHC configuration for validation

#circuit inputs
circuit1 = comp.Circuit("circuit1",solveSS=True)
circuit1.assign_fluid("Water","CoolProp",incomp=True)

circuit2 = comp.Circuit("circuit2")
circuit2.assign_fluid("Water","CoolProp",incomp=True)

#node inputs
node1 = circuit1.add_node("node1",elevation=0.)
node2 = circuit1.add_node("node2",elevation=2.2,ttemp_old=325.)
node3 = circuit1.add_node("node3",elevation=2.2)
node4 = circuit1.add_node("node4",elevation=0.)

node5 = circuit2.add_node("node5")
node6 = circuit2.add_node("node6")

#pipe inputs
pipe1=circuit1.add_pipe(identifier="pipe1",diameter=0.026,length=2.2,unode="node1",dnode="node2",fricopt=0.05,roughness=30.,ncell=5)
pipe2=circuit1.add_pipe("pipe2",0.026,1.415,"node2","node3",0.05,30.,5)
pipe3=circuit1.add_pipe("pipe3",0.026,2.2,"node3","node4",0.05,30.,5)
pipe4=circuit1.add_pipe("pipe4",0.026,1.415,"node4","node1",0.05,30.,5,heat_input=1000.)

pipe5=circuit2.add_pipe(identifier="pipe5",diameter=0.004,length=1.415,unode="node5",dnode="node6",fricopt='DW',roughness=30.E-5,ncell=5,cfarea=0.000188)

#boundary conditions
bc1 = comp.BC("bc1","node5",'P',2.E5)
bc2 = comp.BC("bc2","node5",'T',283.)
bc3 = comp.BC("bc3","node6",'msource',-0.1666667)

bc4 = comp.BC("bc4","node1",'P',70.E5,trans=False)
bc5 = comp.BC("bc5","node1",'T',330.,trans=False)

#Heat Slabs
Au = math.pi*0.026*0.8
Ad = math.pi*0.028*0.8
hslab1 = HTcomp.HSlab("hslab1",ucomp="pipe2",uvar="pipe",uval=[1000.],dcomp="pipe5",dvar="pipe",dval=[1000.],uarea=Au,config="counter",solveSS=True)
layer1 = hslab1.add_layer(thk_elem=0.002,thk_cros=1.415,nnodes=3,darea=Ad,solname='glass',sollib='thinmam')

from PINET import scheduler
scheduler.delt = 1.0
scheduler.etime = 10000.

from PINET import solver_settings
solver_settings.temp_solve = True
solver_settings.T_ambient = 283.
solver_settings.conv_crit_temp_SS = 1.E-7
solver_settings.conv_crit_flow = 1.E-7
