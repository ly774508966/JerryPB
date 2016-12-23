using UnityEditor;
using System.IO;
using System.Diagnostics;

namespace Jerry
{
    /// <summary>
    /// 打表工具
    /// </summary>
    public class TablePacker : Editor
    {
        #region 配置信息

        private static string _toolsPath = "/table/tools/";

        #endregion 配置信息

        /// <summary>
        /// 工程所在目录，是Assets的父目录
        /// </summary>
        private static string dir;

        [MenuItem("Assets/JerryTable/PackAndCopy")]
        public static void PackAndCopyTables()
        {
            DoPackTable(true, true, "PackAndCopyTables");
        }

        [MenuItem("Assets/JerryTable/Pack")]
        public static void PackTables()
        {
            DoPackTable(true, false, "PackTables");
        }

        [MenuItem("Assets/JerryTable/Copy")]
        public static void CopyTables()
        {
            DoPackTable(false, true, "CopyTables");
        }

        private static void DoPackTable(bool pack = true, bool copy = false, string flag = "")
        {
            dir = Directory.GetCurrentDirectory();
            string toolsPath = dir + _toolsPath;
            try
            {
                Directory.SetCurrentDirectory(toolsPath);
                CallProcess("python.exe", string.Format("{0}{1} type-{2}_copy-{3}", toolsPath, "run.py", pack ? "client" : "none", copy ? "1" : "0"));
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

            UnityEngine.Debug.Log(flag + " Finish " + System.DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss"));
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
    }
}