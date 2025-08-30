from gdsfactory.read.import_gds import import_gds

from glayout import MappedPDK, sky130 , gf180 , ihp130
#from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle
from glayout import resistor
from glayout import nmos, pmos
from glayout import via_stack, via_array
from glayout import rename_ports_by_orientation
from glayout import tapring
from glayout import mimcap_array, mimcap
from glayout.util.comp_utils import evaluate_bbox, prec_center, prec_ref_center, align_comp_to_port, prec_array, movey
from glayout.util.port_utils import add_ports_perimeter,print_ports
from glayout.util.snap_to_grid import component_snap_to_grid
from glayout.spice.netlist import Netlist

from glayout.routing.straight_route import straight_route
from glayout.routing.c_route import c_route
from glayout.routing.L_route import L_route

###### Only Required for IIC-OSIC Docker
import os
import subprocess

# Run a shell, source .bashrc, then printenv
cmd = 'bash -c "source ~/.bashrc && printenv"'
result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
env_vars = {}
for line in result.stdout.splitlines():
    if '=' in line:
        key, value = line.split('=', 1)
        env_vars[key] = value

# Now, update os.environ with these
os.environ.update(env_vars)

from inv import inverter

def dpi_inv2(pdk: MappedPDK,
        multipliers: tuple[int,int] = (1,1),
        dummy_1: tuple[bool,bool] = (True,True),
        dummy_2: tuple[bool,bool] = (True,True),
        tie_layers1: tuple[str,str] = ("met2","met1"),
        tie_layers2: tuple[str,str] = ("met2","met1"),
    ) -> Component:
    pdk.activate()
    top_level = Component(name="dpi_inv2")

    mp14=resistor(pdk,width=2.4,length=3.0,num_series=1)
    mp14_ref=prec_ref_center(mp14)
    top_level.add(mp14_ref)

    width=(2.4,1.2);length=(0.28,0.28);fingers=(1,1);
    
    #two fets
    fet_P = pmos(pdk, width=width[0], fingers=fingers[0], length=length[0], tie_layers=tie_layers1,multipliers=multipliers[0], with_dummy=True, with_substrate_tap=False, dnwell=False)
    fet_N = nmos(pdk, width=width[1], fingers=fingers[1], multipliers=multipliers[1],length=length[1], tie_layers=tie_layers2, with_dummy=True, with_substrate_tap=False, with_dnwell=False)

    # #top_level.info.update({"fet_P": fet_P, "fet_N": fet_N}) #for later access in other functions
    
    fet_P_ref = prec_ref_center(fet_P)
    fet_P_ref.movey(top_level.ymin - evaluate_bbox(fet_P)[1]/2 - pdk.util_max_metal_seperation())
    top_level.add(fet_P_ref)
    fet_N_ref = prec_ref_center(fet_N) 
    #Relative move
    fet_N_ref.movey(top_level.ymin - evaluate_bbox(fet_N)[1]/2 - pdk.util_max_metal_seperation())
    top_level.add(fet_N_ref)

     top_level << L_route(pdk, fet_P_ref.ports["multiplier_0_gate_E"], gate_P_via.ports["bottom_met_N"])








    

    # #Routing
    # viam2m3 = via_stack(pdk, "met2", "met3", centered=True) #met2 is the bottom layer. met3 is the top layer.
    
    # #we need four such vias
    # drain_P_via = top_level << viam2m3
    # #source_P_via = top_level << viam2m3
    # gate_P_via = top_level << viam2m3

    # drain_N_via = top_level << viam2m3
    # gate_N_via = top_level << viam2m3

    # in_via = top_level << viam2m3
    # out_via = top_level << viam2m3
    # vdd_via = top_level << viam2m3
    # vss_via = top_level << viam2m3
        
    # drain_P_via.move(fet_P_ref.ports["multiplier_0_drain_W"].center).movex(-1.5)
    # drain_N_via.move(fet_N_ref.ports["multiplier_0_drain_W"].center).movex(-1.5)

    # #source_P_via.move(fet_P_ref.ports["multiplier_0_source_E"].center).movex(1.5)

    # gate_P_via.move(fet_P_ref.ports["multiplier_0_gate_E"].center).movex(1)
    # gate_N_via.move(fet_N_ref.ports["multiplier_0_gate_E"].center).movex(1)

    # in_via.move(fet_P_ref.ports["multiplier_0_gate_E"].center).movex(3)
    # out_via.move(fet_N_ref.ports["multiplier_0_drain_W"].center).movex(-3.5)

    # vdd_via.move(fet_P_ref.ports["multiplier_0_source_W"].center).movex(-3.5)
    # vss_via.move(fet_N_ref.ports["multiplier_0_source_W"].center).movex(-3.5)

    
    

    # top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_gate_E"], gate_P_via.ports["bottom_met_N"])
    # top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_gate_E"], gate_N_via.ports["bottom_met_W"])
    # #top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_source_E"], source_P_via.ports["bottom_met_W"])
    # top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_drain_W"], drain_P_via.ports["bottom_met_E"])
    # top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_drain_W"], drain_N_via.ports["bottom_met_E"])
    
    # top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_gate_E"], in_via.ports["bottom_met_W"])
    # top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_drain_W"], out_via.ports["bottom_met_W"])
    
    
    # gate_short=top_level << straight_route(pdk, gate_P_via.ports["top_met_S"], gate_N_via.ports["top_met_S"])
    # drain_short=top_level << straight_route(pdk, drain_P_via.ports["top_met_N"], drain_N_via.ports["top_met_N"])
    
    
    # top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_source_W"], fet_N_ref.ports["tie_W_top_met_W"], glayer1=tie_layers2[1], fullbottom=True)
    # top_level << straight_route(pdk, vdd_via.ports["bottom_met_E"],fet_P_ref.ports["tie_W_top_met_W"],glayer1=tie_layers2[1], fullbottom=True )
    
    
    # top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_source_W"], fet_N_ref.ports["tie_W_top_met_W"], glayer1=tie_layers2[1], fullbottom=True)
    # top_level << straight_route(pdk, vss_via.ports["bottom_met_E"],fet_N_ref.ports["tie_W_top_met_W"],glayer1=tie_layers2[1], fullbottom=True )









    

    

    # mp7_12=inverter(ihp130,)
    # mp7_12_ref=prec_ref_center(mp7_12)
    # mp7_12_ref.movey(top_level.ymin - evaluate_bbox(mp7_12)[1]/2 - pdk.util_max_metal_seperation())

    #mp14.pprint_ports()
    #mp7_12.pprint_ports()

    #top_level << L_route(pdk, mp14.ports["pfet_gate_W"], mp7_12.ports["vdd_via_top_met_N"])

    # mp16=resistor(pdk,width=2.4,length=3.0,num_series=1)
    # mp16_ref=prec_ref_center(mp14)
    # mp16_ref.movex(top_level.xmax + 4.5 * (evaluate_bbox(mp16)[0]/2) + pdk.util_max_metal_seperation())
    

    # mp13_15=inverter(ihp130,width=(2.4,1.2),length=(0.28,0.28),fingers=(1,1))
    # mp13_15_ref=prec_ref_center(mp13_15)
    # mp13_15_ref.movex(top_level.xmax + 3.5 * (evaluate_bbox(mp13_15)[0]/2) + pdk.util_max_metal_seperation())
    # mp13_15_ref.movey(top_level.ymin - evaluate_bbox(mp13_15)[1]/2 - pdk.util_max_metal_seperation())
    # top_level.add(mp16_ref)
    # top_level.add(mp13_15_ref)
    # top_level.add(mp7_12_ref)

    

    return component_snap_to_grid(rename_ports_by_orientation(top_level))
    


if __name__ == "__main__":
    comp = dpi_inv2(ihp130)
    # comp.pprint_ports()
    #comp = add_inv_labels(comp, ihp130)
    comp.name = "DPINV"
    #comp.write_gds('out_INV.gds')
    comp.show()
    #print("...Running DRC...")
    #drc_result = gf180.drc_magic(comp, "INV")
    #drc_result = gf180.drc(comp)
    