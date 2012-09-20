# /!\ warning /!\ uglyssimo code ahead ;)

SCRIPT_NAME = "Xenos shader emitter generator by GliGli"
SCRIPT_VERSION = "0.03"

SHADER_COMPILER = "../rshadercompiler/rshadercompiler.exe"
OUTPUT_DIR = "./compiled"

OUTPUT_C_FILE = "../xemitops.c"

# array of [opname,[args swizzles]]
OPS = \
[
	# sequencer
#	['exec',0],
#	['exece',0],
#	['cnop',0],

	# alu vector
	['add',[0,4,4]],
	['cndeq',[0,4,4,4]],
	['cndge',[0,4,4,4]],
	['cndgt',[0,4,4,4]],
	['cube',[0,4,4]],
	['dp2add',[0,4,4,4]],
	['dp3',[0,4,4]],
	['dp4',[0,4,4]],
	['dst',[0,4,4]],
	['floor',[0,2]],
	['frc',[0,2]],
	['kill_eq',[0,4,4]],
	['kill_ge',[0,4,4]],
	['kill_gt',[0,4,4]],
	['kill_ne',[0,4,4]],
	['mad',[0,4,4,4]],
	['max',[0,4,4]],
	['maxa',[0,4,4]],
	['max4',[0,2]],
	['min',[0,4,4]],
	['mov',[0,2]],
	['mova',[0,2]],
	['mul',[0,4,4]],
	['nop',[]],
	['seq',[0,4,4]],
	['setp_eq_push',[0,4,4]],
	['setp_ge_push',[0,4,4]],
	['setp_gt_push',[0,4,4]],
	['setp_ne_push',[0,4,4]],
	['sge',[0,4,4]],
	['sgt',[0,4,4]],
	['sne',[0,4,4]],
	['trunc',[0,2]],

	['add_sat',[0,4,4]],
	['cndeq_sat',[0,4,4,4]],
	['cndge_sat',[0,4,4,4]],
	['cndgt_sat',[0,4,4,4]],
	['cube_sat',[0,4,4]],
	['dp2add_sat',[0,4,4,4]],
	['dp3_sat',[0,4,4]],
	['dp4_sat',[0,4,4]],
	['dst_sat',[0,4,4]],
	['floor_sat',[0,2]],
	['frc_sat',[0,2]],
	['kill_eq_sat',[0,4,4]],
	['kill_ge_sat',[0,4,4]],
	['kill_gt_sat',[0,4,4]],
	['kill_ne_sat',[0,4,4]],
	['mad_sat',[0,4,4,4]],
	['max_sat',[0,4,4]],
	['maxa_sat',[0,4,4]],
	['max4_sat',[0,2]],
	['min_sat',[0,4,4]],
	['mov_sat',[0,2]],
	['mova_sat',[0,2]],
	['mul_sat',[0,4,4]],
	['nop_sat',[]],
	['seq_sat',[0,4,4]],
	['setp_eq_push_sat',[0,4,4]],
	['setp_ge_push_sat',[0,4,4]],
	['setp_gt_push_sat',[0,4,4]],
	['setp_ne_push_sat',[0,4,4]],
	['sge_sat',[0,4,4]],
	['sgt_sat',[0,4,4]],
	['sne_sat',[0,4,4]],
	['trunc_sat',[0,2]],


	# alu scalar
	['adds',[0,2]],
#	['addsc',[0,1,1]],
	['adds_prev',[0,1]],
	['cos',[0,1]],
	['exp',[0,1]],
	['floors',[0,1]],
	['frcs',[0,1]],
	['kills_eq',[0,1]],
	['kills_ge',[0,1]],
	['kills_gt',[0,1]],
	['kills_ne',[0,1]],
	['kills_one',[0,1]],
	['log',[0,1]],
	['logc',[0,1]],
	['maxas',[0,2]],
	['maxasf',[0,2]],
	['maxs',[0,2]],
	['mins',[0,2]],
	['movas',[0,1]],
	['movasf',[0,1]],
	['movs',[0,1]],
	['muls',[0,2]],
#	['mulsc',[0,1,1]],
	['muls_prev',[0,1]],
	['muls_prev2',[0,2]],
	['nops',[]],
	['rcp',[0,1]],
	['rcpc',[0,1]],
	['rcpf',[0,1]],
	['retain_prev',[0]],
	['rsq',[0,1]],
	['rsqc',[0,1]],
	['rsqf',[0,1]],
	['seqs',[0,1]],
	['setp_clr',[0]],
	['setp_eq',[0,1]],
	['setp_ge',[0,1]],
	['setp_gt',[0,1]],
	['setp_inv',[0,1]],
	['setp_ne',[0,1]],
	['setp_pop',[0,1]],
	['setp_rstr',[0,1]],
	['sges',[0,1]],
	['sgts',[0,1]],
	['sin',[0,1]],
	['snes',[0,1]],
	['sqrt',[0,1]],
	['subs',[0,2]],
#	['subsc',[0,1,1]],
	['subs_prev',[0,1]],
	['truncs',[0,1]],

	['adds_sat',[0,2]],
#	['addsc_sat',[0,1,1]],
	['adds_prev_sat',[0,1]],
	['cos_sat',[0,1]],
	['exp_sat',[0,1]],
	['floors_sat',[0,1]],
	['frcs_sat',[0,1]],
	['kills_eq_sat',[0,1]],
	['kills_ge_sat',[0,1]],
	['kills_gt_sat',[0,1]],
	['kills_ne_sat',[0,1]],
	['kills_one_sat',[0,1]],
	['log_sat',[0,1]],
	['logc_sat',[0,1]],
	['maxas_sat',[0,2]],
	['maxasf_sat',[0,2]],
	['maxs_sat',[0,2]],
	['mins_sat',[0,2]],
	['movas_sat',[0,1]],
	['movasf_sat',[0,1]],
	['movs_sat',[0,1]],
	['muls_sat',[0,2]],
#	['mulsc_sat',[0,1,1]],
	['muls_prev_sat',[0,1]],
	['muls_prev2_sat',[0,2]],
	['nops_sat',[]],
	['rcp_sat',[0,1]],
	['rcpc_sat',[0,1]],
	['rcpf_sat',[0,1]],
	['retain_prev_sat',[0]],
	['rsq_sat',[0,1]],
	['rsqc_sat',[0,1]],
	['rsqf_sat',[0,1]],
	['seqs_sat',[0,1]],
	['setp_clr_sat',[0]],
	['setp_eq_sat',[0,1]],
	['setp_ge_sat',[0,1]],
	['setp_gt_sat',[0,1]],
	['setp_inv_sat',[0,1]],
	['setp_ne_sat',[0,1]],
	['setp_pop_sat',[0,1]],
	['setp_rstr_sat',[0,1]],
	['sges_sat',[0,1]],
	['sgts_sat',[0,1]],
	['sin_sat',[0,1]],
	['snes_sat',[0,1]],
	['sqrt_sat',[0,1]],
	['subs_sat',[0,2]],
#	['subsc_sat',[0,1,1]],
	['subs_prev_sat',[0,1]],
	['truncs_sat',[0,1]],


	# fetch
	['getBCF1D',[0,1,0]],
	['getBCF2D',[0,2,0]],
	['getBCF3D',[0,3,0]],
	['getBCFCube',[0,3,0]],
	['getCompTexLOD1D',[0,1,0]],
	['getCompTexLOD2D',[0,2,0]],
	['getCompTexLOD3D',[0,3,0]],
	['getCompTexLODCube',[0,3,0]],
	['getGradients',[0,4,0]],
	['getWeights1D',[0,1,0]],
	['getWeights2D',[0,2,0]],
	['getWeights3D',[0,3,0]],
	['getWeightsCube',[0,3,0]],
	['setGradientH',[3]],
	['setGradientV',[3]],
	['setTexLOD',[1]],
	['tfetch1D',[0,1,0]],
	['tfetch2D',[0,2,0]],
	['tfetch3D',[0,3,0]],
	['tfetchCube',[0,3,0]],
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
from md5 import md5
import os
import subprocess
import tempfile
import math
import binascii
import struct

def xlong(s):
    return sum([ord(c) << e*8 for e,c in enumerate(s)])

def rxstr(x,l):
    return chr(x&255) + rxstr(x >> 8,l+1) if l<12 else ''

def xstr(x):
	return rxstr(x,0)

print "%s %s" % (SCRIPT_NAME, SCRIPT_VERSION)

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

		tmpfile=open('__tmp__.psa','wb')
		
		tmpfile.write('xps_3_0\n')

#		tmpfile.write('alloc colors\n');
#		tmpfile.write('mov oC0,c0\n');
#		tmpfile.write('mov oC1,c0\n');
#		tmpfile.write('mov oC2,c0\n');
#		tmpfile.write('mov oC3,c0\n');
#		tmpfile.write('mov r0,c0\n');
#		tmpfile.write('mov r31,c0\n');
#		tmpfile.write('exec\n\n')

		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write(stmt+'\n');
		tmpfile.write('exece\n\n')
		tmpfile.close()

		outname=OUTPUT_DIR+'/'+stmt+'.bin'
		out=os.tmpfile()

		subprocess.call(SHADER_COMPILER+" \""+tmpfile.name+"\" \""+outname+"\" /xps /Debug /SkipValidation",stdout=out)

		out.seek(0,0)
		outs=out.read()

#		print outs

		compiled='- Compiled!' in  outs

		print stmt,'\t\t\t',

		if not compiled:
			print
			continue

		out=open(outname,'rb')
		
		outsize=os.fstat(out.fileno()).st_size;

		print "Valid!"

		out.seek(-48,os.SEEK_END)

		check=xlong(out.read(12))
		current=xlong(out.read(12))

		out.close()

		assert(current==check)
		
		if curswiz==-1 and curmask==-1 and curarg==-1:
#			print "ref %024x"%current
			reference=current;
			outops.append([op[0],reference,argtype,[],[],-1,-1])
			continue

		current=current ^ reference

		bit=-1;
		start=-1;
		prevbit=0;
		regplace=[]

#		print "%024x"%current

		if curswiz!=-1:
			for bitnum in range(97):
				bit=(current>>bitnum) & 1

				if prevbit==0 and bit==1:
					start=bitnum

					lowerswiz=False
					for ps in outops[len(outops)-1][4]:
						if ps[0]==curarg and ps[3]<curswiz:
							lowerswiz=True;

					if not lowerswiz:
						outops[len(outops)-1][4].append([curarg,start,start+7,curswiz])

					break;

				prevbit=bit

		elif curmask!=-1:
			for bitnum in range(97):
				bit=(current>>bitnum) & 1

				if prevbit==0 and bit==1:
					start=bitnum

				if prevbit==1 and bit==0:
					outops[len(outops)-1][5]=start
					outops[len(outops)-1][6]=bitnum-1
					start=-1
					bit=0

				prevbit=bit

		elif curarg!=-1:
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
		print oo

	outopslastidx=len(outops)-1

print "Step 1 done!"

# generate c code

C_REGTYPE=['XEMR_TEMP','XEMR_CONST','XEMR_COLOR_OUT','XEMR_TEX_FETCH']

cfile=open(OUTPUT_C_FILE,'w')

print>>cfile,'// generated with %s %s (%s)' % (SCRIPT_NAME,SCRIPT_VERSION,__file__)
print>>cfile
print>>cfile,'#include "xemitops.h"'
print>>cfile
print>>cfile,'struct xemit_op_s xemit_ops[%d]=' % len(outops)
print>>cfile,'{'
for oo in outops:
	print>>cfile,'\t{',

	print>>cfile,'"'+oo[0]+'",',

	print>>cfile,'{',
	for i in struct.unpack('BBBBBBBBBBBB',xstr(oo[1])):
		print>>cfile,'0x%x,'%(i),
	print>>cfile,'},',

	print>>cfile,'{',oo[5],',',oo[6],'},',

	print>>cfile,'{'
	for ri in range(4):
		print>>cfile,'\t\t{',

		if ri<len(oo[2]):
			print>>cfile,C_REGTYPE[oo[2][ri]],',',

			print>>cfile,'{',
			rmi=-1
			for rm in oo[3]:
				if rm[0]==ri:
					rmi=rmi+1
					print>>cfile,'{',rm[1],',',rm[2],'},',
			if rmi<1:
				print>>cfile,'{',-1,',',-1,'},',
			print>>cfile,'},',

			for op in OPS:
				if op[0]==oo[0]:
					print>>cfile,op[1][ri],',',
					break;

			swi=-1
			for sw in oo[4]:
				if sw[0]==ri:
					swi=swi+1
					print>>cfile,'{',sw[1],',',sw[2],'},',
					break;
			if swi<0:
				print>>cfile,'{',-1,',',-1,'},',
		else:
			print>>cfile,'XEMR_NONE',


		print>>cfile,'},'
	print>>cfile,'\t},',

	print>>cfile,'},'


print>>cfile,'};\n'

cfile.close()

print "All done!"
