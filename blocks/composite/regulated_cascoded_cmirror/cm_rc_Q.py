from glayout import MappedPDK, sky130,gf180
from glayout import nmos, pmos, tapring,via_stack

from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from n_fets_interdigitized import n_transistor_interdigitized
from gdsfactory import cell
from gdsfactory.component import Component
from gdsfactory.components import text_freetype, rectangle

from glayout.routing import c_route,L_route,straight_route
from glayout.spice.netlist import Netlist

from glayout.util.port_utils import add_ports_perimeter,rename_ports_by_orientation
from glayout.util.comp_utils import evaluate_bbox, prec_center, prec_ref_center, align_comp_to_port
from glayout.util.snap_to_grid import component_snap_to_grid
from typing import Optional, Union 

from pathlib import Path

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

# def generate_self_biased_current_mirror_netlist(
#     names: str = "SelfBiasedCurrentMirror",
#     regulator: Component = None,
#     base: Component = None,
#     show_netlist : Optional[bool] = False,
#     ) -> Netlist:
#     """Generate a netlist for a current mirror."""
    
#     topnet = Netlist(
#         circuit_name=names,
#         nodes=['IREF', 'ICOPY', 'VSS'],
#     )
    
#     base_ref = topnet.connect_netlist(
#         base.info['netlist'],
#         [('VSS', 'VSS') ]
#     )

#     regulator_ref = topnet.connect_netlist(
#         regulator.info['netlist'],
#         [('IREF', 'IREF'), ('ICOPY', 'ICOPY'), ('VSS', 'VSS')]
#     )
    
#     topnet.connect_subnets(
#         base_ref,
#         regulator_ref,
#         [('IREF', 'INTA'), (('ICOPY', 'INTB')),('VSS', 'VSS')]
#     )
    
#     if show_netlist:
#         generated_netlist_for_lvs = topnet.generate_netlist()
#         print(f"Generated netlist :\n", generated_netlist_for_lvs)

#         file_path_local_storage = "./gen_netlist.txt"
#         try:
#             with open(file_path_local_storage, 'w') as file:
#                 file.write(generated_netlist_for_lvs)
#         except:
#             print(f"Verify the file availability and type: ", generated_netlist_for_lvs, type(generated_netlist_for_lvs))
#     return topnet

