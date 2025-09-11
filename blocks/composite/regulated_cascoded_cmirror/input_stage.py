from glayout import MappedPDK, sky130,gf180
from glayout import nmos, pmos, tapring,via_stack

# from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from test import n_transistor_interdigitized
from two import two_pfet_interdigitized2
from gdsfactory import cell
from gdsfactory.component import Component
from gdsfactory.components import text_freetype, rectangle
from pathlib import Path

from glayout.routing import c_route,L_route,straight_route
from glayout.spice.netlist import Netlist

from glayout.util.port_utils import add_ports_perimeter,rename_ports_by_orientation
from glayout.util.comp_utils import evaluate_bbox, prec_center, prec_ref_center, align_comp_to_port
from glayout.util.snap_to_grid import component_snap_to_grid
from typing import Optional, Union 

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

####################Import the Base structure#######################
from cm_prim import current_mirror_base
from cm_wl import current_mirror_WL
from cm_sb import self_biased_cascode_current_mirror
from cm_rc import regulated_cascode_current_mirror

def met3_anchor(pdk, met_layer, w=0.3, h=0.3):
    c = Component()
    c << rectangle(size=(w,h), centered=True, layer=pdk.get_glayer(met_layer))
    c.add_port(name="P", center=(0,0), width=h, orientation=180, layer=pdk.get_glayer(met_layer))
    return c

