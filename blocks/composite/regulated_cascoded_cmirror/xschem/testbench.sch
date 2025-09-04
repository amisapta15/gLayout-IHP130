v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 420 -660 420 -620 {lab=VDD}
N 420 -490 420 -460 {lab=GND}
N 710 -490 710 -450 {lab=GND}
N 1070 -440 1070 -410 {lab=GND}
N 1270 -620 1400 -620 {lab=#net1}
N 1400 -630 1400 -620 {lab=#net1}
N 1270 -600 1400 -600 {lab=#net2}
N 1400 -600 1400 -540 {lab=#net2}
N 1270 -580 1370 -580 {lab=#net3}
N 1370 -580 1370 -440 {lab=#net3}
N 1370 -440 1400 -440 {lab=#net3}
N 590 -540 590 -500 {lab=GND}
N 500 -640 830 -640 {lab=VDD}
N 1070 -450 1070 -440 {lab=GND}
N 420 -560 420 -550 {lab=#net4}
N 1070 -700 1070 -670 {lab=VDD}
N 590 -600 830 -600 {lab=#net5}
N 710 -550 830 -550 {lab=#net6}
C {title.sym} 160 -30 0 0 {name=l1 author="Quentin Halbach"}
C {devices/code_shown.sym} 20 -140 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
*.include Chipathon2025_pads/xschem/gf180mcu_fd_io.spice
*.include Chipathon2025_pads/xschem/gf180mcu_fd_io__asig_5p0_extracted.spice
"}
C {vsource.sym} 420 -520 0 0 {name=V1 value=3.3 savecurrent=false}
C {gnd.sym} 420 -460 0 0 {name=l10 lab=GND}
C {isource.sym} 590 -570 0 0 {name=I_in value=1u}
C {vsource.sym} 1490 -630 3 0 {name=v_vanilla value=1.65 savecurrent=true}
C {gnd.sym} 1520 -630 3 0 {name=l15 lab=GND}
C {code_shown.sym} 20 -780 0 0 {name=code only_toplevel=false 
value="
.options savecurrents
.param temp=27
.control
set wr_singlescale
set noaskquit
*set appendwrite
set hcopypscolor=1

save all
op
write tb_vcm.raw
* --- Run vanilla sweep ---
dc v_vanilla 0 3.3 0.01
let i_vanilla = -i(v_vanilla)
wrdata vanilla.txt i_vanilla
write tb_vcm.raw
* --- Run biased sweep ---
reset
write tb_bcm.raw
dc v_biased 0 3.3 0.01
let i_biased = -i(v_biased)
wrdata biased.txt i_biased
write tb_bcm.raw
* --- Run cascode sweep ---
reset
write tb_ccm.raw
dc v_cascode 0 3.3 0.01 I_aux 1n 100n 10n
let i_cascode = -i(v_cascode)
wrdata cascode.txt i_cascode
write tb_ccm.raw
.endc
"
}
C {gnd.sym} 1070 -410 0 0 {name=l3 lab=GND}
C {vsource.sym} 1490 -540 3 0 {name=v_biased value=1.65 savecurrent=true}
C {gnd.sym} 1520 -540 3 0 {name=l4 lab=GND}
C {vsource.sym} 1490 -440 3 0 {name=v_cascode value=1.65 savecurrent=true}
C {gnd.sym} 1520 -440 3 0 {name=l5 lab=GND}
C {isource.sym} 710 -520 0 0 {name=I_aux value=1n}
C {gnd.sym} 710 -450 0 0 {name=l16 lab=GND}
C {res.sym} 420 -590 0 0 {name=R4
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1430 -630 3 0 {name=R3
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1430 -540 3 0 {name=R5
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 1430 -440 3 0 {name=R6
value=50
footprint=1206
device=resistor
m=1}
C {gnd.sym} 590 -500 0 0 {name=l2 lab=GND}
C {vdd.sym} 1070 -700 0 0 {name=l6 lab=VDD}
C {vdd.sym} 420 -660 0 0 {name=l8 lab=VDD}
C {top_level.sym} 1070 -560 0 0 {name=x1}
C {vdd.sym} 500 -640 0 0 {name=l7 lab=VDD}
