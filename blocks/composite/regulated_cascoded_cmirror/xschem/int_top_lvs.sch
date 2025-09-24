v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 640 -410 970 -410 {lab=ENA}
N 1210 -220 1210 -210 {lab=VSS}
N 1210 -470 1210 -440 {lab=VDD}
N 730 -370 970 -370 {lab=VIN_INT}
N 850 -320 970 -320 {lab=VBIAS_INT}
N 320 -1180 500 -1180 {lab=#net1}
N 590 -1130 850 -1130 {lab=#net2}
N 380 -1160 380 -1150 {lab=#net2}
N 320 -1160 380 -1160 {lab=#net2}
N 780 -1140 780 -1100 {lab=VSS}
N 920 -1000 920 -980 {lab=VSS}
N 920 -1180 920 -1150 {lab=VDD}
N 780 -1310 780 -1290 {lab=VDD}
N 1210 -210 1210 -190 {lab=VSS}
N -110 -870 50 -870 {lab=VIN}
N -100 -620 60 -620 {lab=VBIAS}
N 250 -870 380 -870 {lab=VIN}
N 260 -620 370 -620 {lab=VBIAS}
N -120 -1200 60 -1200 {lab=EN}
N 1410 -390 1500 -390 {lab=VCM_OUT}
N 1500 -410 1500 -390 {lab=VCM_OUT}
N 1500 -410 1570 -410 {lab=VCM_OUT}
N 1410 -370 1570 -370 {lab=BCM_OUT}
N 1410 -350 1500 -350 {lab=CCM_OUT}
N 1500 -350 1500 -330 {lab=CCM_OUT}
N 1500 -330 1570 -330 {lab=CCM_OUT}
N 10 -340 90 -340 {lab=DVDD}
N 10 -280 90 -280 {lab=VDD}
N 270 -340 360 -340 {lab=DVSS}
N 270 -280 360 -280 {lab=VSS}
N 380 -1290 380 -1200 {lab=#net3}
N 580 -1290 610 -1290 {lab=ENA}
N 320 -1200 380 -1200 {lab=#net3}
N 500 -1160 710 -1160 {lab=#net1}
N 500 -1180 500 -1160 {lab=#net1}
N 380 -1130 590 -1130 {lab=#net2}
N 380 -1150 380 -1130 {lab=#net2}
N 1410 -410 1480 -410 {lab=VIN_OUT}
N 1480 -440 1480 -410 {lab=VIN_OUT}
N 1480 -440 1570 -440 {lab=VIN_OUT}
N 60 -620 260 -620 {lab=VBIAS}
N 50 -870 250 -870 {lab=VIN}
C {title.sym} 190 -90 0 0 {name=l1 author="Quentin Halbach and Sapta"}
C {lab_pin.sym} 140 -1280 0 0 {name=p105 lab=DVDD}
C {lab_pin.sym} 140 -1120 0 0 {name=p106 lab=DVSS}
C {lab_pin.sym} 180 -1280 0 1 {name=p109 lab=VDD}
C {lab_pin.sym} 180 -1120 0 1 {name=p110 lab=VSS}
C {ipin.sym} -120 -1200 0 0 {name=p120 lab=EN}
C {lab_pin.sym} 920 -1180 2 1 {name=p108 lab=VDD}
C {lab_pin.sym} 780 -1310 2 1 {name=p111 lab=VDD}
C {lab_pin.sym} 920 -980 2 1 {name=p164 lab=VSS}
C {iopin.sym} 90 -280 0 0 {name=p92 lab=VDD}
C {iopin.sym} 90 -340 0 0 {name=p181 lab=DVDD}
C {symbols/rm3.sym} 90 -310 2 0 {name=R1
W=1e-6
L=1e-6
model=rm3
spiceprefix=X
m=1}
C {iopin.sym} 360 -340 0 0 {name=p182 lab=DVSS}
C {iopin.sym} 360 -280 0 0 {name=p51 lab=VSS}
C {symbols/rm3.sym} 360 -310 2 0 {name=R2
W=1e-6
L=1e-6
model=rm3
spiceprefix=X
m=1}
C {Chipathon2025_pads/xschem/io_in_c.sym} 60 -1120 0 0 {name=IO6
model=gf180mcu_fd_io__in_c
spiceprefix=X
}
C {Chipathon2025_pads/xschem/tieH.sym} 920 -1050 0 0 {name=x2}
C {Chipathon2025_pads/xschem/tieL.sym} 780 -1210 0 0 {name=x3}
C {lab_pin.sym} 610 -1290 0 1 {name=p1 lab=ENA}
C {lab_pin.sym} 780 -1100 2 1 {name=p2 lab=VSS}
C {lab_pin.sym} 1210 -470 2 1 {name=p3 lab=VDD}
C {lab_pin.sym} 1210 -190 2 1 {name=p4 lab=VSS}
C {lab_pin.sym} 640 -410 2 1 {name=p5 lab=ENA}
C {ipin.sym} -110 -870 0 0 {name=p6 lab=VIN}
C {ipin.sym} -100 -620 0 0 {name=p7 lab=VBIAS}
C {lab_pin.sym} 580 -870 0 1 {name=p8 lab=VIN_INT}
C {lab_pin.sym} 570 -620 0 1 {name=p9 lab=VBIAS_INT}
C {lab_pin.sym} 730 -370 2 1 {name=p10 lab=VIN_INT}
C {lab_pin.sym} 850 -320 2 1 {name=p11 lab=VBIAS_INT}
C {opin.sym} 1570 -410 0 0 {name=p24 lab=VCM_OUT}
C {opin.sym} 1570 -370 0 0 {name=p20 lab=BCM_OUT}
C {opin.sym} 1570 -330 0 0 {name=p28 lab=CCM_OUT}
C {lab_pin.sym} 10 -280 2 1 {name=p41 lab=VDD}
C {lab_pin.sym} 10 -340 0 0 {name=p42 lab=DVDD}
C {lab_pin.sym} 270 -280 2 1 {name=p43 lab=VSS}
C {lab_pin.sym} 270 -340 0 0 {name=p44 lab=DVSS}
C {lab_pin.sym} 500 -950 2 1 {name=p45 lab=VDD}
C {lab_pin.sym} 500 -790 2 1 {name=p46 lab=VSS}
C {lab_pin.sym} 490 -700 2 1 {name=p47 lab=VDD}
C {lab_pin.sym} 490 -540 2 1 {name=p48 lab=VSS}
C {Chipathon2025_pads/xschem/symbols/io_secondary_5p0/io_secondary_5p0.sym} 580 -790 0 1 {name=IO9
spiceprefix=X
}
C {Chipathon2025_pads/xschem/symbols/io_secondary_5p0/io_secondary_5p0.sym} 570 -540 0 1 {name=IO7
spiceprefix=X
}
C {Chipathon2025_pads/xschem/symbols/io_secondary_5p0/io_secondary_5p0.sym} 580 -1210 0 1 {name=IO8
spiceprefix=X
}
C {lab_pin.sym} 500 -1370 2 1 {name=p49 lab=VDD}
C {lab_pin.sym} 500 -1210 2 1 {name=p50 lab=VSS}
C {gLayout-mahowalders/blocks/composite/regulated_cascoded_cmirror/xschem/top_level.sym} 1210 -330 0 0 {name=x1}
C {opin.sym} 1570 -440 0 0 {name=p54 lab=VIN_OUT}
