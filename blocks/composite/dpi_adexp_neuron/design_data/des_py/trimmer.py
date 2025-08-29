from gdsfactory.read.import_gds import import_gds

from glayout import MappedPDK, sky130 , gf180 , ihp130
#from gdsfactory.cell import cell
from gdsfactory import Component
from gdsfactory.components import text_freetype, rectangle

from glayout import resistor
from glayout import two_pfet_interdigitized
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

    mp1_2=resistor(pdk,width=0.28,length=8.0,num_series=2)
    mp1_2_ref=prec_ref_center(mp1_2)
    
    pfet_2 = pmos(pdk, length=2.0,width=2.0, fingers=1, multipliers=2, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_1 = pmos(pdk, length=2.0,width=2.0, fingers=1, multipliers=1, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_3 = pmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=2, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_4 = pmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=1, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_5 = pmos(pdk, length=8.0,width=0.28, fingers=1, multipliers=1, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    
    mp3_ref = prec_ref_center(pfet_1)
    mp5_ref = prec_ref_center(pfet_2) 
    mp7_ref = prec_ref_center(pfet_2)
    mp10_ref = prec_ref_center(pfet_2)

    mp4_ref = prec_ref_center(pfet_3)
    mp6_ref = prec_ref_center(pfet_3) 
    mp8_ref = prec_ref_center(pfet_3)
    mp11_ref = prec_ref_center(pfet_3)

    
    mp3_ref.movex(top_level.xmin - (evaluate_bbox(pfet_1)[0]/2) - pdk.util_max_metal_seperation())
    mp5_ref.movex(top_level.xmax + (evaluate_bbox(pfet_1)[0]/2) + pdk.util_max_metal_seperation())
    mp7_ref.movex(top_level.xmax + (3*evaluate_bbox(pfet_1)[0]/2) + 3 *pdk.util_max_metal_seperation())
    mp10_ref.movex(top_level.xmin + (5*evaluate_bbox(pfet_1)[0]/2) + 5*pdk.util_max_metal_seperation())


    mp4_ref.movex(top_level.xmin - (evaluate_bbox(pfet_2)[0]/2) - pdk.util_max_metal_seperation())
    mp4_ref.movey(top_level.ymin - (2*evaluate_bbox(pfet_2)[1]/2) - 2*pdk.util_max_metal_seperation())
    mp6_ref.movex(top_level.xmax + (evaluate_bbox(pfet_2)[0]/2) + pdk.util_max_metal_seperation())
    mp6_ref.movey(top_level.ymin - (2*evaluate_bbox(pfet_2)[1]/2) - 2*pdk.util_max_metal_seperation())
    mp8_ref.movex(top_level.xmax + ( 3* evaluate_bbox(pfet_2)[0]/2) + 2* pdk.util_max_metal_seperation())
    mp8_ref.movey(top_level.ymin - (2*evaluate_bbox(pfet_2)[1]/2) - 2*pdk.util_max_metal_seperation())
    mp11_ref.movex(top_level.xmax + (5*evaluate_bbox(pfet_2)[0]/2) + 4*pdk.util_max_metal_seperation())
    mp11_ref.movey(top_level.ymin - (2*evaluate_bbox(pfet_2)[1]/2) - 2*pdk.util_max_metal_seperation())

    mp1_2_ref.movex(top_level.xmin - (3*evaluate_bbox(pfet_1)[0]/2) - 2* pdk.util_max_metal_seperation())

    top_level.add(mp3_ref)
    top_level.add(mp5_ref)
    top_level.add(mp7_ref)
    top_level.add(mp10_ref)
    top_level.add(mp4_ref)
    top_level.add(mp6_ref)
    top_level.add(mp8_ref)
    top_level.add(mp11_ref)
    top_level.add(mp1_2_ref)

    

    
    
    ncm12 = current_mirror(pdk,numcols=1,width=0.28,length=8.0,device='nfet',with_tie=False)
    ncm12_ref= prec_ref_center(ncm12)
    ncm34 = current_mirror(pdk,numcols=1,width=0.28,length=8.0,device='nfet',with_tie=False)
    ncm34_ref= prec_ref_center(ncm34)
    

    mp9_ref=prec_ref_center(pfet_5)
    mp9_ref.movey(top_level.ymin - (evaluate_bbox(pfet_2)[1]/2) + 2*pdk.util_max_metal_seperation())
    #ncm34_ref.movex(top_level.xmin + evaluate_bbox(ncm34)[0]/2 + pdk.util_max_metal_seperation()+1)
    ncm12_ref.movey(top_level.ymin - (2*evaluate_bbox(pfet_2)[1]/2) + 2*pdk.util_max_metal_seperation())
    ncm34_ref.movey(top_level.ymin - (3*evaluate_bbox(pfet_2)[1]/2) + 2*pdk.util_max_metal_seperation())
    
    top_level.add(mp9_ref)
    top_level.add(ncm12_ref)
    top_level.add(ncm34_ref)

    mp19_ref = prec_ref_center(pfet_4)
    mp20_ref = prec_ref_center(pfet_4)
    mp18_ref = prec_ref_center(pfet_3)
    mp17_ref = prec_ref_center(pfet_3)
    mp16_ref = prec_ref_center(pfet_4)
    mp12_ref = prec_ref_center(pfet_3)

    mp19_ref.movex(top_level.xmin + (evaluate_bbox(pfet_4)[1]/2) + 2* pdk.util_max_metal_seperation())
    mp19_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_4)[1]/2) - 2* pdk.util_max_metal_seperation())

    mp20_ref.movex(top_level.xmin + (4* evaluate_bbox(pfet_4)[1]/2) + 4* pdk.util_max_metal_seperation())
    mp20_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_4)[1]/2) - 2* pdk.util_max_metal_seperation())

    mp18_ref.movex(top_level.xmin + (4* evaluate_bbox(pfet_3)[1]/2) + 4*pdk.util_max_metal_seperation())
    mp18_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_3)[1]/2) -  pdk.util_max_metal_seperation())

    mp17_ref.movex(top_level.xmin + (6* evaluate_bbox(pfet_3)[1]/2) + 6* pdk.util_max_metal_seperation())
    mp17_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_3)[1]/2) -  pdk.util_max_metal_seperation())

    mp16_ref.movex(top_level.xmin + (8* evaluate_bbox(pfet_3)[1]/2) + 8* pdk.util_max_metal_seperation())
    mp16_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_3)[1]/2) -  pdk.util_max_metal_seperation())

    mp12_ref.movex(top_level.xmin + (10* evaluate_bbox(pfet_3)[1]/2) + 10* pdk.util_max_metal_seperation())
    mp12_ref.movey(top_level.ymax + (2* evaluate_bbox(pfet_3)[1]/2) -  pdk.util_max_metal_seperation())

    ############################
    
    pfet_4 = pmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=4, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_5 = pmos(pdk, length=2.0,width=2.0, fingers=1, multipliers=4, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    mp15_ref=prec_ref_center(pfet_3)
    mp13_ref=prec_ref_center(pfet_5)
    mp14_ref=prec_ref_center(pfet_4)

    mp13_ref.movex(top_level.xmax + (evaluate_bbox(pfet_5)[0]/2) + pdk.util_max_metal_seperation())
    mp15_ref.movex(top_level.xmax + (evaluate_bbox(pfet_4)[0]/2) + pdk.util_max_metal_seperation())
    mp14_ref.movex(top_level.xmax + (evaluate_bbox(pfet_4)[0]/2) + pdk.util_max_metal_seperation())
    top_level.add(mp15_ref)
    
    
    mp15_ref.movey(top_level.ymax + (evaluate_bbox(pfet_4)[1]/2) + pdk.util_max_metal_seperation())
    mp14_ref.movey(top_level.ymin + (evaluate_bbox(pfet_4)[1]/2) + pdk.util_max_metal_seperation())

    ############################
    top_level.add(mp13_ref)
    top_level.add(mp14_ref)
    ############################
    pfet_6 = pmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=8, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_7 = pmos(pdk, length=2.0,width=2.0, fingers=1, multipliers=8, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    mp23_ref=prec_ref_center(pfet_3)
    mp21_ref=prec_ref_center(pfet_7)
    mp22_ref=prec_ref_center(pfet_6)

    mp23_ref.movex(top_level.xmax + (evaluate_bbox(pfet_3)[0]/2) + pdk.util_max_metal_seperation())
    mp21_ref.movex(top_level.xmax + (evaluate_bbox(pfet_7)[0]/2) + pdk.util_max_metal_seperation())
    mp22_ref.movex(top_level.xmax + (evaluate_bbox(pfet_6)[0]/2) + pdk.util_max_metal_seperation())
    top_level.add(mp21_ref)
    
    
    mp23_ref.movey(top_level.ymax + (evaluate_bbox(pfet_4)[1]/2) + pdk.util_max_metal_seperation())
    mp22_ref.movey(top_level.ymin - 2* (evaluate_bbox(pfet_6)[1]/2) - 2* pdk.util_max_metal_seperation())

    ############################
    top_level.add(mp22_ref)
    top_level.add(mp23_ref)
    ###########################

    pfet_8 = pmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=16, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    pfet_9 = pmos(pdk, length=2.0,width=2.0, fingers=1, multipliers=16, with_dummy=True, dnwell=False,  with_substrate_tap=False)
    mp26_ref=prec_ref_center(pfet_3)
    mp24_ref=prec_ref_center(pfet_9)
    mp25_ref=prec_ref_center(pfet_8)

    mp26_ref.movex(top_level.xmax + (evaluate_bbox(pfet_3)[0]/2) + pdk.util_max_metal_seperation())
    mp24_ref.movex(top_level.xmax + (evaluate_bbox(pfet_9)[0]/2) + pdk.util_max_metal_seperation())
    mp25_ref.movex(top_level.xmax + (evaluate_bbox(pfet_8)[0]/2) + pdk.util_max_metal_seperation())
    top_level.add(mp24_ref)
    
    
    mp26_ref.movey(top_level.ymax + (evaluate_bbox(pfet_4)[1]/2) + pdk.util_max_metal_seperation())
    mp25_ref.movey(top_level.ymin - (2* evaluate_bbox(pfet_8)[1]/2) - 2* pdk.util_max_metal_seperation())

    ############################
    top_level.add(mp26_ref)
    top_level.add(mp25_ref)
    ############################
    top_level.add(mp19_ref)
    top_level.add(mp20_ref)
    top_level.add(mp18_ref)
    top_level.add(mp17_ref)
    top_level.add(mp16_ref)
    top_level.add(mp12_ref)

    ############################

    nfet_1 = nmos(pdk, length=0.28,width=2.0, fingers=1, multipliers=1, with_dummy=True, with_dnwell=False,  with_substrate_tap=False)
    mn5_ref = prec_ref_center(nfet_1)
    mn6_ref = prec_ref_center(nfet_1)

    mn5_ref.movex(top_level.xmin + (4* evaluate_bbox(nfet_1)[1]/2) + 4* pdk.util_max_metal_seperation())
    mn5_ref.movey(top_level.ymin - (evaluate_bbox(pfet_2)[1]/2) + 2*pdk.util_max_metal_seperation())

    mn6_ref.movex(top_level.xmin + (8* evaluate_bbox(nfet_1)[1]/2) + 8*pdk.util_max_metal_seperation())
    mn6_ref.movey(top_level.ymin - (evaluate_bbox(pfet_2)[1]/2) + 2*pdk.util_max_metal_seperation())

    top_level.add(mn5_ref)
    top_level.add(mn6_ref)

   
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
