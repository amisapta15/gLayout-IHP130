from pathlib import Path
from typing import Optional, Union
import os
import re
import subprocess

from gdsfactory import cell
from gdsfactory.component import Component
from gdsfactory.components import rectangle, text_freetype

from glayout import MappedPDK, sky130, gf180, nmos, pmos, tapring, via_stack
from glayout.placement.two_transistor_interdigitized import (
    two_nfet_interdigitized,
    two_pfet_interdigitized,
)
from glayout.routing import L_route, c_route, straight_route
from glayout.spice.netlist import Netlist
from glayout.util.comp_utils import (
    align_comp_to_port,
    evaluate_bbox,
    prec_center,
    prec_ref_center,
)
from glayout.util.port_utils import add_ports_perimeter, rename_ports_by_orientation
from glayout.util.snap_to_grid import component_snap_to_grid

from cm_v import current_mirror_base
from cm_sb import self_biased_cascode_current_mirror
from cm_rc import regulated_cascode_current_mirror
from input import input_stage
from bias import bias_stage

###### Only Required for IIC-OSIC Docker
# Run a shell, source .bashrc, then printenv
cmd = 'bash -c "source ~/.bashrc && printenv"'
result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
env_vars = {}
for line in result.stdout.splitlines():
    if "=" in line:
        key, value = line.split("=", 1)
        env_vars[key] = value
os.environ.update(env_vars)

# ---- helpers ----
_HEADER_RE = re.compile(
    r"^\s*\.subckt\s+(\S+)\s+(.*)\s*$", re.IGNORECASE | re.MULTILINE
)


def _parse_subckt_header(source: str):
    m = _HEADER_RE.search(source)
    if not m:
        raise ValueError("Could not find .subckt header in child netlist")
    name = m.group(1)
    pins = [t for t in m.group(2).split() if t.strip()]
    return name, pins


def _instance_line(
    inst_name: str,
    subckt_name: str,
    ordered_child_pins: list[str],
    pinmap: dict[str, str],
):
    try:
        nodes_in_order = [pinmap[p] for p in ordered_child_pins]
    except KeyError as e:
        missing = str(e).strip("'")
        raise ValueError(
            f"Missing mapping for child pin '{missing}' when instantiating {subckt_name}"
        )
    return f"X{inst_name} " + " ".join(nodes_in_order) + f" {subckt_name}\n"


def generate_top_netlist(
    prefix: str,
    in_net: str,
    aux_net: str,
    en_net: str,
    out_vcm_net: str,
    out_sbcm_net: str,
    out_rccm_net: str,
    nl_input: Netlist,
    nl_vcm: Netlist,
    nl_sbcm: Netlist,
    nl_rccm: Netlist,
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
        out_rccm_net,
        out_sbcm_net,
        out_vcm_net,
        aux_net,
        en_net,
    ]

    # Render children and parse headers
    child_texts = {
        "INPUT": nl_input.generate_netlist(),
        "VCM": nl_vcm.generate_netlist(),
        "SBCM": nl_sbcm.generate_netlist(),
        "RCCM": nl_rccm.generate_netlist(),
    }
    parsed = {}
    for key, text in child_texts.items():
        subckt_name, pins = _parse_subckt_header(text)
        parsed[key] = {"name": subckt_name, "pins": pins, "text": text}

    # Internal nets
    in_vcm_int = "IN_VCM"
    in_sbcm_int = "IN_SBCM"
    in_rccm_int = "IN_RCCM"

    # Pin maps matching the child headers
    # INPUT: .subckt INPUT VIN EN VOUT_VCM VOUT_BCM VOUT_CCM VDD
    pinmap_input = {
        "VIN": in_net,
        "EN": en_net,
        "VOUT_VCM": in_vcm_int,
        "VOUT_BCM": in_sbcm_int,
        "VOUT_CCM": in_rccm_int,
        "VDD": "VDD",
    }
    # VCM: .subckt VCM VIN VOUT VSS
    pinmap_vcm = {"VIN": in_vcm_int, "VOUT": out_vcm_net, "VSS": "VSS"}
    # SBCM: .subckt SBCM VIN VOUT VSS
    pinmap_sbcm = {"VIN": in_sbcm_int, "VOUT": out_sbcm_net, "VSS": "VSS"}
    # RCCM: .subckt RCCM VIN VAUX VOUT VSS
    pinmap_rccm = {
        "VIN": in_rccm_int,
        "VAUX": aux_net,
        "VOUT": out_rccm_net,
        "VSS": "VSS",
    }

    # Build instance lines using parsed child pin order
    x_lines = [
        _instance_line(
            f"{prefix}IN",
            parsed["INPUT"]["name"],
            parsed["INPUT"]["pins"],
            pinmap_input,
        ),
        _instance_line(
            f"{prefix}VCM",
            parsed["VCM"]["name"],
            parsed["VCM"]["pins"],
            pinmap_vcm,
        ),
        _instance_line(
            f"{prefix}SBCM",
            parsed["SBCM"]["name"],
            parsed["SBCM"]["pins"],
            pinmap_sbcm,
        ),
        _instance_line(
            f"{prefix}RCCM",
            parsed["RCCM"]["name"],
            parsed["RCCM"]["pins"],
            pinmap_rccm,
        ),
    ]

    # Write children FIRST, then TOP
    src = []
    for key in ("INPUT", "VCM", "SBCM", "RCCM"):
        src.append(parsed[key]["text"].rstrip())
        src.append("")

    src.append(f".subckt {prefix} " + " ".join(top_pins))
    src.extend(x_lines)
    src.append(".ends " + prefix)
    src.append("")

    source_netlist = "\n".join(src)

    topnet = Netlist(
        circuit_name=prefix,
        nodes=top_pins,
        source_netlist=source_netlist,
        instance_format="X{name} {nodes} {circuit_name}",
        parameters={},
    )

    if show_netlist:
        print("Generated top-level netlist:\n")
        print(topnet.generate_netlist())

    return topnet

