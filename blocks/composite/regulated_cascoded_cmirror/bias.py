from glayout import MappedPDK, sky130, gf180
from glayout import nmos, pmos, tapring, via_stack

# from glayout.placement.two_transistor_interdigitized import two_nfet_interdigitized, two_pfet_interdigitized
from bias_base import biased_base
from gdsfactory import cell
from gdsfactory.component import Component
from gdsfactory.components import text_freetype, rectangle
from pathlib import Path

from glayout.routing import c_route, L_route, straight_route
from glayout.spice.netlist import Netlist

from glayout.util.port_utils import add_ports_perimeter, rename_ports_by_orientation
from glayout.util.comp_utils import (
    evaluate_bbox,
    prec_center,
    prec_ref_center,
    align_comp_to_port,
)
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
    if "=" in line:
        key, value = line.split("=", 1)
        env_vars[key] = value

# Now, update os.environ with these
os.environ.update(env_vars)


# @validate_arguments
def generate_bias_netlist(
    prefix: str,
    in_net: str,
    en_net: str,
    out_net: str,
    nl_base_bottom: Netlist,
    nl_base_left: Netlist,
    nl_base_right: Netlist,
    nl_fet_left: Netlist,
    nl_fet_right: Netlist,
    show_netlist: bool = False,
) -> Netlist:
    """
    Build top-level .subckt that instantiates child subckts and wires them to top nets.
    TOP pin order must match layout header:
    .subckt TOP VIN VSS VDD VOUT_RCCM VOUT_SBCM VOUT_VCM VAUX EN
    """
    top_pins = [
        in_net,
        "VSS",
        "VDD",
        out_net,
        en_net,
    ]

    netlist = Netlist(
        circuit_name=prefix,
        nodes=top_pins,
    )


    base_bottom_comp = netlist.connect_netlist(nl_base_bottom, [('VSS','VSS')])
    base_left_comp = netlist.connect_netlist(nl_base_left, [('VIN',in_net),('VDD','VDD')])
    base_right_comp = netlist.connect_netlist(nl_base_right, [('VOUT',out_net),('VDD','VDD')])
    fet_left = netlist.connect_netlist(nl_fet_left, [(('G',en_net),('B','VDD'))])
    fet_right = netlist.connect_netlist(nl_fet_right, [(('G',en_net),('B','VDD'))])

    netlist.connect_subnets(base_left_comp, base_bottom_comp, [('VOUT','VIN')])
    netlist.connect_subnets(base_bottom_comp, base_right_comp, [('VOUT','VIN')])
    netlist.connect_subnets(fet_left, base_left_comp, [('D','VIN')])

    if show_netlist:
        print("Generated top-level netlist:\n")
        print(netlist.generate_netlist())

    return netlist


