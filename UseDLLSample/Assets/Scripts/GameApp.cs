using UnityEngine;
using System.Collections;
using Jerry;

public class GameApp : MonoBehaviour
{
    private bool _isTableOK = false;

    void Awake()
    {
        JerryDebug.Inst.Set(true, false, false, true, false);

#if TableFromAB
        JABMgr.Init((success) =>
        {
            if (success)
            {
                this.StartCoroutine(MyTableLoader.Inst.LoadTables(() =>
                {
                    _isTableOK = true;
                }));
            }
        }, JABUtil.Platform.Android);
#else
        this.StartCoroutine(MyTableLoader.Inst.LoadTables(() =>
        {
            _isTableOK = true;
        }));
#endif
    }

    void Start()
    {
        this.StartCoroutine(WaitResOK());
    }

    private IEnumerator WaitResOK()
    {
        yield return new WaitUntil(() => this._isTableOK == true);
        GameStart();
    }

    private void GameStart()
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