# def generate_top_netlist(
#     prefix: str,
#     in_net: str,
#     aux_net: str,
#     en_net: str,
#     out_vcm_net: str,
#     out_sbcm_net: str,
#     out_rccm_net: str,
#     nl_input: Netlist,
#     nl_vcm: Netlist,
#     nl_sbcm: Netlist,
#     nl_rccm: Netlist,
#     show_netlist: bool = False,
# ) -> Netlist:
#     """
#     Build top-level .subckt that instantiates child subckts and wires them to top nets.
#     TOP pin order must match layout header:
#     .subckt TOP VIN VSS VDD VOUT_RCCM VOUT_SBCM VOUT_VCM VAUX EN
#     """
#     top_pins = [
#         in_net,
#         "VSS",
#         "VDD",
#         out_rccm_net,
#         out_sbcm_net,
#         out_vcm_net,
#         aux_net,
#         en_net,
#     ]

#     netlist = Netlist(
#         circuit_name=prefix,
#         nodes=top_pins,
#     )


#     in_comp = netlist.connect_netlist(nl_input, [('VIN',in_net),('EN',en_net), ('VDD','VDD')])
#     vcm_comp = netlist.connect_netlist(nl_vcm, [('VOUT',out_vcm_net),('VSS','VSS')])
#     sbcm_comp = netlist.connect_netlist(nl_sbcm, [('VOUT',out_sbcm_net),('VSS','VSS')])
#     rccm_comp = netlist.connect_netlist(nl_rccm, [('VAUX',aux_net),('VOUT',out_rccm_net),('VSS','VSS')])

#     netlist.connect_subnets(in_comp, vcm_comp, [('VOUT_VCM','VIN')])
#     netlist.connect_subnets(in_comp, sbcm_comp, [('VOUT_BCM','VIN')])
#     netlist.connect_subnets(in_comp, rccm_comp, [('VOUT_CCM','VIN')])

#     if show_netlist:
#         print("Generated top-level netlist:\n")
#         print(netlist.generate_netlist())

#     return netlist


