using UnityEditor;
using System.IO;
using System;
using System.Diagnostics;

/// <summary>
/// 打表工具
/// </summary>
public class TablePacker : EditorWindow
{
    #region 配置信息

    /// <summary>
    /// table所在文件夹名称
    /// </summary>
    private static string m_strTableFileName = "table";

    /// <summary>
    /// 是否更新SVN
    /// </summary>
    private static bool m_bIsUpdateSVN = false;

    /// <summary>
    /// <para>生成的表格资源存储地址</para>
    /// <para>TODO:现在是本地加载，地址暂时放在Resources里</para>
    /// </summary>
    private static string m_strStreamingPath = "/Assets/Resources/Table/";//"/Assets/StreamingAssets/Table/";

    /// <summary>
    /// 生成的表格cs存储路径
    /// </summary>
    private static string m_strTableProtoPath = "/Assets/Scripts/Table/proto_gen/";

    /// <summary>
    /// 生成的消息cs存储路径
    /// </summary>
    private static string m_strMsgProtoPath = "/Assets/Scripts/MSG/proto_gen/";

    #endregion 配置信息

    /// <summary>
    /// 工程所在目录，是Assets的父目录
    /// </summary>
    private static string dir;

    /// <summary>
    /// table路径
    /// </summary>
    private static string tablePath;

    /// <summary>
    /// table_output路径
    /// </summary>
    private static string table_outputPath;

    /// <summary>
    /// table_tools路径
    /// </summary>
    private static string table_toolsPath;

    /// <summary>
    /// proto路径
    /// </summary>
    private static string protoPath;

    /// <summary>
    /// 打出的表格文件存储路径
    /// </summary>
    private static string table_outputStreamingPath;

    /// <summary>
    /// 执行外部程序
    /// </summary>
    /// <param name="processName"></param>
    /// <param name="param"></param>
    /// <returns></returns>
    private static bool CallProcess(string processName, string param)
    {
        ProcessStartInfo process = new ProcessStartInfo
        {
            CreateNoWindow = false,
            UseShellExecute = false,
            RedirectStandardError = true,
            RedirectStandardOutput = true,
            FileName = processName,
            Arguments = param,
        };

        UnityEngine.Debug.Log(processName + " " + param);

        Process p = Process.Start(process);
        p.StandardOutput.ReadToEnd();
        p.WaitForExit();

        string error = p.StandardError.ReadToEnd();
        if (!string.IsNullOrEmpty(error))
        {
            UnityEngine.Debug.LogError(processName + " " + param + "  ERROR! " + "\n" + error);

            string output = p.StandardOutput.ReadToEnd();
            if (!string.IsNullOrEmpty(output))
            {
                UnityEngine.Debug.Log(output);
            }
            return false;
        }
        return true;
    }

