using UnityEditor;
using System.IO;
using System.Diagnostics;

/// <summary>
/// 打表工具
/// </summary>
public class TablePacker : Editor
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

    [MenuItem("Assets/NewPack")]
    public static void NewPack()
    {
        dir = Directory.GetCurrentDirectory();
        string toolsPath = dir + string.Format(@"\{0}\tools\", m_strTableFileName);
        try
        {
            Directory.SetCurrentDirectory(toolsPath);
            CallProcess("python.exe", toolsPath + "run_type-client.py");
            Directory.SetCurrentDirectory(dir);
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);
            Directory.SetCurrentDirectory(dir);
        }
    }
}