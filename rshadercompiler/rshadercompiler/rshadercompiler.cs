//          The R 360 XNA Shader Compiler (by Tser)
//
//          This Compiler generates binary code out of text shader code, using the effect of the XNA Frameworks
//          Note, the compiler is inside a dll mapped to extern located at
//          "X":\Program Files\Common Files\microsoft shared\XNA\Framework\v1.0X\XNANative1.dll
//          This dll hosts functions like CompileEffectForXbox
//          This allows you to easely precompile binary shader code and
//          use it with other xbox360 projects (like Linux , XBMC)
//
//          History 25-08-22 Creation, Tser                                     
//
//          How to Compile this                                                     
//          - Install the XNA FrameWork                                         
//          - Create a new Windows Console Application                    
//          - Add reference to Microsoft.XNA.FrameWork                   
//          - Replace your program.cs with this program.cs :)             

using System;
using System.Collections.Generic;
using System.Text;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace rshadercompiler
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                Console.WriteLine("R 360 XNA Shader / Effect Compiler");
                if (args.Length < 3)
                {


                    if (args.Length == 1 && args[0] == "/test")
                    {
                        SelfTest();
                        return;
                    }
                    Console.WriteLine("usage: rshadercompiler Input.fx output.bin /type NameOfMainFunction /options...");
                    Console.WriteLine("       where /type is /ps for xbox PixelShader");
                    Console.WriteLine("                      /vs for xbox VertexShader");
                    Console.WriteLine("                      /xps for asm based xbox PixelShader");
                    Console.WriteLine("                      /xvs for asm based xbox VertexShader");
                    Console.WriteLine("                      /effect for effects");
                    Console.WriteLine("       where /options is one or more of:");
                    Console.WriteLine("                      Debug");
                    Console.WriteLine("                      SkipValidation");
                    Console.WriteLine("                      SkipOptimization");
                    Console.WriteLine("                      PackMatrixRowMajor");
                    Console.WriteLine("                      PackMatrixColumnMajor");
                    Console.WriteLine("                      PartialPrecision");
                    Console.WriteLine("                      ForceVertexShaderSoftwareNoOptimizations");
                    Console.WriteLine("                      ForcePixelShaderSoftwareNoOptimizations");
                    Console.WriteLine("                      NoPreShader");
                    Console.WriteLine("                      AvoidFlowControl");
                    Console.WriteLine("                      PreferFlowControl");
                    Console.WriteLine("                      NotCloneable");

                    Console.WriteLine("       if you use /vs or /ps supply NameOfMainFunction");

                }
                else
                {
                    CompilerOptions co=CompilerOptions.None;
                    string NameofMainFunction = "main";
                    if (args.Length > 3)
                    {
                        NameofMainFunction = args[3];
                    }

                    if (args.Length > 4)
                    {
                        int i;
                        for (i = 4; i < args.Length; ++i)
                        {
                            switch (args[i].ToLower())
                            {
                                case "/debug":
                                    co = co | CompilerOptions.Debug;
                                    break;
                                case "/skipvalidation":
                                    co = co | CompilerOptions.SkipValidation;
                                    break;
                                case "/skipoptimization":
                                    co = co | CompilerOptions.SkipOptimization;
                                    break;
                                case "/packmatrixrowmajor":
                                    co = co | CompilerOptions.PackMatrixRowMajor;
                                    break;
                                case "/packmatrixcolumnmajor":
                                    co = co | CompilerOptions.PackMatrixColumnMajor;
                                    break;
                                case "/partialprecision":
                                    co = co | CompilerOptions.PartialPrecision;
                                    break;
                                case "/forcevertexshadersoftwarenooptimizations":
                                    co = co | CompilerOptions.ForceVertexShaderSoftwareNoOptimizations;
                                    break;
                                case "/forcepixelshadersoftwarenooptimizations":
                                    co = co | CompilerOptions.ForcePixelShaderSoftwareNoOptimizations;
                                    break;
                                case "/nopreshader":
                                    co = co | CompilerOptions.NoPreShader;
                                    break;
                                case "/avoidflowcontrol":
                                    co = co | CompilerOptions.AvoidFlowControl;
                                    break;
                                case "/preferflowcontrol":
                                    co = co | CompilerOptions.PreferFlowControl;
                                    break;
                                case "/notcloneable":
                                    co = co | CompilerOptions.NotCloneable;
                                    break;
                                default:
                                    Console.WriteLine(" I have no clue whatsoever how to handle " + args[i]);
                                    break;
                            }
                        }
                    }
                    
                    switch (args[2])
                    {
                        case "/ps":
                            shaderCompiler(args[0], args[1], ShaderProfile.PS_3_0, false, NameofMainFunction, co);
                            break;
                        case "/vs":
                            shaderCompiler(args[0], args[1], ShaderProfile.VS_3_0, false, NameofMainFunction, co);
                            break;
                        case "/xps":
                            shaderCompiler(args[0], args[1], ShaderProfile.XPS_3_0, true, string.Empty, co);
                            break;
                        case "/xvs":
                            shaderCompiler(args[0], args[1], ShaderProfile.XVS_3_0, true, string.Empty, co);
                            break;
                        case "/effect":
                            EffectParser(args[0], args[1], co);
                            break;
                        default:
                            Console.WriteLine(" I have no clue whatsoever how to handle " + args[2]);
                            break;
                    }

                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("We encoutered an undocumented feature\n" + ex.Message.ToString());
                Console.WriteLine(ex.StackTrace.ToString()); // main stack
            }
        }

        static void shaderCompiler(string inputfile, string outputfile, ShaderProfile shaderProfile, bool isASM, string entryname, CompilerOptions co)
        {
            Console.WriteLine(String.Format("- Parsing {0}\n- into {1}", inputfile, outputfile));
            CompilerMacro[] macroArray = null;
            macroArray = new CompilerMacro[2];
            macroArray[0].Name = "XBOX";
            macroArray[1].Name = "XBOX360";

            CompiledShader compiledShader;

            if (isASM)
            {
                compiledShader = Microsoft.Xna.Framework.Graphics.ShaderCompiler.AssembleFromFile(inputfile, macroArray, null, co, TargetPlatform.Xbox360);
            }
            else
            {
                compiledShader = Microsoft.Xna.Framework.Graphics.ShaderCompiler.CompileFromFile(inputfile, macroArray, null, co, entryname, shaderProfile, TargetPlatform.Xbox360);

            }
            Console.WriteLine(compiledShader.ErrorsAndWarnings);

            if (compiledShader.Success)
            {
                Console.WriteLine("- Compiled! ");
                System.IO.File.WriteAllBytes(outputfile, compiledShader.GetShaderCode());
                Console.WriteLine(String.Format("- bytecode stored into {0}\n", outputfile));
            }
            else
            {
                Console.WriteLine("- Errors Compiling File");
            }
        }





        static void EffectParser(string inputfile, string outputfile, CompilerOptions co)
        {
            Console.WriteLine(String.Format("- Parsing {0}\n- into {1}", inputfile, outputfile));
            CompilerMacro[] macroArray = null;
            macroArray = new CompilerMacro[2];
            macroArray[0].Name = "XBOX";
            macroArray[1].Name = "XBOX360";
            CompiledEffect compiledEffect = Microsoft.Xna.Framework.Graphics.Effect.CompileEffectFromFile(inputfile, macroArray, null, co, TargetPlatform.Xbox360);
            Console.WriteLine(compiledEffect.ErrorsAndWarnings);

            if (compiledEffect.Success)
            {
                Console.WriteLine("- Compiled! \n\n");
                System.IO.File.WriteAllBytes(outputfile, compiledEffect.GetEffectCode());
                Console.WriteLine(String.Format("- Parsing {0}\n- into {1}", inputfile, outputfile));
            }
            else
            {
                Console.WriteLine("- Errors Compiling File");
            }
        }


        static void SelfTest()
        {
            const string Folder = "..\\..\\..\\";
            string[] test1VertexShader = { Folder + "color_vs.hlsl", Folder + "color.vsu", "/vs" };
            string[] test1PixelShader = { Folder + "color_ps.hlsl", Folder + "color.psu", "/ps" };
            string[] test2VertexShader = { Folder + "texture_vs.hlsl", Folder + "texture.vsu", "/vs", };
            string[] test2PixelShader = { Folder + "texture_ps.hlsl", Folder + "texture.psu", "/ps" };
            //string[] testEffect = { Folder + "Effectje.fx", Folder + "effectje.bin", "/effect" };
            //string[] testAsmPixelShader = { Folder + "xps.asm", Folder + "xps.bin", "/xps", };

            Main(test1VertexShader);
            Main(test1PixelShader);
            Main(test2VertexShader);
            Main(test2PixelShader);
            
            //Main(testEffect);
            //Main(testAsmPixelShader);

            Console.WriteLine("Press a key.");
            Console.ReadKey();


        }
    }
}