    /// <summary>
    /// 生成cs文件
    /// </summary>
    /// <param name="name"></param>
    /// <returns></returns>
    private static bool ProcessProto(string name, string path)
    {
        string param = string.Format("-i:{0}.proto -o:{0}.cs -p:detectMissing", name);
        if (CallProcess("protogen.exe", param))
        {
            if (!Directory.Exists(dir + path))
            {
                Directory.CreateDirectory(dir + path);
            }
            File.Copy(@".\" + name + ".cs", dir + path + name + ".cs", true);
            File.Delete(@".\" + name + ".cs");
            return true;
        }

        return false;
    }

    /// <summary>
    /// 生成Python文件
    /// </summary>
    /// <param name="name"></param>
    private static void GeneratePythonFile(string name)
    {
        string param = string.Format("-I. --python_out=. {0}.proto", name);
        CallProcess("protoc.exe", param);
    }

    /// <summary>
    /// 表格打成二进制文件
    /// </summary>
    [MenuItem("Assets/Pack All Tables To Binary")]
    public static void PackTables()
    {
        dir = Directory.GetCurrentDirectory();

        tablePath = dir + string.Format(@"\{0}\table\", m_strTableFileName);
        table_outputPath = dir + string.Format(@"\{0}\table_output\", m_strTableFileName);
        table_toolsPath = dir + string.Format(@"\{0}\table_tools\", m_strTableFileName);
        protoPath = dir + string.Format(@"\{0}\proto\", m_strTableFileName);

        //本地化内容收集文件
        string strLocalizeTableWorldCollectPath = table_outputPath + "chinese.txt";
        if (File.Exists(strLocalizeTableWorldCollectPath))
        {
            File.Delete(strLocalizeTableWorldCollectPath);
        }

        table_outputStreamingPath = dir + @m_strStreamingPath;

        if (!Directory.Exists(table_outputStreamingPath))
        {
            Directory.CreateDirectory(table_outputStreamingPath);
        }

        if (m_bIsUpdateSVN)
        {
            Directory.SetCurrentDirectory(tablePath);
            Process p = Process.Start("TortoiseProc.exe", @"/command:update /path:"".\"" /closeonend:1");
            p.WaitForExit();

            Directory.SetCurrentDirectory(table_toolsPath);
            p = Process.Start("TortoiseProc.exe", @"/command:update /path:"".\"" /closeonend:1");
            p.WaitForExit();

            Directory.SetCurrentDirectory(protoPath);
            p = Process.Start("TortoiseProc.exe", @"/command:update /path:"".\"" /closeonend:1");
            p.WaitForExit();
        }

        try
        {
            Directory.SetCurrentDirectory(protoPath);

            GeneratePythonFile("c_table_*");

            GeneratePythonFile("common_*");

            Directory.SetCurrentDirectory(table_toolsPath);

            Environment.SetEnvironmentVariable("DEFAULT_PROTO_PREFIX", "c_table_");

            Environment.SetEnvironmentVariable("DEFAULT_OUTPUT_PREFIX", "");

            foreach (TableLoader.TableDesc desc in TableLoader.Instance.tableDescList)
            {
                string param = "";
                string bytesName = "";
                if (string.IsNullOrEmpty(desc.outFileName))
                {
                    param = string.Format(@"table_writer.py ""{0}""", desc.tableName);
                    bytesName = desc.tableName.ToLower();
                }
                else
                {
                    param = string.Format(@"table_writer.py -s {0} -m {1} -o {2} {3}", desc.sheetIndex, desc.proto_message_name, desc.outFileName, desc.excelName);
                    bytesName = desc.outFileName;
                }

                UnityEngine.Debug.LogError(Directory.GetCurrentDirectory());
                UnityEngine.Debug.LogError(param);

                if (CallProcess("python.exe", param))
                {
                    File.Copy(table_outputPath + bytesName + ".tbl", table_outputStreamingPath + bytesName + ".bytes", true);
                    File.Delete(table_outputPath + bytesName + ".tbl");
                }
                else
                {
                    Directory.SetCurrentDirectory(dir);
                    return;
                }
            }

            Directory.SetCurrentDirectory(dir);

            UnityEngine.Debug.Log("(.)  Success  (.)");
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);
            Directory.SetCurrentDirectory(dir);
        }
    }

    [MenuItem("Assets/Compile Table Proto File")]
    public static void ComplieTableProtoFile()
    {
        dir = Directory.GetCurrentDirectory();
        protoPath = dir + string.Format(@"\{0}\proto\", m_strTableFileName);

        Directory.SetCurrentDirectory(protoPath);

        try
        {
            if (m_bIsUpdateSVN)
            {
                Process p = Process.Start("TortoiseProc.exe", @"/command:update /path:"".\"" /closeonend:1");
                p.WaitForExit();
            }

            string[] fileNames = Directory.GetFiles(@".\");

            foreach (string fileName in fileNames)
            {
                if (fileName.Contains("common_") && fileName.Contains(".proto"))
                {
                    string name = fileName.Substring(0, fileName.LastIndexOf('.'));
                    name = name.Replace(".\\", "");
                    if (ProcessProto(name, m_strMsgProtoPath) == false)
                    {
                        Directory.SetCurrentDirectory(dir);
                        return;
                    }
                }
            }

            foreach (string fileName in fileNames)
            {
                if (fileName.Contains("c_table_") && fileName.Contains(".proto"))
                {
                    string name = fileName.Substring(0, fileName.LastIndexOf('.'));
                    name = name.Replace(".\\", "");
                    if (ProcessProto(name, m_strTableProtoPath) == false)
                    {
                        Directory.SetCurrentDirectory(dir);
                        return;
                    }
                }
            }

            CallProcess("python.exe", protoPath + "XMLDeleter.py " + dir + @m_strTableProtoPath);
            Directory.SetCurrentDirectory(dir);

            UnityEngine.Debug.Log("(.)   Success   (.)");
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);
            Directory.SetCurrentDirectory(dir);
        }
    }

    [MenuItem("Assets/Complie MSG Proto File")]
    public static void ComplieMSGProtoFile()
    {
        dir = Directory.GetCurrentDirectory();
        protoPath = dir + string.Format(@"\{0}\proto\", m_strTableFileName);

        Directory.SetCurrentDirectory(protoPath);

        try
        {
            if (m_bIsUpdateSVN)
            {
                Process p = Process.Start("TortoiseProc.exe", @"/command:update /path:"".\"" /closeonend:1");
                p.WaitForExit();
            }

            string[] fileNames = Directory.GetFiles(@".\");
            foreach (string fileName in fileNames)
            {
                // 只读command_user_  common_
                if ((fileName.Contains("command_user") && fileName.Contains(".proto"))
                    || (fileName.Contains("common_") && fileName.Contains(".proto")))
                {
                    string name = fileName.Substring(0, fileName.LastIndexOf('.'));

                    ProcessProto(name, m_strMsgProtoPath);
                }
            }
            CallProcess("python.exe", protoPath + "XMLDeleter.py " + dir + @m_strMsgProtoPath);
            Directory.SetCurrentDirectory(dir);
            UnityEngine.Debug.Log("(.)   Success  (.)");
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);

            Directory.SetCurrentDirectory(dir);
        }
    }
}