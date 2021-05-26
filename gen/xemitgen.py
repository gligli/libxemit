#!/usr/bin/python3

# /!\ warning /!\ uglyssimo code ahead ;)

SCRIPT_NAME = "Xenos shader emitter generator by GliGli"
SCRIPT_VERSION = "0.06"

SHADER_COMPILER = "../xenosc/xenosc.exe"
OUTPUT_DIR = "./compiled"

OUTPUT_C_FILE = "../xemitops.c"

# array of [opname,[args swizzles],optype]
OPS = \
[
	# sequencer
#	['exec',[],0],
#	['exece',[],0],
	['cnop',[],0],

	# alu vector
	['add',[0,4,4],1],
	['cndeq',[0,4,4,4],1],
	['cndge',[0,4,4,4],1],
	['cndgt',[0,4,4,4],1],
	['cube',[0,4,4],1],
	['dp2add',[0,4,4,4],1],
	['dp3',[0,4,4],1],
	['dp4',[0,4,4],1],
	['dst',[0,4,4],1],
	['floor',[0,4],1],
	['frc',[0,4],1],
	['kill_eq',[0,4,4],1],
	['kill_ge',[0,4,4],1],
	['kill_gt',[0,4,4],1],
	['kill_ne',[0,4,4],1],
	['mad',[0,4,4,4],1],
	['max',[0,4,4],1],
	['maxa',[0,4,4],1],
	['max4',[0,4],1],
	['min',[0,4,4],1],
	['mov',[0,4],1],
	['mova',[0,4],1],
	['mul',[0,4,4],1],
	['nop',[],1],
	['seq',[0,4,4],1],
	['setp_eq_push',[0,4,4],1],
	['setp_ge_push',[0,4,4],1],
	['setp_gt_push',[0,4,4],1],
	['setp_ne_push',[0,4,4],1],
	['sge',[0,4,4],1],
	['sgt',[0,4,4],1],
	['sne',[0,4,4],1],
	['trunc',[0,4],1],

	['add_sat',[0,4,4],2],
	['cndeq_sat',[0,4,4,4],2],
	['cndge_sat',[0,4,4,4],2],
	['cndgt_sat',[0,4,4,4],2],
	['cube_sat',[0,4,4],2],
	['dp2add_sat',[0,4,4,4],2],
	['dp3_sat',[0,4,4],2],
	['dp4_sat',[0,4,4],2],
	['dst_sat',[0,4,4],2],
	['floor_sat',[0,4],2],
	['frc_sat',[0,4],2],
	['kill_eq_sat',[0,4,4],2],
	['kill_ge_sat',[0,4,4],2],
	['kill_gt_sat',[0,4,4],2],
	['kill_ne_sat',[0,4,4],2],
	['mad_sat',[0,4,4,4],2],
	['max_sat',[0,4,4],2],
	['maxa_sat',[0,4,4],2],
	['max4_sat',[0,4],2],
	['min_sat',[0,4,4],2],
	['mov_sat',[0,4],2],
	['mova_sat',[0,4],2],
	['mul_sat',[0,4,4],2],
	['nop_sat',[],2],
	['seq_sat',[0,4,4],2],
	['setp_eq_push_sat',[0,4,4],2],
	['setp_ge_push_sat',[0,4,4],2],
	['setp_gt_push_sat',[0,4,4],2],
	['setp_ne_push_sat',[0,4,4],2],
	['sge_sat',[0,4,4],2],
	['sgt_sat',[0,4,4],2],
	['sne_sat',[0,4,4],2],
	['trunc_sat',[0,4],2],


	# alu scalar
	['adds',[0,2],3],
#	['addsc',[0,1,1],3],
	['adds_prev',[0,1],3],
	['cos',[0,1],3],
	['exp',[0,1],3],
	['floors',[0,1],3],
	['frcs',[0,1],3],
	['kills_eq',[0,1],3],
	['kills_ge',[0,1],3],
	['kills_gt',[0,1],3],
	['kills_ne',[0,1],3],
	['kills_one',[0,1],3],
	['log',[0,1],3],
	['logc',[0,1],3],
	['maxas',[0,2],3],
	['maxasf',[0,2],3],
	['maxs',[0,2],3],
	['mins',[0,2],3],
	['movas',[0,1],3],
	['movasf',[0,1],3],
	['movs',[0,1],3],
	['muls',[0,2],3],
#	['mulsc',[0,1,1],3],
	['muls_prev',[0,1],3],
	['muls_prev2',[0,2],3],
	['nops',[],3],
	['rcp',[0,1],3],
	['rcpc',[0,1],3],
	['rcpf',[0,1],3],
	['retain_prev',[0],3],
	['rsq',[0,1],3],
	['rsqc',[0,1],3],
	['rsqf',[0,1],3],
	['seqs',[0,1],3],
	['setp_clr',[0],3],
	['setp_eq',[0,1],3],
	['setp_ge',[0,1],3],
	['setp_gt',[0,1],3],
	['setp_inv',[0,1],3],
	['setp_ne',[0,1],3],
	['setp_pop',[0,1],3],
	['setp_rstr',[0,1],3],
	['sges',[0,1],3],
	['sgts',[0,1],3],
	['sin',[0,1],3],
	['snes',[0,1],3],
	['sqrt',[0,1],3],
	['subs',[0,2],3],
#	['subsc',[0,1,1],3],
	['subs_prev',[0,1],3],
	['truncs',[0,1],3],

	['adds_sat',[0,2],4],
#	['addsc_sat',[0,1,1],4],
	['adds_prev_sat',[0,1],4],
	['cos_sat',[0,1],4],
	['exp_sat',[0,1],4],
	['floors_sat',[0,1],4],
	['frcs_sat',[0,1],4],
	['kills_eq_sat',[0,1],4],
	['kills_ge_sat',[0,1],4],
	['kills_gt_sat',[0,1],4],
	['kills_ne_sat',[0,1],4],
	['kills_one_sat',[0,1],4],
	['log_sat',[0,1],4],
	['logc_sat',[0,1],4],
	['maxas_sat',[0,2],4],
	['maxasf_sat',[0,2],4],
	['maxs_sat',[0,2],4],
	['mins_sat',[0,2],4],
	['movas_sat',[0,1],4],
	['movasf_sat',[0,1],4],
	['movs_sat',[0,1],4],
	['muls_sat',[0,2],4],
#	['mulsc_sat',[0,1,1],4],
	['muls_prev_sat',[0,1],4],
	['muls_prev2_sat',[0,2],4],
	['nops_sat',[],4],
	['rcp_sat',[0,1],4],
	['rcpc_sat',[0,1],4],
	['rcpf_sat',[0,1],4],
	['retain_prev_sat',[0],4],
	['rsq_sat',[0,1],4],
	['rsqc_sat',[0,1],4],
	['rsqf_sat',[0,1],4],
	['seqs_sat',[0,1],4],
	['setp_clr_sat',[0],4],
	['setp_eq_sat',[0,1],4],
	['setp_ge_sat',[0,1],4],
	['setp_gt_sat',[0,1],4],
	['setp_inv_sat',[0,1],4],
	['setp_ne_sat',[0,1],4],
	['setp_pop_sat',[0,1],4],
	['setp_rstr_sat',[0,1],4],
	['sges_sat',[0,1],4],
	['sgts_sat',[0,1],4],
	['sin_sat',[0,1],4],
	['snes_sat',[0,1],4],
	['sqrt_sat',[0,1],4],
	['subs_sat',[0,2],4],
#	['subsc_sat',[0,1,1],4],
	['subs_prev_sat',[0,1],4],
	['truncs_sat',[0,1],4],


	# fetch
	['getBCF1D',[0,1,0],5],
	['getBCF2D',[0,2,0],5],
	['getBCF3D',[0,3,0],5],
	['getBCFCube',[0,3,0],5],
	['getCompTexLOD1D',[0,1,0],5],
	['getCompTexLOD2D',[0,2,0],5],
	['getCompTexLOD3D',[0,3,0],5],
	['getCompTexLODCube',[0,3,0],5],
	['getGradients',[0,4,0],5],
	['getWeights1D',[0,1,0],5],
	['getWeights2D',[0,2,0],5],
	['getWeights3D',[0,3,0],5],
	['getWeightsCube',[0,3,0],5],
	['setGradientH',[3],5],
	['setGradientV',[3],5],
	['setTexLOD',[1],5],
	['tfetch1D',[0,1,0],5],
	['tfetch2D',[0,2,0],5],
	['tfetch3D',[0,3,0],5],
	['tfetchCube',[0,3,0],5],
]

