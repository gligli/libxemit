#pragma once

#include <xetypes.h>

#define XEMIT_MAX_SHADER_INSTRUCTION_SLOTS 512

struct XemitShader
{
	int is_pixel_shader;
	u32 next_slot;
	u8 slots[XEMIT_MAX_SHADER_INSTRUCTION_SLOTS][12];
	void * generated_shader;
};

typedef enum
{
	XEMR_NONE=-1,
	XEMR_TEMP=0,
	XEMR_CONST=1,
	XEMR_COLOR_OUT=2,
	XEMR_TEX_FETCH=3,
} XemitRegType;

struct XemitShader *Xemit_Create(int is_pixel_shader);
void Xemit_Destroy(struct XemitShader * shader);

int Xemit_Op1(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd);
int Xemit_Op2(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1);
int Xemit_Op3(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1,
		XemitRegType rs2_type, int rs2);
int Xemit_Op4(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd,
		XemitRegType rs1_type, int rs1,
		XemitRegType rs2_type, int rs2,
		XemitRegType rs3_type, int rs3);

int Xemit_Op1Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask);
int Xemit_Op2Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle);
int Xemit_Op3Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle);
int Xemit_Op4Ex(struct XemitShader *shader, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle,
		XemitRegType rs3_type, int rs3, char * rs3_swizzle);

int Xemit_OpFull(struct XemitShader *shader, int reg_count, char * name,
		XemitRegType rd_type, int rd, char * rd_mask,
		XemitRegType rs1_type, int rs1, char * rs1_swizzle,
		XemitRegType rs2_type, int rs2, char * rs2_swizzle,
		XemitRegType rs3_type, int rs3, char * rs3_swizzle);

void * Xemit_Generate(struct XemitShader *shader);
void * Xemit_GetGeneratedShader(struct XemitShader *shader);