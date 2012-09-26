#include "xemit.h"
#include "xemitops.h"


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <debug.h>

#if 1
# define XEMIT_LOG(a...) printf("[xemit] " a)
#else
# define XEMIT_LOG(a...)
#endif

#define XEMIT_ERROR(a...) XEMIT_LOG("error: " a)

#ifndef min
#define min(a,b) ((a) < (b) ? (a) : (b))
#endif
#ifndef max
#define max(a,b) ((a) > (b) ? (a) : (b))
#endif

#define BIN_SLOTS 6

static xemit_reg_type_t encodeRegType(char * regtype)
{
	xemit_reg_type_t ert=XEMR_NONE;
	
	if(regtype)
	{
		if(!strcmp(regtype,"r"))
		{
			ert=XEMR_TEMP;
		}
		else if(!strcmp(regtype,"c"))
		{
			ert=XEMR_CONST;
		}
		else if(!strcmp(regtype,"oC"))
		{
			ert=XEMR_COLOR_OUT;
		}
		else if(!strcmp(regtype,"tf"))
		{
			ert=XEMR_TEX_FETCH;
		}
	}
	
	return ert;
}

static int encodeNibble(char nibble)
{
	int n=-1;
	
	switch (nibble)
	{
		case 'x': n=0; break;
		case 'y': n=1; break;
		case 'z': n=2; break;
		case 'w': n=3; break;
		case 'r': n=0; break;
		case 'g': n=1; break;
		case 'b': n=2; break;
		case 'a': n=3; break;
	}
	
	return n;
}

static u32 encodeOutputMask(char * mask)
{
	int len=strlen(mask);
	
	if(len>4)
	{
		XEMIT_ERROR("output mask '%s' is too long, ignoring\n",mask);
		return 0;
	}
	
	int i;
	u32 encoded=0;
	int pc=-1;
	
	for(i=0;i<len;++i)
	{
		if(mask[i]=='_') continue;
		
		int c=encodeNibble(mask[i]);
		
		if (c<0 || c<=pc)
		{
			XEMIT_ERROR("invalid char '%c' in output mask '%s', ignoring\n",mask[i],mask);
			return 0;
		}
		
		encoded|=1<<c;
		
		pc=c;
	}
	
//	XEMIT_LOG("%s %08x\n",mask,encoded);
	
	return encoded;
}


static u32 encodeSwizzle(char * swizzle, int expected_len)
{
	int len=strlen(swizzle);
	
	if(len!=expected_len)
	{
		XEMIT_ERROR("swizzle '%s' should have a length of %d, ignoring\n",swizzle,expected_len);
		return 0;
	}
	
	int i;
	u32 encoded=0;
	
	for(i=0;i<len;++i)
	{
		int c=encodeNibble(swizzle[i]);
		
		if (c<0)
		{
			XEMIT_ERROR("invalid char '%c' in swizzle '%s', ignoring\n",swizzle[i],swizzle);
			return 0;
		}
		
		c-=i;
		
		encoded|=(c&3)<<(i*2);
	}
	
//	XEMIT_LOG("%s %08x\n",swizzle,encoded);
	
	return encoded;
}

static void maskInOp(u8 * opbin, int value, int start, int end, int masked)
{
//	XEMIT_LOG("maskInOp %d %d %d %d\n",value,start,end,masked);
	
	if(start==-1 || end==-1) return;
			
	u8 biti,bytei;
	
	for(biti=0;biti<96;++biti)
	{
		bytei=11-(biti>>3);

		if(biti>=start && biti<=end)
		{
			u8 bitv=(value>>(masked+(biti-start)))&1;
			u8 bits=biti&7;
			
//			XEMIT_LOG("%2d %2d %d\n",bytei,biti,bitv);
			
			opbin[bytei]&=~(1<<bits); // make sure bit is cleared
			
			opbin[bytei]|=bitv<<bits;
		}
	}
}

struct XemitShader *Xemit_Create(int is_pixel_shader,int last_used_temp_register)
{
	if(!is_pixel_shader)
	{
		XEMIT_ERROR("only pixel shaders can be emitted right now\n");
		return NULL;
	}
		
