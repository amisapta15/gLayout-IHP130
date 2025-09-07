v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -70 -320 -70 -280 {lab=VDD}
N 420 -320 420 -280 {lab=VDD}
N 150 -320 150 -200 {lab=VDD}
N 150 -140 150 -80 {lab=#net1}
N 70 -170 110 -170 {lab=#net1}
N 70 -170 70 -110 {lab=#net1}
N 70 -110 150 -110 {lab=#net1}
N -70 -220 -70 -0 {lab=#net2}
N -70 -0 150 0 {lab=#net2}
N 150 -20 150 0 {lab=#net2}
N 70 -50 110 -50 {lab=#net2}
N 70 -50 70 0 {lab=#net2}
N 380 -40 570 -40 {lab=bias_P}
N 420 -220 420 -40 {lab=bias_P}
N 340 -320 340 -70 {lab=VDD}
N 600 140 600 250 {lab=bias_N}
N 600 140 610 140 {lab=bias_N}
N 610 -10 610 140 {lab=bias_N}
N 340 -10 340 250 {lab=bias_P}
N 340 30 420 30 {lab=bias_P}
N 420 -40 420 30 {lab=bias_P}
N 380 280 560 280 {lab=bias_N}
N 600 310 600 420 {lab=VGND}
N 340 310 340 410 {lab=VGND}
N 340 410 340 420 {lab=VGND}
N 460 280 460 310 {lab=bias_N}
N 460 370 460 420 {lab=VGND}
N 170 280 230 280 {lab=bias_N}
N 230 210 230 280 {lab=bias_N}
N 230 210 450 210 {lab=bias_N}
N 450 210 450 280 {lab=bias_N}
N 540 140 540 280 {lab=bias_N}
N 540 140 600 140 {lab=bias_N}
N 130 310 130 420 {lab=VGND}
N 130 0 130 250 {lab=#net2}
N -110 130 -110 160 {lab=bias_P}
N -110 130 340 130 {lab=bias_P}
N -70 190 130 190 {lab=#net2}
N -110 220 -110 290 {lab=#net3}
N -110 350 -110 420 {lab=VGND}
N 610 -180 610 -70 {lab=#net4}
N 610 -320 610 -240 {lab=VDD}
N -300 -320 600 -320 {lab=VDD}
N 600 -320 610 -320 {lab=VDD}
N -190 320 -150 320 {lab=en}
N -250 -250 -110 -250 {lab=en}
N 400 340 420 340 {lab=enN}
N -290 420 600 420 {lab=VGND}
N -360 100 -240 100 {lab=GND}
N -300 100 -300 110 {lab=GND}
N -360 -110 -360 -50 {lab=VDD}
N -240 -120 -240 -50 {lab=en}
N -360 10 -360 40 {lab=VGND}
N -240 10 -240 40 {lab=enN}
N 370 -250 380 -250 {lab=en}
N 610 -320 1050 -320 {lab=VDD}
N 1050 -320 1050 -280 {lab=VDD}
N 800 -320 800 -280 {lab=VDD}
N 840 -250 1010 -250 {lab=#net5}
N 800 -220 800 -50 {lab=#net5}
N 1050 -220 1050 -40 {lab=#net6}
N 1230 -200 1230 -40 {lab=#net7}
N 1050 -320 1230 -320 {lab=VDD}
N 1230 -320 1230 -260 {lab=VDD}
N 1060 90 1120 90 {lab=#net8}
N 900 -250 900 -160 {lab=#net5}
N 800 -160 900 -160 {lab=#net5}
N 800 10 800 90 {lab=bias_P}
N 840 -20 1010 -20 {lab=bias_P}
N 800 40 890 40 {lab=bias_P}
N 890 -20 890 40 {lab=bias_P}
N 1230 -30 1230 90 {lab=#net7}
N 1230 -40 1230 -30 {lab=#net7}
N 1050 10 1050 90 {lab=#net8}
N 1050 90 1060 90 {lab=#net8}
N 1180 90 1230 90 {lab=#net7}
C {symbols/pfet_03v3.sym} -90 -250 0 0 {name=M2
L=0.3u
W=3.0u
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
C {symbols/pfet_03v3.sym} 130 -170 0 0 {name=M3
L=0.30u
W=10.0u
nf=4
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
C {symbols/pfet_03v3.sym} 130 -50 0 0 {name=M4
L=0.30u
W=10.0u
nf=4
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
C {symbols/pfet_03v3.sym} 400 -250 0 0 {name=M5
L=0.3u
W=3.0u
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
C {symbols/pfet_03v3.sym} 360 -40 0 1 {name=M6
L=0.3u
W=10.0u
nf=2
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
C {symbols/pfet_03v3.sym} 590 -40 0 0 {name=M7
L=0.3u
W=0.6u
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
C {symbols/nfet_03v3.sym} 360 280 0 1 {name=M8
L=0.3u
W=0.6u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 580 280 0 0 {name=M9
L=0.3u
W=0.6u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 440 340 0 0 {name=M1
L=0.3u
W=2.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} 150 280 0 1 {name=M10
L=0.3u
W=12.0u
nf=4
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} -130 320 0 0 {name=M11
L=0.3u
W=3.0u
nf=1
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/nfet_03v3.sym} -90 190 0 1 {name=M12
L=0.3u
W=12.0u
nf=4
m=1
ad="'int((nf+1)/2) * W/nf * 0.18u'"
pd="'2*int((nf+1)/2) * (W/nf + 0.18u)'"
as="'int((nf+2)/2) * W/nf * 0.18u'"
ps="'2*int((nf+2)/2) * (W/nf + 0.18u)'"
nrd="'0.18u / W'" nrs="'0.18u / W'"
sa=0 sb=0 sd=0
model=nfet_03v3
spiceprefix=X
}
C {symbols/ppolyf_u_1k.sym} 610 -210 0 0 {name=R1
W=10e-6
L=10e-6
model=ppolyf_u_1k
spiceprefix=X
m=22}
C {lab_wire.sym} -300 -320 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -290 420 0 0 {name=p2 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} -250 -250 0 0 {name=p3 sig_type=std_logic lab=en}
C {lab_wire.sym} -190 320 0 0 {name=p5 sig_type=std_logic lab=en}
C {lab_wire.sym} 370 -250 0 0 {name=p6 sig_type=std_logic lab=en}
C {lab_wire.sym} 400 340 0 0 {name=p4 sig_type=std_logic lab=enN}
C {lab_wire.sym} 340 180 0 0 {name=p7 sig_type=std_logic lab=bias_P}
C {lab_wire.sym} 610 110 0 0 {name=p8 sig_type=std_logic lab=bias_N}
C {vsource.sym} -360 -20 0 0 {name=V1 value=3 savecurrent=false}
C {vsource.sym} -360 70 0 0 {name=V2 value=0}
C {vsource.sym} -240 -20 0 0 {name=V3 value=3 savecurrent=false}
C {vsource.sym} -240 70 0 0 {name=V4 value=0}
C {gnd.sym} -300 110 0 0 {name=l1 lab=GND}
C {lab_wire.sym} -240 -120 0 0 {name=p9 sig_type=std_logic lab=en}
C {lab_wire.sym} -240 30 0 0 {name=p10 sig_type=std_logic lab=enN}
C {lab_wire.sym} -360 -110 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -360 30 0 0 {name=p12 sig_type=std_logic lab=VGND
}
C {devices/code_shown.sym} -250 520 0 0 {name=MODELS only_toplevel=true
format="tcleval( @value )"
value="
*.include /foss/designs/gLayout-mahowalders/blocks/composite/regulated_cascoded_cmirror/xschem/Chipathon2025_pads/xschem/gf180mcu_fd_io.spice
*.include /foss/designs/gLayout-mahowalders/blocks/composite/regulated_cascoded_cmirror/xschem/Chipathon2025_pads/xschem/gf180mcu_fd_io__asig_5p0_extracted.spice
.include /foss/pdks/gf180mcuD/libs.tech/ngspice/design.ngspice
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice diode_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice res_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice moscap_typical
.lib /foss/pdks/gf180mcuD/libs.tech/ngspice/sm141064.ngspice mimcap_typical
"}
C {code_shown.sym} -660 0 0 0 {name=code only_toplevel=false 
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

dc Vload 0 3.3 0.1
plot Vmeas#branch
.endc

"
}
C {lab_wire.sym} -70 -250 2 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 420 -250 2 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 150 -170 2 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 150 -50 2 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 340 -40 0 0 {name=p17 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 610 -40 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 590 -210 0 0 {name=p19 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} -110 190 0 0 {name=p20 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} -110 320 2 0 {name=p21 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} 130 280 0 0 {name=p22 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} 340 280 0 0 {name=p23 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} 460 340 2 0 {name=p24 sig_type=std_logic lab=VGND
}
C {lab_wire.sym} 600 280 2 0 {name=p25 sig_type=std_logic lab=VGND
}
C {symbols/pfet_03v3.sym} 1030 -250 0 0 {name=M13
L=0.3u
W=0.6u
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
C {symbols/pfet_03v3.sym} 820 -250 0 1 {name=M14
L=0.3u
W=0.6u
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
C {lab_wire.sym} 800 90 2 0 {name=p26 sig_type=std_logic lab=bias_P}
C {vsource.sym} 1230 -230 0 0 {name=Vload value=0}
C {lab_wire.sym} 800 -250 0 0 {name=p27 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1050 -250 2 0 {name=p28 sig_type=std_logic lab=VDD}
C {ammeter.sym} 1150 90 3 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {symbols/pfet_03v3.sym} 1030 -20 0 0 {name=M15
L=0.3u
W=0.6u
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
C {symbols/pfet_03v3.sym} 820 -20 0 1 {name=M16
L=0.3u
W=0.6u
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
C {lab_wire.sym} 1050 -20 2 0 {name=p29 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 800 -20 0 0 {name=p30 sig_type=std_logic lab=VDD}
