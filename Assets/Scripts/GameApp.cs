using UnityEngine;
using Jerry;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        JerryDebug.Set(true, false, false, true, typeof(ProtoBuf.ProtoMemberAttribute));
        TableMgr.Instance.LoadTables();
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
}