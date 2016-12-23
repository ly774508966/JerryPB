using Jerry;

[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestATableManager : TableManager<Table.TestA_ARRAY, Table.TestA, int, TestATableManager>
{
    public override int GetKey(Table.TestA table)
    {
        return table.id;
    }
}

[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestBTableManager : TableManager<Table.TestB_ARRAY, Table.TestB, long, TestBTableManager>
{
    public static long MakeKey(int id1, int id2)
    {
        return (((long)id1) << 32) + id2;
    }

    public override long GetKey(Table.TestB table)
    {
        return MakeKey(table.id1, table.id2);
    }
}