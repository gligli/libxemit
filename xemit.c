#include "xemit.h"
#include "xemitops.h"


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if 1
# define XEMIT_LOG(a...) printf("[xemit] " a)
#else
# define XEMIT_LOG(a...)
#endif

#define XEMIT_ERROR(a...) XEMIT_LOG("error: " a)

static void maskInOp(u8 * opbin, int value, int start, int end, int masked)
{
	int biti,bytei;
	
	for(biti=0;biti<96;++biti);
	{
		bytei=biti&~7;
		
		if(biti>=start && biti<=end)
		{
			opbin[bytei]|=((value>>(masked+biti-start))&1)<<(biti&7);
		}
	}
}

struct XemitShader *Xemit_Create(int is_pixel_shader)
{
	struct XemitShader *s = malloc(sizeof(struct XemitShader));
	memset(s, 0, sizeof(*s));
	
	s->is_pixel_shader=is_pixel_shader?1:0;

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
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle,
		XemitRegType rs3_type, int rs3, char * rs3_swizzle)
{
	// basic regs sanity tests	
	
	if (reg_count>4)
	{
		XEMIT_ERROR("an op can't have more than 4 parameters");
		return 1;
	}
	
	switch(reg_count)
	{
		case 4: /* fall through */
			if (rs3<0 || rs3_type==XEMR_NONE)
			{
				XEMIT_ERROR("rs3 must be valid");
				return 5;
			}
		case 3: /* fall through */
			if (rs2<0 || rs2_type==XEMR_NONE)
			{
				XEMIT_ERROR("rs2 must be valid");
				return 4;
			}
		case 2: /* fall through */
			if (rs1<0 || rs1_type==XEMR_NONE)
			{
				XEMIT_ERROR("rs1 must be valid");
				return 3;
			}
		case 1:
			if (rd<0 || rd_type==XEMR_NONE)
			{
				XEMIT_ERROR("rd must be valid");
				return 2;
			}
	}
	
	int regs[4]= {rd,rs1,rs2,rs3};
	int rts[4]= {rd_type,rs1_type,rs2_type,rs3_type};
	
	// find which op we will generate
	
	struct xemit_op_s * opd = NULL;
	u8 op[12];
	int i,j;
	
	for(i=0;xemit_ops[i].name;++i)
	{
		if (!strcmp(name,xemit_ops[i].name))
		{
			int ok=TRUE;
			for(j=0;j<reg_count;++j)
			{
				ok=ok || (xemit_ops[i].regs[j].reg_type==rts[j]);
			}

			if (ok)
			{
				opd=&xemit_ops[i];
			}
		}
	}
	
	if (!opd)
	{
		XEMIT_ERROR("op not found");
		return 6;
	}

	memcpy(op,opd->base_bin,12);
	
	// mask-in regs
	
	for(i=0;i<reg_count;++i)
	{
		int masked=0;
		for(j=0;j<2;++j)
		{
			maskInOp(op,regs[i],opd->regs[i].reg_mask[j].start,opd->regs[i].reg_mask[j].end,masked);
			masked+=opd->regs[i].reg_mask[j].end-opd->regs[i].reg_mask[j].start+1;
		}
	}
	
	// mask-in output mask
	
	// mask-in swizzles
	
	// copy op to slot
	
	memcpy(shader->slots[shader->next_slot++],op,12);
	
	return 0;
}


int Xemit_Op1(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd)
{
	return Xemit_OpFull(shader,1,name,rd_type,rd,NULL,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL);
}

int Xemit_Op2(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1)
{
	return Xemit_OpFull(shader,2,name,rd_type,rd,NULL,rs1_type,rs1,NULL,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL);
}

int Xemit_Op3(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1,
		XemitRegType rs2_type, int rs2)
{
	return Xemit_OpFull(shader,3,name,rd_type,rd,NULL,rs1_type,rs1,NULL,rs2_type,rs2,NULL,XEMR_NONE,-1,NULL);
}

int Xemit_Op4(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1,
		XemitRegType rs2_type, int rs2,
		XemitRegType rs3_type, int rs3)
{
	return Xemit_OpFull(shader,4,name,rd_type,rd,NULL,rs1_type,rs1,NULL,rs2_type,rs2,NULL,rs3_type,rs3,NULL);
}


int Xemit_Op1Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask)
{
	return Xemit_OpFull(shader,1,name,rd_type,rd,rd_mask,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL);
}

int Xemit_Op2Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle)
{
	return Xemit_OpFull(shader,2,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,XEMR_NONE,-1,NULL,XEMR_NONE,-1,NULL);
}

int Xemit_Op3Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle)
{
	return Xemit_OpFull(shader,3,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,rs2_type,rs2,rs2_swizzle,XEMR_NONE,-1,NULL);
}

int Xemit_Op4Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle,
		XemitRegType rs3_type, int rs3, char * rs3_swizzle)
{
	return Xemit_OpFull(shader,4,name,rd_type,rd,rd_mask,rs1_type,rs1,rs1_swizzle,rs2_type,rs2,rs2_swizzle,rs3_type,rs3,rs3_swizzle);
}


void * Xemit_Generate(struct XemitShader *shader)
{
	return shader->generated_shader;
}

void * Xemit_GetGeneratedShader(struct XemitShader *shader)
{
	return shader->generated_shader;
}