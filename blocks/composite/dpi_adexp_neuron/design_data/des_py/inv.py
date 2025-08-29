from gdsfactory.read.import_gds import import_gds

from glayout import MappedPDK, sky130 , gf180 , ihp130
#from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle

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

def inverter(
        pdk: MappedPDK,
        width: tuple[float,float] = (3,3),
        length: tuple[float,float] = (None,None),
        fingers: tuple[int,int] = (1,1),
        multipliers: tuple[int,int] = (1,1),
        dummy_1: tuple[bool,bool] = (True,True),
        dummy_2: tuple[bool,bool] = (True,True),
        tie_layers1: tuple[str,str] = ("met2","met1"),
        tie_layers2: tuple[str,str] = ("met2","met1"),
        sd_rmult: int=1,
        **kwargs
        ) -> Component:

    pdk.activate()
    
    #top level component
    top_level = Component(name="inverter")

    #two fets
    fet_P = pmos(pdk, width=width[0], fingers=fingers[0], multipliers=multipliers[0], with_dummy=dummy_1, with_substrate_tap=False, length=length[0], tie_layers=tie_layers1, sd_rmult=sd_rmult, dnwell=False,**kwargs )
    fet_N = nmos(pdk, width=width[1], fingers=fingers[1], multipliers=multipliers[1], with_dummy=dummy_2, with_substrate_tap=False, length=length[1], tie_layers=tie_layers2, sd_rmult=sd_rmult, with_dnwell=False, **kwargs)

    top_level.info.update({"fet_P": fet_P, "fet_N": fet_N}) #for later access in other functions
    
    #Relative move
    fet_N_ref.movey(top_level.ymin - evaluate_bbox(fet_N)[1]/2 - pdk.util_max_metal_seperation()-1)
    
    fet_P_ref = top_level << fet_P
    fet_N_ref = top_level << fet_N 

    #Routing
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True) #met2 is the bottom layer. met3 is the top layer.
    
    #we need four such vias
    drain_P_via = top_level << viam2m3
    source_P_via = top_level << viam2m3
    gate_P_via = top_level << viam2m3

    drain_N_via = top_level << viam2m3
    gate_N_via = top_level << viam2m3
    
        
    drain_P_via.move(fet_P_ref.ports["multiplier_0_drain_W"].center).movex(-1.5)
    drain_N_via.move(fet_N_ref.ports["multiplier_0_drain_W"].center).movex(-1.5)

    source_P_via.move(fet_P_ref.ports["multiplier_0_source_E"].center).movex(1.5)

    gate_P_via.move(fet_P_ref.ports["multiplier_0_gate_E"].center).movex(1)
    gate_N_via.move(fet_N_ref.ports["multiplier_0_gate_E"].center).movex(1)


    top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_gate_E"], gate_P_via.ports["bottom_met_N"])
    top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_gate_E"], gate_N_via.ports["bottom_met_W"])
    top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_source_E"], source_P_via.ports["bottom_met_W"])
    top_level << straight_route(pdk, fet_P_ref.ports["multiplier_0_drain_W"], drain_P_via.ports["bottom_met_E"])
    top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_drain_W"], drain_N_via.ports["bottom_met_E"])

    top_level << straight_route(pdk, gate_P_via.ports["top_met_S"], gate_N_via.ports["top_met_S"])
    top_level << straight_route(pdk, drain_P_via.ports["top_met_N"], drain_N_via.ports["top_met_N"])

    try:
        top_level << straight_route(pdk, fet_N_ref.ports["multiplier_0_source_W"], fet_N_ref.ports["tie_W_top_met_W"], glayer1=tie_layers2[1], fullbottom=True)
    except:
        pass

    top_level.add_ports(fet_P_ref.get_ports_list(), prefix="P_")
    top_level.add_ports(fet_N_ref.get_ports_list(), prefix="N_")
    top_level.add_ports(drain_P_via.get_ports_list(), prefix="P_drain_")
    top_level.add_ports(source_P_via.get_ports_list(), prefix="P_source_")
    top_level.add_ports(gate_P_via.get_ports_list(), prefix="P_gate_")
    top_level.add_ports(drain_N_via.get_ports_list(), prefix="N_drain_")
    top_level.add_ports(gate_N_via.get_ports_list(), prefix="N_gate_")

    return component_snap_to_grid(rename_ports_by_orientation(top_level))

if __name__ == "__main__":
    comp = inverter(ihp130)
    # comp.pprint_ports()
    comp = add_inv_labels(comp, ihp130)
    comp.name = "INV"
    #comp.write_gds('out_INV.gds')
    comp.show()
    #print("...Running DRC...")
    #drc_result = gf180.drc_magic(comp, "INV")
    #drc_result = gf180.drc(comp)
    
