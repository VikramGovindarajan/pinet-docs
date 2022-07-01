# PFBR SG SS simulation

#geometry inputs
Do = 0.855
Di = 0.831
do = 0.0172
di = 0.0126
N = 547
L = 22.
E = 0.0322
ninc = 50

#sodium circuit
circuit1 = comp.Circuit("circuit1")
circuit1.assign_fluid("Na","User",incomp=True)
node1 = circuit1.add_node("node1",elevation=L)
node2 = circuit1.add_node("node2",elevation=0.)
Af = math.pi*Di**2/4.-N*math.pi*do**2/4.
Pw = math.pi*Di+N*math.pi*do
dh = 4.*Af/Pw
pipe1=circuit1.add_pipe(identifier="pipe1",diameter=dh,length=L,unode="node2",dnode="node1",cfarea=Af,fricopt='DW',roughness=30E-6,ncell=ninc,heat_input=0.)
bc1 = comp.BC("bc1","node1",'P',5.E5)
def fun1(time):
    if time <=900.:
        y = 798.-time/15.
    else:
        y = 798.-900./15.
    # y = 798.
    return y
bc3 = comp.BC("bc3","node1",'T',fun1)
bc2 = comp.BC("bc2","node2",'msource',-730.)

def script3(flow_elem,wall_node):
    heat_flux = wall_node.heat_transfer/(math.pi*flow_elem.diameter*flow_elem.delx)/flow_elem.pipe.npar
    mass_velocity = flow_elem.vflow_gues*flow_elem.ther_gues.rhomass()/flow_elem.cfarea
    term5 = heat_flux**(-0.125)
    term6 = mass_velocity**(-1./3.)
    term7 = (flow_elem.diameter*1000.0)**(-0.07)
    term8 = math.exp(-0.00795*flow_elem.spres_gues*1.E-5)
    quality_crit=76.6*term5*term6*term7*term8

    return quality_crit

#water circuit
circuit2 = comp.Circuit("circuit2")
circuit2.assign_fluid("Water","CoolProp",incomp=True)
node3 = circuit2.add_node("node3",elevation=0.)
node4 = circuit2.add_node("node4",elevation=L)
def fun3(time):
    if time <=10:
        y = (156.-time)*1.E6
    else:
        y = (156.-10.)*1.E6
    return y
pipe2=circuit2.add_pipe(identifier="pipe2",diameter=di,length=L,unode="node3",dnode="node4",fricopt='DW',roughness=30E-6,ncell=ninc,npar=N,heat_input=0.,flag_tp=True,qcrit=script3) #158.E6
bc4 = comp.BC("bc4","node3",'P',170.E5)
bc5 = comp.BC("bc5","node3",'T',508.)
bc6 = comp.BC("bc6","node4",'msource',-70.3)

Au = math.pi*do*L*N
Ad = math.pi*di*L*N
def script1(flow_elem,wall_node):
    global dh,L,E,do
    Pe = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
    Nu = 8 * (dh/L + 0.027*(E/do-1.1)**0.46) * Pe**0.6
    h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
    return h
    
