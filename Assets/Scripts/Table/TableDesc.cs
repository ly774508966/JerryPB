[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestATableManager : TableManager<Table.TestA_ARRAY, Table.TestA, int, TestATableManager>
{
    public override int GetKey(Table.TestA table)
    {
        return table.id;
    }
}

[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestBTableManager : TableManager<Table.TestB_ARRAY, Table.TestB, int, TestBTableManager>
{
    public override int GetKey(Table.TestB table)
    {
        return table.id1;
    }
}