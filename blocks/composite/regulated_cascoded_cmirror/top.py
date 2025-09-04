from glayout import MappedPDK, sky130,gf180
from glayout import nmos, pmos, tapring,via_stack

from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from gdsfactory import cell
from gdsfactory.component import Component
from gdsfactory.components import text_freetype, rectangle

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


# @validate_arguments
def top(
        pdk: MappedPDK,
        Width: float = 1,
        Length: Optional[float] = None,
        num_cols: int = 2,
        fingers: int = 1,
        multipliers: int = 1,
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
    top_level= Component(name="top_design")
    Length = Length if Length is not None else pdk.get_grule('poly')['min_width']
    top_ref = prec_ref_center(top_level)

    #creating fets for output branches
    fet = pmos(pdk, width=Width,  length=Length, fingers=fingers, multipliers=multipliers, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    fet_1_ref = prec_ref_center(fet)
    fet_2_ref = prec_ref_center(fet) 
    fet_3_ref = prec_ref_center(fet)
    fet_4_ref = prec_ref_center(fet)
    

    fet_1_ref.move(top_ref.center).movex(- (evaluate_bbox(fet)[0]/2) - pdk.util_max_metal_seperation())
    fet_2_ref.move(top_ref.center).movex(- (3 * evaluate_bbox(fet)[0]/2) - 2*pdk.util_max_metal_seperation())
    fet_3_ref.move(top_ref.center).movex( (evaluate_bbox(fet)[0]/2) + pdk.util_max_metal_seperation())
    fet_4_ref.move(top_ref.center).movex( (3*evaluate_bbox(fet)[0]/2) + 2*pdk.util_max_metal_seperation())

    top_level.add(fet_1_ref)
    top_level.add(fet_2_ref)
    top_level.add(fet_3_ref)
    top_level.add(fet_4_ref)

    
    VCM = current_mirror_base(pdk, num_cols=1,Length=5,Width=1, device='nfet')
    vcm_ref = prec_ref_center(VCM)
    vcm_ref.move(top_ref.center).movey(-3*evaluate_bbox(top_ref)[1]).movex(- (evaluate_bbox(fet)[0]) - 30 * pdk.util_max_metal_seperation())
    
    
    SBCM = self_biased_cascode_current_mirror(pdk, num_cols=1, Length=5,Width=1, device='nfet')
    sbcm_ref = prec_ref_center(SBCM)
    sbcm_ref.move(top_ref.center).movey(-3*evaluate_bbox(top_ref)[1]).movex(- 1 * (evaluate_bbox(fet)[0]/2) + 32 * pdk.util_max_metal_seperation())
    
    
    RCCM= regulated_cascode_current_mirror(pdk, num_cols=1, Length=5,Width=1, device='nfet',show_netlist=False)
    rccm_ref = prec_ref_center(RCCM)
    rccm_ref.move(top_ref.center).movey(-3*evaluate_bbox(top_ref)[1]).movex( 2* (evaluate_bbox(fet)[0]/2) +  20 * pdk.util_max_metal_seperation())
    

    top_level.add(vcm_ref)
    top_level.add_ports(vcm_ref.get_ports_list(), prefix="vcm_")
    top_level.add(sbcm_ref)
    top_level.add_ports(sbcm_ref.get_ports_list(), prefix="sbcm_")
    top_level.add(rccm_ref)
    top_level.add_ports(rccm_ref.get_ports_list(), prefix="rccm_")
    
    
    return rename_ports_by_orientation(component_snap_to_grid(top_level))

    
if __name__ == "__main__":
    selected_pdk=gf180
    comp = top(selected_pdk, num_cols=2, Length=5,Width=1,show_netlist=False)
    #comp.pprint_ports()
    #comp = add_cm_labels(comp, pdk=selected_pdk)
    comp.name = "TOP"
    comp.show()
    ##Write the current mirror layout to a GDS file
    comp.write_gds("GDS/top.gds")
    
    # # #Generate the netlist for the current mirror
    # print("\n...Generating Netlist...")
    #print(comp.info["netlist"].generate_netlist())
    # # #DRC Checks
    #drc_result = selected_pdk.drc_magic(comp, comp.name,output_file=Path("DRC/"))
    # # #LVS Checks
    # #print("\n...Running LVS...")
    #netgen_lvs_result = selected_pdk.lvs_netgen(comp, comp.name,output_file_path=Path("LVS/"),copy_intermediate_files=True)        

    
    