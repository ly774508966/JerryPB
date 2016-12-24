using Jerry;
using System.Collections.Generic;
using UnityEngine;
using System;
using System.Collections;

public class TableMgr : TableSingleton<TableMgr>
{
    private Action _allTblComplete = null;
    private int _cnt = 0;

    public TableMgr()
    {
        TableLoader.Inst.loaders = new List<TableLoader.Loader>()
        {
            new TableLoader.Loader("Table/c_table_TestA", TestATblMgr.Inst.OnResLoaded, ()=>
            {
                TestATblMgr.Inst.onTblComplete += () =>
                {
                    this._cnt--;
                };
            }),
            new TableLoader.Loader("Table/c_table_TestB", TestBTblMgr.Inst.OnResLoaded, ()=>
            {
                TestBTblMgr.Inst.onTblComplete += ()=>
                {
                    this._cnt--;
                };
            }),
        };
    }

    public IEnumerator LoadTables(Action allTblComplete = null)
    {
        this._cnt = 0;
        this._allTblComplete = allTblComplete;
        foreach (TableLoader.Loader loader in TableLoader.Inst.loaders)
        {
            if (this._allTblComplete != null)
            {
                this._cnt++;
            }

            TextAsset tex = Resources.Load<TextAsset>(loader.resPath);
            if (loader.callBack != null)
            {
                loader.callBack(tex);
            }
        }

        if (this._allTblComplete != null)
        {
            yield return new WaitUntil(() => this._cnt == 0);

            if (this._allTblComplete != null)
            {
                this._allTblComplete();
            }
        }
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