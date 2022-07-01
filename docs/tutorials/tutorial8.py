# Two phase fluid simulation Collier example 2.1

#circuit inputs
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Water","CoolProp",incomp=True)

#node inputs
node1 = circuit1.add_node("node1",elevation=0.)
node2 = circuit1.add_node("node2",elevation=3.66)

#pipe inputs
pipe1=circuit1.add_pipe("pipe1",0.01016,3.66,"node1","node2",'BL',30.E-6,20,heat_input=100.E3,flag_tp=True)

#boundary conditions
bc1 = comp.BC("bc1","node1",'P',68.9E5)
bc3 = comp.BC("bc3","node1",'T',477.15)

# def fun1(time):
    # if time <= 20:
        # y = -753.6*(20.-time)/20.
    # else:
        # y = 0.
    
    # return y
bc2 = comp.BC("bc2","node2",'msource',-0.108)