def script2(flow_elem,wall_node):
    
    index_spl_nb = wall_node.layer.hslab.dind_spl_nb
    index_nb_pd = wall_node.layer.hslab.dind_nb_pd
    index_pd_spv = wall_node.layer.hslab.dind_pd_spv
    
    if ( flow_elem.faceno < index_spl_nb ): #single phase liquid
        Re = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter/flow_elem.ther_gues.viscosity() #may be flow_elem.Re directly used
        Pr = flow_elem.ther_gues.viscosity()*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
        n = 0.43
        if Re < 2300.:
            Nu = 4.364
        elif Re > 5000.:
            Nu = 0.021*Re**0.8*Pr**n
        else:
            Nu1 = 4.364
            Nu2 = 0.023*5000.**0.8*Pr**n
            Nu = Nu1 + (Re-2300.)*(Nu2-Nu1)/(5000.-2300.)
        h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
        Sc = h*flow_elem.stemp_gues
        Sp = -h
        # h = 20000.
    elif ( flow_elem.faceno < index_nb_pd ): #nucleate boiling

        Ref = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter/flow_elem.ther_gues.muf
        Prf = flow_elem.ther_gues.muf*flow_elem.ther_gues.cpf/flow_elem.ther_gues.kf
        hc=0.019*flow_elem.ther_gues.kf/flow_elem.diameter*Ref**0.8*Prf**0.333
		
        Tsat = flow_elem.ther_gues.Tsat
        hfg = flow_elem.ther_gues.hg-flow_elem.ther_gues.hf
        term1 = flow_elem.ther_gues.muf*hfg
        sigma = (7.66789E-02) - 1.675265E-04*(Tsat-273.) - 1.0E-07*(Tsat-273.)*(Tsat-273.) #pending move to appropriate location
        term2 = (grav*(flow_elem.ther_gues.rhof-flow_elem.ther_gues.rhog)/sigma)**0.5
        term3 = (flow_elem.ther_gues.cpf/(0.013*hfg*Prf**1.7))**3
        
        C = term1*term2*term3
        
        Tw = wall_node.temp_gues
        Tf = flow_elem.stemp_gues
        hb = C*(Tw-Tsat)**2
        h = (hb+hc)*(Tw-Tsat)/(Tw-Tf)
        
        B = hc
        Sp = -3.*C*(Tw-Tsat)**2-B
        Sc = -C*((Tw-Tsat)**3-3.*(Tw-Tsat)**2*Tw) + B*Tsat
        
    elif ( flow_elem.faceno < index_pd_spv ): #post dryout
        x = flow_elem.ther_gues.Q()
        if x >1.: #to avoid complex number error #pending improvise
            x = 1.
        Yf = (1. - 0.1*(flow_elem.ther_gues.rhof/flow_elem.ther_gues.rhog-1.)**0.4*(1.-x)**0.4) * (x+flow_elem.ther_gues.rhog/flow_elem.ther_gues.rhof*(1.0-x))**0.8
        Re_vap = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter/flow_elem.ther_gues.mug
        prandtl_vap = flow_elem.ther_gues.mug * flow_elem.ther_gues.cpg/flow_elem.ther_gues.kg
        Nu=0.021*Re_vap**0.8*prandtl_vap**0.43
        Nu = Nu * Yf
        h = Nu * flow_elem.ther_gues.flstate.conductivity() / flow_elem.diameter
        Sc = h*flow_elem.stemp_gues
        Sp = -h
        # h = 20000.
    else: #single phase vapor
        Re = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter/flow_elem.ther_gues.viscosity() #may be flow_elem.Re directly used
        Pr = flow_elem.ther_gues.viscosity()*flow_elem.ther_gues.cpmass()/flow_elem.ther_gues.conductivity()
        n = 0.43
        if Re < 2300.:
            Nu = 4.364
        elif Re > 5000.:
            Nu = 0.021*Re**0.8*Pr**n
        else:
            Nu1 = 4.364
            Nu2 = 0.023*5000.**0.8*Pr**n
            Nu = Nu1 + (Re-2300.)*(Nu2-Nu1)/(5000.-2300.)
        h = Nu * flow_elem.ther_gues.conductivity() / flow_elem.diameter
        Sc = h*flow_elem.stemp_gues
        Sp = -h
    return Sc,Sp,h
    # h = 20000.
    # Sc = h*flow_elem.stemp_gues
    # Sp = -h
    # return h

# def script4(flow_elem):
    # global index_spl_nb

    # if (flow_elem.faceno < index_spl_nb):
        # if (flow_elem.Re == 0.):
            # f = 0.1*(100./400.)**0.25
        # else:
            # f = 0.1*(100./flow_elem.Re)**0.25
    # else:
        # if (flow_elem.ther_gues.Q()<1.0):
            # Re_liq = flow_elem.ther_gues.rhomass()*abs(flow_elem.velocity)*flow_elem.diameter/muf
            # if (Re_liq == 0.):
                # f = 0.1*(100./400.)**0.25
            # else:
                # f = 0.1*Math.Pow(100.0/Re_liq,0.25);

            # R = flow_elem.ther_gues.Q()*100.
            # U = math.log(R)        
            # Y1 = 0.3600674 + 2.054117*U - 1.718411*U*U + 0.57778*U*U*U - 0.05518658*U*U*U*U
            
            # if (flow_elem.ther_gues.Q() <= 0):
                # ak =1.
            # else:
                # if (Y1<=0):
                    # ak = 1.
                # else:
                    # Y2 = 2.499461 - 0.3748926*U + 1.582906*U*U - 0.285898*U*U*U + 0.01903476*U*U*U*U
                    # B = math.log(Y2/Y1) / math.log(8.)
                    # X = 4.3429*math.log(220.*1.E5/flow_elem.spres_gues)
                    # Y = Y1*(X**B)
                    # ak = math.exp(0.230259*Y)
            # f = f * ak * density/density_liq
        # else:
            # f = 0.1*(100.0/Re)**0.25

    # return f
        

# tube thickness
hslab1 = HTcomp.HSlab("hslab1",ucomp="pipe1",uvar="pipe",uval=[script1],dcomp="pipe2",dvar="pipenl",dval=[script2],uarea=Au,config="parallel")
layer1 = hslab1.add_layer(thk_elem=(do-di)/2.,thk_cros=L,nnodes=3,darea=Ad,mat='chromoly')

# import solver_settings
# solver_settings.relax_enth = 0.35
# solver_settings.relax_pres = 0.9
# solver_settings.conv_crit_ht = 1.E-4
# solver_settings.conv_crit_flow = 1.E-6
# solver_settings.conv_crit_temp_trans = 1.E-4
# solver_settings.conv_crit_temp_SS = 1.E-7

import scheduler
scheduler.delt = 1.
scheduler.etime = 900.
