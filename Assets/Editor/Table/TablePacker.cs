using UnityEditor;
using System.IO;
using System.Diagnostics;
using UnityEngine;
using System.Collections.Generic;

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

    private static string _unityCommonCSPath = Application.dataPath + "/Scripts/MSG/proto_gen/";
    private static string _unityTableCSPath = Application.dataPath + "/Scripts/Table/proto_gen/";
    private static string _unityTableDataPath = Application.dataPath + "/Resources/Table/";

    #endregion 配置信息

    /// <summary>
    /// 工程所在目录，是Assets的父目录
    /// </summary>
    private static string dir;

    [MenuItem("Assets/PackAndCopyTables")]
    public static void PackAndCopyTables()
    {
        DoPackTable(true, "PackAndCopyTables");
    }

    [MenuItem("Assets/PackTables")]
    public static void PackTables()
    {
        DoPackTable(false, "PackTables");
    }

    [MenuItem("Assets/CopyTables")]
    public static void CopyTables()
    {
        CopyDirectory(_outputCommonCSPath, _unityCommonCSPath, new List<string> { "common_", ".cs" });
        CopyDirectory(_outputTableCSPath, _unityTableCSPath, new List<string> { "c_table_", ".cs" });
        CopyDirectory(_outputTableDataPath, _unityTableDataPath, new List<string> { "c_table_", ".bytes" });
        AssetDatabase.SaveAssets();
        AssetDatabase.Refresh();
        UnityEngine.Debug.Log("CopyTables Finish");
    }

    private static void DoPackTable(bool copy = false, string flag = "")
    {
        dir = Directory.GetCurrentDirectory();
        string toolsPath = dir + _toolsPath;
        try
        {
            Directory.SetCurrentDirectory(toolsPath);
            CallProcess("python.exe", string.Format("{0}{1} type-client_copy-{2}", toolsPath, "run_type-client_copy-0.py", copy ? "1" : "0"));
            Directory.SetCurrentDirectory(dir);
        }
        catch (System.Exception ex)
        {
            UnityEngine.Debug.LogError(ex);
            Directory.SetCurrentDirectory(dir);
        }

        if (copy)
        {
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
        }
        UnityEngine.Debug.Log(flag + " Finish");
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

    /// <summary>
    /// 文件名过滤
    /// </summary>
    /// <param name="fileName"></param>
    /// <param name="fileNameFilter"></param>
    /// <param name="include"></param>
    /// <returns>通过</returns>
    private static bool FileNameFilter(string fileName, List<string> fileNameFilter = null, bool include = true)
    {
        if (fileNameFilter == null
            || fileNameFilter.Count <= 0
            || string.IsNullOrEmpty(fileName))
        {
            return true;
        }
        foreach (string filter in fileNameFilter)
        {
            if (include)
            {
                if (!fileName.Contains(filter))
                {
                    return false;
                }
            }
            else
            {
                if (fileName.Contains(filter))
                {
                    return false;
                }
            }
        }
        return true;
    }

    private static void CopyDirectory(string pathFrom, string pathTo, List<string> fileNameFilter = null, List<string> fileNameNotFilter = null)
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
            if (FileNameFilter(fileName, fileNameFilter, true) == false || FileNameFilter(fileName, fileNameNotFilter, false) == false)
            {
                continue;
            }
            File.Copy(pathFrom + "/" + fileName, pathTo + "/" + fileName);
        }

        string[] directs = Directory.GetDirectories(pathFrom);
        string directName;
        foreach (string direct in directs)
        {
            directName = Path.GetFileName(direct);
            CopyDirectory(direct, pathTo + "/" + directName, fileNameFilter, fileNameNotFilter);
        }
    }
}