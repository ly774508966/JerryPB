using Jerry;
using System.Collections.Generic;
using UnityEngine;

public class TableMgr : TableSingleton<TableMgr>
{
    public TableMgr()
    {
        TableLoader.Instance.loaders = new List<TableLoader.Loader>()
        {
            new TableLoader.Loader("Table/c_table_TestA", TestATableManager.Instance.OnResourceLoaded),
            new TableLoader.Loader("Table/c_table_TestB", TestBTableManager.Instance.OnResourceLoaded),
        };
    }

    public void LoadTables()
    {
        foreach(TableLoader.Loader loader in TableLoader.Instance.loaders)
        {
            TextAsset tex = Resources.Load<TextAsset>(loader.resPath);
            if (loader.callBack != null)
            {
                loader.callBack(tex);
            }
        }
    }
}

public class TestATableManager : TableManager<Table.TestA_ARRAY, Table.TestA, int, TestATableManager>
{
    protected override int GetKey(Table.TestA table)
    {
        return table.id;
    }
}

public class TestBTableManager : TableManager<Table.TestB_ARRAY, Table.TestB, long, TestBTableManager>
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