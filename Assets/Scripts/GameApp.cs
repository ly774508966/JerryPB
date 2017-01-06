using UnityEngine;
using System.Collections;
using Jerry;
using System;

public class GameApp : MonoBehaviour
{
#if TableFromAB
    private bool _isJABOK = false;
#endif
    private bool _isTableOK = false;

    void Awake()
    {
        JerryDebug.Inst.Set(true, false, false, true, false);

#if TableFromAB
        this.StartCoroutine(InitializeJAB(() =>
        {
            _isJABOK = true;

            this.StartCoroutine(MyTableLoader.Inst.LoadTables(() =>
            {
                _isTableOK = true;
            }));
        }));
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
#if TableFromAB
        yield return new WaitUntil(() => this._isJABOK == true);
#endif
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

#if TableFromAB
    private IEnumerator InitializeJAB(Action callback = null)
    {
        JABMgr.Set(JABUtil.JPlatformName.Android);

        JABLoadManifestOperation request = JABMgr.LoadManifest();
        if (request != null)
        {
            yield return this.StartCoroutine(request);
        }

        if (callback != null)
        {
            callback();
        }
    }
#endif
}