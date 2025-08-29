v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 110 -200 110 -170 {lab=VDD}
N -30 -200 -30 -170 {lab=VDD}
N -30 -200 110 -200 {lab=VDD}
N 30 -140 70 -140 {lab=#net1}
N -30 30 -30 70 {lab=#net1}
N 110 -110 110 -30 {lab=#net2}
N 10 -140 30 -140 {lab=#net1}
N 50 0 70 0 {lab=IREF}
N -30 -110 -30 -30 {lab=#net3}
N 30 -140 30 70 {lab=#net1}
N -90 160 -90 190 {lab=IREF}
N -90 70 -90 90 {lab=#net1}
N -90 70 -30 70 {lab=#net1}
N -130 -200 -130 120 {lab=VDD}
N -130 -200 -30 -200 {lab=VDD}
N -30 70 30 70 {lab=#net1}
N -90 150 -90 160 {lab=IREF}
N 50 0 50 160 {lab=IREF}
N 10 0 50 0 {lab=IREF}
N -90 160 50 160 {lab=IREF}
N 110 30 110 180 {lab=ICOPY}
N -180 -200 -130 -200 {lab=VDD}
N -320 -190 -310 -190 {lab=VDD}
N -320 -160 -310 -160 {lab=GND}
C {sg13g2_pr/sg13_lv_pmos.sym} 90 -140 0 0 {name=M6
l=0.5u
w=15.0u
ng=5
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} -30 -140 0 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 110 -140 0 1 {name=p9 sig_type=std_logic lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} -10 -140 0 1 {name=M9
l=0.5u
w=15.0u
ng=5
m=10
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 90 0 0 0 {name=M1
l=0.5u
w=15.0u
ng=5
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} -30 0 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 110 0 0 1 {name=p2 sig_type=std_logic lab=VDD}
C {sg13g2_pr/sg13_lv_pmos.sym} -10 0 0 1 {name=M2
l=0.5u
w=15.0u
ng=5
m=10
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -110 120 0 0 {name=M23
l=0.5u
w=21.0u
ng=7
m=10
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} -90 120 0 1 {name=p4 sig_type=std_logic lab=GND}
C {iopin.sym} -320 -190 2 0 {name=p3 lab=VDD}
C {lab_pin.sym} -310 -190 2 0 {name=p5 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -180 -200 0 0 {name=p6 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -310 -160 0 1 {name=p7 sig_type=std_logic lab=GND}
C {iopin.sym} -320 -160 2 0 {name=p10 lab=GND}
C {iopin.sym} -90 190 2 0 {name=p11 lab=IREF}
C {iopin.sym} 110 180 2 0 {name=p12 lab=ICOPY}