# @validate_arguments
def input_stage(
        pdk: MappedPDK,
        Width: float = 1,
        Length: Optional[float] = None,
        num_cols: int = 1,
        fingers: int = 1,
        multipliers: int = 1,
        type: Optional[str] = 'nfet',
        with_substrate_tap: Optional[bool] = False,
        with_tie: Optional[bool] = True,
        with_dummy: Optional[bool] = False,
        tie_layers: tuple[str,str]=("met2","met1"),
        show_netlist: Optional[bool] = False,
        **kwargs
    ) -> Component:
    """An instantiable self biased casoded current mirror that returns a Component object."""
    
    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    n_well_sep = maxmet_sep
    psize=(0.35,0.35)
    
    # Create the current mirror component
    top_level = Component(name="input_stage")
    top_level.name="input_stage"
    Length = Length if Length is not None else pdk.get_grule('poly')['min_width']
    top_ref = prec_ref_center(top_level)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BOTTOM CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    currm_bottom = n_transistor_interdigitized(pdk, device="pfet", numcols=1, n_devices=4, with_substrate_tap=False, with_tie=False, width=10, length=2)

    currm_bottom = top_level<< currm_bottom
    currm_bottom.name="currm_bottom"

    currm_bottom_ref = prec_ref_center(currm_bottom)
    currm_bottom_ref.move(top_ref.center)
    top_level.add(currm_bottom_ref)

    top_level.add_ports(currm_bottom_ref.get_ports_list(),prefix="currm_bottom_")

    dist_DS = abs(top_level.ports[f"currm_bottom_A_0_drain_E"].center[0] - top_level.ports[f"currm_bottom_A_0_drain_W"].center[0])/2

    dist_GS = abs(top_level.ports[f"currm_bottom_A_0_gate_E"].center[0] - top_level.ports[f"currm_bottom_A_0_gate_W"].center[0])/2

    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)

    bottomA_drain_via  = top_level << viam2m3

    bottomA_drain_via.move(top_level.ports[f"currm_bottom_A_0_drain_W"].center).movex(dist_DS)

    bottomA_gate_via  = top_level << viam2m3

    bottomA_gate_via.move(top_level.ports[f"currm_bottom_A_0_gate_W"].center).movex(dist_GS)

    top_level << straight_route(pdk, bottomA_drain_via.ports["top_met_N"], bottomA_gate_via.ports["top_met_S"], glayer1="met3", glayer2="met3")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # MIDDLE CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    currm_middle = n_transistor_interdigitized(pdk, device="pfet", numcols=1, n_devices=4, with_substrate_tap=False, with_tie=False, width=10, length=2)

    currm_middle = top_level<< currm_middle
    currm_middle.name="currm_middle"

    currm_middle_ref = prec_ref_center(currm_middle)
    currm_middle_ref.move(top_ref.center).movey(evaluate_bbox(currm_bottom_ref)[1]+2*n_well_sep)
    top_level.add(currm_middle_ref)

    top_level.add_ports(currm_middle_ref.get_ports_list(),prefix="currm_middle_")

    middleA_gate_via  = top_level << viam2m3

    middleA_gate_via.move(top_level.ports[f"currm_middle_A_0_gate_W"].center).movex(dist_GS)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TOP CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    currm_top = n_transistor_interdigitized(pdk, device="pfet", numcols=1, n_devices=3, with_substrate_tap=False, with_tie=False, width=10, length=2)

    currm_top = top_level<< currm_top
    currm_top.name="currm_top"

    currm_top_ref = prec_ref_center(currm_top)
    currm_top_ref.move(currm_middle.center).movey(evaluate_bbox(currm_middle_ref)[1]+2*n_well_sep)
    top_level.add(currm_top_ref)

    top_level.add_ports(currm_top_ref.get_ports_list(),prefix="currm_top_")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # INTERCONNECTIONS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    bottomA_source_via = top_level << viam2m3
    bottomA_source_via.move(top_level.ports[f"currm_bottom_A_0_source_W"].center).movex(-dist_DS)

    top_level << straight_route(pdk, bottomA_source_via.ports["top_met_W"], top_level.ports[f"currm_bottom_A_0_source_E"], glayer1="met2", glayer2="met2")

    middleA_drain_via  = top_level << viam2m3
    middleA_drain_via.move(top_level.ports[f"currm_middle_A_0_drain_W"].center).movex(-dist_DS)

    top_level << straight_route(pdk, middleA_drain_via.ports["top_met_W"], top_level.ports[f"currm_middle_A_0_drain_E"], glayer1="met2", glayer2="met2")

    bottom_middle_route = straight_route(pdk, bottomA_source_via.ports["top_met_S"], middleA_drain_via.ports["top_met_N"], glayer1="met3", glayer2="met3")

    bottom_middle_ref = top_level << bottom_middle_route

    bottom_middle_route.name="bottomAsource_to_middleAdrain"

    bottom_middle_x_tap = bottom_middle_ref.center[0]           

    bottom_middle_anchor = top_level << met3_anchor(pdk, met_layer="met3", w=0.5, h=0.5)

    x_diff_anchor = abs(bottom_middle_x_tap - middleA_gate_via.center[0])
    bottom_middle_anchor.move((middleA_gate_via.center))
    bottom_middle_anchor.movex(-x_diff_anchor)
    top_level.add(bottom_middle_anchor)
    spur = straight_route(pdk, middleA_gate_via.ports["top_met_E"], bottom_middle_anchor.ports["P"], glayer2="met3")
    top_level << spur

    letters = ['B','C','D']
    for letter in letters:

        bottomL_source_via = top_level << viam2m3
        bottomL_source_via.move(top_level.ports[f"currm_bottom_{letter}_0_source_W"].center).movex(dist_DS)

        middleL_drain_via = top_level << viam2m3
        middleL_drain_via.move(top_level.ports[f"currm_middle_{letter}_0_drain_W"].center).movex(dist_DS)

        top_level << straight_route(pdk, bottomL_source_via.ports["top_met_S"], middleL_drain_via.ports["top_met_N"], glayer1="met3", glayer2="met3")

    middleD_gate_via = top_level << viam2m3
    middleD_gate_via.move(top_level.ports[f"currm_middle_D_0_gate_W"].center).movex(dist_GS+1.5*dist_DS)

    top_level << straight_route(pdk, middleD_gate_via.ports["top_met_E"], top_level.ports[f"currm_middle_D_0_gate_W"], glayer1="met2", glayer2="met2")

    topC_drain_via = top_level << viam2m3

    topC_drain_via.move((middleD_gate_via.center[0], top_level.ports[f"currm_top_C_0_drain_W"].center[1]))

    top_level << straight_route(pdk, topC_drain_via.ports["top_met_E"], top_level.ports[f"currm_top_C_0_drain_W"], glayer1="met2", glayer2="met2")

    middle_top_route = straight_route(pdk, middleD_gate_via.ports["top_met_S"], topC_drain_via.ports["top_met_N"], glayer1="met3", glayer2="met3")

    middle_top_ref = top_level << middle_top_route

    middle_top_route.name="middleDgate_to_topdrains"

    middle_top_x_tap = middle_top_ref.center[0]           

    middle_top_A_anchor = top_level << met3_anchor(pdk, met_layer="met3", w=0.5, h=0.5)

    x_diff_anchor = abs(middle_top_x_tap - middleD_gate_via.center[0])

    middle_top_A_anchor.move((middleD_gate_via.center[0], top_level.ports[f"currm_top_A_0_drain_W"].center[1]))

    top_level.add(middle_top_A_anchor)

    middle_top_B_anchor = top_level << met3_anchor(pdk, met_layer="met3", w=0.5, h=0.5)

    middle_top_B_anchor.move((middleD_gate_via.center[0], top_level.ports[f"currm_top_B_0_drain_W"].center[1]))

    top_level.add(middle_top_B_anchor)

    top_level << straight_route(pdk, top_level.ports[f"currm_top_A_0_drain_W"], middle_top_B_anchor.ports["P"], glayer2="met2")

    top_level << straight_route(pdk, top_level.ports[f"currm_top_B_0_drain_W"], middle_top_B_anchor.ports["P"], glayer2="met2")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TAP RING
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    core = top_level.copy()      # so we don't mutate while measuring
    core_flat = core.flatten()   # include all placed children

    xmin, xmax = core_flat.xmin, core_flat.xmax
    ymin, ymax = core_flat.ymin, core_flat.ymax

    core_w = xmax - xmin
    core_h = ymax - ymin

    cx = (xmin + xmax) / 2
    cy = (ymin + ymax) / 2

    # Adding tapring
    if with_tie:
        well, sdglayer = "nwell", "p+s/d"
        tap_sep = max(maxmet_sep,
            pdk.get_grule("active_diff", "active_tap")["min_separation"])
        tap_sep += pdk.get_grule(sdglayer, "active_tap")["min_enclosure"]
        tap_encloses = (
            (2*tap_sep + core_w),
            (2*tap_sep + core_h),
        )
        tie_ref = top_level << tapring(pdk, enclosed_rectangle = tap_encloses, sdlayer = sdglayer, horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
        #tie_ref.movey(-(BCM.ymax+tap_sep));
        # tie_ref.movey(-5.1);
        tie_ref.move((cx, cy))
        top_level.add_ports(tie_ref.get_ports_list(), prefix="welltie_")
        ##tie_ref.pprint_ports()
    
  
        # add the substrate tap if specified
        if with_substrate_tap:
            subtap_sep = pdk.get_grule("dnwell", "active_tap")["min_separation"]
            subtap_enclosure = (
                2.5 * (subtap_sep + top_level.xmax),
                2.5 * (subtap_sep + top_level.ymax),
            )
            subtap_ring_ref = top_level << tapring(pdk, enclosed_rectangle = subtap_enclosure, sdlayer = "p+s/d", horizontal_glayer = tie_layers[0], vertical_glayer = tie_layers[1])
            # subtap_ring_ref.movey(-5.1);
            subtap_ring_ref.move(top_ref.center)
            top_level.add_ports(subtap_ring_ref.get_ports_list(), prefix="substrate_tap_")

        # add well
        top_level.add_padding(default=pdk.get_grule(well, "active_tap")["min_enclosure"],layers=[pdk.get_glayer(well)])
        top_level = add_ports_perimeter(top_level, layer = pdk.get_glayer(well), prefix="well_")

        # Connect well ties to well
        try:
            top_level << straight_route(pdk, top_level.ports["currm_bottom_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")
            

            top_level << straight_route(pdk, top_level.ports[f'currm_bottom_D_{num_cols - 1}_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")
            

            top_level << straight_route(pdk, top_level.ports["currm_middle_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")
            

            top_level << straight_route(pdk, top_level.ports[f'currm_middle_D_{num_cols - 1}_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")
            

            top_level << straight_route(pdk, top_level.ports["currm_top_A_0_dummy_L_gsdcon_top_met_W"],top_level.ports["welltie_W_top_met_W"],glayer2="met1")
            

            top_level << straight_route(pdk, top_level.ports[f'currm_top_C_{num_cols - 1}_dummy_R_gsdcon_top_met_E'], top_level.ports["welltie_E_top_met_E"], glayer2="met1")
            


        except KeyError:
            pass
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # CONNECT SOURCES TO VDD
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    top_level << straight_route(pdk, top_level.ports["currm_middle_A_0_source_W"],top_level.ports["welltie_W_top_met_E"],glayer2="met1")

    return rename_ports_by_orientation(component_snap_to_grid(top_level))

    
if __name__ == "__main__":
    selected_pdk=gf180 
    comp = input_stage(selected_pdk, num_cols=1, Length=5,Width=1,show_netlist=False)
    #comp.pprint_ports()
    #comp = add_cm_labels(comp, pdk=selected_pdk)
    comp.name = "INPUT_STAGE"
    comp.show()
    ##Write the current mirror layout to a GDS file
    comp.write_gds("GDS/input_stage.gds")
    
    # # #Generate the netlist for the current mirror
    # print("\n...Generating Netlist...")
    #print(comp.info["netlist"].generate_netlist())
    # # #DRC Checks
    # drc_result = selected_pdk.drc_magic(comp, comp.name,output_file=Path("DRC/"))
    # # #LVS Checks
    # #print("\n...Running LVS...")
    # netgen_lvs_result = selected_pdk.lvs_netgen(comp, comp.name,output_file_path=Path("LVS/"),copy_intermediate_files=True)        

    
    