# @validate_arguments
def top(
    pdk: MappedPDK,
    with_tie: Optional[bool] = True,
    with_dummy: Optional[bool] = True,
    tie_layers: tuple[str, str] = ("met2", "met1"),
    show_netlist: Optional[bool] = False,
    add_labels: bool = True,
    **kwargs,
) -> Component:
    """An instantiable self biased cascoded current mirror that returns a Component."""
    pdk.activate()

    # Create the current mirror component
    top_level = Component(name="top_design")
    top_ref = prec_ref_center(top_level)

    # -------------------------------------------------------------------------
    # CREATING THE INPUT STAGE
    # -------------------------------------------------------------------------
    print("Creating Input Stage ...")

    input_stage_comp = input_stage(
        pdk,
        num_cols=1,
        Length=2,
        Width=10,
        device="pfet",
        with_substrate_tap=False,
        with_tie=with_tie,
        with_dummy=with_dummy,
        tie_layers=tie_layers,
        add_labels=False,
    )
    input_stage_ref = prec_ref_center(input_stage_comp)
    input_stage_ref.move(top_ref.center)
    top_level.add(input_stage_ref)
    top_level.add_ports(input_stage_ref.get_ports_list(), prefix="input_")

    center = top_level.center

    # -------------------------------------------------------------------------
    # CREATING THE VANILLA CURRENT MIRROR STAGE
    # -------------------------------------------------------------------------
    print("Creating Vanilla Current Mirror ...")

    VCM = current_mirror_base(
        pdk,
        num_cols=1,
        Length=1,
        Width=4,
        device="nfet",
        with_substrate_tap=False,
        add_labels=False,
    )
    vcm_ref = prec_ref_center(VCM)
    vcm_ref.move(center).movex(
        evaluate_bbox(input_stage_ref)[0] + 4 * pdk.util_max_metal_seperation()
    ).movey(-evaluate_bbox(input_stage_ref)[1] / 2)

    top_level.add(vcm_ref)
    top_level.add_ports(vcm_ref.get_ports_list(), prefix="vcm_")

    top_level << L_route(
        pdk, vcm_ref.ports["IN_top_met_N"], input_stage_ref.ports["OUT_B_top_met_E"]
    )

    # -------------------------------------------------------------------------
    # CREATING THE SELF-BIASED CURRENT MIRROR STAGE
    # -------------------------------------------------------------------------
    print("Creating Self-Biased Current Mirror ...")

    SBCM = self_biased_cascode_current_mirror(
        pdk, num_cols=1, Length=1, Width=4, device="nfet", add_labels=False
    )
    sbcm_ref = prec_ref_center(SBCM)
    sbcm_ref.move(center).movex(
        evaluate_bbox(input_stage_ref)[0] + 4 * pdk.util_max_metal_seperation()
    )

    top_level.add(sbcm_ref)
    top_level.add_ports(sbcm_ref.get_ports_list(), prefix="sbcm_")

    top_level << L_route(
        pdk, sbcm_ref.ports["IN_top_met_N"], input_stage_ref.ports["OUT_C_top_met_E"]
    )

    # -------------------------------------------------------------------------
    # CREATING THE REGULATED CASCODE CURRENT MIRROR STAGE
    # -------------------------------------------------------------------------
    print("Creating Regulated Cascoded Current Mirror ...")

    RCCM = regulated_cascode_current_mirror(
        pdk, num_cols=2, Length=1, Width=4, device="nfet", show_netlist=False, add_labels=False
    )
    rccm_ref = prec_ref_center(RCCM)
    rccm_ref.move(center).movex(
        evaluate_bbox(input_stage_ref)[0] + 4 * pdk.util_max_metal_seperation()
    ).movey(+evaluate_bbox(input_stage_ref)[1] / 2)

    top_level.add(rccm_ref)
    top_level.add_ports(rccm_ref.get_ports_list(), prefix="rccm_")

    top_level << L_route(
        pdk, rccm_ref.ports["IN_top_met_W"], input_stage_ref.ports["OUT_D_top_met_N"]
    )

    # -------------------------------------------------------------------------
    # CREATING THE BIAS STAGE
    # -------------------------------------------------------------------------
    print("Creating Bias Stage ...")

    bias_stage_comp = bias_stage(
        pdk,
        add_labels=False,
    )
    bias_stage_ref = prec_ref_center(bias_stage_comp)
    # bias_stage_ref.move(center).movex(-evaluate_bbox(bias_stage_ref)[0]).movey(
    #     evaluate_bbox(bias_stage_ref)[1] / 2
    # )
    bias_stage_ref.move(center).movex(
        -3 * evaluate_bbox(input_stage_ref)[0] + 4 * pdk.util_max_metal_seperation()
    ).movey(+evaluate_bbox(input_stage_ref)[1] / 2)
    top_level.add(bias_stage_ref)
    top_level.add_ports(bias_stage_ref.get_ports_list(), prefix="bias_")

    # -------------------------------------------------------------------------
    # CONNECTING AUX
    # -------------------------------------------------------------------------
    viam1m2 = via_stack(pdk, "met1", "met2", centered=True)
    viam2m3 = via_stack(pdk, "met2", "met3", centered=True)
    # rccm_aux_via = top_level << viam1m2
    # rccm_aux_via.move(
    #     (
    #         top_level.ports["input_EN_A_top_met_N"].center[0],
    #         rccm_ref.ports["AUX_A_top_met_W"].center[1],
    #     )
    # )
    # top_level.add_ports(rccm_aux_via.get_ports_list(), prefix="AUX_")

    # top_level << straight_route(
    #     pdk,
    #     rccm_aux_via.ports["top_met_E"],
    #     rccm_ref.ports["AUX_A_top_met_W"],
    #     glayer1="met1",
    #     glayer2="met1",
    # )

    top_level << L_route(
        pdk, bias_stage_ref.ports["base_right_OUT_top_met_N"], rccm_ref.ports["AUX_A_top_met_W"], hglayer="met1", vglayer="met1",
    )

    en_via = top_level << viam1m2
    en_via.move(bias_stage_ref.ports["fet_right_multiplier_0_gate_E"].center).movex(evaluate_bbox(bias_stage_ref)[0])

    top_level << straight_route(
        pdk,
        bias_stage_ref.ports["fet_right_multiplier_0_gate_E"],
        en_via.ports["top_met_W"],
        glayer1="met2",
        glayer2="met2",
    )

    en_input_via = top_level << viam2m3
    en_input_via.move((input_stage_ref.ports["EN_A_top_met_N"].center[0], en_via.center[1]))

    top_level << straight_route(
        pdk,
        en_input_via.ports["top_met_S"],
        input_stage_ref.ports["EN_A_top_met_N"],
        glayer1="met3",
        glayer2="met3",
    )

    aux_via = top_level << viam1m2
    aux_via.move(en_via.center).movey(evaluate_bbox(rccm_ref)[1])

    top_level << L_route(
        pdk,
        bias_stage_ref.ports["base_left_IN_top_met_N"],
        aux_via.ports["top_met_W"],
    )

    # Outputs

    vcm_via = top_level << viam1m2
    vcm_via.move((en_via.center[0], vcm_ref.ports["OUT_top_met_W"].center[1]))

    top_level << straight_route(
        pdk,
        vcm_via.ports["top_met_W"],
        vcm_ref.ports["OUT_top_met_E"],
        glayer1="met2",
        glayer2="met2",
    )

    sbcm_via = top_level << viam1m2
    sbcm_via.move((en_via.center[0], sbcm_ref.ports["OUT_top_met_W"].center[1]))

    top_level << straight_route(
        pdk,
        sbcm_via.ports["top_met_W"],
        sbcm_ref.ports["OUT_top_met_E"],
        glayer1="met2",
        glayer2="met2",
    )

    rccm_via = top_level << viam1m2
    rccm_via.move((en_via.center[0], rccm_ref.ports["OUT_top_met_W"].center[1]))

    top_level << straight_route(
        pdk,
        rccm_via.ports["top_met_W"],
        rccm_ref.ports["OUT_top_met_E"],
        glayer1="met2",
        glayer2="met2",
    )

    # Input

    vin1_via = top_level << viam1m2
    vin1_via.move(input_stage_ref.ports["IN_A_top_met_N"].center).movey(-evaluate_bbox(sbcm_ref)[1])

    vin2_via = top_level << viam1m2
    vin2_via.move(vin1_via.center).movex(2*evaluate_bbox(input_stage_ref)[0])

    vin3_via = top_level << viam1m2
    vin3_via.move(aux_via.center).movey(evaluate_bbox(rccm_ref)[1])

    top_level << straight_route(
        pdk,
        input_stage_ref.ports["IN_A_top_met_S"],
        vin1_via.ports["top_met_N"],
        glayer1="met1",
        glayer2="met1",
    )

    top_level << straight_route(
        pdk,
        vin1_via.ports["top_met_E"],
        vin2_via.ports["top_met_W"],
        glayer1="met1",
        glayer2="met1",
    )

    top_level << L_route(
        pdk,
        vin2_via.ports["top_met_N"],
        vin3_via.ports["top_met_W"],
        hglayer="met1", vglayer="met1",
    )

    # VSS

    vss_via = top_level << viam1m2
    vss_via.move(vin3_via.center).movey(evaluate_bbox(rccm_ref)[1])

    top_level << L_route(
        pdk,
        vss_via.ports["top_met_W"],
        rccm_ref.ports["welltie_N_top_met_N"],
        hglayer="met1", vglayer="met1",
        vwidth=5, hwidth=5
    )

    vdd_via = top_level << viam1m2
    vdd_via.move(vss_via.center).movey(evaluate_bbox(rccm_ref)[1])

    top_level << L_route(
        pdk,
        vdd_via.ports["top_met_W"],
        bias_stage_ref.ports["fet_right_tie_N_top_met_N"],
        hglayer="met1", vglayer="met1",
        vwidth=5, hwidth=5
    )



    # -------------------------------------------------------------------------
    # CONNECTING VSS TOGETHER
    # -------------------------------------------------------------------------
    top_level << straight_route(
        pdk,
        top_level.ports["vcm_welltie_N_top_met_N"],
        top_level.ports["sbcm_welltie_S_top_met_S"],
        glayer1="met1",
        glayer2="met1",
        width=10,
    )
    top_level << straight_route(
        pdk,
        top_level.ports["sbcm_welltie_N_top_met_N"],
        top_level.ports["rccm_welltie_S_top_met_S"],
        glayer1="met1",
        glayer2="met1",
        width=10,
    )

    top_level = component_snap_to_grid(rename_ports_by_orientation(top_level))

    top_level.info["netlist"] = generate_top_netlist(
        prefix="TOP",
        in_net="VIN",
        aux_net="VAUX",
        en_net="EN",
        out_vcm_net="VOUT_VCM",
        out_sbcm_net="VOUT_SBCM",
        out_rccm_net="VOUT_RCCM",
        nl_input=input_stage_comp.info["netlist"],
        nl_vcm=VCM.info["netlist"],
        nl_sbcm=SBCM.info["netlist"],
        nl_rccm=RCCM.info["netlist"],
        show_netlist=show_netlist,
    )

    if add_labels:
        return add_cm_labels(top_level, pdk)
    return top_level


