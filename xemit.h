#pragma once

#include <xetypes.h>
#include <xenos/xe.h>

#define XEMIT_MAX_SHADER_INSTRUCTION_SLOTS 512

struct XemitShader
{
	int is_pixel_shader;
	
	u32 next_slot;
	u8 slots[XEMIT_MAX_SHADER_INSTRUCTION_SLOTS][12];
	u32 slot_op_index[XEMIT_MAX_SHADER_INSTRUCTION_SLOTS];

	void * generated_shader;
	u32 generated_size;
};

struct XemitShader *Xemit_Create(int is_pixel_shader);
void Xemit_Destroy(struct XemitShader * shader);

int Xemit_Op0(struct XemitShader *shader, char * name);
int Xemit_Op1(struct XemitShader *shader, char * name,
		char * rd_type, int rd);
int Xemit_Op2(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1);
int Xemit_Op3(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1,
		char * rs2_type, int rs2);
int Xemit_Op4(struct XemitShader *shader, char * name,
		char * rd_type, int rd,
		char * rs1_type, int rs1,
		char * rs2_type, int rs2,
		char * rs3_type, int rs3);

int Xemit_Op1Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask);
int Xemit_Op2Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle);
int Xemit_Op3Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle);
int Xemit_Op4Ex(struct XemitShader *shader, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle,
		char * rs3_type, int rs3, char * rs3_swizzle);

int Xemit_OpFull(struct XemitShader *shader, int reg_count, char * name,
		char * rd_type, int rd, char * rd_mask,
		char * rs1_type, int rs1, char * rs1_swizzle,
		char * rs2_type, int rs2, char * rs2_swizzle,
		char * rs3_type, int rs3, char * rs3_swizzle);

void * Xemit_Generate(struct XemitShader *shader);
struct XenosShader * Xemit_LoadGeneratedShader(struct XenosDevice *xe, struct XemitShader *shader);
void Xemit_DumpGeneratedShaderToFile(struct XemitShader *shader, char * filename);
