using UnityEngine;
using System.Collections;
using Jerry;

public class GameApp : MonoBehaviour
{
    private bool _isTableOK = false;

    void Awake()
    {
        JerryDebug.Set(true, false, false, true, typeof(ProtoBuf.ProtoMemberAttribute));

        this.StartCoroutine(TableMgr.Inst.LoadTables(() =>
        {
            _isTableOK = true;
        }));
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
            JerryDebug.LogInfo(testA, true);
        }
        else
        {
            Debug.LogError("not exist");
        }

        Table.TestB testB = null;
        if (TestBTblMgr.Inst.TryGetValue(TestBTblMgr.MakeKey(10000, 10000), out testB))
        {
            JerryDebug.LogInfo(testB, true);
        }
        else
        {
            Debug.LogError("not exist");
        }
    }
}