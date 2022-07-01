# Wichowski (1991)

#circuit inputs
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Water","User")

#node inputs
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")

#pipe inputs
pipe1=circuit1.add_pipe("pipe1",0.8,6000.,"node1","node2",'DW',2.E-3,60)
wall1=pipe1.add_wall(thk=0.019,mat='SS3',restraint="long")

#boundary conditions
bc1 = comp.BC("bc1","node1",'P',1.E6)

bc2 = comp.BC("bc2","node2",'msource',-753.6)
def fun1(time,delt):
    if time <= 20:
        y = -753.6*(20.-time)/20.
    else:
        y = 0.
    
    return y
action_setup.Action("bc2","bval",fun1)
#bc3 = comp.BC("bc3","node1",'T',300.)

from PINET import scheduler
scheduler.delt = 0.005
scheduler.etime = 95.0

from PINET import solver_settings
solver_settings.temp_solve = False

val1 = post.Monitor("node2","tpres_gues")
