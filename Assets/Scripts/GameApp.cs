using UnityEngine;
using Jerry;
using System.IO;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        JerryDebug.Set(true, false, false, true, typeof(ProtoBuf.ProtoMemberAttribute));
        LoadTables();
    }

    void Start()
    {
        Table.TestA testA = null;
        if (TestATableManager.Instance.TryGetValue(10000, out testA))
        {
            JerryDebug.LogInfo(testA, true);
        }
        else
        {
            Debug.LogError("not exist");
        }

        Table.TestB testB = null;
        if (TestBTableManager.Instance.TryGetValue(TestBTableManager.MakeKey(10000, 10000), out testB))
        {
            JerryDebug.LogInfo(testB, true);
        }
        else
        {
            Debug.LogError("not exist");
        }
    }

    private void LoadTables()
    {
        string path = Application.dataPath + "/Resources/Table/";
        string[] files = Directory.GetFiles(path);
        foreach (string file in files)
        {
            string fileName = Path.GetFileName(file);
            if (fileName.EndsWith(".bytes") && fileName.StartsWith("c_table_"))
            {
                string fileNameWithoutExtension = Path.GetFileNameWithoutExtension(file);

                TextAsset tex = Resources.Load<TextAsset>("Table/" + fileNameWithoutExtension);
                
                TableLoader.OnLoaded func = TableLoader.Instance.LoadTable(fileNameWithoutExtension.Substring("c_table_".Length));
                if (func != null)
                {
                    func(tex);
                }
            }
        }
    }
}