v {xschem version=3.4.7 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -20 -910 0 -910 {lab=VDD}
N 510 -910 510 -740 {lab=VDD}
N 740 -910 740 -740 {lab=VDD}
N 630 -910 630 -850 {lab=VDD}
N 550 -710 700 -710 {lab=#net1}
N 630 -790 630 -710 {lab=#net1}
N 550 -590 700 -590 {lab=V_IN}
N 510 -680 510 -620 {lab=#net1}
N 740 -680 740 -620 {lab=#net2}
N 630 -710 630 -650 {lab=#net1}
N 510 -650 630 -650 {lab=#net1}
N 1010 -910 1010 -740 {lab=VDD}
N 870 -910 870 -850 {lab=VDD}
N 1120 -910 1120 -850 {lab=VDD}
N 740 -560 740 -470 {lab=#net3}
N 980 -470 2020 -470 {lab=V_OUT_VCM}
N 1010 -560 1010 -340 {lab=#net4}
N 1250 -340 2030 -340 {lab=V_OUT_BCM}
N 1350 -560 1350 -240 {lab=#net5}
N 1350 -910 1350 -740 {lab=VDD}
N 1350 -680 1350 -620 {lab=#net6}
N 630 -760 1310 -760 {lab=#net1}
N 1310 -760 1310 -710 {lab=#net1}
N 910 -710 970 -710 {lab=#net1}
N 910 -760 910 -710 {lab=#net1}
N 1010 -680 1010 -620 {lab=#net7}
N 870 -790 870 -760 {lab=#net1}
N 1120 -790 1120 -760 {lab=#net1}
N 1080 -880 1080 -820 {lab=EN}
N -20 -880 1080 -880 {lab=EN}
N 550 -820 590 -820 {lab=EN}
N 550 -880 550 -820 {lab=EN}
N 790 -820 830 -820 {lab=EN}
N 790 -880 790 -820 {lab=EN}
N 1310 -650 1310 -590 {lab=V_IN}
N 660 -650 660 -590 {lab=V_IN}
N 660 -650 1310 -650 {lab=V_IN}
N 920 -590 970 -590 {lab=V_IN}
N 920 -650 920 -590 {lab=V_IN}
N 1590 -240 2040 -240 {lab=V_OUT_CCM}
N 170 -340 170 -280 {lab=#net8}
N 620 -200 1350 -200 {lab=#net9}
N 210 -250 350 -250 {lab=V_AUX_CCM}
N 210 -370 350 -370 {lab=#net8}
N 390 -340 390 -280 {lab=#net10}
N 170 -310 260 -310 {lab=#net8}
N 260 -250 260 -190 {lab=V_AUX_CCM}
N 280 -390 280 -370 {lab=#net8}
N 280 -370 280 -320 {lab=#net8}
N 280 -320 280 -310 {lab=#net8}
N 260 -310 280 -310 {lab=#net8}
N 170 -470 170 -400 {lab=VDD}
N 280 -470 280 -450 {lab=VDD}
N 390 -470 390 -400 {lab=VDD}
N 210 -420 240 -420 {lab=EN}
N 210 -880 210 -420 {lab=EN}
N -20 -190 260 -190 {lab=V_AUX_CCM}
N 170 -220 170 -190 {lab=V_AUX_CCM}
N 390 -200 620 -200 {lab=#net9}
N 390 -220 390 -200 {lab=#net9}
N 1120 -910 1350 -910 {lab=VDD}
N 1010 -910 1120 -910 {lab=VDD}
N 870 -910 1010 -910 {lab=VDD}
N 740 -910 870 -910 {lab=VDD}
N 630 -910 740 -910 {lab=VDD}
N 510 -910 630 -910 {lab=VDD}
N 160 -910 510 -910 {lab=VDD}
N -30 -70 1470 -70 {lab=VSS}
N 1470 -150 1470 -70 {lab=VSS}
N 1130 -250 1130 -70 {lab=VSS}
N 860 -380 860 -70 {lab=VSS}
N -20 -520 510 -520 {lab=V_IN}
N 510 -520 630 -520 {lab=V_IN}
N 630 -590 630 -520 {lab=V_IN}
N 510 -560 510 -520 {lab=V_IN}
C {iopin.sym} -30 -70 2 0 {name=p1 lab=VSS
}
C {ipin.sym} -20 -190 0 0 {name=p3 lab=V_AUX_CCM
}
C {iopin.sym} -20 -910 2 0 {name=p4 lab=VDD
}
C {opin.sym} 2020 -470 0 0 {name=p5 lab=V_OUT_VCM}
C {opin.sym} 2030 -340 0 0 {name=p6 lab=V_OUT_BCM}
C {opin.sym} 2040 -240 0 0 {name=p7 lab=V_OUT_CCM}
C {ipin.sym} -20 -520 0 0 {name=p9 lab=V_IN
}
C {symbols/pfet_03v3.sym} 530 -710 0 1 {name=M1
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 530 -590 0 1 {name=M2
L=2.0u
W=60.0u
nf=15
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
C {symbols/pfet_03v3.sym} 720 -710 0 0 {name=M3
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 720 -590 0 0 {name=M4
L=2.0u
W=60.0u
nf=15
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
C {symbols/pfet_03v3.sym} 990 -710 0 0 {name=M5
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 990 -590 0 0 {name=M6
L=2.0u
W=60.0u
nf=15
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
C {symbols/pfet_03v3.sym} 1330 -710 0 0 {name=M7
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 1330 -590 0 0 {name=M8
L=2.0u
W=60.0u
nf=15
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
C {symbols/pfet_03v3.sym} 190 -370 0 1 {name=M11
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 190 -250 0 1 {name=M12
L=2.0u
W=60.0u
nf=15
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
C {symbols/pfet_03v3.sym} 850 -820 0 0 {name=M14
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 610 -820 0 0 {name=M18
L=2.0u
W=40.0u
nf=10
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
C {lab_pin.sym} 0 -910 2 0 {name=p10 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 160 -910 0 0 {name=p11 sig_type=std_logic lab=VDD}
C {ipin.sym} -20 -880 0 0 {name=p12 lab=EN
}
C {symbols/pfet_03v3.sym} 1100 -820 0 0 {name=M15
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 260 -420 0 0 {name=M16
L=2.0u
W=40.0u
nf=10
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
C {lab_pin.sym} 630 -820 2 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 870 -820 2 0 {name=p8 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1120 -820 2 0 {name=p13 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1010 -710 2 0 {name=p14 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 740 -710 2 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 510 -710 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 510 -590 0 0 {name=p17 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 740 -590 2 0 {name=p18 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1010 -590 2 0 {name=p19 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1350 -710 2 0 {name=p20 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 1350 -590 2 0 {name=p21 sig_type=std_logic lab=VDD}
C {symbols/pfet_03v3.sym} 370 -370 0 0 {name=M17
L=2.0u
W=40.0u
nf=10
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
C {symbols/pfet_03v3.sym} 370 -250 0 0 {name=M19
L=2.0u
W=60.0u
nf=15
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
C {lab_pin.sym} 280 -470 0 0 {name=p22 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 170 -470 0 0 {name=p23 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 390 -470 0 0 {name=p24 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 170 -370 0 0 {name=p25 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 170 -250 0 0 {name=p26 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 390 -370 2 0 {name=p27 sig_type=std_logic lab=VDD}
C {lab_pin.sym} 390 -250 2 0 {name=p28 sig_type=std_logic lab=VDD}
C {vanilla_cm.sym} 860 -430 0 0 {name=x1}
C {biased_cm.sym} 1130 -300 0 0 {name=x2}
C {cascode_cm.sym} 1470 -200 0 0 {name=x3}
C {lab_pin.sym} 280 -420 2 0 {name=p29 sig_type=std_logic lab=VDD}
