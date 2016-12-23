using UnityEditor;
using System.IO;
using System.Diagnostics;
using UnityEngine;

/// <summary>
/// 打表工具
/// </summary>
public class TablePacker : Editor
{
    #region 配置信息

    private static string _toolsPath = "/table/tools/";

    private static string _outputCommonCSPath = Application.dataPath + "/../table/output/common_cs/";

    private static string _outputTableCSPath = Application.dataPath + "/../table/output/table_cs/";

    private static string _outputTableDataPath = Application.dataPath + "/../table/output/table_data/";

    #endregion 配置信息

    /// <summary>
    /// 工程所在目录，是Assets的父目录
    /// </summary>
    private static string dir;

    [MenuItem("Assets/CopyTables")]
    public static void CopyTables()
    {
        dir = Directory.GetCurrentDirectory();
        string toolsPath = dir + _toolsPath;
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

    private static void CopyDirectory(string pathFrom, string pathTo)
    {
        if (string.IsNullOrEmpty(pathFrom) ||
            string.IsNullOrEmpty(pathTo))
        {
            return;
        }

        if (Directory.Exists(pathFrom) == false)
        {
            return;
        }

        if (Directory.Exists(pathTo))
        {
            Directory.Delete(pathTo, true);
        }
        Directory.CreateDirectory(pathTo);

        string[] files = Directory.GetFiles(pathFrom);
        string fileName;
        foreach (string file in files)
        {
            fileName = Path.GetFileName(file);
            File.Copy(pathFrom + "/" + fileName, pathTo + "/" + fileName);
        }

        string[] directs = Directory.GetDirectories(pathFrom);
        string directName;
        foreach (string direct in directs)
        {
            directName = Path.GetFileName(direct);
            CopyDirectory(direct, pathTo + "/" + directName);
        }
    }

    [MenuItem("Assets/PackTables")]
    public static void PackTables()
    {
        dir = Directory.GetCurrentDirectory();
        string toolsPath = dir + _toolsPath;
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