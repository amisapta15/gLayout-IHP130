v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
P 4 1 -1510 -170 {}
N -1550 -850 -1550 -820 {lab=#net1}
N -1510 -910 -1450 -910 {lab=#net1}
N -1450 -910 -1450 -850 {lab=#net1}
N -1550 -850 -1450 -850 {lab=#net1}
N -1550 -880 -1550 -850 {lab=#net1}
N -1510 -790 -1450 -790 {lab=#net2}
N -1450 -790 -1450 -720 {lab=#net2}
N -1550 -720 -1450 -720 {lab=#net2}
N -1550 -760 -1550 -720 {lab=#net2}
N -1550 -980 -1550 -940 {lab=VDD}
N -1460 -610 -1360 -610 {lab=#net2}
N -1550 -580 -1550 -510 {lab=GND}
N -1780 -510 -1550 -510 {lab=GND}
N -1320 -580 -1320 -510 {lab=GND}
N -1550 -510 -1320 -510 {lab=GND}
N -1550 -670 -1550 -640 {lab=#net2}
N -1550 -670 -1460 -670 {lab=#net2}
N -1550 -720 -1550 -670 {lab=#net2}
N -1460 -670 -1460 -610 {lab=#net2}
N -1510 -610 -1460 -610 {lab=#net2}
N -1320 -870 -1320 -810 {lab=#net3}
N -1320 -980 -1320 -930 {lab=VDD}
N -1550 -980 -1320 -980 {lab=VDD}
N -1320 -690 -1320 -640 {lab=#net4}
N -940 -900 -890 -900 {lab=#net5}
N -910 -780 -890 -780 {lab=VDD}
N -1280 -900 -1260 -900 {lab=#net5}
N -1260 -950 -1260 -900 {lab=#net5}
N -1260 -950 -940 -950 {lab=#net5}
N -1030 -900 -940 -900 {lab=#net5}
N -1280 -780 -1260 -780 {lab=VDD}
N -1260 -830 -1260 -780 {lab=VDD}
N -1260 -830 -990 -830 {lab=VDD}
N -990 -830 -990 -780 {lab=VDD}
N -1030 -780 -990 -780 {lab=VDD}
N -1320 -690 -1200 -690 {lab=#net4}
N -1320 -750 -1320 -690 {lab=#net4}
N -1160 -980 -1160 -720 {lab=VDD}
N -1320 -980 -1160 -980 {lab=VDD}
N -1070 -870 -1070 -810 {lab=#net6}
N -850 -870 -850 -810 {lab=#net7}
N -850 -980 -850 -930 {lab=VDD}
N -1070 -980 -850 -980 {lab=VDD}
N -1070 -980 -1070 -930 {lab=VDD}
N -1160 -980 -1070 -980 {lab=VDD}
N -1020 -600 -870 -600 {lab=#net8}
N -1070 -570 -1070 -510 {lab=GND}
N -1320 -510 -1070 -510 {lab=GND}
N -1070 -660 -1070 -630 {lab=#net8}
N -1160 -660 -1070 -660 {lab=#net8}
N -1070 -750 -1070 -660 {lab=#net8}
N -1020 -660 -1020 -600 {lab=#net8}
N -1030 -600 -1020 -600 {lab=#net8}
N -1070 -660 -1020 -660 {lab=#net8}
N -830 -680 -700 -680 {lab=vbp_casc}
N -830 -680 -830 -630 {lab=vbp_casc}
N -850 -740 -700 -740 {lab=vbp}
N -850 -750 -850 -740 {lab=vbp}
N -990 -680 -830 -680 {lab=vbp_casc}
N -940 -740 -850 -740 {lab=vbp}
N -940 -950 -940 -900 {lab=#net5}
N -730 -610 -700 -610 {lab=#net9}
N -830 -570 -830 -550 {lab=#net9}
N -830 -550 -730 -550 {lab=#net9}
N -730 -610 -730 -550 {lab=#net9}
N -700 -550 -700 -510 {lab=GND}
N -1070 -510 -700 -510 {lab=GND}
N -910 -830 -910 -780 {lab=VDD}
N -990 -780 -910 -780 {lab=VDD}
N -910 -830 -720 -830 {lab=VDD}
N -720 -980 -720 -830 {lab=VDD}
N -850 -980 -720 -980 {lab=VDD}
N -940 -900 -940 -870 {lab=#net5}
N -940 -810 -940 -740 {lab=vbp}
N -990 -780 -990 -770 {lab=VDD}
N -990 -710 -990 -680 {lab=vbp_casc}
N -720 -980 -420 -980 {lab=VDD}
N -420 -980 -420 -790 {lab=VDD}
N -1780 -980 -1780 -810 {lab=VDD}
N -1780 -510 -1780 -470 {lab=GND}
N -1780 -750 -1780 -510 {lab=GND}
N -1780 -980 -1550 -980 {lab=VDD}
N -420 -730 -420 -700 {lab=#net10}
N -420 -640 -420 -450 {lab=GND}
C {devices/title.sym} -1610 -70 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/code_shown.sym} -1080 -320 0 0 {name=NGSPICE only_toplevel=true 
value="
.options savecurrrents
.include trimmer.save
.param temp=27
.control
save all 
op
tran 50p 20n
write tran_neuron.raw
plot I(Vload)
.endc
"}
C {devices/code_shown.sym} -1760 -180 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib $::SG13G2_MODELS/cornerMOSlv.lib mos_tt
.lib $::SG13G2_MODELS/cornerRES.lib res_typ_stat
"}
C {sg13g2_pr/annotate_fet_params.sym} -1800 -370 0 0 {name=annot2 ref=MP1}
C {sg13g2_pr/sg13_lv_pmos.sym} -1530 -910 0 1 {name=MP1
l=8.0u
w=0.28u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1530 -790 0 1 {name=MP2
l=8.0u
w=0.28u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -1340 -610 0 0 {name=MN2
l=8.0u
w=0.28u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -1530 -610 0 1 {name=MN1
l=8.0u
w=0.28u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1300 -900 0 1 {name=MP3
l=2.0u
w=2.0u
ng=2
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1300 -780 0 1 {name=MP4
l=0.28u
w=2.0u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1050 -900 0 1 {name=MP5
l=2.0u
w=2.0u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1050 -780 0 1 {name=MP6
l=0.28u
w=2.0u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -870 -900 0 0 {name=MP7
l=2.0u
w=2.0u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -870 -780 0 0 {name=MP8
l=0.28u
w=2.0u
ng=1
m=2
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -1180 -690 0 0 {name=MP9
l=8.0u
w=0.28u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -1050 -600 0 1 {name=MN3
l=2.0u
w=2.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -850 -600 0 0 {name=MN4
l=2.0u
w=2.0u
ng=1
m=4
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/rppd.sym} -700 -710 0 0 {name=R1
w=0.5e-6
l=389e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rhigh.sym} -700 -580 0 0 {name=R2
w=0.5e-6
l=152.5e-6
model=rhigh
spiceprefix=X
b=0
m=1
}
C {lab_pin.sym} -940 -800 0 0 {name=p9 sig_type=std_logic lab=vbp}
C {lab_pin.sym} -990 -700 0 1 {name=p10 sig_type=std_logic lab=vbp_casc}
C {devices/ammeter.sym} -940 -840 0 0 {name=vbp}
C {devices/ammeter.sym} -990 -740 0 0 {name=vbp_casc}
C {devices/vsource.sym} -1780 -780 0 0 {name=Vdd value=1.8}
C {devices/gnd.sym} -1780 -470 0 0 {name=l1 lab=GND}
C {devices/gnd.sym} -420 -450 0 0 {name=l2 lab=GND}
C {lab_pin.sym} -1780 -980 2 1 {name=p1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1780 -510 2 1 {name=p4 sig_type=std_logic lab=GND}
C {lab_pin.sym} -1550 -610 2 1 {name=p3 sig_type=std_logic lab=GND}
C {lab_pin.sym} -1070 -600 2 1 {name=p5 sig_type=std_logic lab=GND}
C {lab_pin.sym} -1320 -610 0 1 {name=p6 sig_type=std_logic lab=GND}
C {lab_pin.sym} -830 -600 0 1 {name=p7 sig_type=std_logic lab=GND}
C {lab_pin.sym} -850 -900 0 1 {name=p8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1070 -900 2 1 {name=p12 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1070 -780 2 1 {name=p13 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1320 -900 2 1 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1320 -780 2 1 {name=p15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1550 -910 2 1 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1550 -790 2 1 {name=p17 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -850 -780 0 1 {name=p18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1160 -690 0 1 {name=p19 sig_type=std_logic lab=VDD}
C {devices/ammeter.sym} -420 -760 0 0 {name=vload}
C {capa.sym} -420 -670 0 0 {name=C1
m=1
value=0.5p
footprint=1206
device="ceramic capacitor"}