def add_cm_labels(cm_in: Component, pdk: MappedPDK) -> Component:
    cm_in.unlock()

    psize = (0.35, 0.35)
    move_info = []

    # VIN
    vinlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    vinlabel.add_label(text="VIN", layer=pdk.get_glayer("met2_label"))
    move_info.append((vinlabel, cm_in.ports["input_IN_A_top_met_N"], None))

    # EN
    vEnlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    vEnlabel.add_label(text="EN", layer=pdk.get_glayer("met2_label"))
    move_info.append((vEnlabel, cm_in.ports["input_EN_A_top_met_N"], None))

    # VAUX
    vauxlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    vauxlabel.add_label(text="VAUX", layer=pdk.get_glayer("met2_label"))
    move_info.append((vauxlabel, cm_in.ports["AUX_top_met_N"], None))

    # VOUT VCM
    voutvcmlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    voutvcmlabel.add_label(text="VOUT_VCM", layer=pdk.get_glayer("met2_label"))
    move_info.append((voutvcmlabel, cm_in.ports["vcm_OUT_top_met_N"], None))

    # VOUT SBCM
    voutsbcmlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    voutsbcmlabel.add_label(text="VOUT_SBCM", layer=pdk.get_glayer("met2_label"))
    move_info.append((voutsbcmlabel, cm_in.ports["sbcm_OUT_top_met_N"], None))

    # VOUT RCCM
    voutrccmlabel = rectangle(layer=pdk.get_glayer("met2_pin"), size=psize, centered=True).copy()
    voutrccmlabel.add_label(text="VOUT_RCCM", layer=pdk.get_glayer("met2_label"))
    move_info.append((voutrccmlabel, cm_in.ports["rccm_OUT_top_met_N"], None))

    # VDD (well tie)
    vddlabel = rectangle(layer=pdk.get_glayer("met1_pin"), size=psize, centered=True).copy()
    vddlabel.add_label(text="VDD", layer=pdk.get_glayer("met1_label"))
    move_info.append((vddlabel, cm_in.ports["input_welltie_N_top_met_N"], None))

    # VSS (well tie)
    vsslabel = rectangle(layer=pdk.get_glayer("met1_pin"), size=psize, centered=True).copy()
    vsslabel.add_label(text="VSS", layer=pdk.get_glayer("met1_label"))
    move_info.append((vsslabel, cm_in.ports["vcm_welltie_N_top_met_N"], None))

    for comp, prt, alignment in move_info:
        alignment = ("c", "b") if alignment is None else alignment
        compref = align_comp_to_port(comp, prt, alignment=alignment)
        cm_in.add(compref)

    return cm_in.flatten()


if __name__ == "__main__":
    selected_pdk = gf180

    comp = top(selected_pdk, show_netlist=False, add_labels=False)
    # comp.pprint_ports()
    comp.name = "TOP"
    comp.show()

    # Write the layout to GDS
    comp.write_gds("GDS/top.gds")

    # DRC
    drc_result = selected_pdk.drc_magic(comp, comp.name, output_file=Path("DRC/"))

    # LVS
    # netgen_lvs_result = selected_pdk.lvs_netgen(
    #     comp, comp.name, output_file_path=Path("LVS/"), copy_intermediate_files=True
    # )
