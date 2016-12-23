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
        Table.Scene scene = null;
        
        if (SceneTableManager.Instance.TryGetValue(10000, out scene))
        {
            JerryDebug.LogInfo(scene, true);
        }
        else
        {
            Debug.LogError("not exist");
        }
    }
}