# @validate_arguments
def bias_stage(
    pdk: MappedPDK,
    Width: float = 1,
    Length: Optional[float] = 1,
    num_cols: int = 1,
    fingers: int = 1,
    multipliers: int = 1,
    type: Optional[str] = "pfet",
    with_substrate_tap: Optional[bool] = False,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[bool] = False,
    tie_layers: tuple[str, str] = ("met2", "met1"),
    show_netlist: Optional[bool] = False,
    add_labels = True,
    **kwargs,
) -> Component:
    """An instantiable self biased casoded current mirror that returns a Component object."""

    pdk.activate()
    maxmet_sep = pdk.util_max_metal_seperation()
    n_well_sep = maxmet_sep
    psize = (0.35, 0.35)

    # Create the current mirror component
    top_level = Component(name="bias_stage")
    top_level.name = "bias_stage"
    Length = Length if Length is not None else pdk.get_grule("poly")["min_width"]
    top_ref = prec_ref_center(top_level)

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BOTTOM CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    base_bottom = biased_base(
        pdk,
        device="nfet",
        width=(8, 8),
        length=1,
        fingers=(10,1),
        with_substrate_tap=False,
        with_tie=True,
    )


    base_bottom_ref = prec_ref_center(base_bottom)
    base_bottom_ref.move(top_ref.center)
    top_level.add(base_bottom_ref)

    top_level.add_ports(base_bottom_ref.get_ports_list(), prefix="base_bottom_")

    core1 = base_bottom.copy().flatten()   # so we don't mutate while measuring

    xmin1, xmax1 = core1.xmin, core1.xmax
    ymin1, ymax1 = core1.ymin, core1.ymax

    # dist_DS = (
    #     abs(
    #         top_level.ports[f"base_bottom_A_0_drain_E"].center[0]
    #         - top_level.ports[f"base_bottom_A_0_drain_W"].center[0]
    #     )
    #     / 2
    # )

    # dist_GS = (
    #     abs(
    #         top_level.ports[f"base_bottom_A_0_gate_E"].center[0]
    #         - top_level.ports[f"base_bottom_A_0_gate_W"].center[0]
    #     )
    #     / 2
    # )

    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    viam1m2 = via_stack(pdk, "met1", "met2", centered=True)


    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # MIDDLE CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    base_top = biased_base(
        pdk,
        device="pfet",
        width=(10, 10),
        length=2,
        fingers=(10,1),
        with_substrate_tap=False,
        with_tie=True,
    )

    core2 = base_top.copy().flatten()   # so we don't mutate while measuring

    xmin2, xmax2 = core2.xmin, core2.xmax
    ymin2, ymax2 = core2.ymin, core2.ymax

    base_left_ref = prec_ref_center(base_top)
    base_left_ref.move(base_bottom_ref.center).movey(
        (ymax1-ymin1)  + 4 * n_well_sep + 4*maxmet_sep
    ).movex(-(xmax1 - xmin1)/2 -  (xmax2 - xmin2)/2 - 2*n_well_sep - 2*maxmet_sep)
    top_level.add(base_left_ref)

    top_level.add_ports(base_left_ref.get_ports_list(), prefix="base_left_")

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # TOP CURRENT MIRRORS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------


    base_right_ref = prec_ref_center(base_top)
    base_right_ref.move(base_bottom_ref.center).movey(
        (ymax1-ymin1)  + 4 * n_well_sep + 4*maxmet_sep
    ).movex((xmax1 - xmin1)/2 + (xmax2 - xmin2)/2 + 2*n_well_sep + 2*maxmet_sep)
    top_level.add(base_right_ref)

    top_level.add_ports(base_right_ref.get_ports_list(), prefix="base_right_")


    # ------------------------------------------------------------------------------------------------------------------------------------------------------------
    # INTERCONNECTIONS
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------

    top_level << L_route(
        pdk, base_left_ref.ports["OUT_top_met_S"], base_bottom_ref.ports["IN_top_met_W"]
    )

    top_level << L_route(
        pdk, base_right_ref.ports["IN_top_met_S"], base_bottom_ref.ports["OUT_top_met_E"]
    )

    fet = pmos(pdk, width=10, length=2, fingers=1, with_tie=True, with_substrate_tap=False)

    fet_ref_left = prec_ref_center(fet)

    # fet_ref_right = prec_ref_center(fet)

    fet_ref_left.move(base_left_ref.ports["GATE_CONN_top_met_N"].center).movey(4*maxmet_sep + 1.5*evaluate_bbox(fet_ref_left)[1] + 2*n_well_sep)
    top_level.add(fet_ref_left)

    top_level.add_ports(fet_ref_left.get_ports_list(), prefix="fet_left_")


    dist_DS = (
        abs(
            top_level.ports[f"fet_left_multiplier_0_drain_E"].center[0]
            - top_level.ports[f"fet_left_multiplier_0_drain_W"].center[0]
        )
        / 2
    )

    drain_gate_via = top_level << viam2m3
    drain_gate_via.move(top_level.ports[f"fet_left_multiplier_0_drain_W"].center).movex(dist_DS)

    top_level << straight_route(pdk, drain_gate_via.ports["top_met_S"], base_left_ref.ports["GATE_CONN_top_met_N"], glayer1="met3", glayer2="met3")

    fet_ref_right = prec_ref_center(fet)
    fet_ref_right.move(base_right_ref.ports["GATE_CONN_top_met_N"].center).movey(4*maxmet_sep + 1.5*evaluate_bbox(fet_ref_right)[1] + 2*n_well_sep)
    top_level.add(fet_ref_right)

    top_level.add_ports(fet_ref_right.get_ports_list(), prefix="fet_right_")

    drain_gate_via = top_level << viam2m3
    drain_gate_via.move(top_level.ports[f"fet_right_multiplier_0_drain_W"].center).movex(dist_DS)

    top_level << straight_route(pdk, drain_gate_via.ports["top_met_S"], base_right_ref.ports["GATE_CONN_top_met_N"], glayer1="met3", glayer2="met3")

    top_level << straight_route(pdk, fet_ref_left.ports["tie_S_top_met_S"], base_left_ref.ports["welltie_N_top_met_N"], glayer1="met1", glayer2="met1", width=6)
    top_level << straight_route(pdk, fet_ref_right.ports["tie_S_top_met_S"], base_right_ref.ports["welltie_N_top_met_N"], glayer1="met1", glayer2="met1", width=6)

    top_level << straight_route(pdk, fet_ref_left.ports["multiplier_0_gate_E"], fet_ref_right.ports["multiplier_0_gate_W"], glayer1="met2", glayer2="met2")

    # gate_fet_via = top_level << viam1m2

    # gate_fet_via.move((fet_ref_left.ports["tie_W_top_met_E"].center[0], fet_ref_left.ports["multiplier_0_gate_E"].center[1])).movex(-2*dist_DS)

    # top_level << straight_route(pdk, gate_fet_via.ports["top_met_E"], fet_ref_left.ports["multiplier_0_gate_W"], glayer1="met2", glayer2="met2")

    # top_level.add_ports(gate_fet_via.get_ports_list(), prefix=f"EN_")

    top_level << straight_route(pdk, fet_ref_left.ports["multiplier_0_source_W"], fet_ref_left.ports["tie_W_top_met_E"], glayer1="met2", glayer2="met2")

    top_level << straight_route(pdk, fet_ref_right.ports["multiplier_0_source_W"], fet_ref_right.ports["tie_W_top_met_E"], glayer1="met2", glayer2="met2")
    
    top_level << straight_route(pdk, fet_ref_left.ports["tie_E_top_met_E"], fet_ref_right.ports["tie_W_top_met_W"], glayer1="met1", glayer2="met1", width=6)


    top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))

    # top_level.info["netlist"] = generate_bias_stage_netlist(
    #     pdk=pdk,
    #     prefix="BIAS",
    #     CM_size=(Width, Length, num_cols, fingers),  # (width, length, multipliers, fingers)
    #     transistor_type=type,
    #     net_in="VIN",  # Input drain connected to IREF
    #     net_en="EN",  # Auxiliary node
    #     net_out="VOUT",
    #     subckt_only=True,
    #     show_netlist=show_netlist,
    # )

    if add_labels:
        return add_cm_labels(top_level, pdk)
    else:
        return top_level