# array of [regtype,regcount,[valid arg positions]]
REGTYPE = \
[
	['r', 32, [0,1,2,3]],
	['c', 256, [1,2,3]],
	['oC', 4, [0]],
	['tf', 32, [2]],
]

import time
from hashlib import md5
import os
import subprocess
import tempfile
import math
import binascii

def xlong(s):
    return sum([c << (11-e)*8 for e,c in enumerate(s)])

def rxstr(x,l):
	return [((x>>(11*8))&255)] + rxstr(x << 8,l+1) if l<12 else []

def xstr(x):
	return bytes(rxstr(x,0))

os.chdir(os.path.dirname(os.path.abspath(__file__))) # .py path in working dir

print("%s %s" % (SCRIPT_NAME, SCRIPT_VERSION))

swizzles=\
[
	['','.x','.xy','.xyz','.xyzw'],
	['','.w','.wx','.wxy','.wxyz'],
]

arglist=[]
argtypes=[]

def genargstuff(args):

	arglist = \
	[
		[['',-1,-1,-1]],
		[],
		[],
		[],
		[],
	]

	argtypes = \
	[
		[[]],
		[],
		[],
		[],
		[],
	]

	for rt1 in REGTYPE:
		if not 0 in rt1[2]:
			continue

		arglist[1].append(["%s%d" % (rt1[0], 0),-1,-1,-1])
		arglist[1].append(["%s%d" % (rt1[0], rt1[1]-1),0,-1,-1])

		arglist[1].append(["%s0._"%rt1[0],0,-1,0])

		argtypes[1].append([REGTYPE.index(rt1)])

		if len(args)>1:
			for rt2 in REGTYPE:
				if not 1 in rt2[2]:
					continue

				sw2=swizzles[0][args[1]]
				sx2=swizzles[1][args[1]]
				arglist[2].append(["%s%d,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2),-1,-1,-1])
				arglist[2].append(["%s%d,%s%d%s" % (rt1[0], rt1[1]-1, rt2[0], 0, sw2),0,-1,-1])
				arglist[2].append(["%s%d,%s%d%s" % (rt1[0], 0, rt2[0], rt2[1]-1, sw2),1,-1,-1])

				arglist[2].append(["%s0._,%s0%s"%(rt1[0],rt2[0], sw2),0,-1,0])

				if sx2!='':
					arglist[2].append(["%s%d,%s%d%s" % (rt1[0], 0, rt2[0], 0, sx2),1,1,-1])

				argtypes[2].append([REGTYPE.index(rt1),REGTYPE.index(rt2)])

				if len(args)>2:
					for rt3 in REGTYPE:
						if not 2 in rt3[2]:
							continue

						sw3=swizzles[0][args[2]]
						sx3=swizzles[1][args[2]]
						arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2, rt3[0], 0,sw3),-1,-1,-1])
						arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], rt1[1]-1, rt2[0], 0, sw2, rt3[0], 0,sw3),0,-1,-1])
						arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], rt2[1]-1, sw2, rt3[0], 0,sw3),1,-1,-1])
						arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2,rt3[0], rt3[1]-1,sw3),2,-1,-1])

						arglist[3].append(["%s0._,%s0%s,%s0%s"%(rt1[0],rt2[0],sw2,rt3[0],sw3),0,-1,0])

						if sx2!='':
							arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sx2,rt3[0], 0, sw3),1,1,-1])
						if sx3!='':
							arglist[3].append(["%s%d,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2,rt3[0], 0, sx3),2,2,-1])

						argtypes[3].append([REGTYPE.index(rt1),REGTYPE.index(rt2),REGTYPE.index(rt3)])

						if len(args)>3:
							for rt4 in REGTYPE:
								if not 3 in rt4[2]:
									continue

								sw4=swizzles[0][args[3]]
								sx4=swizzles[1][args[3]]
								arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2, rt3[0], 0, sw3, rt4[0], 0 ,sw4),-1,-1,-1])
								arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], rt1[1]-1, rt2[0], 0,  sw2, rt3[0], 0, sw3, rt4[0], 0 ,sw4),0,-1,-1])
								arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], rt2[1]-1, sw2, rt3[0], 0, sw3, rt4[0], 0 ,sw4),1,-1,-1])
								arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2, rt3[0], rt3[1]-1, sw3, rt4[0], 0 ,sw4),2,-1,-1])
								arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2, rt3[0], 0, sw3, rt4[0], rt4[1]-1 ,sw4),3,-1,-1])

								arglist[4].append(["%s0._,%s0%s,%s0%s,%s0%s"%(rt1[0],rt2[0],sw2,rt3[0],sw3,rt4[0],sw4),0,-1,0])

								if sx2!='':
									arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sx2,rt3[0], 0, sw3, rt4[0], 0 ,sw4),1,1,-1])
								if sx3!='':
									arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2,rt3[0], 0, sx2, rt4[0], 0 ,sw4),2,2,-1])
								if sx4!='':
									arglist[4].append(["%s%d,%s%d%s,%s%d%s,%s%d%s" % (rt1[0], 0, rt2[0], 0, sw2,rt3[0], 0, sw3, rt4[0], 0 ,sx4),3,3,-1])

								argtypes[4].append([REGTYPE.index(rt1),REGTYPE.index(rt2),REGTYPE.index(rt3),REGTYPE.index(rt4)])

	return arglist, argtypes