# @validate_arguments
def regulated_cascode_current_mirror(
        pdk: MappedPDK,
        Width: float = 1,
        Length: Optional[float] = None,
        num_cols: int = 2,
        fingers: int = 1,
        type: Optional[str] = 'nfet',
        with_substrate_tap: Optional[bool] = False,
        with_tie: Optional[bool] = True,
        with_dummy: Optional[bool] = True,
        tie_layers: tuple[str,str]=("met2","met1"),
        show_netlist: Optional[bool] = False,
        **kwargs
    ) -> Component:
    """An instantiable self biased casoded current mirror that returns a Component object."""
    
    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    psize=(0.35,0.35)
    
    # Create the current mirror component
    top_level = Component(name="SBCurrentMirror")
    Length = Length if Length is not None else pdk.get_grule('poly')['min_width']
    top_ref = prec_ref_center(top_level)
    
    # Create the interdigitized fets
    if type.lower() =="pfet" or type.lower() =="pmos":
        currm= n_transistor_interdigitized(pdk, device='pfet', numcols=num_cols, n_devices=2, width=Width,length=Length,fingers=fingers,with_substrate_tap=False,with_tie=False)
        well, sdglayer = "nwell", "n+s/d"
    elif type.lower() =="nfet" or type.lower() =="nmos":
        currm= n_transistor_interdigitized(pdk, device='nfet', numcols=num_cols, n_devices=2, width=Width,length=Length,fingers=fingers,with_substrate_tap=False,with_tie=False)
        well, sdglayer = "pwell", "p+s/d"
    else:
        raise ValueError("type must be either nfet or pfet")
        
    # Add the interdigitized fets to the current mirror top component
    bottom_currm_ref = prec_ref_center(currm)
    mid_currm_ref = prec_ref_center(currm)
    top_currm_ref = prec_ref_center(currm)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BOTTOM CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    top_level.add(bottom_currm_ref)
    bottom_currm_ref.move(top_ref.center)
    top_level.add_ports(bottom_currm_ref.get_ports_list(),prefix="currm_bottom_")

    dist_DS = abs(top_level.ports[f"currm_bottom_A_0_drain_E"].center[0] - top_level.ports[f"currm_bottom_A_0_drain_W"].center[0])/2

    dist_GS = abs(top_level.ports[f"currm_bottom_A_0_gate_E"].center[0] - top_level.ports[f"currm_bottom_A_0_gate_W"].center[0])/2

    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)

    viam1m2 = via_stack(pdk, "met1", "met2", centered=True)

    bottomBdrain_via  = top_level << viam2m3   

    bottomBdrain_via.move(top_level.ports["currm_bottom_B_1_drain_E"].center).movex(-dist_DS)

    bottomA_gate_via  = top_level << viam2m3

    bottomA_gate_via.move((bottomBdrain_via.center[0], top_level.ports["currm_bottom_A_0_gate_W"].center[1]))

    top_level << straight_route(pdk, bottomBdrain_via.ports["bottom_met_N"], bottomA_gate_via.ports["bottom_met_S"], glayer2="met3")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # MIDDLE CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    top_level.add(mid_currm_ref)
    mid_currm_ref.move(top_ref.center).movey(evaluate_bbox(bottom_currm_ref)[1] + maxmet_sep)
    top_level.add_ports(mid_currm_ref.get_ports_list(),prefix="currm_middle_")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TOP CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    top_level.add(top_currm_ref)
    top_currm_ref.move(mid_currm_ref.center).movey(evaluate_bbox(mid_currm_ref)[1] + maxmet_sep)
    top_level.add_ports(top_currm_ref.get_ports_list(),prefix="currm_top_")

    topAdrain_via  = top_level << viam2m3   

    topAdrain_via.move(top_level.ports["currm_top_A_0_drain_W"].center).movex(dist_DS)

    topB_gate_via  = top_level << viam2m3

    topB_gate_via.move((topAdrain_via.center[0], top_level.ports["currm_top_B_0_gate_W"].center[1]))

    top_level << straight_route(pdk, topAdrain_via.ports["top_met_N"], topB_gate_via.ports["top_met_S"], glayer2="met3")


    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # INTERCONNECTIONS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    bottomB_gate_via  = top_level << viam2m3
    bottomB_gate_via.move((top_level.ports["currm_bottom_B_0_gate_W"].center)).movex(dist_GS)

    middleB_drain_via  = top_level << viam2m3
    middleB_drain_via.move(top_level.ports["currm_middle_B_0_drain_E"].center).movex(-dist_DS)

    top_level << straight_route(pdk, bottomB_gate_via.ports["top_met_S"], middleB_drain_via.ports["top_met_N"], glayer2="met3")

    topA_gate_via  = top_level << viam2m3
    topA_gate_via.move((top_level.ports["currm_top_A_1_gate_W"].center)).movex(dist_GS)

    middleA_drain_via  = top_level << viam2m3
    middleA_drain_via.move(top_level.ports["currm_middle_A_1_drain_E"].center).movex(-dist_DS)

    top_level << straight_route(pdk, topA_gate_via.ports["top_met_N"], middleA_drain_via.ports["top_met_S"], glayer2="met3")

    topB_drain_via  = top_level << viam2m3
    topB_drain_via.move(top_level.ports["currm_top_B_1_drain_E"].center).movex(-dist_DS)

    middleB_gate_via  = top_level << viam2m3
    middleB_gate_via.move(top_level.ports["currm_middle_B_1_gate_E"].center).movex(-dist_GS)

    middleA_gate_via  = top_level << viam2m3
    middleA_gate_via.move((middleB_gate_via.center[0], top_level.ports["currm_middle_A_1_gate_E"].center[1]))

    top_level << straight_route(pdk, middleB_gate_via.ports["top_met_S"], topB_drain_via.ports["top_met_N"], glayer2="met3")

    top_level << straight_route(pdk, middleA_gate_via.ports["top_met_S"], middleB_gate_via.ports["top_met_N"], glayer2="met3")


    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TAP RING
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    snap = pdk.snap_to_2xgrid

    core = top_level.copy()      # so we don't mutate while measuring
    core_flat = core.flatten()   # include all placed children

    xmin, xmax = core_flat.xmin, core_flat.xmax
    ymin, ymax = core_flat.ymin, core_flat.ymax

    core_w = xmax - xmin
    core_h = ymax - ymin

    cx = snap((xmin + xmax) / 2)
    cy = snap((ymin + ymax) / 2)

    # Adding tapring
    if with_tie:
        well, sdglayer = "pwell", "p+s/d"
        tap_separation = max(maxmet_sep,
            pdk.get_grule("active_diff", "active_tap")["min_separation"])
        tap_separation += pdk.get_grule(sdglayer, "active_tap")["min_enclosure"]
        tap_encloses = (
            (snap(4*tap_separation + core_w)),
            (snap(4*tap_separation + core_h)),
        )
        tie_ref = top_level << tapring(pdk, enclosed_rectangle = tap_encloses, sdlayer = sdglayer, horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
        tie_ref.move((cx, cy))
        top_level.add_ports(tie_ref.get_ports_list(), prefix="welltie_")
        
    # add pwell
    top_level.add_padding(default=pdk.get_grule(well, "active_tap")["min_enclosure"],layers=[pdk.get_glayer(well)])
    top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer(well), prefix="well_")    
    
    # add the substrate tap if specified
    if with_substrate_tap:
        substrate_tap_separation = pdk.get_grule("dnwell", "active_tap")["min_separation"]
        substrate_tap_enclosure = (
            (snap(4*substrate_tap_separation + core_w)),
            (snap(4*substrate_tap_separation + core_h)),
        )
        ringtoadd = tapring(pdk, enclosed_rectangle = substrate_tap_enclosure, sdlayer = "p+s/d", horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
        substrate_tap_ring_ref = top_level << ringtoadd
        substrate_tap_ring_ref.move((cx, cy))
        top_level.add_ports(substrate_tap_ring_ref.get_ports_list(), prefix="substrate_tap_")


    # Connect well ties to well
    try:
        top_level << straight_route(pdk, top_level.ports["currm_bottom_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")
        
        top_level << straight_route(pdk, top_level.ports[f'currm_bottom_B_1_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")

        top_level << straight_route(pdk, top_level.ports["currm_middle_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")          

        top_level << straight_route(pdk, top_level.ports[f'currm_middle_B_1_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")

        top_level << straight_route(pdk, top_level.ports["currm_top_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")

        top_level << straight_route(pdk, top_level.ports[f'currm_top_B_1_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")
        
    except KeyError:
        pass

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # CONNECT DRAINS TO OTHER STAGES
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    dist_ring = abs(top_level.ports["welltie_W_top_met_W"].center[0] - top_level.ports["welltie_W_top_met_E"].center[0])/2

    topA_drain_aux_via = top_level << viam1m2   
    topA_drain_aux_via.move((top_level.ports["welltie_W_top_met_E"].center[0], top_level.ports[f"currm_top_A_0_drain_E"].center[1])).movex(-dist_ring - 2*dist_DS)

    top_level << straight_route(pdk, top_level.ports[f"currm_top_A_0_drain_W"], topA_drain_aux_via.ports["top_met_W"], glayer2="met2")

    topB_drain_in_via = top_level << viam1m2
    topB_drain_in_via.move((top_level.ports["welltie_W_top_met_E"].center[0], top_level.ports[f"currm_top_B_0_drain_E"].center[1])).movex(-dist_ring - 2*dist_DS)

    top_level << straight_route(pdk, top_level.ports[f"currm_top_B_0_drain_W"], topB_drain_in_via.ports["top_met_W"], glayer2="met2")

    bottomB_drain_aux_via = top_level << viam1m2
    bottomB_drain_aux_via.move((top_level.ports["welltie_W_top_met_E"].center[0], top_level.ports[f"currm_bottom_B_0_drain_W"].center[1])).movex(dist_ring - 2*dist_DS)

    top_level << straight_route(pdk, top_level.ports[f"currm_bottom_B_0_drain_W"], bottomB_drain_aux_via.ports["top_met_W"], glayer2="met2")

    bottomA_drain_out_via = top_level << viam1m2
    bottomA_drain_out_via.move((top_level.ports["welltie_E_top_met_W"].center[0], top_level.ports[f"currm_bottom_A_0_drain_E"].center[1])).movex(dist_ring + 2*dist_DS)

    top_level << straight_route(pdk, top_level.ports[f"currm_bottom_A_0_drain_E"], bottomA_drain_out_via.ports["top_met_E"], glayer2="met2")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # CONNECT SOURCES TO GND
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    topA_source_via = top_level << viam1m2
    topA_source_via.move((top_level.ports["welltie_W_top_met_E"].center[0], top_level.ports[f"currm_top_A_0_source_W"].center[1])).movex(-dist_ring)

    top_level << straight_route(pdk, top_level.ports[f"currm_top_A_0_source_W"], topA_source_via.ports["top_met_W"], glayer2="met2")

    middleA_source_via = top_level << viam1m2
    middleA_source_via.move((top_level.ports["welltie_W_top_met_E"].center[0], top_level.ports[f"currm_middle_A_0_source_W"].center[1])).movex(-dist_ring)

    top_level << straight_route(pdk, top_level.ports[f"currm_middle_A_0_source_W"], middleA_source_via.ports["top_met_W"], glayer2="met2")

    middleB_source_via = top_level << viam1m2
    middleB_source_via.move((top_level.ports["welltie_E_top_met_E"].center[0], top_level.ports[f"currm_middle_B_0_source_W"].center[1])).movex(-dist_ring)

    top_level << straight_route(pdk, top_level.ports[f"currm_middle_B_0_source_W"], middleB_source_via.ports["top_met_W"], glayer2="met2")

    bottomB_source_via = top_level << viam1m2
    bottomB_source_via.move((top_level.ports["welltie_E_top_met_W"].center[0], top_level.ports[f"currm_bottom_B_0_source_W"].center[1])).movex(dist_ring)

    top_level << straight_route(pdk, top_level.ports[f"currm_bottom_B_0_source_W"], bottomB_source_via.ports["top_met_E"], glayer2="met2")

    return rename_ports_by_orientation(component_snap_to_grid(top_level))

def add_regulated_cascode_current_mirror_cm_labels(
    CMS: Component, 
    transistor_type: str = "nfet",
    pdk: MappedPDK =sky130
    ) -> Component:  
    """Add labels to the current mirror layout for LVS, handling both nfet and pfet."""

    #Would be adjusted for pdk agonastic later
    met2_pin = (69, 16)
    met2_label = (69, 5)
    met3_pin = (70, 16)
    met3_label = (70, 5)
    
    CMS.unlock()
    move_info = []
    psize=(0.35,0.35)
    
    
    # VREF label (for both gate and drain of transistor A, and dummy drains)
    Iref_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Iref_label.add_label(text="IREF", layer=met2_label)
    move_info.append((Iref_label, CMS.ports["refport_N"], None)) # Drain of A
    #move_info.append((Iref_label, CMS.ports["gateshortports_con_N"], None))  # Gate of A & B
    
    # VCOPY label (for drain of transistor B)
    Icopy_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Icopy_label.add_label(text="ICOPY", layer=met2_label)
    move_info.append((Icopy_label, CMS.ports["copyport_N"], None))  # Drain of B
    
     # VCOPY label (for drain of transistor B)
    Ibias_label = rectangle(layer=met2_pin, size=psize, centered=True).copy()
    Ibias_label.add_label(text="IBIAS", layer=met2_label)
    move_info.append((Ibias_label, CMS.ports["biasport_N"], None))  # Drain of B


   # # VSS/VDD label (for sources/bulk connection)
   #  if transistor_type.lower() == "nfet":
   #      bulk_net_name = "VSS"
   #      bulk_pin_layer = met2_pin 
   #      bulk_label_layer = met2_label 
   #  else:  # pfet
   #      bulk_net_name = "VDD"
   #      bulk_pin_layer = met2_pin 
   #      bulk_label_layer = met2_label 
    
   #  ##Need to clarify the bulk and source connection??
   #  # VB label 
   #  vb_label = rectangle(layer=bulk_pin_layer, size=psize, centered=True).copy() 
   #  vb_label.add_label(text=bulk_net_name , layer=bulk_label_layer)
   #  move_info.append((vb_label, CMS.ports["bulkport_N"], None)) 
    
    # Add labels to the component
    for label, port, alignment in move_info:
        if port:
            alignment = ('c', 'b') if alignment is None else alignment
            aligned_label = align_comp_to_port(label, port, alignment=alignment)
            CMS.add(aligned_label)

    return CMS.flatten()




## To Test their primitives
# from current_mirror import current_mirror, current_mirror_netlist

if __name__ == "__main__":
	# Main function to generate the current mirror layout
    # mappedpdk, Width, Length, num_cols, fingers, transistor type
    selected_pdk=gf180
    comp = regulated_cascode_current_mirror(selected_pdk, num_cols=2, Width=4, Length=1, device='nfet',show_netlist=False)
    #comp.pprint_ports()
    #comp = add_self_biased_cascode_cm_labels(comp, transistor_type='nfet', pdk=gf180)
 

    comp.name = "RM"
    comp.show()
    ##Write the current mirror layout to a GDS file
    comp.write_gds("./RM.gds")
    
    # # #Generate the netlist for the current mirror
    # print("\n...Generating Netlist...")
    # print(comp.info["netlist"].generate_netlist())
    # # #DRC Checks
    drc_result = selected_pdk.drc_magic(comp, comp.name,output_file=Path("DRC/"))

  