	struct XemitShader *s = malloc(sizeof(struct XemitShader));
	memset(s, 0, sizeof(*s));
	
	s->is_pixel_shader=is_pixel_shader?1:0;
	s->last_used_temp_register=last_used_temp_register;

	return s;
}

void Xemit_Destroy(struct XemitShader * shader)
{
	if(!shader)
		return;
	
	if(shader->generated_shader)
		free(shader->generated_shader);
	
	free(shader);
}

int Xemit_OpFull(struct XemitShader *shader, int reg_count, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle,
		char * rs3_type, int rs3, char * rs3_swizzle)
{
	if (shader->next_slot>=XEMIT_MAX_SHADER_INSTRUCTION_SLOTS)
	{
		XEMIT_ERROR("too many ops in shader\n");
		return 7;
	}
	
	// basic regs sanity tests	
	
	if (reg_count>4)
	{
		XEMIT_ERROR("an op can't have more than 4 parameters\n");
		return 1;
	}
	
	xemit_reg_type_t rts[4]={encodeRegType(rd_type),encodeRegType(rs1_type),encodeRegType(rs2_type),encodeRegType(rs3_type)};

	switch(reg_count)
	{
		case 4: /* fall through */
			if (rs3<0 || rts[3]==XEMR_NONE)
			{
				XEMIT_ERROR("rs3 must be valid\n");
				return 5;
			}
		case 3: /* fall through */
			if (rs2<0 || rts[2]==XEMR_NONE)
			{
				XEMIT_ERROR("rs2 must be valid\n");
				return 4;
			}
		case 2: /* fall through */
			if (rs1<0 || rts[1]==XEMR_NONE)
			{
				XEMIT_ERROR("rs1 must be valid\n");
				return 3;
			}
		case 1:
			if (rd<0 || rts[0]==XEMR_NONE)
			{
				XEMIT_ERROR("rd must be valid\n");
				return 2;
			}
	}
	
	int regs[4]= {rd,rs1,rs2,rs3};
	char * rsws[4]= {NULL,rs1_swizzle,rs2_swizzle,rs3_swizzle};
	
	// find which op we will generate
	
	struct xemit_op_s * opd = NULL;
	u8 op[12];
	int i,j;
	int opi=-1;
	
	for(i=0;xemit_ops[i].name;++i)
	{
		if (!strcmp(name,xemit_ops[i].name))
		{
			int ok=TRUE;
			for(j=0;j<reg_count;++j)
			{
				ok=ok && (xemit_ops[i].regs[j].reg_type==rts[j]);
			}

			if (ok)
			{
				opd=&xemit_ops[i];
				opi=i;
				break;
			}
		}
	}
	
	if (!opd)
	{
		XEMIT_ERROR("op '%s' not found\n",name);
		return 6;
	}

	memcpy(op,opd->base_bin,12);
	
	// mask-in regs
	
	for(i=0;i<reg_count;++i)
	{
		int prev_masked=0,masked;
		for(j=0;j<2;++j)
		{
			masked=opd->regs[i].reg_mask[j].end-opd->regs[i].reg_mask[j].start+1;
			
			if(masked==prev_masked) prev_masked=0; // handle a special case where we should write a reg twice
			
			maskInOp(op,regs[i],opd->regs[i].reg_mask[j].start,opd->regs[i].reg_mask[j].end,prev_masked);
			prev_masked=masked;
		}
	}
	
	// mask-in output mask
	
	if(rd_mask)
		maskInOp(op,encodeOutputMask(rd_mask),opd->out_mask.start,opd->out_mask.end,0);
	
	// mask-in swizzles

	for(i=1;i<reg_count;++i)
	{
		if(rsws[i])
		{
			u32 encoded_sw=encodeSwizzle(rsws[i],opd->regs[i].swizzle_count);
			
			for(j=0;j<2;++j)
			{
				maskInOp(op,encoded_sw,opd->regs[i].swizzle_mask[j].start,opd->regs[i].swizzle_mask[j].end,0);
			}
		}
	}
	
	// copy op to slot
	
	shader->slot_op_index[shader->next_slot]=opi;
	memcpy(shader->slots[shader->next_slot++],op,12);
			
	return 0;
}


