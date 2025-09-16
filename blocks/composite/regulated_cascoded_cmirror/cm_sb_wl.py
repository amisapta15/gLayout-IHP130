from glayout import MappedPDK, sky130,gf180
from glayout import nmos, pmos, tapring,via_stack

from glayout.spice.netlist import Netlist
from glayout.routing import c_route,L_route,straight_route

from gdsfactory.cell import cell
from gdsfactory.component import Component, copy
from gdsfactory.components.rectangle import rectangle
from gdsfactory.routing.route_quad import route_quad
from gdsfactory.routing.route_sharp import route_sharp

from gdsfactory.component import Component
from gdsfactory.component_reference import ComponentReference
from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle

from glayout.util.comp_utils import evaluate_bbox, prec_center, align_comp_to_port, prec_ref_center,movex,movey
from glayout.util.snap_to_grid import component_snap_to_grid
from glayout.util.port_utils import set_port_orientation, rename_ports_by_orientation, create_private_ports, add_ports_perimeter, get_orientation
from itertools import product

###### Only Required for IIC-OSIC Docker
import os
import subprocess
from pathlib import Path
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
###############################################################################
from typing import Optional, Union
import time

def add_lvcm_labels(lvcm_in: Component,
                pdk: MappedPDK
                ) -> Component:
	
    lvcm_in.unlock()
    # list that will contain all port/comp info
    move_info = list()
    # create labels and append to info list
    # gnd
    gndlabel = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.5,0.5),centered=True).copy()
    gndlabel.add_label(text="GND",layer=pdk.get_glayer("met2_label"))
    move_info.append((gndlabel,lvcm_in.ports["M_1_B_tie_N_top_met_N"],None))
    
    #currentbias
    ibias1label = rectangle(layer=pdk.get_glayer("met3_pin"),size=(0.5,0.5),centered=True).copy()
    ibias1label.add_label(text="IBIAS1",layer=pdk.get_glayer("met3_label"))
    move_info.append((ibias1label,lvcm_in.ports["M_1_A_drain_bottom_met_N"],None))
    
    ibias2label = rectangle(layer=pdk.get_glayer("met3_pin"),size=(0.5,0.5),centered=True).copy()
    ibias2label.add_label(text="IBIAS2",layer=pdk.get_glayer("met3_label"))
    move_info.append((ibias2label,lvcm_in.ports["M_2_A_drain_bottom_met_N"],None))

    # output 
    output1label = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    output1label.add_label(text="IOUT1",layer=pdk.get_glayer("met2_label"))
    move_info.append((output1label,lvcm_in.ports["M_3_A_multiplier_0_drain_N"],None))
    
    output2label = rectangle(layer=pdk.get_glayer("met2_pin"),size=(0.27,0.27),centered=True).copy()
    output2label.add_label(text="IOUT2",layer=pdk.get_glayer("met2_label"))
    move_info.append((output2label,lvcm_in.ports["M_4_A_multiplier_0_drain_N"],None))

    # move everything to position
    for comp, prt, alignment in move_info:
        alignment = ('c','b') if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        lvcm_in.add(compref)
    return lvcm_in.flatten() 

def low_voltage_cmirr_netlist(bias_fvf: Component, cascode_fvf: Component, fet_1_ref: ComponentReference, fet_2_ref: ComponentReference, fet_3_ref: ComponentReference, fet_4_ref: ComponentReference) -> Netlist:
    
        netlist = Netlist(circuit_name='Low_voltage_current_mirror', nodes=['IBIAS1', 'IBIAS2', 'GND', 'IOUT1', 'IOUT2'])
        netlist.connect_netlist(bias_fvf.info['netlist'], [('VIN','IBIAS1'),('VBULK','GND'),('Ib','IBIAS1'),('VOUT','local_net_1')])
        netlist.connect_netlist(cascode_fvf.info['netlist'], [('VIN','IBIAS1'),('VBULK','GND'),('Ib', 'IBIAS2'),('VOUT','local_net_2')])
        fet_1A_ref=netlist.connect_netlist(fet_2_ref.info['netlist'], [('D', 'IOUT1'),('G','IBIAS1'),('B','GND')])
        fet_2A_ref=netlist.connect_netlist(fet_4_ref.info['netlist'], [('D', 'IOUT2'),('G','IBIAS1'),('B','GND')])
        fet_1B_ref=netlist.connect_netlist(fet_1_ref.info['netlist'], [('G','IBIAS2'),('S', 'GND'),('B','GND')])
        fet_2B_ref=netlist.connect_netlist(fet_3_ref.info['netlist'], [('G','IBIAS2'),('S', 'GND'),('B','GND')])
        netlist.connect_subnets(
                fet_1A_ref,
                fet_1B_ref,
                [('S', 'D')]
                )
        netlist.connect_subnets(
                fet_2A_ref,
                fet_2B_ref,
                [('S', 'D')]
                )

        return netlist
   
