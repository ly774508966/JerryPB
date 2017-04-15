using UnityEngine;
using Jerry;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        JerryDebug.Inst.Set(true, false, false, true, false);

#if TableFromAB
        JABMgr.Init((success) =>
        {
            if (success)
            {
                MyTableLoader.Inst.LoadTables(() =>
                {
                    GameLogicStart();
                });
            }
        }, JABUtil.Platform.Android);
#else
        MyTableLoader.Inst.LoadTables(() =>
        {
            GameStart();
        });
#endif
    }

    void Start()
    {
    }

    private void GameLogicStart()
    {
        Table.TestA testA = null;
        if (TestATblMgr.Inst.TryGetValue(10000, out testA))
        {
            JerryDebug.Inst.LogInfo(testA, JerryDebug.LogChannel.Channel_All, true);
        }
        else
        {
            Debug.LogError("not exist");
        }

        Table.TestB testB = null;
        if (TestBTblMgr.Inst.TryGetValue(TestBTblMgr.MakeKey(10000, 10000), out testB))
        {
            JerryDebug.Inst.LogInfo(testB, JerryDebug.LogChannel.Channel_All, true);
        }
        else
        {
            Debug.LogError("not exist");
        }
    }
}