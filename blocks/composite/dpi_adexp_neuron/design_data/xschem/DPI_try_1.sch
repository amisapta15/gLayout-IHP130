v {xschem version=3.4.8RC file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 330 -680 890 -380 {flags=graph
y1=-1.2e-05
y2=-6.5e-08
ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=-0.061603875
x2=-0.027826877
divx=5
subdivx=1
node=i(vd)
color=4
dataset=-1
unitx=1
logx=0
logy=0
sim_type=dc
autoload=1}
T {Ctrl-Click to execute launcher} 470 -360 0 0 0.3 0.3 {layer=11}
T {.save file can be created with IHP->"Create FET and BIP .save file"} 470 -240 0 0 0.3 0.3 {layer=11}
N -950 -490 -950 -450 {lab=GND}
N -700 -600 -700 -560 {lab=#net1}
N -950 -600 -950 -550 {lab=#net1}
N -660 -530 -590 -530 {lab=#net2}
N -590 -530 -590 -470 {lab=#net2}
N -700 -470 -590 -470 {lab=#net2}
N -700 -500 -700 -470 {lab=#net2}
N -750 -170 -750 -120 {lab=GND}
N -930 -170 -930 -120 {lab=GND}
N -930 -120 -750 -120 {lab=GND}
N -750 -290 -750 -230 {lab=#net3}
N -750 -290 -700 -290 {lab=#net3}
N -860 -200 -790 -200 {lab=#net4}
N -930 -260 -930 -230 {lab=#net4}
N -860 -260 -860 -200 {lab=#net4}
N -890 -200 -860 -200 {lab=#net4}
N -930 -260 -860 -260 {lab=#net4}
N -930 -340 -930 -260 {lab=#net4}
N -1020 -760 -880 -760 {lab=#net5}
N -840 -600 -700 -600 {lab=#net1}
N -840 -730 -840 -700 {lab=#net6}
N -840 -640 -840 -600 {lab=#net1}
N -950 -600 -840 -600 {lab=#net1}
N -700 -350 -700 -290 {lab=#net3}
N -700 -470 -700 -410 {lab=#net2}
N -1080 -800 -1080 -790 {lab=VDD}
N -840 -800 -840 -790 {lab=VDD}
N -1080 -700 -1080 -680 {lab=#net5}
N -1020 -760 -1020 -700 {lab=#net5}
N -1040 -760 -1020 -760 {lab=#net5}
N -1080 -700 -1020 -700 {lab=#net5}
N -1080 -730 -1080 -700 {lab=#net5}
N -1150 -760 -1080 -760 {lab=VDD}
N -1150 -800 -1150 -760 {lab=VDD}
N -1150 -800 -1080 -800 {lab=VDD}
N -1080 -820 -1080 -800 {lab=VDD}
N -840 -760 -760 -760 {lab=VDD}
N -840 -800 -760 -800 {lab=VDD}
N -840 -810 -840 -800 {lab=VDD}
N -760 -800 -760 -760 {lab=VDD}
N -1030 -520 -990 -520 {lab=#net7}
N -1110 -520 -1090 -520 {lab=#net8}
N -1170 -570 -1170 -550 {lab=#net8}
N -1110 -570 -1110 -520 {lab=#net8}
N -1130 -520 -1110 -520 {lab=#net8}
N -1170 -570 -1110 -570 {lab=#net8}
N -1170 -600 -1170 -570 {lab=#net8}
N -1170 -490 -1170 -480 {lab=GND}
N -1280 -520 -1170 -520 {lab=GND}
N -1280 -520 -1280 -480 {lab=GND}
N -1280 -480 -1170 -480 {lab=GND}
N -1170 -480 -1170 -470 {lab=GND}
C {devices/title.sym} 250 550 0 0 {name=l5 author="Copyright 2023 IHP PDK Authors"}
C {devices/launcher.sym} 530 -290 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {devices/launcher.sym} 530 -260 0 0 {name=h2
descr="Load waves" 
tclcommand="
xschem raw_read $netlist_dir/[file rootname [file tail [xschem get current_name]]].raw dc
xschem setprop rect 2 0 fullxzoom
"
}
C {launcher.sym} 530 -320 0 0 {name=h3
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {devices/code_shown.sym} -1170 80 0 0 {name=NGSPICE only_toplevel=true 
value="
.options savecurrrents
.include DPI_try_1.save
.param temp=27
.control
save all 
op
write DPI_try_1.raw
set appendwrite
*dc Vds 0 1.2 0.01 Vgs 0.3 1.0 0.1
*dc Vgs 0 0.5 0.05
dc vds 0 -1.2 -0.01 Vgs -0.35 -1.1 -0.05
write DPI_try_1.raw
.endc
"}
C {devices/code_shown.sym} -1480 110 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_tt
"}
C {sg13g2_pr/annotate_fet_params.sym} -580 70 0 0 {name=annot2 ref=M3}
C {devices/vsource.sym} -1780 -650 0 0 {name=Vgs value=-0.75}
C {devices/ammeter.sym} -1630 -680 1 0 {name=Vd}
C {devices/gnd.sym} -1860 -540 0 0 {name=l1 lab=GND}
C {sg13g2_pr/sg13_lv_pmos.sym} -970 -520 0 0 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -680 -530 0 1 {name=M2
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} -1520 -570 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_pin.sym} -1540 -520 0 0 {name=p2 sig_type=std_logic lab=VTh}
C {devices/gnd.sym} -950 -450 0 0 {name=l2 lab=GND}
C {sg13g2_pr/sg13_lv_nmos.sym} -770 -200 0 0 {name=M4
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} -910 -200 0 1 {name=M5
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/gnd.sym} -840 -120 0 0 {name=l3 lab=GND}
C {sg13g2_pr/sg13_lv_pmos.sym} -1060 -760 0 1 {name=M6
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -860 -760 0 0 {name=M7
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {devices/ammeter.sym} -840 -670 0 0 {name=Vin}
C {devices/ammeter.sym} -700 -380 2 0 {name=Vtau}
C {vdd.sym} -1360 -860 0 0 {name=l4 lab=VDD}
C {vdd.sym} -1080 -820 0 0 {name=l6 lab=VDD}
C {vdd.sym} -840 -810 0 0 {name=l7 lab=VDD}
C {devices/gnd.sym} -1170 -470 0 0 {name=l8 lab=GND}
C {sg13g2_pr/sg13_lv_nmos.sym} -1150 -520 0 1 {name=M3
l=0.13u
w=0.15u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {devices/ammeter.sym} -1060 -520 3 0 {name=VTh}
