using UnityEngine;
using Jerry;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        JerryDebug.Set(true, false, false, true, typeof(ProtoBuf.ProtoMemberAttribute));
        TableLoader.Instance.LoadTables();
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
    }
}