# generate list of ops

outopslastidx=-1;
outops=[]

for op in OPS:
	argidx=0
	argtype=[]

	numargs=len(op[1])

	arglist,argtypes=genargstuff(op[1])

	for args in arglist[numargs]:

		stmt=op[0]+' '+args[0]

		curarg=args[1]
		curswiz=args[2]
		curmask=args[3]

		if curarg==-1:
			reference=None;
			atidx=-1
			for a2 in arglist[numargs]:
				if a2[1]==-1 and a2[2]==-1 and a2[3]==-1:
					atidx=atidx+1
				if a2==args:
					break
			argtype=argtypes[numargs][atidx]

		argidx=argidx+1

		tmpfile=open('__tmp__.psa','w')
		
		tmpfile.write('xps_3_0\n')

		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write('exece\n\n')
		tmpfile.close()

		outname=OUTPUT_DIR+'/'+stmt+'.bin'

		outi, outn=tempfile.mkstemp()
		out = open(outi, "r")

		subprocess.call(SHADER_COMPILER+" \""+tmpfile.name+"\" asm -o \""+outname+"\" -a -d -cv",stdout=out)

		out.seek(0,0)
		outs=out.read()

#		print outs

		compiled='- Compiled!' in  outs

		print(stmt,'\t\t\t',)

		if not compiled:
			print
			continue

		out=open(outname,'rb')

		outsize=os.fstat(out.fileno()).st_size;

		print("Valid!")

		out.seek(-48,os.SEEK_END)

		check=xlong(out.read(12))
		current=xlong(out.read(12))

		out.close()

		assert(current==check)
		
		if curswiz==-1 and curmask==-1 and curarg==-1:
#			print("ref %024x" % current)
			reference=current;
			outops.append([op[0],reference,argtype,[],[],-1,-1])
			continue

		current=current ^ reference

		bit=-1;
		start=-1;
		regplace=[]

#		print("%024x" % current)

		if curswiz!=-1:
			prevbit=0;
			for bitnum in range(97):
				bit=(current>>bitnum) & 1

				if prevbit==0 and bit==1:
					start=bitnum

				if (prevbit==1 and bit==0) or (start!=-1 and bitnum-start>=7):
					lowerswiz=False
					for ps in outops[len(outops)-1][4]:
						if ps[0]==curarg and ps[3]<curswiz:
							lowerswiz=True;

					if not lowerswiz:
						outops[len(outops)-1][4].append([curarg,start,start+7,curswiz])

					start=-1
					bit=0

				prevbit=bit

		elif curmask!=-1:
			prevbit=0;
			for bitnum in range(97):
				bit=(current>>bitnum) & 1

				if prevbit==0 and bit==1:
					start=bitnum

				if prevbit==1 and bit==0:
					outops[len(outops)-1][5]=start
					outops[len(outops)-1][6]=bitnum-1

					break;

				prevbit=bit

		elif curarg!=-1:
			prevbit=0;
			for bitnum in range(97):
				bit=(current>>bitnum) & 1

				if prevbit==0 and bit==1:
					start=bitnum

				if (prevbit==1 and bit==0) or (start!=-1 and bitnum-start>=math.log(REGTYPE[argtype[curarg]][1],2)):
					outops[len(outops)-1][3].append([curarg,start,bitnum-1])
					start=-1
					bit=0

				prevbit=bit

	for oo in outops[outopslastidx+1:]:
		print(oo)

	outopslastidx=len(outops)-1

