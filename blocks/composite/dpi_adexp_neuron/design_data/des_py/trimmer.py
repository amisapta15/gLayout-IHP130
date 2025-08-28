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

import sys
sys.path.append('../../../../elementary/diff_pair/')
from diff_pair import diff_pair, diff_pair_generic, diff_pair_netlist, add_df_labels
sys.path.append('../../../../elementary/current_mirror/')
from current_mirror import current_mirror,add_cm_labels


def trimmer(
        pdk: MappedPDK,
        #device_type: str = "nmos", 
        #placement: str = "horizontal",
        #width: tuple[float,float] = (3,3),
        #length: tuple[float,float] = (None,None),
        #fingers: tuple[int,int] = (1,1),
        #multipliers: tuple[int,int] = (1,1),
        #with_substrate_tap: bool = False,
        #dummy_1: tuple[bool,bool] = (True,True),
        #dummy_2: tuple[bool,bool] = (True,True),
        #tie_layers1: tuple[str,str] = ("met2","met1"),
        #tie_layers2: tuple[str,str] = ("met2","met1"),
        #sd_rmult: int=1,
        #**kwargs
        ) -> Component:

    pdk.activate()
    
    #top level component
    top_level = Component(name="trimmer")

    comp = top_level << current_mirror(pdk)
    # comp.pprint_ports()
    #comp = add_cm_labels(comp,gf180)

    return top_level
                     

    

if __name__ == "__main__":
	comp = trimmer(ihp130)

	# comp.pprint_ports()
	#comp = add_fvf_labels(comp, ihp130)
	comp.name = "TRIM"
	#comp.write_gds('out_FVF.gds')
	comp.show()

	#print("...Running DRC...")
	#drc_result = ihp130.drc(comp,comp.name)
