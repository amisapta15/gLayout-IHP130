v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 660 -640 990 -640 {lab=ENA}
N 1230 -450 1230 -440 {lab=VSS}
N 1230 -700 1230 -670 {lab=VDD}
N 750 -600 990 -600 {lab=VIN_INT}
N 870 -550 990 -550 {lab=VBIAS_INT}
N 320 -1200 420 -1200 {lab=ENA}
N 320 -1180 500 -1180 {lab=#net1}
N 380 -1150 640 -1150 {lab=#net2}
N 380 -1160 380 -1150 {lab=#net2}
N 320 -1160 380 -1160 {lab=#net2}
N 570 -1160 570 -1120 {lab=VSS}
N 710 -1020 710 -1000 {lab=VSS}
N 710 -1200 710 -1170 {lab=VDD}
N 570 -1330 570 -1310 {lab=VDD}
N 1230 -440 1230 -420 {lab=VSS}
N -110 -870 50 -870 {lab=VIN}
N -100 -620 60 -620 {lab=VBIAS}
N 250 -870 380 -870 {lab=VIN_INT}
N 260 -620 370 -620 {lab=VBIAS_INT}
N -120 -1200 60 -1200 {lab=EN}
N 1040 -1220 1080 -1220 {lab=VCM_OUT_INT}
N 1070 -960 1110 -960 {lab=BCM_OUT_INT}
N 1440 -810 1470 -810 {lab=CCM_OUT_INT}
N 1430 -620 1520 -620 {lab=VCM_OUT_INT}
N 1520 -640 1520 -620 {lab=VCM_OUT_INT}
N 1520 -640 1590 -640 {lab=VCM_OUT_INT}
N 1430 -600 1590 -600 {lab=BCM_OUT_INT}
N 1430 -580 1520 -580 {lab=CCM_OUT_INT}
N 1520 -580 1520 -560 {lab=CCM_OUT_INT}
N 1520 -560 1590 -560 {lab=CCM_OUT_INT}
N 1280 -1220 1770 -1220 {lab=VCM_OUT}
N 1670 -810 1790 -810 {lab=BCM_OUT}
N 1310 -960 1770 -960 {lab=CCM_OUT}
N 1160 -1320 1160 -1300 {lab=VDD}
N 1200 -1320 1200 -1300 {lab=DVDD}
N 1160 -1140 1160 -1120 {lab=VSS}
N 1200 -1140 1200 -1120 {lab=DVSS}
N 1190 -1070 1190 -1040 {lab=VDD}
N 1230 -1070 1230 -1040 {lab=DVDD}
N 1190 -880 1190 -870 {lab=VSS}
N 1230 -880 1230 -870 {lab=DVSS}
N 1550 -920 1550 -890 {lab=VDD}
N 1590 -920 1590 -890 {lab=DVDD}
N 1590 -730 1590 -710 {lab=DVSS}
N 1550 -730 1550 -710 {lab=VSS}
N 620 -840 700 -840 {lab=DVDD}
N 620 -780 700 -780 {lab=VDD}
N 880 -840 970 -840 {lab=DVSS}
N 880 -780 970 -780 {lab=VSS}
C {title.sym} 190 -90 0 0 {name=l1 author="Quentin Halbach and Sapta"}
C {top_level.sym} 1230 -560 0 0 {name=x1}
C {lab_pin.sym} 140 -1280 0 0 {name=p105 lab=DVDD}
C {lab_pin.sym} 140 -1120 0 0 {name=p106 lab=DVSS}
C {lab_pin.sym} 180 -1280 0 1 {name=p109 lab=VDD}
C {lab_pin.sym} 180 -1120 0 1 {name=p110 lab=VSS}
C {ipin.sym} -120 -1200 0 0 {name=p120 lab=EN}
C {lab_pin.sym} 710 -1200 2 1 {name=p108 lab=VDD}
C {lab_pin.sym} 570 -1330 2 1 {name=p111 lab=VDD}
C {lab_pin.sym} 710 -1000 2 1 {name=p164 lab=VSS}
C {iopin.sym} 700 -780 0 0 {name=p92 lab=VDD}
C {iopin.sym} 700 -840 0 0 {name=p181 lab=DVDD}
C {symbols/rm3.sym} 700 -810 2 0 {name=R1
W=1e-6
L=1e-6
model=rm3
spiceprefix=X
m=1}
C {iopin.sym} 970 -840 0 0 {name=p182 lab=DVSS}
C {iopin.sym} 970 -780 0 0 {name=p51 lab=VSS}
C {symbols/rm3.sym} 970 -810 2 0 {name=R2
W=1e-6
L=1e-6
model=rm3
spiceprefix=X
m=1}
C {Chipathon2025_pads/xschem/io_in_c.sym} 60 -1120 0 0 {name=IO6
model=gf180mcu_fd_io__in_c
spiceprefix=X
}
C {Chipathon2025_pads/xschem/tieH.sym} 710 -1070 0 0 {name=x2}
C {Chipathon2025_pads/xschem/tieL.sym} 570 -1230 0 0 {name=x3}
C {lab_pin.sym} 420 -1200 0 1 {name=p1 lab=ENA}
C {lab_pin.sym} 570 -1120 2 1 {name=p2 lab=VSS}
C {lab_pin.sym} 1230 -700 2 1 {name=p3 lab=VDD}
C {lab_pin.sym} 1230 -420 2 1 {name=p4 lab=VSS}
C {lab_pin.sym} 660 -640 2 1 {name=p5 lab=ENA}
C {ipin.sym} -110 -870 0 0 {name=p6 lab=VIN}
C {ipin.sym} -100 -620 0 0 {name=p7 lab=VBIAS}
C {lab_pin.sym} 380 -870 0 1 {name=p8 lab=VIN_INT}
C {lab_pin.sym} 370 -620 0 1 {name=p9 lab=VBIAS_INT}
C {lab_pin.sym} 750 -600 2 1 {name=p10 lab=VIN_INT}
C {lab_pin.sym} 870 -550 2 1 {name=p11 lab=VBIAS_INT}
C {lab_pin.sym} 130 -790 0 0 {name=p12 lab=DVSS}
C {lab_pin.sym} 140 -540 0 0 {name=p13 lab=DVSS}
C {lab_pin.sym} 170 -790 0 1 {name=p14 lab=VSS}
C {lab_pin.sym} 180 -540 0 1 {name=p15 lab=VSS}
C {lab_pin.sym} 130 -950 0 0 {name=p16 lab=DVDD}
C {lab_pin.sym} 140 -700 0 0 {name=p17 lab=DVDD}
C {lab_pin.sym} 170 -950 0 1 {name=p18 lab=VDD}
C {lab_pin.sym} 180 -700 0 1 {name=p19 lab=VDD}
C {lab_pin.sym} 1070 -960 2 1 {name=p21 lab=BCM_OUT_INT}
C {lab_pin.sym} 1040 -1220 2 1 {name=p22 lab=VCM_OUT_INT}
C {lab_pin.sym} 1440 -810 2 1 {name=p23 lab=CCM_OUT_INT}
C {opin.sym} 1770 -1220 0 0 {name=p24 lab=VCM_OUT}
C {lab_pin.sym} 1590 -600 0 1 {name=p25 lab=BCM_OUT_INT}
C {lab_pin.sym} 1590 -640 0 1 {name=p26 lab=VCM_OUT_INT}
C {lab_pin.sym} 1590 -560 0 1 {name=p27 lab=CCM_OUT_INT}
C {opin.sym} 1790 -810 0 0 {name=p20 lab=BCM_OUT}
C {opin.sym} 1770 -960 0 0 {name=p28 lab=CCM_OUT}
C {lab_pin.sym} 1190 -1070 2 1 {name=p29 lab=VDD}
C {lab_pin.sym} 1160 -1320 2 1 {name=p30 lab=VDD}
C {lab_pin.sym} 1550 -920 2 1 {name=p31 lab=VDD}
C {lab_pin.sym} 1160 -1120 2 1 {name=p32 lab=VSS}
C {lab_pin.sym} 1190 -870 2 1 {name=p33 lab=VSS}
C {lab_pin.sym} 1550 -710 2 1 {name=p34 lab=VSS}
C {lab_pin.sym} 1200 -1320 2 0 {name=p35 lab=DVDD}
C {lab_pin.sym} 1230 -1070 2 0 {name=p36 lab=DVDD}
C {lab_pin.sym} 1590 -920 2 0 {name=p37 lab=DVDD}
C {lab_pin.sym} 1590 -710 2 0 {name=p38 lab=DVSS}
C {lab_pin.sym} 1230 -870 2 0 {name=p39 lab=DVSS}
C {lab_pin.sym} 1200 -1120 2 0 {name=p40 lab=DVSS}
C {lab_pin.sym} 620 -780 2 1 {name=p41 lab=VDD}
C {lab_pin.sym} 620 -840 0 0 {name=p42 lab=DVDD}
C {lab_pin.sym} 880 -780 2 1 {name=p43 lab=VSS}
C {lab_pin.sym} 880 -840 0 0 {name=p44 lab=DVSS}
C {Chipathon2025_pads/xschem/io_asig_5p0.sym} 50 -790 0 0 {name=IO1
model=gf180mcu_fd_io__asig_5p0_extracted
spiceprefix=X
}
C {Chipathon2025_pads/xschem/io_asig_5p0.sym} 60 -540 0 0 {name=IO2
model=gf180mcu_fd_io__asig_5p0_extracted
spiceprefix=X
}
C {Chipathon2025_pads/xschem/io_asig_5p0.sym} 1080 -1140 0 0 {name=IO3
model=gf180mcu_fd_io__asig_5p0_extracted
spiceprefix=X
}
C {Chipathon2025_pads/xschem/io_asig_5p0.sym} 1110 -880 0 0 {name=IO4
model=gf180mcu_fd_io__asig_5p0_extracted
spiceprefix=X
}
C {Chipathon2025_pads/xschem/io_asig_5p0.sym} 1470 -730 0 0 {name=IO5
model=gf180mcu_fd_io__asig_5p0_extracted
spiceprefix=X
}