print("Step 1 done!")

# generate c code

C_REGTYPE=['XEMR_TEMP','XEMR_CONST','XEMR_COLOR_OUT','XEMR_TEX_FETCH']
C_OPTYPE=['XEMO_SEQUENCER','XEMO_ALU_VECTOR','XEMO_ALU_VECTOR_SAT','XEMO_ALU_SCALAR','XEMO_ALU_SCALAR_SAT','XEMO_FETCHES']

cfile=open(OUTPUT_C_FILE,'w')

print('// generated with %s %s (%s)' % (SCRIPT_NAME,SCRIPT_VERSION,__file__), end="\n", file=cfile)
print(end="\n", file=cfile)
print('#include "xemitops.h"', end="\n", file=cfile)
print(end="\n", file=cfile)
print('struct xemit_op_s xemit_ops[%d]=' % (len(outops)+1), end="\n", file=cfile)
print('{', end="\n", file=cfile)
for oo in outops:
	print('\t{', end="", file=cfile)

	print(' "'+oo[0]+'",', end="", file=cfile)

	ot=-1;

	for o in OPS:
		if o[0]==oo[0]:
			ot=o[2];
			break
			
	print(" %s, "%(C_OPTYPE[ot]), end="", file=cfile)

	print('{', end="", file=cfile)
	for i in xstr(oo[1]):
		print(' 0x%x,'%(i), end="", file=cfile)
	print(' }, ', end="", file=cfile)

	print('{',oo[5],',',oo[6],'},', end="", file=cfile)

	print(' {', end="\n", file=cfile)
	for ri in range(4):
		print('\t\t{ ', end="", file=cfile)

		if ri<len(oo[2]):
			print(C_REGTYPE[oo[2][ri]],',', end="", file=cfile)

			print(' {', end="", file=cfile)
			rmi=-1
			for rm in oo[3]:
				if rm[0]==ri:
					rmi=rmi+1
					print(' {',rm[1],',',rm[2],'},', end="", file=cfile)
			if rmi<1:
				print(' {',-1,',',-1,'},', end="", file=cfile)
			print(' }, ', end="", file=cfile)

			if ot!=5: # TODO: no swizzles for fetches for now (different format)
				for op in OPS:
					if op[0]==oo[0]:
						print(op[1][ri],',', end="", file=cfile)
						break;
			else:
				print('0 ,', end="", file=cfile)

			print(' {', end="", file=cfile)
			swi=-1
			for sw in oo[4]:
				if sw[0]==ri:
					swi=swi+1
					print(' {',sw[1],',',sw[2],'},', end="", file=cfile)

					if ot!=1: # TODO: double swizzle only for alu vector
						break
			if swi<0:
				print(' {',-1,',',-1,'},', end="", file=cfile)
			if swi<1:
				print(' {',-1,',',-1,'},', end="", file=cfile)
			print(' },', end="", file=cfile)
		else:
			print('XEMR_NONE', end="", file=cfile)


		print(' },', end="\n", file=cfile)
	print('\t}, ', end="", file=cfile)

	print('},', end="\n", file=cfile)

print('\t{NULL}', end="\n", file=cfile)
print('};', end="\n", file=cfile)
print(end="\n", file=cfile)

cfile.close()

print("All done!")
