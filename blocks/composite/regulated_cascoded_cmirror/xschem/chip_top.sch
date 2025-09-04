v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -510 -380 -510 -340 {lab=VDD}
N -510 -210 -510 -180 {lab=GND}
N -510 -280 -510 -270 {lab=#net1}
N -60 -110 50 -110 {lab=VSS}
N -20 -140 -20 -110 {lab=VSS}
N 50 -140 50 -110 {lab=VSS}
N -30 -300 40 -300 {lab=VDD}
N -0 -330 0 -300 {lab=VDD}
N -510 -190 -440 -190 {lab=GND}
N -440 -210 -440 -190 {lab=GND}
N -440 -410 -440 -270 {lab=ENABLE}
N 160 -260 580 -260 {lab=#net2}
N 160 -220 490 -220 {lab=#net3}
N 160 -180 410 -180 {lab=#net4}
N -440 -190 -350 -190 {lab=GND}
N -350 -210 -350 -190 {lab=GND}
N -350 -190 -290 -190 {lab=GND}
N -290 -210 -290 -190 {lab=GND}
N -290 -300 -290 -270 {lab=BIAS}
N -350 -290 -350 -270 {lab=IN}
N -160 -220 -140 -220 {lab=IN}
N -160 -180 -140 -180 {lab=BIAS}
C {iopin.sym} 1500 -270 0 0 {name=p182 lab=DVSS}
C {iopin.sym} 1500 -210 0 0 {name=p51 lab=VSS}
C {symbols/rm3.sym} 1500 -240 2 0 {name=R2
W=1e-6
L=1e-6
model=rm3
spiceprefix=X
m=1}
C {vsource.sym} 580 -170 0 0 {name=v_vanilla value=1.65 savecurrent=true}
C {gnd.sym} 580 -140 0 0 {name=l15 lab=GND}
C {vsource.sym} 490 -130 0 0 {name=v_biased value=1.65 savecurrent=true}
C {gnd.sym} 490 -100 0 0 {name=l4 lab=GND}
C {vsource.sym} 410 -90 0 0 {name=v_cascode value=1.65 savecurrent=true}
C {gnd.sym} 410 -60 0 0 {name=l5 lab=GND}
C {res.sym} 580 -230 0 0 {name=R3
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 490 -190 0 0 {name=R5
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 410 -150 0 0 {name=R6
value=50
footprint=1206
device=resistor
m=1}
C {vsource.sym} -510 -240 0 0 {name=V1 value=3.3 savecurrent=false}
C {gnd.sym} -510 -180 0 0 {name=l10 lab=GND}
C {res.sym} -510 -310 0 0 {name=R4
value=50
footprint=1206
device=resistor
m=1}
C {vdd.sym} -510 -380 0 0 {name=l8 lab=VDD}
C {devices/code_shown.sym} -900 150 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
.include /foss/designs/gLayout-mahowalders/blocks/composite/regulated_cascoded_cmirror/xschem/Chipathon2025_pads/xschem/gf180mcu_fd_io.spice
.include /foss/designs/gLayout-mahowalders/blocks/composite/regulated_cascoded_cmirror/xschem/Chipathon2025_pads/xschem/gf180mcu_fd_io__asig_5p0_extracted.spice
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice diode_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice res_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice moscap_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -900 -490 0 0 {name=code only_toplevel=false 
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
dc v_cascode 0 3.3 0.01 I_aux 1u 10u 100n
let i_cascode = -i(v_cascode)
wrdata cascode.txt i_cascode
write tb_ccm.raw
.endc
"
}
C {int_top_tb.sym} 10 -220 0 0 {name=x1}
C {lab_wire.sym} -510 -190 0 0 {name=p1 sig_type=std_logic lab=VSS}
C {lab_wire.sym} -60 -110 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {vdd.sym} 0 -330 0 0 {name=l1 lab=VDD}
C {vsource.sym} -440 -240 0 0 {name=V2 value=3.3 savecurrent=false}
C {lab_wire.sym} -440 -410 2 0 {name=p3 sig_type=std_logic lab=ENABLE}
C {lab_wire.sym} -140 -260 0 0 {name=p4 sig_type=std_logic lab=ENABLE}
C {isource.sym} -350 -240 0 0 {name=Iin value=10u}
C {isource.sym} -290 -240 0 0 {name=I_aux value=1u}
C {lab_wire.sym} -350 -290 0 0 {name=p5 sig_type=std_logic lab=IN}
C {lab_wire.sym} -290 -300 2 0 {name=p6 sig_type=std_logic lab=BIAS}
C {lab_wire.sym} -160 -220 0 0 {name=p7 sig_type=std_logic lab=IN}
C {lab_wire.sym} -160 -180 0 0 {name=p8 sig_type=std_logic lab=BIAS}
