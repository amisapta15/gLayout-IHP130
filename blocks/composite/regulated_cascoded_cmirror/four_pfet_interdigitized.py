# four_transistor_interdigitized.py
from __future__ import annotations

from typing import Literal, Optional, Union

from pydantic import validate_arguments
from gdsfactory.component import Component
from gdsfactory.functions import transformed

from glayout.pdk.mappedpdk import MappedPDK
from glayout.util.comp_utils import evaluate_bbox, prec_ref_center
from glayout.util.port_utils import add_ports_perimeter
from glayout.routing.straight_route import straight_route
from glayout.primitives.guardring import tapring
from glayout.spice.netlist import Netlist
from gdsfactory.components import rectangle as gf_rectangle

# ---------------------------------------------------------------------------
# If macro_two_transistor_interdigitized lives elsewhere, update this import:
# from your_module import macro_two_transistor_interdigitized
from glayout.placement.two_transistor_interdigitized import macro_two_transistor_interdigitized
# ---------------------------------------------------------------------------


# -------------------------
# Netlist (4T interdigitized)
# -------------------------
def four_tran_interdigitized_netlist(
    pdk: MappedPDK,
    width: float | None,
    length: float | None,
    fingers: int,
    multipliers: int,
    with_dummy: bool,
    n_or_p_fet: Literal["nfet", "pfet"] = "nfet",
) -> Netlist:
    """Build a flat subckt with XA/XB/XC/XD. Nodes:
       VDD1..4, VSS1..4, VG1..4, VB
    """
    if length is None:
        length = pdk.get_grule("poly")["min_width"]
    if width is None:
        width = 3

    model = pdk.models[n_or_p_fet]
    mtop = fingers * multipliers

    src = (
        """.subckt {circuit_name} {nodes} """
        f"l={length} w={width} m={1}\n"
        f"XA VDD1 VG1 VSS1 VB {model} l={length} w={width} m={mtop}\n"
        f"XB VDD2 VG2 VSS2 VB {model} l={length} w={width} m={mtop}\n"
        f"XC VDD3 VG3 VSS3 VB {model} l={length} w={width} m={mtop}\n"
        f"XD VDD4 VG4 VSS4 VB {model} l={length} w={width} m={mtop}\n"
    )
    if with_dummy:
        src += f"XDUMMY VB VB VB VB {model} l={length} w={width} m={2}\n"
    src += ".ends {circuit_name}"

    return Netlist(
        circuit_name="four_trans_interdigitized",
        nodes=[
            "VDD1", "VDD2", "VDD3", "VDD4",
            "VSS1", "VSS2", "VSS3", "VSS4",
            "VG1",  "VG2",  "VG3",  "VG4",
            "VB",
        ],
        source_netlist=src,
        instance_format="X{name} {nodes} {circuit_name} l={length} w={width} m={1}",
        parameters={
            "model": model,
            "width": width,
            "length": length,
            "mult": multipliers,
        },
    )


