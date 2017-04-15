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

        [MenuItem("Assets/JerryPB/PackAndCopyTables")]
        public static void PackAndCopyTables()
        {
            ExeCmd(1, true, "PackAndCopyTables");
        }

        [MenuItem("Assets/JerryPB/PackTables")]
        public static void PackTables()
        {
            ExeCmd(1, false, "PackTables");
        }

        [MenuItem("Assets/JerryPB/CopyTables")]
        public static void CopyTables()
        {
            ExeCmd(0, true, "CopyTables");
        }

        /// <summary>
        /// 打包协议
        /// </summary>
        [MenuItem("Assets/JerryPB/PackCommand")]
        public static void PackCommand()
        {
            ExeCmd(2, true, "PackCommand");
        }

        private static void ExeCmd(int cmd = 0, bool copy = false, string flag = "")
        {
            dir = Directory.GetCurrentDirectory();
            string toolsPath = dir + _toolsPath;
            try
            {
                string cmdFile = "run.py";
                string cmdPar = "";
                switch (cmd)
                {
                    case 0:
                    case 1:
                        {
                            cmdFile = "run.py";
                            cmdPar = string.Format(" type-{0}_copy-{1}", cmd == 0 ? "none" : "client", copy ? "1" : "0");
                        }
                        break;
                    case 2:
                        {
                            cmdFile = "packCmd.py";
                            cmdPar = "";
                        }
                        break;
                }
                
                Directory.SetCurrentDirectory(toolsPath);
                CallProcess("python.exe", string.Format("{0}{1}{2}", toolsPath, cmdFile, cmdPar));
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