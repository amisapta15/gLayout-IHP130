from glayout import MappedPDK, sky130,gf180
from glayout import nmos, pmos, tapring,via_stack

from glayout.spice.netlist import Netlist
from glayout.routing import c_route,L_route,straight_route

from gdsfactory.component import Component
from gdsfactory.component_reference import ComponentReference
from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle

from glayout.util.comp_utils import evaluate_bbox, prec_center, align_comp_to_port, prec_ref_center,movex,movey
from glayout.util.snap_to_grid import component_snap_to_grid
from glayout.util.port_utils import set_port_orientation, rename_ports_by_orientation, create_private_ports, add_ports_perimeter
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
    a_topl = rename_ports_by_orientation(a_topl.mirror_y())
    
    b_topr = SBCurrentMirror << fetR
    b_topr = rename_ports_by_orientation(b_topr.mirror_y())
    
    a_botr = SBCurrentMirror << fetL
    a_botr = rename_ports_by_orientation(a_botr.mirror_x())
    b_botl = SBCurrentMirror << fetR
    b_botl = rename_ports_by_orientation(b_botl.mirror_x())
    
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
    
    SBCurrentMirror.add_padding(default=0,layers=[pdk.get_glayer(well)])

  

    # if substrate tap place substrate tap, and route dummy to substrate tap
    if with_substrate_tap:
        tapref = SBCurrentMirror << tapring(pdk,evaluate_bbox(SBCurrentMirror,padding=1))#,horizontal_glayer="met1")
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
    # correct pwell place, add ports, flatten, and return
    SBCurrentMirror.add_ports(a_topl.get_ports_list(),prefix="tl_")
    SBCurrentMirror.add_ports(b_topr.get_ports_list(),prefix="tr_")
    SBCurrentMirror.add_ports(b_botl.get_ports_list(),prefix="bl_")
    SBCurrentMirror.add_ports(a_botr.get_ports_list(),prefix="br_")
    # route asrc to asrc
    vsrca1 = SBCurrentMirror << g1g2via
    vsrca2 = SBCurrentMirror << g1g2via
    align_comp_to_port(vsrca1,movey(SBCurrentMirror.ports["tl_multiplier_0_drain_W"],-extra_g1g2_spacing),alignment=("right","bottom"))
    align_comp_to_port(vsrca2,movey(SBCurrentMirror.ports["br_multiplier_0_drain_W"],extra_g1g2_spacing),alignment=("right","top"))
    SBCurrentMirror << L_route(pdk, movey(vsrca1.ports["top_met_W"],extra_g1g2_spacing), vsrca2.ports["top_met_N"])
    # route bsrc to bsrc
    vsrcb1 = SBCurrentMirror << g1g2via
    vsrcb2 = SBCurrentMirror << g1g2via
    align_comp_to_port(vsrcb1,SBCurrentMirror.ports["tr_multiplier_0_drain_E"],alignment=("left","bottom"))
    align_comp_to_port(vsrcb2,SBCurrentMirror.ports["bl_multiplier_0_drain_E"],alignment=("left","top"))
    intermediate_port = SBCurrentMirror.ports["bl_multiplier_0_source_E"].copy()
    intermediate_port.layer = pdk.get_glayer(pdk.layer_to_glayer(vsrcb1.ports["top_met_E"].layer))
    SBCurrentMirror << L_route(pdk, vsrcb1.ports["top_met_S"], intermediate_port)
    SBCurrentMirror << L_route(pdk,intermediate_port, vsrcb2.ports["top_met_S"])
    # route adrain to adrain
    vdraina1 = SBCurrentMirror << g0g1via # first via
    align_comp_to_port(vdraina1, SBCurrentMirror.ports[f"tl_multiplier_0_row0_col{fingers[0]-1}_rightsd_top_met_N"],alignment=("right","top"))
    align_comp_to_port(vdraina1, SBCurrentMirror.ports["tl_multiplier_0_drain_E"],alignment=("right","none"))
    vdraina1.movex(pdk.get_grule(glayer1)["min_separation"])
    SBCurrentMirror << straight_route(pdk, vdraina1.ports["top_met_W"],SBCurrentMirror.ports["tr_multiplier_0_leftsd_top_met_E"],glayer2=glayer1)
    vdraina2 = SBCurrentMirror << g0g1via # second via
    align_comp_to_port(vdraina2, SBCurrentMirror.ports["tl_multiplier_0_drain_E"],alignment=("right","c"))
    vdraina2.movex(pdk.get_grule(glayer1)["min_separation"])
    vdraina2_mdprt = movex(vdraina2.ports["bottom_met_S"],pdk.get_grule("met2","via1")["min_enclosure"])
    vdraina2_mdprt.width = vdraina2_mdprt.width + 2*pdk.get_grule("met2","via1")["min_enclosure"]
    SBCurrentMirror << straight_route(pdk, vdraina2_mdprt, vdraina1.ports["bottom_met_N"])
    SBCurrentMirror << L_route(pdk, vdraina2.ports["top_met_N"],SBCurrentMirror.ports["bl_multiplier_0_source_E"])
    # route bdrain to bdrain
    vdrainb1 = SBCurrentMirror << g0g1via # first via
    align_comp_to_port(vdrainb1, SBCurrentMirror.ports["br_multiplier_0_leftsd_top_met_N"],alignment=("left","bottom"))
    align_comp_to_port(vdrainb1, SBCurrentMirror.ports["br_multiplier_0_drain_W"],alignment=("left","none"))
    vdrainb1.movex(-pdk.get_grule(glayer1)["min_separation"])
    # TODO: fix slight overhang (both this one and the adrain->bdrain)
    SBCurrentMirror << straight_route(pdk, vdrainb1.ports["top_met_W"],SBCurrentMirror.ports["br_multiplier_0_leftsd_top_met_E"],glayer2=glayer1)
    vdrainb2 = SBCurrentMirror << g0g1via # second via
    align_comp_to_port(vdrainb2, SBCurrentMirror.ports["br_multiplier_0_drain_W"],alignment=("left","c"))
    vdrainb2.movex(-pdk.get_grule(glayer1)["min_separation"])
    vdrainb2_mdprt = movex(vdrainb2.ports["bottom_met_N"],-pdk.get_grule("met2","via1")["min_enclosure"])
    vdrainb2_mdprt.width = vdrainb2_mdprt.width + 2*pdk.get_grule("met2","via1")["min_enclosure"]
    SBCurrentMirror << straight_route(pdk, vdrainb2_mdprt, vdrainb1.ports["bottom_met_S"])
    SBCurrentMirror << L_route(pdk, vdrainb2.ports["top_met_N"],SBCurrentMirror.ports["tl_multiplier_0_source_E"])
    # agate to agate
    gate2rt_sep = pdk.get_grule(glayer2)["min_separation"]
    vgatea1 = SBCurrentMirror << g1g2via# first via
    align_comp_to_port(vgatea1,SBCurrentMirror.ports["tl_multiplier_0_gate_E"],alignment=("right","bottom"))
    vgatea2 = SBCurrentMirror << g1g2via# second via
    align_comp_to_port(vgatea2,SBCurrentMirror.ports["br_multiplier_0_gate_S"],alignment=("right","bottom"))
    vgatea2.movey(-gate2rt_sep)
    SBCurrentMirror << straight_route(pdk, vgatea2.ports["bottom_met_S"], SBCurrentMirror.ports["br_multiplier_0_gate_N"])
    g1extension = pdk.util_max_metal_seperation()+pdk.snap_to_2xgrid(SBCurrentMirror.ports["tr_multiplier_0_plusdoped_E"].center[0] - vgatea2.ports["top_met_E"].center[0])
    cext1 = SBCurrentMirror << c_route(pdk, vgatea2.ports["top_met_E"], vgatea1.ports["top_met_E"], cglayer=glayer2, extension=g1extension)
    SBCurrentMirror.add_ports(ports=cext1.get_ports_list(),prefix="A_gate_route_")
    # bgate to bgate
    vgateb1 = SBCurrentMirror << g1g2via# first via
    align_comp_to_port(vgateb1,SBCurrentMirror.ports["bl_multiplier_0_gate_E"],alignment=("right","top"))
    vgateb2 = SBCurrentMirror << g1g2via# second via
    align_comp_to_port(vgateb2,SBCurrentMirror.ports["tr_multiplier_0_gate_S"],alignment=("right","top"))
    vgateb2.movey(gate2rt_sep)
    SBCurrentMirror << straight_route(pdk, vgateb2.ports["bottom_met_N"], SBCurrentMirror.ports["tr_multiplier_0_gate_S"])
    g2extension = pdk.util_max_metal_seperation()+pdk.snap_to_2xgrid(abs(SBCurrentMirror.ports["tl_multiplier_0_plusdoped_W"].center[0] - vgateb1.ports["top_met_W"].center[0]))
    cext2 = SBCurrentMirror << c_route(pdk, vgateb2.ports["top_met_W"], vgateb1.ports["top_met_W"], cglayer=glayer2, extension=g2extension)
    SBCurrentMirror.add_ports(ports=cext2.get_ports_list(),prefix="B_gate_route_")
    # create better toplevel ports
    b_drainENS = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tr_multiplier_0_drain_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_drainENS = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["br_multiplier_0_drain_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_sourceENS = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tr_multiplier_0_source_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_sourceENS = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["br_multiplier_0_source_E"], movex(cext1.ports["con_N"],cext2.ports["con_N"].width/2+pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_drainW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["bl_multiplier_0_drain_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_drainW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tl_multiplier_0_drain_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    b_sourceW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["bl_multiplier_0_source_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    a_sourceW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tl_multiplier_0_source_W"], movex(cext2.ports["con_N"],-cext2.ports["con_N"].width/2-pdk.util_max_metal_seperation()), glayer2=glayer1)
    # add the ports
    def makeNorS(portin, direction: str):
        mdprt = set_port_orientation(movex(portin.copy(),(-1 if portin.name.endswith("E") else 1)*pdk.snap_to_2xgrid(portin.width/2)),direction)
        mdprt.name = (mdprt.name.strip("EW") + direction.strip().capitalize()).removeprefix("route_")
        return movey(mdprt,(1 if direction.endswith("N") else -1)*pdk.snap_to_2xgrid(mdprt.width/2))
    def addENS(topcomp: Component, straightrouteref, device: str, pin: str):
        # device is A or B and pin is source drain or gate
        eastport = straightrouteref.ports["route_E"].copy()
        eastport.name = eastport.name.removeprefix("route_")
        topcomp.add_ports(ports=[eastport,makeNorS(eastport,"N"),makeNorS(eastport,"S")],prefix=device+"_"+pin+"_")
    addENS(SBCurrentMirror,b_drainENS,"B","drain")
    addENS(SBCurrentMirror,a_drainENS,"A","drain")
    addENS(SBCurrentMirror,b_sourceENS,"B","source")
    addENS(SBCurrentMirror,a_sourceENS,"A","source")
    def localportrename(portin):
        portin = portin.copy()
        portin.name = portin.name.removeprefix("route_")
        return portin
    SBCurrentMirror.add_ports(ports=[localportrename(b_drainW.ports["route_W"])],prefix="B_drain_")
    SBCurrentMirror.add_ports(ports=[localportrename(a_drainW.ports["route_W"])],prefix="A_drain_")
    SBCurrentMirror.add_ports(ports=[localportrename(b_sourceW.ports["route_W"])],prefix="B_source_")
    SBCurrentMirror.add_ports(ports=[localportrename(a_sourceW.ports["route_W"])],prefix="A_source_")
    # better gate routes
    a_gateE = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["br_multiplier_0_gate_E"], SBCurrentMirror.ports["A_drain_E"])
    b_gateE = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tr_multiplier_0_gate_E"], SBCurrentMirror.ports["A_drain_E"])
    a_gateW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["tl_multiplier_0_gate_W"], SBCurrentMirror.ports["A_drain_W"])
    b_gateW = SBCurrentMirror << straight_route(pdk, SBCurrentMirror.ports["bl_multiplier_0_gate_W"], SBCurrentMirror.ports["A_drain_W"])
    SBCurrentMirror.add_ports(ports=[localportrename(a_gateE.ports["route_E"])],prefix="A_gate_")
    SBCurrentMirror.add_ports(ports=[localportrename(b_gateE.ports["route_E"])],prefix="B_gate_")
    SBCurrentMirror.add_ports(ports=[localportrename(a_gateW.ports["route_W"])],prefix="A_gate_")
    SBCurrentMirror.add_ports(ports=[localportrename(b_gateW.ports["route_W"])],prefix="B_gate_")
    rename_north_portb = vgateb2.ports["top_met_N"].copy()# add B_gate_N
    rename_north_portb.name = "B_gate_N"
    SBCurrentMirror.add_ports(ports=[rename_north_portb])
    rename_south_porta = vgatea2.ports["top_met_S"].copy()# add A_gate_S
    rename_south_porta.name = "A_gate_S"
    SBCurrentMirror.add_ports(ports=[rename_south_porta])
    rename_south_portb = vgateb1.ports["top_met_S"].copy()# add B_gate_S
    rename_south_portb.name = "B_gate_S"
    SBCurrentMirror.add_ports(ports=[rename_south_portb])
    # rename ports and add private ports for smart route
    SBCurrentMirror = rename_ports_by_orientation(SBCurrentMirror)
    SBCurrentMirror.add_ports(create_private_ports(SBCurrentMirror,["".join(prtp) for prtp in product(["A_","B_"],["drain","source","gate"])]))
    SBCurrentMirror.info["route_genid"]="common_centroid_ab_ba"

        # Adding tapring
    if with_tie:
        tap_sep = max(maxmet_sep,
            pdk.get_grule("active_diff", "active_tap")["min_separation"])
        tap_sep += pdk.get_grule(sdglayer, "active_tap")["min_enclosure"]
        tap_encloses = (
        2 * (tap_sep + SBCurrentMirror.xmax),
        2 * (tap_sep + SBCurrentMirror.ymax),
        )
        tie_ref = SBCurrentMirror << tapring(pdk, enclosed_rectangle = tap_encloses, sdlayer = sdglayer, horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
        SBCurrentMirror.add_ports(tie_ref.get_ports_list(), prefix="welltie_")

    
    
# # create transistors
#     well = None
#     if isinstance(with_dummy, bool):
#         dummy = (with_dummy, with_dummy)
        
#     if device.lower() in ['nmos', 'nfet']:
#         fetL = nmos(pdk, width=width[0], fingers=fingers[0],length=length,multipliers=multipliers[0],with_dummy=(dummy[0], False),with_dnwell=False,with_substrate_tap=False,with_tie=False)
#         fetR = nmos(pdk, width=width[1], fingers=fingers[1],length=length,multipliers=multipliers[1],with_dummy=(False,dummy[1]),with_dnwell=False,with_substrate_tap=False,with_tie=False)
#         min_spacing_x = pdk.get_grule("n+s/d")["min_separation"] - 2*(fetL.xmax - fetL.ports["multiplier_0_plusdoped_E"].center[0])
#         well = "pwell"
#     elif device.lower() in ['pmos', 'pfet']:
#         fetL = pmos(pdk, width=width[0], fingers=fingers[0],length=length,multipliers=multipliers[0],with_tie=with_tie,with_dummy=(dummy[0], False),dnwell=False,with_substrate_tap=False)
#         fetR = pmos(pdk, width=width[1], fingers=fingers[1],length=length,multipliers=multipliers[1],with_tie=with_tie,with_dummy=(False,dummy[1]),dnwell=False,with_substrate_tap=False)
#         min_spacing_x = pdk.get_grule("p+s/    d")["min_separation"] - 2*(fetL.xmax - fetL.ports["multiplier_0_plusdoped_E"].center[0])
#         well = "nwell"
#     else:
#         raise ValueError(f"device must be either 'nmos' or 'pmos', got {device}")

#     # place transistors
#     viam2m3 = via_stack(pdk,"met2","met3",centered=True)
#     metal_min_dim = max(pdk.get_grule("met2")["min_width"],pdk.get_grule("met3")["min_width"])
#     metal_space = max(pdk.get_grule("met2")["min_separation"],pdk.get_grule("met3")["min_separation"],metal_min_dim)
#     gate_route_os = evaluate_bbox(viam2m3)[0] - fetL.ports["multiplier_0_gate_W"].width + metal_space
#     min_spacing_y = metal_space + 2*gate_route_os
#     min_spacing_y = min_spacing_y - 2*abs(fetL.ports["well_S"].center[1] - fetL.ports["multiplier_0_gate_S"].center[1])
#     # TODO: fix spacing where you see +-0.5
#     a_topl = (SBCurrentMirror << fetL).movey(fetL.ymax+min_spacing_y/2+0.5).movex(0-fetL.xmax-min_spacing_x/2)
#     b_topr = (SBCurrentMirror << fetR).movey(fetR.ymax+min_spacing_y/2+0.5).movex(fetL.xmax+min_spacing_x/2)
#     a_botr = (SBCurrentMirror << fetR)
#     a_botr.mirror_y().movey(0-0.5-fetL.ymax-min_spacing_y/2).movex(fetL.xmax+min_spacing_x/2)
#     b_botl = (SBCurrentMirror << fetL)
#     b_botl.mirror_y().movey(0-0.5-fetR.ymax-min_spacing_y/2).movex(0-fetL.xmax-min_spacing_x/2)
    
    component = component_snap_to_grid(rename_ports_by_orientation(SBCurrentMirror))
    #component.info['netlist'] = low_voltage_cmirr_netlist(bias_fvf, cascode_fvf, fet_1_ref, fet_2_ref, fet_3_ref, fet_4_ref)
    
    return component

if __name__ == "__main__":
    comp =self_biased_cascode_current_mirror_base(gf180,multipliers=(4,2),fingers=(4,2))
    # comp.pprint_ports()
    #comp =add_lvcm_labels(comp,sky130)
    comp.name = "CMWL"
    comp.show()
    #print(comp.info['netlist'].generate_netlist())
    #print("...Running DRC...")
    drc_result = gf180.drc_magic(comp, comp.name)
    ## Klayout DRC
    #drc_result = sky130.drc(comp)
    
    #time.sleep(5)
        
    #print("...Running LVS...")
    #lvs_res=sky130.lvs_netgen(comp, "LVCM")
    #print("...Saving GDS...")
    #comp.write_gds('out_LVCM.gds')