def add_cm_labels(cm_in: Component, pdk: MappedPDK) -> Component:
    cm_in.unlock()

    psize = (0.35, 0.35)
    move_info = []

    # VIN
    vinlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    vinlabel.add_label(text="VIN", layer=pdk.get_glayer("met2_label"))
    move_info.append((vinlabel, cm_in.ports["base_left_IN_top_met_N"], None))

    # EN
    venlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    venlabel.add_label(text="EN", layer=pdk.get_glayer("met2_label"))
    move_info.append((venlabel, cm_in.ports["EN_top_met_N"], None))

    # VOUT 
    voutlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    voutlabel.add_label(text="VOUT", layer=pdk.get_glayer("met2_label"))
    move_info.append((voutlabel, cm_in.ports["base_right_OUT_top_met_N"], None))

    # VDD (well tie)
    vddlabel = rectangle(layer=pdk.get_glayer("met1_pin"), size=psize, centered=True).copy()
    vddlabel.add_label(text="VDD", layer=pdk.get_glayer("met1_label"))
    move_info.append((vddlabel, cm_in.ports["fet_left_tie_N_top_met_N"], None))

    # VSS (well tie)
    vsslabel = rectangle(layer=pdk.get_glayer("met1_pin"), size=psize, centered=True).copy()
    vsslabel.add_label(text="VSS", layer=pdk.get_glayer("met1_label"))
    move_info.append((vsslabel, cm_in.ports["base_bottom_welltie_S_top_met_S"], None))

    for comp, prt, alignment in move_info:
        alignment = ("c", "b") if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        cm_in.add(compref)

    return cm_in.flatten()


if __name__ == "__main__":
    selected_pdk = gf180
    comp = bias_stage(
        selected_pdk, num_cols=1, Width=10, Length=2, with_substrate_tap=False, show_netlist=False, add_labels=False
    )
    
    comp.name = "BIAS_STAGE"
    comp.show()
    # Write the current mirror layout to a GDS file
    comp.write_gds("GDS/bias_stage.gds")

    # Generate the netlist for the current mirror
    # print(comp.info["netlist"].generate_netlist())

    # DRC Checks
    drc_result = selected_pdk.drc_magic(comp, comp.name, output_file=Path("DRC/"))

    # LVS Checks
    # netgen_lvs_result = selected_pdk.lvs_netgen(
    #     comp, comp.name, output_file_path=Path("LVS/"), copy_intermediate_files=True
    # )
    