int Xemit_Op0(struct XemitShader *shader, char * name)
{
	return Xemit_OpFull(shader,0,name,NULL,-1,NULL,NULL,-1,NULL,NULL,-1,NULL,NULL,-1,NULL);
}

int Xemit_Op1(struct XemitShader *shader, char * name,
		char * rd_type, int rd)
{
	return Xemit_OpFull(shader,1,name,rd_type,rd,NULL,NULL,-1,NULL,NULL,-1,NULL,NULL,-1,NULL);
}

int Xemit_Op2(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1)
{
	return Xemit_OpFull(shader,2,name,rd_type,rd,NULL,rs1_type,rs1,NULL,NULL,-1,NULL,NULL,-1,NULL);
}

int Xemit_Op3(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1,
		char * rs2_type, int rs2)
{
	return Xemit_OpFull(shader,3,name,rd_type,rd,NULL,rs1_type,rs1,NULL,rs2_type,rs2,NULL,NULL,-1,NULL);
}

int Xemit_Op4(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1,
		char * rs2_type, int rs2,
		char * rs3_type, int rs3)
{
	return Xemit_OpFull(shader,4,name,rd_type,rd,NULL,rs1_type,rs1,NULL,rs2_type,rs2,NULL,rs3_type,rs3,NULL);
}


int Xemit_Op1Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask)
{
	return Xemit_OpFull(shader,1,name,rd_type,rd,rd_mask,NULL,-1,NULL,NULL,-1,NULL,NULL,-1,NULL);
}

int Xemit_Op2Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle)
{
	return Xemit_OpFull(shader,2,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,NULL,-1,NULL,NULL,-1,NULL);
}

int Xemit_Op3Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle)
{
	return Xemit_OpFull(shader,3,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,rs2_type,rs2,rs2_swizzle,NULL,-1,NULL);
}

int Xemit_Op4Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle,
		char * rs3_type, int rs3, char * rs3_swizzle)
{
	return Xemit_OpFull(shader,4,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,rs2_type,rs2,rs2_swizzle,rs3_type,rs3,rs3_swizzle);
}


