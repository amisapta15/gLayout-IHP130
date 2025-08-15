v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 900 -470 900 -430 {lab=VDD_3V3}
N 900 -310 900 -280 {lab=GND}
N 1050 -550 1050 -490 {lab=VDD_3V3}
N 1090 -460 1130 -460 {lab=V_IN}
N 1050 -430 1050 -390 {lab=V_IN}
N 1030 -460 1050 -460 {lab=VDD_3V3}
N 1030 -500 1030 -460 {lab=VDD_3V3}
N 1030 -500 1050 -500 {lab=VDD_3V3}
N 1110 -460 1110 -410 {lab=V_IN}
N 1050 -410 1110 -410 {lab=V_IN}
N 1050 -270 1050 -230 {lab=GND}
N 1280 -540 1280 -480 {lab=VDD_3V3}
N 1320 -450 1360 -450 {lab=V_AUX}
N 1280 -420 1280 -380 {lab=V_AUX}
N 1260 -450 1280 -450 {lab=VDD_3V3}
N 1260 -490 1260 -450 {lab=VDD_3V3}
N 1260 -490 1280 -490 {lab=VDD_3V3}
N 1340 -450 1340 -400 {lab=V_AUX}
N 1280 -400 1340 -400 {lab=V_AUX}
N 1280 -270 1280 -230 {lab=GND}
N 1520 -370 1550 -370 {lab=VDD_3V3}
N 1550 -190 1550 -160 {lab=GND}
N 2000 -350 2130 -350 {lab=#net1}
N 2130 -360 2130 -350 {lab=#net1}
N 2000 -330 2130 -330 {lab=#net2}
N 2130 -330 2130 -270 {lab=#net2}
N 2000 -310 2100 -310 {lab=#net3}
N 2100 -310 2100 -170 {lab=#net3}
N 2100 -170 2130 -170 {lab=#net3}
N 1520 -350 1550 -350 {lab=V_IN}
N 1520 -310 1550 -310 {lab=V_IN}
N 1450 -330 1550 -330 {lab=V_IN}
N 1510 -250 1550 -250 {lab=V_AUX}
N 1520 -330 1520 -310 {lab=V_IN}
N 1520 -350 1520 -330 {lab=V_IN}
C {title.sym} 160 -30 0 0 {name=l1 author="Quentin Halbach"}
C {devices/code_shown.sym} 20 -140 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical

"}
C {vsource.sym} 900 -340 0 0 {name=V1 value=3.3 savecurrent=false}
C {gnd.sym} 900 -280 0 0 {name=l10 lab=GND}
C {symbols/pfet_03v3.sym} 1070 -460 0 1 {name=M7
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
C {isource.sym} 1050 -360 0 0 {name=I_in value=1u}
C {lab_wire.sym} 1130 -460 2 0 {name=p1 sig_type=std_logic lab=V_IN}
C {gnd.sym} 1050 -230 0 0 {name=l11 lab=GND}
C {vsource.sym} 2220 -360 3 0 {name=v_vanilla value=1.65 savecurrent=true}
C {gnd.sym} 2250 -360 3 0 {name=l15 lab=GND}
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
C {lab_wire.sym} 1450 -330 0 0 {name=p3 sig_type=std_logic lab=V_IN}
C {gnd.sym} 1550 -160 0 0 {name=l3 lab=GND}
C {vsource.sym} 2220 -270 3 0 {name=v_biased value=1.65 savecurrent=true}
C {gnd.sym} 2250 -270 3 0 {name=l4 lab=GND}
C {vsource.sym} 2220 -170 3 0 {name=v_cascode value=1.65 savecurrent=true}
C {gnd.sym} 2250 -170 3 0 {name=l5 lab=GND}
C {symbols/pfet_03v3.sym} 1300 -450 0 1 {name=M1
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
C {isource.sym} 1280 -350 0 0 {name=I_aux value=1n}
C {lab_wire.sym} 1360 -450 2 0 {name=p6 sig_type=std_logic lab=V_AUX}
C {gnd.sym} 1280 -230 0 0 {name=l16 lab=GND}
C {res.sym} 900 -400 0 0 {name=R4
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1050 -300 0 0 {name=R1
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1280 -290 0 0 {name=R2
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 2160 -360 3 0 {name=R3
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 2160 -270 3 0 {name=R5
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 2160 -170 3 0 {name=R6
value=50
footprint=1206
device=resistor
m=1}
C {top_level.sym} 1370 -90 0 0 {name=x1}
C {lab_wire.sym} 1510 -250 0 0 {name=p4 sig_type=std_logic lab=V_AUX}
C {lab_wire.sym} 900 -470 1 0 {name=p5 sig_type=std_logic lab=VDD_3V3}
C {lab_wire.sym} 1050 -550 1 0 {name=p7 sig_type=std_logic lab=VDD_3V3}
C {lab_wire.sym} 1280 -540 1 0 {name=p8 sig_type=std_logic lab=VDD_3V3}
C {lab_wire.sym} 1520 -370 0 0 {name=p2 sig_type=std_logic lab=VDD_3V3}
