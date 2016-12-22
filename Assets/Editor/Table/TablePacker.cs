using UnityEditor;
using System.IO;
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
        UnityEngine.Debug.LogError(param + " " + path);
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

    [MenuItem("Assets/NewPack")]
    public static void NewPack()
    {
        dir = Directory.GetCurrentDirectory();
        string toolsPath = dir + string.Format(@"\{0}\tools\", m_strTableFileName);
        try
        {
            Directory.SetCurrentDirectory(toolsPath);
            CallProcess("python.exe", toolsPath + "run.py");
            Directory.SetCurrentDirectory(dir);
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);
            Directory.SetCurrentDirectory(dir);
        }
    }
}