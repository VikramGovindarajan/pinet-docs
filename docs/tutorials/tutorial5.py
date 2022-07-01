# Greyvenstein (2002) problem 4

#circuit inputs
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("He","User")

#node inputs
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")

#pipe inputs
pipe1=circuit1.add_pipe("pipe1",0.1,10.,"node1","node2",0.02,0.,40)

#boundary conditions
def fun1(t):
    # y = 700.*1000.
    import math
    y = (650. + 50.*math.exp(-0.004*t))*1000.
    # print t
    return y

bc1 = comp.BC("bc1","node1",'P',fun1)
bc2 = comp.BC("bc2","node1",'T',300.)
bc3 = comp.BC("bc3","node2",'P',650.*1000.)
#bc3 = comp.BC("bc3","node2",'msource',-1.75)

val1 = post.Monitor("node1","msource")

import scheduler
scheduler.etime = 1800.
scheduler.delt = 10.
