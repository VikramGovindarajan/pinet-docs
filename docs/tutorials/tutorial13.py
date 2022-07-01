# FFTF SA problem
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Na13","User",incomp=True)

#node inputs
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")

#pipe inputs
pipe1=circuit1.add_pipe("pipe1",length=0.9144,diameter=0.003238,unode="node1",dnode="node2",fricopt=0.02,roughness=0.,ncell=10,heat_input=0.0,cfarea=0.00433)

def fun1(time):
    if time <=100.:
        y = -25.3928+time/10.
    else:
        y = -25.3928+10.
    return y

#boundary conditions
bc1 = comp.BC("bc1","node1",'P',7.E5)
bc2 = comp.BC("bc2","node1",'T',598.899)
bc3 = comp.BC("bc3","node2",'msource',fun1)

def script1(flow_elem,WallTemp):
    Pe = flow_elem.ther_gues.rhomass()*flow_elem.velocity*flow_elem.diameter*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
    Nu = 5.0 + 0.025*Pe**0.8
    h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
    return h

snode1 = HTcomp.SNode("snode1")

hslab1 = HTcomp.HSlab("hslab1",ucomp="pipe1",uvar="pipe",uval=[script1],dcomp="snode1",dvar="hflux",dval=0.0,uarea=3.642,nlayers=3)
layer1 = hslab1.add_layer(thk_elem=3.81E-4,thk_cros=0.9144,nnodes=2,darea=3.167,mat='SS13')
layer2 = hslab1.add_layer(thk_elem=7.5E-5,thk_cros=0.9144,nnodes=2,darea=3.079,mat='gap13',heat_input=0.)
layer3 = hslab1.add_layer(thk_elem=0.00247,thk_cros=0.9144,nnodes=2,darea=3.079,mat='MOX13',heat_input=3174806.,AFF=[0.0740, 0.0937, 0.1107, 0.1222, 0.1271, 0.1248,0.1156, 0.0999, 0.0786, 0.0534])

import scheduler
scheduler.delt = 1.0
scheduler.etime = 200.

# val1 = post.Monitor("node1","tpres_gues")
val2 = post.Monitor("node2","stemp_gues")