void * Xemit_Generate(struct XemitShader *shader)
{
	// build sequencing ops
	
	u32 i,j;

	u32 num_ops=shader->next_slot;
	u32 num_bins=(num_ops+BIN_SLOTS-1)/BIN_SLOTS;
	u32 num_sequencing_ops=max(2,1+num_bins/2);

	u8 sequencing_ops[num_sequencing_ops][12];
	u32 seq_op_num_bins[num_sequencing_ops];

	u32 fetch_info[2]={0,0};

	u32 awaiting_fetch_op=0;
	u32 awaiting_bins=0;
	u32 cur_seq_op=0;
	u32 cur_op=0;

	j=num_bins;
	for(i=0;i<num_sequencing_ops;++i)
	{
		if(i==0)
		{
			seq_op_num_bins[i]=1;
		}
		else
		{
			seq_op_num_bins[i]=min(2,j);
		}

		j-=seq_op_num_bins[i];
	}
	
	memset(sequencing_ops,0,sizeof(sequencing_ops));
	
	for(i=0;i<max(num_bins,num_sequencing_ops);++i)
	{
		if(cur_op<num_ops)
		{
			for(j=0;j<min(BIN_SLOTS,num_ops-cur_op);++j)
			{
				if(awaiting_fetch_op)
				{
					fetch_info[awaiting_bins]|=0x02<<(j*2);
					--awaiting_fetch_op;
				}

				if (xemit_ops[shader->slot_op_index[cur_op+j]].op_type==XEMO_FETCHES)
				{
					fetch_info[awaiting_bins]|=0x01<<(j*2);
					++awaiting_fetch_op;
				}
			}

			++awaiting_bins;
		}

		if(awaiting_bins>=seq_op_num_bins[cur_seq_op])
		{
			if(cur_seq_op==0)
			{
				// start op
				sequencing_ops[cur_seq_op][4]=j<<4;
				sequencing_ops[cur_seq_op][5]=num_sequencing_ops;
				sequencing_ops[cur_seq_op][10]=(fetch_info[0]>>8)&0x0f;
				sequencing_ops[cur_seq_op][11]=fetch_info[0]&0xff;

				sequencing_ops[cur_seq_op][6]=0xc4;
				sequencing_ops[cur_seq_op][8]=(num_ops)?0x12:0x22;
			}
			else
			{
				// middle/end ops
				sequencing_ops[cur_seq_op][0]=(fetch_info[0]>>8)&0x0f;
				sequencing_ops[cur_seq_op][1]=fetch_info[0]&0xff;

				if(awaiting_bins==2)
				{
					sequencing_ops[cur_seq_op][2]=BIN_SLOTS<<4;
					sequencing_ops[cur_seq_op][4]=j<<4;

					sequencing_ops[cur_seq_op][3]=num_sequencing_ops+cur_op-BIN_SLOTS;
					sequencing_ops[cur_seq_op][5]=num_sequencing_ops+cur_op;

					sequencing_ops[cur_seq_op][10]=(fetch_info[1]>>8)&0x0f;
					sequencing_ops[cur_seq_op][11]=fetch_info[1]&0xff;
					
					sequencing_ops[cur_seq_op][6]=0x12;
					sequencing_ops[cur_seq_op][8]=(cur_op<num_ops-1)?0x12:0x22;
				}
				else if(awaiting_bins==1)
				{
					sequencing_ops[cur_seq_op][2]=j<<4;

					sequencing_ops[cur_seq_op][3]=num_sequencing_ops+cur_op;
					sequencing_ops[cur_seq_op][5]=num_sequencing_ops+cur_op+1;

					sequencing_ops[cur_seq_op][6]=0x12;
					sequencing_ops[cur_seq_op][8]=0x22;
				}
				else
				{
					sequencing_ops[cur_seq_op][3]=num_sequencing_ops+cur_op+1;

					sequencing_ops[cur_seq_op][6]=0x22;
				}
			}

			awaiting_bins=0;
			memset(fetch_info,0,sizeof(fetch_info));
			
			++cur_seq_op;
		}

		cur_op+=j;
	}
	
	// shaders must end with this it seems
	
	Xemit_Op0(shader,"cnop");
	
	// build shader
	
	u32 code_size=sizeof(sequencing_ops)+shader->next_slot*12;
	u32 size=code_size+sizeof(struct XenosShaderHeader)+sizeof(struct XenosShaderData);

	u8 * sb = calloc(1,size);
	
	struct XenosShaderHeader * sh = (struct XenosShaderHeader*)sb;
	struct XenosShaderData * sd = (struct XenosShaderData*)(sb+sizeof(struct XenosShaderHeader));

	sh->magic=0x102a1100;
	sh->offset=sizeof(struct XenosShaderHeader)+sizeof(struct XenosShaderData);
	sh->off_shader=sizeof(struct XenosShaderHeader);
	sh->unk1[0]=code_size;
	
	sd->program_control=0x10020000|(shader->last_used_temp_register<<8);
	sd->sh_size=code_size;
	sd->unk1[3]=1;
	
	memcpy(sb+sh->offset,sequencing_ops,sizeof(sequencing_ops));
	memcpy(sb+sh->offset+sizeof(sequencing_ops),shader->slots,shader->next_slot*12);
	
	shader->generated_shader=sb;
	shader->generated_size=size;

	return shader->generated_shader;
}

struct XenosShader * Xemit_LoadGeneratedShader(struct XenosDevice *xe, struct XemitShader *shader)
{
	if(!shader->generated_shader)
	{
		Xemit_Generate(shader);
	}
	
	return Xe_LoadShaderFromMemory(xe,shader->generated_shader);
}

void Xemit_DumpGeneratedShaderToFile(struct XemitShader *shader, char * filename)
{
	if(!shader->generated_shader)
	{
		Xemit_Generate(shader);
	}

	FILE * f = fopen(filename,"wb");
	
	if(f)
	{
		fwrite(shader->generated_shader,1,shader->generated_size,f);
		fclose(f);
	}
	else
	{
		XEMIT_ERROR("couldn't open '%s'\n",filename);
	}
}
