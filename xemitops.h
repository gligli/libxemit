#pragma once

#include <xetypes.h>

typedef enum
{
	XEMR_NONE=-1,
	XEMR_TEMP=0,
	XEMR_CONST=1,
	XEMR_COLOR_OUT=2,
	XEMR_TEX_FETCH=3,
} xemit_regtype_t;

struct xemit_mask_s
{
	s8 start;
	s8 end;
};

struct xemit_reg_s
{
	xemit_regtype_t reg_type;
	struct xemit_mask_s reg_mask[2]; // there can be 2 reg masks
	u8 swizzle_count;
	struct xemit_mask_s swizzle_mask;
};

struct xemit_op_s
{
	char* name;
	u8 base_bin[12];
	struct xemit_mask_s out_mask;
	struct xemit_reg_s regs[4];
};

extern struct xemit_op_s xemit_ops[];