# -------------------------
# Geometry/placement (4T)
# -------------------------
@validate_arguments
def macro_four_transistor_interdigitized(
    pdk: MappedPDK,
    numcols: int,
    deviceA_B_C_D: Literal["nfet", "pfet"],
    dummy: Union[bool, tuple[bool, bool]] = True,
    *,
    # rails config
    bus_layer: str = "met2",        # metal for long rails
    spur_layer: str = "met2",       # metal for short device-to-rail spur
    add_gate_stitch: bool = False,  # if True, stitch A_gate↔C_gate and B_gate↔D_gate across the row
    **kwargs,
) -> Component:
    """
    Build a *single-row* 4T interdigitized block by composing two 2T rows:
      - Left  block → A/B interdigitized (from macro_two_transistor_interdigitized)
      - Right block → C/D interdigitized (renamed from A/B of the second row)

    Then create 8 continuous rails (A_S, A_D, B_S, B_D, C_S, C_D, D_S, D_D)
    spanning the full width. Each rail connects ONLY to its designated terminal
    via a short spur → no shorts between devices.
    """
    # Build two 2-T rows with your proven macro (AB and CD)
    ab = macro_two_transistor_interdigitized(pdk, numcols, deviceA_B_C_D, dummy, **kwargs)
    cd = macro_two_transistor_interdigitized(pdk, numcols, deviceA_B_C_D, dummy, **kwargs)

    top = Component()

    # Place AB at origin
    ab_ref = top << ab

    # Place CD to the right with PDK-aware spacing
    gap = pdk.util_max_metal_seperation()
    dx = pdk.snap_to_2xgrid(evaluate_bbox(ab)[0] + gap + evaluate_bbox(cd)[0] / 2)
    cd_ref = top << cd
    cd_ref.movex(dx)

    # Bring AB ports directly
    for pname, port in ab_ref.ports.items():
        top.add_port(name=pname, port=port)

    # Bring CD ports with A_/B_ -> C_/D_ renames
    def _copy_ports_with_rename(from_ref, prefix_map):
        for pname, port in from_ref.ports.items():
            for old, new in prefix_map:
                if pname.startswith(old):
                    top.add_port(name=pname.replace(old, new, 1), port=port)
                    break

    _copy_ports_with_rename(cd_ref, [("A_", "C_"), ("B_", "D_")])

    # Optional: stitch gates across blocks (keeps 8 S/D rails independent)
    if add_gate_stitch:
        for (l_name, r_name) in [("A_gate_E", "A_gate_W"), ("B_gate_E", "B_gate_W")]:
            if l_name in ab_ref.ports and r_name in cd_ref.ports:
                try:
                    top << straight_route(pdk, ab_ref.ports[l_name], cd_ref.ports[r_name], glayer2="poly")
                except Exception:
                    pass

    # -----------------------------
    # 8 independent S/D rails spanning the row (no cross-shorts)
    # -----------------------------
    track_pitch = pdk.util_max_metal_seperation()     # vertical spacing between rails
    rail_margin = pdk.util_max_metal_seperation()     # horizontal margin beyond blocks
    anchor_w = pdk.snap_to_2xgrid(0.3)
    anchor_h = pdk.snap_to_2xgrid(0.3)

    # Compute left/right x extents for rails' anchors
    x_left = ab_ref.xmin - rail_margin
    x_right = cd_ref.xmax + rail_margin

    # Tiny anchor with a port on bus_layer
    def _anchor_comp() -> Component:
        c = Component()
        r = c << gf_rectangle(size=(anchor_w, anchor_h), layer=pdk.get_glayer(bus_layer), centered=True)
        c.add_port(
            name="P",
            center=(0, 0),
            width=anchor_h,
            layer=pdk.get_glayer(bus_layer),
            orientation=180,
        )
        return c

    # Net list: (public bus prefix, edge to use on device, side for the spur anchor)
    # Left block uses W ports; Right block uses E ports (adjust if your 2-T macro differs)
    nets = [
        ("A_source", "W", "left"),
        ("A_drain",  "W", "left"),
        ("B_source", "W", "left"),
        ("B_drain",  "W", "left"),
        ("C_source", "E", "right"),
        ("C_drain",  "E", "right"),
        ("D_source", "E", "right"),
        ("D_drain",  "E", "right"),
    ]

    # Place rails on distinct vertical tracks centered around the row
    y0 = (ab_ref.ymin + ab_ref.ymax) / 2.0
    start_track = -(len(nets) // 2) * track_pitch + (0.5 * track_pitch if len(nets) % 2 == 0 else 0)

    for idx, (bus_prefix, edge, side) in enumerate(nets):
        y_track = pdk.snap_to_2xgrid(y0 + start_track + idx * track_pitch)

        # Anchors at left and right ends of the rail
        anc_left = top << _anchor_comp()
        anc_right = top << _anchor_comp()
        anc_left.movex(x_left);  anc_left.movey(y_track)
        anc_right.movex(x_right); anc_right.movey(y_track)

        # Long rail spanning the row (left ↔ right)
        try:
            top << straight_route(pdk, anc_left.ports["P"], anc_right.ports["P"], glayer2=bus_layer)
        except Exception:
            pass

        # Connect ONLY the intended device terminal to the nearest anchor (short spur)
        cref = ab_ref if bus_prefix.startswith(("A_", "B_")) else cd_ref
        dev_port = f"{bus_prefix}_{edge}"
        near_anchor = anc_left if side == "left" else anc_right

        if dev_port in cref.ports:
            try:
                top << straight_route(pdk, cref.ports[dev_port], near_anchor.ports["P"], glayer2=spur_layer)
            except Exception:
                # fallback: try the opposite anchor if geometry prevents near connection
                far_anchor = anc_right if near_anchor is anc_left else anc_left
                try:
                    top << straight_route(pdk, cref.ports[dev_port], far_anchor.ports["P"], glayer2=spur_layer)
                except Exception:
                    pass

    # Return a Component (not a CRef) so we can add more later if needed
    top = transformed(prec_ref_center(top))
    top.unlock()
    return top


# -------------------------
# Wrappers (nfet / pfet)
# -------------------------
@validate_arguments
def four_nfet_interdigitized(
    pdk: MappedPDK,
    numcols: int,
    dummy: Union[bool, tuple[bool, bool]] = True,
    with_substrate_tap: bool = True,
    with_tie: bool = True,
    tie_layers: tuple[str, str] = ("met2", "met1"),
    **kwargs,
) -> Component:
    base = macro_four_transistor_interdigitized(pdk, numcols, "nfet", dummy, **kwargs)

    # Optional tie ring (like your 2-T builder)
    if with_tie:
        tap_sep = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_sep += pdk.get_grule("p+s/d", "active_tap")["min_enclosure"]
        encloses = (2 * (tap_sep + base.xmax), 2 * (tap_sep + base.ymax))
        ring = tapring(
            pdk,
            enclosed_rectangle=encloses,
            sdlayer="p+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )
        ring_ref = base << ring
        base.add_ports(ring_ref.get_ports_list(), prefix="welltie_")

    # pwell pad + perimeter ports
    base.add_padding(
        layers=(pdk.get_glayer("pwell"),),
        default=pdk.get_grule("pwell", "active_tap")["min_enclosure"],
    )
    base = add_ports_perimeter(base, layer=pdk.get_glayer("pwell"), prefix="well_")

    # Optional substrate tap ring
    if with_substrate_tap:
        sep = pdk.get_grule("dnwell", "active_tap")["min_separation"]
        encloses = (2 * (sep + base.xmax), 2 * (sep + base.ymax))
        ring = tapring(
            pdk,
            enclosed_rectangle=encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
        ref = base << ring
        base.add_ports(ref.get_ports_list(), prefix="substratetap_")

    base.info["route_genid"] = "four_transistor_interdigitized"
    base.info["netlist"] = four_tran_interdigitized_netlist(
        pdk,
        width=kwargs.get("width", 3),
        length=kwargs.get("length", 0.15),
        fingers=kwargs.get("fingers", 1),
        multipliers=numcols,
        with_dummy=bool(dummy) if isinstance(dummy, bool) else any(dummy),
        n_or_p_fet="nfet",
    )
    return base


@validate_arguments
def four_pfet_interdigitized(
    pdk: MappedPDK,
    numcols: int,
    dummy: Union[bool, tuple[bool, bool]] = True,
    with_substrate_tap: bool = True,
    with_tie: bool = True,
    tie_layers: tuple[str, str] = ("met2", "met1"),
    **kwargs,
) -> Component:
    base = macro_four_transistor_interdigitized(pdk, numcols, "pfet", dummy, **kwargs)

    if with_tie:
        tap_sep = max(
            pdk.util_max_metal_seperation(),
            pdk.get_grule("active_diff", "active_tap")["min_separation"],
        )
        tap_sep += pdk.get_grule("n+s/d", "active_tap")["min_enclosure"]
        encloses = (2 * (tap_sep + base.xmax), 2 * (tap_sep + base.ymax))
        ring = tapring(
            pdk,
            enclosed_rectangle=encloses,
            sdlayer="n+s/d",
            horizontal_glayer=tie_layers[0],
            vertical_glayer=tie_layers[1],
        )
        ring_ref = base << ring
        base.add_ports(ring_ref.get_ports_list(), prefix="welltie_")

    # nwell pad + perimeter ports
    base.add_padding(
        layers=(pdk.get_glayer("nwell"),),
        default=pdk.get_grule("nwell", "active_tap")["min_enclosure"],
    )
    base = add_ports_perimeter(base, layer=pdk.get_glayer("nwell"), prefix="well_")

    if with_substrate_tap:
        sep = pdk.get_grule("dnwell", "active_tap")["min_separation"]
        encloses = (2 * (sep + base.xmax), 2 * (sep + base.ymax))
        ring = tapring(
            pdk,
            enclosed_rectangle=encloses,
            sdlayer="p+s/d",
            horizontal_glayer="met2",
            vertical_glayer="met1",
        )
        ref = base << ring
        base.add_ports(ref.get_ports_list(), prefix="substratetap_")

    base.info["route_genid"] = "four_transistor_interdigitized"
    base.info["netlist"] = four_tran_interdigitized_netlist(
        pdk,
        width=kwargs.get("width", 3),
        length=kwargs.get("length", 0.15),
        fingers=kwargs.get("fingers", 1),
        multipliers=numcols,
        with_dummy=bool(dummy) if isinstance(dummy, bool) else any(dummy),
        n_or_p_fet="pfet",
    )
    return base