		

#circuit inputs
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("water1","User",incomp=True)

#node inputs
node1 = circuit1.add_node("node1")
node2 = circuit1.add_node("node2")
node3 = circuit1.add_node("node3")
node4 = circuit1.add_node("node4")
node5 = circuit1.add_node("node5")
node6 = circuit1.add_node("node6")
node7 = circuit1.add_node("node7")
node8 = circuit1.add_node("node8")
node9 = circuit1.add_node("node9")
node10 = circuit1.add_node("node10")
node11 = circuit1.add_node("node11")
node12 = circuit1.add_node("node12")

#pipe inputs
pipe1 =circuit1.add_pipe("pipe1", 0.305,457.2,"node1", "node2", 'HW',130.,1)
pipe2 =circuit1.add_pipe("pipe2", 0.203,304.8,"node2", "node3", 'HW',130.,1)
pipe3 =circuit1.add_pipe("pipe3", 0.203,365.8,"node3", "node4", 'HW',120.,1)
pipe4 =circuit1.add_pipe("pipe4", 0.203,609.6,"node4", "node5", 'HW',120.,1)
pipe5 =circuit1.add_pipe("pipe5", 0.203,853.4,"node6", "node5", 'HW',120.,1)
pipe6 =circuit1.add_pipe("pipe6", 0.203,335.3,"node7", "node6", 'HW',120.,1)
pipe7 =circuit1.add_pipe("pipe7", 0.203,304.8,"node8", "node7", 'HW',120.,1)
pipe8 =circuit1.add_pipe("pipe8", 0.203,762.0,"node9", "node8", 'HW',120.,1)
pipe9 =circuit1.add_pipe("pipe9", 0.203,243.8,"node1", "node9", 'HW',100.,1)
pipe10=circuit1.add_pipe("pipe10",0.152,396.2,"node9", "node10",'HW',100.,1)
pipe11=circuit1.add_pipe("pipe11",0.152,304.8,"node10","node11",'HW',100.,1)
pipe12=circuit1.add_pipe("pipe12",0.254,335.3,"node11","node12",'HW',130.,1)
pipe13=circuit1.add_pipe("pipe13",0.254,304.8,"node12","node5", 'HW',130.,1)
pipe14=circuit1.add_pipe("pipe14",0.152,548.6,"node10","node8", 'HW',120.,1)
pipe15=circuit1.add_pipe("pipe15",0.152,335.3,"node2","node10", 'HW',120.,1)
pipe16=circuit1.add_pipe("pipe16",0.152,548.6,"node11","node7", 'HW',120.,1)
pipe17=circuit1.add_pipe("pipe17",0.254,365.9,"node3","node11", 'HW',130.,1)
pipe18=circuit1.add_pipe("pipe18",0.152,548.6,"node12","node6", 'HW',120.,1)
pipe19=circuit1.add_pipe("pipe19",0.152,396.2,"node4","node12", 'HW',120.,1)

#boundary conditions
bc1 = comp.BC("bc1","node1",'msource',104.1)
bc2 = comp.BC("bc2","node9",'msource',-37.85)
bc3 = comp.BC("bc3","node6",'msource',-25.24)
bc4 = comp.BC("bc4","node5",'msource',34.7)
bc5 = comp.BC("bc5","node4",'msource',-31.55)
bc6 = comp.BC("bc6","node11",'P',1.E5)

# import solver_settings
# solver_settings.temp_solve = True
from PINET import scheduler
scheduler.etime = 50.
scheduler.delt = 1.