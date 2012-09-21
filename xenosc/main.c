#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <windows.h>

const char * XNA_DLL = "%CommonProgramFiles%\\microsoft shared\\XNA\\Framework\\v3.1\\XnaNative.dll";

const char * XENOSC_NAME = "Xenos shader compiler by GliGli";
const char * XENOSC_VERSION = "1.00 beta";

typedef int (WINAPI * CreateCompileShaderFromSourceForXbox)(char *,unsigned int,void*,void*,char*,char*,unsigned int,void**,unsigned int*,void**,unsigned int*);
typedef int (WINAPI * CreateAssembleShaderFromSourceForXbox)(char *,unsigned int,void*,void*,unsigned int,void**,unsigned int*,void**,unsigned int*);
typedef int (WINAPI * FillXboxBuffer)(void*,void*,unsigned int);

int main(int argc, char* argv[])
{
	// variables
	
	int i;

	int assemble_mode=0;

	char function_name[256]="";
	char output_name[MAX_PATH]="";
	char dll_name[MAX_PATH]="";
	
	unsigned int compiler_options=0;

	char * input_name;
	char * profile_string;

	FILE * inf, * outf;

	HMODULE xna;

	CreateCompileShaderFromSourceForXbox comp;
	CreateAssembleShaderFromSourceForXbox assem;
	FillXboxBuffer fillx;

	char hlsl[65536]={0};
	unsigned int hlsl_len;

	void * code_obj=NULL;
	unsigned int code_len=0;
	char code_buf[64*1024]={0};

	void * err_obj=NULL;
	unsigned int err_len=0;
	char err_txt[64*1024]={0};

	int ret;

	// parameters
	
	printf("%s %s\n\n",XENOSC_NAME,XENOSC_VERSION);

	if(argc<3)
	{
		printf("usage: %s input.hlsl profile_string [options...]\n",argv[0]);
		printf("options:\n");
		printf("\t -o output.bin: output file name\n");
		printf("\t -f main: name of main function\n");
		printf("\t -dll XnaNative.dll: use this dll file as compiler\n");
		printf("\t -a: assemble shader instead of compiling it\n");
		printf("\t -d: debug mode\n");
		printf("\t -co: don't optimize\n");
		printf("\t -cv: don't validate\n");
		printf("\t -mr: pack matrices row major\n");
		printf("\t -mc: pack matrices column major\n");
		printf("\t -fa: avoid flow control\n");
		printf("\t -fp: prefer flow control\n");
		printf("\t -pp: partial precision\n");
		return 0;
	}

	for(i=0;i<argc;++i)
	{
		if(!strcmp(argv[i],"-o"))
		{
			strcpy(output_name,argv[++i]);
		}
		else if(!strcmp(argv[i],"-f"))
		{
			strcpy(function_name,argv[++i]);
		}
		else if(!strcmp(argv[i],"-dll"))
		{
			strcpy(dll_name,argv[++i]);
		}
		else if(!strcmp(argv[i],"-a"))
		{
			assemble_mode=1;
		}
		else if(!strcmp(argv[i],"-d"))
		{
			compiler_options|=1;
		}
		else if(!strcmp(argv[i],"-cv"))
		{
			compiler_options|=2;
		}
		else if(!strcmp(argv[i],"-co"))
		{
			compiler_options|=4;
		}
		else if(!strcmp(argv[i],"-mr"))
		{
			compiler_options|=8;
		}
		else if(!strcmp(argv[i],"-mc"))
		{
			compiler_options|=16;
		}
		else if(!strcmp(argv[i],"-pp"))
		{
			compiler_options|=32;
		}
		else if(!strcmp(argv[i],"-fa"))
		{
			compiler_options|=512;
		}
		else if(!strcmp(argv[i],"-fp"))
		{
			compiler_options|=1024;
		}
	}
	
	input_name=argv[1];
	profile_string=argv[2];

	if(!strlen(output_name))
	{
		char * dot;
		strcpy(output_name,input_name);
		dot=strchr(output_name,'.');
		if (dot) *dot=0;

		strcat(output_name,".bin");
	}
	
	if(!strlen(function_name))
	{
		strcpy(function_name,"main");
	}

	if(!strlen(dll_name))
	{
		ExpandEnvironmentStrings(XNA_DLL,dll_name,sizeof(dll_name));
	}
	
	// read input file
	
	inf=fopen(input_name,"rb");
	
	if(!inf)
	{
		printf("error: couldn't open '%s'\n",input_name);
		return 1;
	}
	
	hlsl_len=fread(hlsl,1,sizeof(hlsl),inf);

	fclose(inf);
	
	// load dll

	xna = LoadLibrary(dll_name);

	if (!xna)
	{
		printf("error: couldn't find '%s'\n",dll_name);
		return 2;
	}
	
	comp = (CreateCompileShaderFromSourceForXbox)GetProcAddress(xna,"CreateCompileShaderFromSourceForXbox");
	assem = (CreateAssembleShaderFromSourceForXbox)GetProcAddress(xna,"CreateAssembleShaderFromSourceForXbox");
	fillx = (FillXboxBuffer)GetProcAddress(xna,"FillXboxBuffer");
	
	if (!comp || !assem || !fillx)
	{
		printf("error: couldn't find entry points in '%s'\n", dll_name);
		return 3;
	}
	
	// compile
	
	printf("- Compiling '%s' into '%s'\n",input_name,output_name);

	if (assemble_mode)
	{
		ret=assem(hlsl,hlsl_len,NULL,NULL,compiler_options,&code_obj,&code_len,&err_obj,&err_len);
	}
	else
	{
		ret=comp(hlsl,hlsl_len,NULL,NULL,function_name,profile_string,compiler_options,&code_obj,&code_len,&err_obj,&err_len);
	}

	// get compile log
	
	if(err_len)
	{
		fillx(err_obj,err_txt,sizeof(err_txt));
		printf("%s",err_txt);
	}
	
	if(ret)
	{
		printf("error: couldn't compile shader\n");
		return 4;
	}

	// get code
	
	fillx(code_obj,code_buf,sizeof(code_buf));

	// write output file

	outf=fopen(output_name,"wb");
	
	if(!outf)
	{
		printf("error: couldn't open '%s'\n",output_name);
		return 1;
	}
	
	fwrite(code_buf,1,code_len,outf);

	fclose(outf);
	
	// all done !
	
	printf("- Compiled!\n");

	return 0;
}

