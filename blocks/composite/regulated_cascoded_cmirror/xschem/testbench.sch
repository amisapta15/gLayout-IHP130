v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 300 -950 300 -910 {lab=VDD}
N 300 -790 300 -760 {lab=GND}
N 590 -940 590 -880 {lab=VDD}
N 630 -850 670 -850 {lab=v_in}
N 590 -820 590 -780 {lab=v_in}
N 570 -850 590 -850 {lab=VDD}
N 570 -890 570 -850 {lab=VDD}
N 570 -890 590 -890 {lab=VDD}
N 650 -850 650 -800 {lab=v_in}
N 590 -800 650 -800 {lab=v_in}
N 590 -660 590 -620 {lab=GND}
N 1590 -840 1640 -840 {lab=#net1}
N 1590 -570 1640 -570 {lab=#net2}
N 1590 -290 1640 -290 {lab=#net3}
N 870 -930 870 -870 {lab=VDD}
N 910 -840 950 -840 {lab=v_aux}
N 870 -810 870 -770 {lab=v_aux}
N 850 -840 870 -840 {lab=VDD}
N 850 -880 850 -840 {lab=VDD}
N 850 -880 870 -880 {lab=VDD}
N 930 -840 930 -790 {lab=v_aux}
N 870 -790 930 -790 {lab=v_aux}
N 870 -660 870 -620 {lab=GND}
N 1030 -550 1290 -550 {lab=v_in}
N 1130 -820 1290 -820 {lab=v_in}
N 1130 -820 1130 -550 {lab=v_in}
N 1130 -550 1130 -270 {lab=v_in}
N 1130 -270 1290 -270 {lab=v_in}
N 1240 -900 1240 -290 {lab=VDD}
N 1240 -290 1290 -290 {lab=VDD}
N 1240 -570 1290 -570 {lab=VDD}
N 1240 -840 1290 -840 {lab=VDD}
N 1260 -800 1260 -160 {lab=GND}
N 1260 -800 1290 -800 {lab=GND}
N 1260 -530 1290 -530 {lab=GND}
N 1260 -250 1290 -250 {lab=GND}
C {title.sym} 160 -30 0 0 {name=l1 author="Quentin Halbach"}
C {devices/code_shown.sym} 20 -140 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical

"}
C {vsource.sym} 300 -820 0 0 {name=V1 value=3.3 savecurrent=false}
C {vdd.sym} 300 -950 0 0 {name=l9 lab=VDD}
C {gnd.sym} 300 -760 0 0 {name=l10 lab=GND}
C {symbols/pfet_03v3.sym} 610 -850 0 1 {name=M7
L=1u
W=5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {isource.sym} 590 -750 0 0 {name=I_in value=1u}
C {lab_wire.sym} 670 -850 2 0 {name=p1 sig_type=std_logic lab=v_in}
C {vdd.sym} 590 -940 0 0 {name=l12 lab=VDD}
C {gnd.sym} 590 -620 0 0 {name=l11 lab=GND}
C {vanilla_cm.sym} 1250 -670 0 0 {name=x1}
C {vsource.sym} 1640 -750 0 0 {name=v_vanilla value=1.65 savecurrent=true}
C {gnd.sym} 1640 -720 0 0 {name=l15 lab=GND}
C {code_shown.sym} 20 -780 0 0 {name=code only_toplevel=false value=
"
.option savecurrent

.control

save all

* --- Run vanilla sweep ---
dc v_vanilla 0 3.3 0.01
let i_vanilla = -i(v_vanilla)
wrdata vanilla.txt i_vanilla

* --- Run biased sweep ---
reset
dc v_biased 0 3.3 0.01
let i_biased = -i(v_biased)
wrdata biased.txt i_biased

* --- Run cascode sweep ---
reset
dc v_cascode 0 3.3 0.01
let i_cascode = -i(v_cascode)
wrdata cascode.txt i_cascode

.endc
"
}
C {biased_cm.sym} 1270 -330 0 0 {name=x2}
C {lab_wire.sym} 1030 -550 0 0 {name=p3 sig_type=std_logic lab=v_in}
C {vdd.sym} 1240 -900 0 0 {name=l2 lab=VDD}
C {gnd.sym} 1260 -160 0 0 {name=l3 lab=GND}
C {vsource.sym} 1640 -480 0 0 {name=v_biased value=1.65 savecurrent=true}
C {gnd.sym} 1640 -450 0 0 {name=l4 lab=GND}
C {cascode_cm.sym} 1260 -10 0 0 {name=x3}
C {lab_wire.sym} 1440 -360 0 0 {name=p5 sig_type=std_logic lab=v_aux}
C {vsource.sym} 1640 -200 0 0 {name=v_cascode value=1.65 savecurrent=true}
C {gnd.sym} 1640 -170 0 0 {name=l5 lab=GND}
C {symbols/pfet_03v3.sym} 890 -840 0 1 {name=M1
L=1u
W=5u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=pfet_03v3
spiceprefix=X
}
C {isource.sym} 870 -740 0 0 {name=I_aux value=1n}
C {lab_wire.sym} 950 -840 2 0 {name=p6 sig_type=std_logic lab=v_aux}
C {vdd.sym} 870 -930 0 0 {name=l14 lab=VDD}
C {gnd.sym} 870 -620 0 0 {name=l16 lab=GND}
C {res.sym} 300 -880 0 0 {name=R4
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 590 -690 0 0 {name=R1
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 870 -680 0 0 {name=R2
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1640 -810 0 0 {name=R3
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1640 -540 0 0 {name=R5
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1640 -260 0 0 {name=R6
value=50
footprint=1206
device=resistor
m=1}