# @cell
def self_biased_cascode_current_mirror_base(
        pdk: MappedPDK,
        width:  tuple[float,float] = (1,1),
        length: Optional[float] = None,
        fingers: tuple[int,int] = (2,2),
        multipliers: tuple[int,int] = (1,1),
        device: Optional[str] = 'nfet',
        plus_minus_seperation: float = 0,
        with_substrate_tap: Optional[bool] = False,
        with_tie: Optional[bool] = True,
        with_dummy: Union[bool, tuple[bool, bool]] = True,
        tie_layers: tuple[str,str]=("met2","met1"),
        show_netlist: Optional[bool] = False,
        **kwargs
    ) -> Component:
    """An instantiable self biased casoded current mirror that returns a Component object."""
    
    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    psize=(0.35,0.35)
    
    # Create the current mirror component
    SBCurrentMirror = Component(name="SBCurrentMirror")
    length = length if length is not None else pdk.get_grule('poly')['min_width']

    if multipliers[1] > multipliers[0]:
        multipliers = (multipliers[1],multipliers[0])

        
    # create transistors
    well = None
    if isinstance(with_dummy, bool):
        dummy = (with_dummy, with_dummy)
    if device.lower() in ['nmos', 'nfet']:
        fetL = nmos(pdk, width=width[0], fingers=fingers[0],length=length,multipliers=multipliers[0],with_tie=False,with_dummy=(dummy[0], False),with_dnwell=False,with_substrate_tap=False)

        fetR = nmos(pdk, width=width[1], fingers=fingers[1],length=length,multipliers=multipliers[1],with_tie=False,with_dummy=(False,dummy[1]),with_dnwell=False,with_substrate_tap=False)

        well, sdglayer = "pwell", "n+s/d"
    elif device.lower() in ['pmos', 'pfet']:
        fetL = pmos(pdk, width=width[0], fingers=fingers[0],length=length,multipliers=multipliers[0],with_tie=False,with_dummy=(dummy[0], False),dnwell=False,with_substrate_tap=False)

        fetR = pmos(pdk, width=width[1], fingers=fingers[1],length=length,multipliers=multipliers[1],with_tie=False,with_dummy=(False,dummy[1]),dnwell=False,with_substrate_tap=False)

        well, sdglayer = "nwell", "p+s/d"
    else:
         raise ValueError(f"device must be either 'nmos' or 'pmos', got {device}")
        
    fetRdims = evaluate_bbox(fetR.flatten().remove_layers(layers=[pdk.get_glayer(well)]))
    fetLdims = evaluate_bbox(fetL.flatten().remove_layers(layers=[pdk.get_glayer(well)]))
    
    # place and flip top transistors such that the drains of bottom and top point towards eachother
    a_topl = SBCurrentMirror << fetL
    #a_topl = rename_ports_by_orientation(a_topl.mirror_y())
    
    b_topr = SBCurrentMirror << fetR
    #b_topr = rename_ports_by_orientation(b_topr.mirror_y())
    
    a_botr = SBCurrentMirror << fetR
    # a_botr = rename_ports_by_orientation(a_botr.mirror_x())
    b_botl = SBCurrentMirror << fetL
    #b_botl = rename_ports_by_orientation(b_botl.mirror_x())
    
    prec_ref_center(a_topl, snapmov2grid=True)
    prec_ref_center(b_topr, snapmov2grid=True)
    prec_ref_center(a_botr, snapmov2grid=True)
    prec_ref_center(b_botl, snapmov2grid=True)
    
    # setup for routing (need viadims to know how far to seperate transistors)
    glayer1 = pdk.layer_to_glayer(a_topl.ports["multiplier_0_drain_E"].layer)
    glayer2 = glayer1[0:-1] + str(int(glayer1[-1])+1)
    glayer0 = glayer1[0:-1] + str(int(glayer1[-1])-1)
    
    g1g2via = via_stack(pdk,glayer1,glayer2)
    g0g1via = via_stack(pdk,glayer0,glayer1)
    
    # move transistors into position
    min_spacing_y = pdk.snap_to_2xgrid(1*(g1g2via.ysize - pdk.get_grule(glayer1)["min_width"])+pdk.get_grule(glayer1)["min_separation"])
    extra_g1g2_spacing = pdk.snap_to_2xgrid(max(pdk.get_grule(glayer2)["min_separation"]-pdk.get_grule(glayer1)["min_separation"],0))
    min_spacing_y += extra_g1g2_spacing
    
    min_spacing_x = 3*pdk.get_grule(glayer1)["min_separation"] + 2*g0g1via.xsize - 2*pdk.get_grule("active_diff",sdglayer)["min_enclosure"]
    min_spacing_x = pdk.snap_to_2xgrid(max(min_spacing_x, pdk.get_grule(sdglayer)["min_separation"]))
    
    a_topl.movex(0-fetLdims[0]/2-min_spacing_x/2).movey(pdk.snap_to_2xgrid(fetRdims[1]/2+min_spacing_y/2))
    b_topr.movex(fetLdims[0]/2+min_spacing_x/2).movey(pdk.snap_to_2xgrid(fetLdims[1]/2+min_spacing_y/2))
    
    a_botr.movex(fetLdims[0]/2+min_spacing_x/2).movey(pdk.snap_to_2xgrid(-fetLdims[1]/2-min_spacing_y/2))
    b_botl.movex(0-fetLdims[0]/2-min_spacing_x/2).movey(pdk.snap_to_2xgrid(-fetLdims[1]/2-min_spacing_y/2))
    
    viam2m3 = via_stack(pdk,"met2","met3",centered=True)
    metal_min_dim = max(pdk.get_grule("met2")["min_width"],pdk.get_grule("met3")["min_width"])
    metal_space = max(pdk.get_grule("met2")["min_separation"],pdk.get_grule("met3")["min_separation"],metal_min_dim)

    
    # route sources (short sources)
    SBCurrentMirror << route_quad(a_topl.ports["multiplier_0_source_E"], b_topr.ports["multiplier_0_source_W"], layer=pdk.get_glayer("met2"))
    SBCurrentMirror << route_quad(b_botl.ports["multiplier_0_source_E"], a_botr.ports["multiplier_0_source_W"], layer=pdk.get_glayer("met2"))
    
    
    sextension = b_topr.ports["well_E"].center[0] - b_topr.ports["multiplier_0_source_E"].center[0]
    source_routeE = SBCurrentMirror << c_route(pdk, b_topr.ports["multiplier_0_source_E"], a_botr.ports["multiplier_0_source_E"],extension=sextension, viaoffset=False)
    source_routeW = SBCurrentMirror << c_route(pdk, a_topl.ports["multiplier_0_source_W"], b_botl.ports["multiplier_0_source_W"],extension=sextension, viaoffset=False)
    # route drains
    # place via at the drain
    drain_br_via = SBCurrentMirror << viam2m3
    drain_bl_via = SBCurrentMirror << viam2m3
    drain_br_via.move(a_botr.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
    drain_bl_via.move(b_botl.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
    drain_br_viatm = SBCurrentMirror << viam2m3
    drain_bl_viatm = SBCurrentMirror << viam2m3
    drain_br_viatm.move(a_botr.ports["multiplier_0_drain_N"].center).movey(viam2m3.ymin)
    drain_bl_viatm.move(b_botl.ports["multiplier_0_drain_N"].center).movey(-1.5 * evaluate_bbox(viam2m3)[1] - metal_space)
    # create route to drain via
    width_drain_route = b_topr.ports["multiplier_0_drain_E"].width
    dextension = source_routeE.xmax - b_topr.ports["multiplier_0_drain_E"].center[0] + metal_space
    bottom_extension = viam2m3.ymax + width_drain_route/2 + 2*metal_space
    drain_br_viatm.movey(0-bottom_extension - metal_space - width_drain_route/2 - viam2m3.ymax)
    SBCurrentMirror << route_quad(drain_br_viatm.ports["top_met_N"], drain_br_via.ports["top_met_S"], layer=pdk.get_glayer("met3"))
    SBCurrentMirror << route_quad(drain_bl_viatm.ports["top_met_N"], drain_bl_via.ports["top_met_S"], layer=pdk.get_glayer("met3"))
    floating_port_drain_bottom_L = set_port_orientation(movey(drain_bl_via.ports["bottom_met_W"],0-bottom_extension), get_orientation("E"))
    floating_port_drain_bottom_R = set_port_orientation(movey(drain_br_via.ports["bottom_met_E"],0-bottom_extension - metal_space - width_drain_route), get_orientation("W"))
    drain_routeTR_BL = SBCurrentMirror << c_route(pdk, floating_port_drain_bottom_L, b_topr.ports["multiplier_0_drain_E"],extension=dextension, width1=width_drain_route,width2=width_drain_route)
    drain_routeTL_BR = SBCurrentMirror << c_route(pdk, floating_port_drain_bottom_R, a_topl.ports["multiplier_0_drain_W"],extension=dextension, width1=width_drain_route,width2=width_drain_route)
    # cross gate route top with c_route. bar_minus ABOVE bar_plus
    get_left_extension = lambda bar, a_topl=a_topl, SBCurrentMirror=SBCurrentMirror, pdk=pdk : (abs(SBCurrentMirror.xmin-min(a_topl.ports["multiplier_0_gate_W"].center[0],bar.ports["e1"].center[0])) + pdk.get_grule("met2")["min_separation"])
    get_right_extension = lambda bar, b_topr=b_topr, SBCurrentMirror=SBCurrentMirror, pdk=pdk : (abs(SBCurrentMirror.xmax-max(b_topr.ports["multiplier_0_gate_E"].center[0],bar.ports["e3"].center[0])) + pdk.get_grule("met2")["min_separation"])
    # lay bar plus and PLUSgate_routeW
    bar_comp = rectangle(centered=True,size=(abs(b_topr.xmax-a_topl.xmin), b_topr.ports["multiplier_0_gate_E"].width),layer=pdk.get_glayer("met2"))
    bar_plus = (SBCurrentMirror << bar_comp).movey(SBCurrentMirror.ymax + bar_comp.ymax + pdk.get_grule("met2")["min_separation"])
    PLUSgate_routeW = SBCurrentMirror << c_route(pdk, a_topl.ports["multiplier_0_gate_W"], bar_plus.ports["e1"], extension=get_left_extension(bar_plus))
    # lay bar minus and MINUSgate_routeE
    plus_minus_seperation = max(pdk.get_grule("met2")["min_separation"], plus_minus_seperation)
    bar_minus = (SBCurrentMirror << bar_comp).movey(SBCurrentMirror.ymax +bar_comp.ymax + plus_minus_seperation)
    MINUSgate_routeE = SBCurrentMirror << c_route(pdk, b_topr.ports["multiplier_0_gate_E"], bar_minus.ports["e3"], extension=get_right_extension(bar_minus))
    # lay MINUSgate_routeW and PLUSgate_routeE
    MINUSgate_routeW = SBCurrentMirror << c_route(pdk, set_port_orientation(b_botl.ports["multiplier_0_gate_E"],"W"), bar_minus.ports["e1"], extension=get_left_extension(bar_minus))
    PLUSgate_routeE = SBCurrentMirror << c_route(pdk, set_port_orientation(a_botr.ports["multiplier_0_gate_W"],"E"), bar_plus.ports["e3"], extension=get_right_extension(bar_plus))
    
    # correct pwell place, add ports, flatten, and return
    SBCurrentMirror.add_ports(a_topl.get_ports_list(),prefix="tl_")
    SBCurrentMirror.add_ports(b_topr.get_ports_list(),prefix="tr_")
    SBCurrentMirror.add_ports(b_botl.get_ports_list(),prefix="bl_")
    SBCurrentMirror.add_ports(a_botr.get_ports_list(),prefix="br_")
    SBCurrentMirror.add_ports(source_routeE.get_ports_list(),prefix="source_routeE_")
    SBCurrentMirror.add_ports(source_routeW.get_ports_list(),prefix="source_routeW_")
    SBCurrentMirror.add_ports(drain_routeTR_BL.get_ports_list(),prefix="drain_routeTR_BL_")
    SBCurrentMirror.add_ports(drain_routeTL_BR.get_ports_list(),prefix="drain_routeTL_BR_")
    SBCurrentMirror.add_ports(MINUSgate_routeW.get_ports_list(),prefix="MINUSgateroute_W_")
    SBCurrentMirror.add_ports(MINUSgate_routeE.get_ports_list(),prefix="MINUSgateroute_E_")
    SBCurrentMirror.add_ports(PLUSgate_routeW.get_ports_list(),prefix="PLUSgateroute_W_")
    SBCurrentMirror.add_ports(PLUSgate_routeE.get_ports_list(),prefix="PLUSgateroute_E_")
    SBCurrentMirror.add_padding(layers=(pdk.get_glayer(well),), default=0)
    
    
    # if substrate tap place substrate tap
    if with_substrate_tap:
        tapref = SBCurrentMirror << tapring(pdk,evaluate_bbox(SBCurrentMirror,padding=1),horizontal_glayer="met1")
        SBCurrentMirror.add_ports(tapref.get_ports_list(),prefix="tap_")
        try:
            SBCurrentMirror<<straight_route(pdk,a_topl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_W_top_met_W"],glayer2="met1")
        except KeyError:
            pass
        try:
            SBCurrentMirror<<straight_route(pdk,b_topr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_E_top_met_E"],glayer2="met1")
        except KeyError:
            pass
        try:
            SBCurrentMirror<<straight_route(pdk,b_botl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_W_top_met_W"],glayer2="met1")
        except KeyError:
            pass
        try:
            SBCurrentMirror<<straight_route(pdk,a_botr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_E_top_met_E"],glayer2="met1")
        except KeyError:
            pass

    # # Adding tapring
    # if with_tie:
    #     tap_sep = max(maxmet_sep,
    #         pdk.get_grule("active_diff", "active_tap")["min_separation"])
    #     tap_sep += pdk.get_grule(sdglayer, "active_tap")["min_enclosure"]
    #     tap_encloses = (
    #     2 * (tap_sep + SBCurrentMirror.xmax),
    #     2 * (tap_sep + SBCurrentMirror.ymax),
    #     )
    #     tie_ref = SBCurrentMirror << tapring(pdk, enclosed_rectangle = tap_encloses, sdlayer = sdglayer, horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
    #     SBCurrentMirror.add_ports(tie_ref.get_ports_list(), prefix="welltie_")

    # # if substrate tap place substrate tap, and route dummy to substrate tap
    # if with_substrate_tap:
    #     tapref = SBCurrentMirror << tapring(pdk,evaluate_bbox(SBCurrentMirror,padding=1))#,horizontal_glayer="met1")
    #     SBCurrentMirror.add_ports(tapref.get_ports_list(),prefix="tap_")
    #     try:
    #         SBCurrentMirror<<straight_route(pdk,a_topl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_W_top_met_W"],glayer2="met1")
    #     except KeyError:
    #         pass
    #     try:
    #         SBCurrentMirror<<straight_route(pdk,b_topr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_E_top_met_E"],glayer2="met1")
    #     except KeyError:
    #         pass
    #     try:
    #         SBCurrentMirror<<straight_route(pdk,b_botl.ports["multiplier_0_dummy_L_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_W_top_met_W"],glayer2="met1")
    #     except KeyError:
    #         pass
    #     try:
    #         SBCurrentMirror<<straight_route(pdk,a_botr.ports["multiplier_0_dummy_R_gsdcon_top_met_W"],SBCurrentMirror.ports["tap_E_top_met_E"],glayer2="met1")
    #     except KeyError:
    #         pass
        
    #SBCurrentMirror.add_padding(default=0,layers=[pdk.get_glayer(well)])

    component = component_snap_to_grid(rename_ports_by_orientation(SBCurrentMirror))
    #component.info['netlist'] = low_voltage_cmirr_netlist(bias_fvf, cascode_fvf, fet_1_ref, fet_2_ref, fet_3_ref, fet_4_ref)
    
    return component

if __name__ == "__main__":
    comp =self_biased_cascode_current_mirror_base(sky130,multipliers=(1,1),fingers=(1,1))
    # comp.pprint_ports()
    #comp =add_lvcm_labels(comp,sky130)
    comp.name = "CMWL"
    comp.show()
    #print(comp.info['netlist'].generate_netlist())
    #print("...Running DRC...")
    #drc_result = gf180.drc_magic(comp, comp.name)
    ## Klayout DRC
    #drc_result = sky130.drc(comp)
    
    #time.sleep(5)
        
    #print("...Running LVS...")
    #lvs_res=sky130.lvs_netgen(comp, "LVCM")
    #print("...Saving GDS...")
    #comp.write_gds('out_LVCM.gds')
