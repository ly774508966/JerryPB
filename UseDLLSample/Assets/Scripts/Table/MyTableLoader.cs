using Jerry;
using UnityEngine;
using System;
using System.Collections;

public class MyTableLoader : TableLoader<MyTableLoader>
{
    public MyTableLoader()
        : base()
    {
#if TableFromAB
        AddLoader(new Loader(TestATblMgr.Inst, "c_table_TestA"));
        AddLoader(new Loader(TestBTblMgr.Inst, "c_table_TestB"));
#else
        AddLoader(new Loader(TestATblMgr.Inst, "Table/c_table_TestA"));
        AddLoader(new Loader(TestBTblMgr.Inst, "Table/c_table_TestB"));
#endif
    }

    public override IEnumerator LoadTables(Action allTblComplete = null)
    {
        yield return base.LoadTables(allTblComplete);

        foreach (Loader loader in _loaders)
        {
            //Load tables start
#if TableFromAB
            JABMgr.LoadAssetAsync<TextAsset>("table_bundle", loader.resPath, loader.loadedCallback);
#else
            TextAsset tex = Resources.Load<TextAsset>(loader.resPath);
            if (loader.loadedCallback != null)
            {
                loader.loadedCallback(tex);
            }
#endif
            //Load tables end
        }

        yield return this.WaitAllTableLoaded();
    }
}

public class TestATblMgr : TableManager<Table.TestA_ARRAY, Table.TestA, int, TestATblMgr>
{
    protected override int GetKey(Table.TestA table)
    {
        return table.id;
    }
}

public class TestBTblMgr : TableManager<Table.TestB_ARRAY, Table.TestB, long, TestBTblMgr>
{
    public static long MakeKey(int id1, int id2)
    {
        return (((long)id1) << 32) + id2;
    }

    protected override long GetKey(Table.TestB table)
    {
        return MakeKey(table.id1, table.id2);
    }
}