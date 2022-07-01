# PFBR IHX

import math

#primary circuit (IHX shell)
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Nacase8","User",incomp=True)
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")
Af = 0.25*math.pi*1.831**2 - 3600*0.25*math.pi*0.019**2
Pw = math.pi*(1.831+3600*0.019)
dh = 4.*Af/(Pw)
pipe1=circuit1.add_pipe("pipe1",dh,7.5,"node1","node2",'DW',30.,20,cfarea=Af,npar=1)

bc1 = comp.BC("bc1","node1",'P',5.E5)
bc2 = comp.BC("bc2","node1",'T',817.)
bc3 = comp.BC("bc3","node2",'msource',-1644.)

#secondary circuit (IHX tube)
circuit2 = comp.Circuit("circuit2")
circuit2.assign_fluid("Nacase8","User",incomp=True)
node3 = circuit2.add_node("node3")
node4 = circuit2.add_node("node4")
pipe2=circuit2.add_pipe("pipe2",0.0174,7.5,"node3","node4",'DW',30.,20,npar=3600)
bc4 = comp.BC("bc4","node3",'P',5.E5)
bc5 = comp.BC("bc5","node3",'T',628.)
bc6 = comp.BC("bc6","node4",'msource',-1461.)

Au = math.pi*0.019*7.5*3600
Ad = math.pi*0.0174*7.5*3600
def script1(flow_elem,WallTemp):
    Pe = flow_elem.ther_gues.rhomass()*flow_elem.velocity*flow_elem.diameter*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
    Nu = 6 + 0.006*Pe
    h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
    Sc = h*flow_elem.stemp_gues
    Sp = -h
    return Sc,Sp,h
    # return h
def script2(flow_elem,WallTemp):
    Pe = flow_elem.ther_gues.rhomass()*flow_elem.velocity*flow_elem.diameter*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
    Nu = 4.82 + 0.0185*Pe**0.827
    h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
    Sc = h*flow_elem.stemp_gues
    Sp = -h
    return Sc,Sp,h
    # return h
hslab1 = HTcomp.HSlab("hslab1",ucomp="pipe1",uvar="pipenl",uval=[script1],dcomp="pipe2",dvar="pipenl",dval=[script2],uarea=Au,config="counter",nlayers=1)
layer1 = hslab1.add_layer(thk_elem=0.0016,thk_cros=7.5,nnodes=3,darea=Ad,solname='SScase8',sollib="User")


def fun1(time):
    if time <=10.:
        y = 817.-5*time
    else:
        y = 767.
    return y
action_setup.Action("bc2","bval",fun1)

from PINET import scheduler
scheduler.etime = 50.
scheduler.delt = 1.