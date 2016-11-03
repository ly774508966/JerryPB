using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

public class TableLoader : Singleton<TableLoader>
{
    /// <summary>
    /// 表格描述列表
    /// </summary>
    public List<TableDesc> tableDescList = new List<TableDesc>
    {
         new TableDesc("Scene",0,"scene","scene","scene"),//场景
         new TableDesc("Test",0,"test","test","test"),
         //new TableDesc("Testa",1,"testa","testa","test"),
    };

    /// <summary>
    /// 表格描述
    /// </summary>
    public class TableDesc
    {
        /// <summary>
        /// 构造
        /// </summary>
        /// <param name="tableName">表名</param>
        public TableDesc(string tableName)
        {
            this.tableName = tableName;
        }

        /// <summary>
        /// 构造
        /// </summary>
        /// <param name="tableName">表名</param>
        /// <param name="sheetIndex">Excel表页签ID，0开始</param>
        /// <param name="proto_message_name">proto消息名</param>
        /// <param name="outFileName">输出二进制文件名</param>
        /// <param name="excelName">Excel表名</param>
        public TableDesc(string tableName, int sheetIndex, string proto_message_name, string outFileName, string excelName)
        {
            this.tableName = tableName;
            this.excelName = excelName;
            this.sheetIndex = sheetIndex;
            this.proto_message_name = proto_message_name;
            this.outFileName = outFileName;
        }

        /// <summary>
        /// 表名
        /// </summary>
        public string tableName;

        /// <summary>
        /// Excel表名
        /// </summary>
        public string excelName;

        /// <summary>
        /// Excel表页签ID，0开始
        /// </summary>
        public int sheetIndex;

        /// <summary>
        /// proto消息名
        /// </summary>
        public string proto_message_name;

        /// <summary>
        /// 输出二进制文件名
        /// </summary>
        public string outFileName;
    }

    public TableLoader() { }

    public delegate void OnLoaded(TextAsset res);
    public OnLoaded loaded;

    /// <summary>
    /// 加载所有表格
    /// </summary>
    public void LoadTables()
    {
        foreach (TableDesc desc in tableDescList)
        {
            string name = desc.tableName.ToLower();
            if (!string.IsNullOrEmpty(desc.outFileName))
            {
                name = desc.outFileName;
            }

            //加载//TODO:暂时改成了本地加载
            TextAsset tex = Resources.Load<TextAsset>("Table/" + name);

            string tableMgrName = desc.tableName + "TableManager";

            Type type = Type.GetType(tableMgrName);
            if (type == null)
            {
                Debug.LogError(string.Format("{0} is Not Defined!", tableMgrName));
                continue;
            }

            PropertyInfo pinfo = null;
            while (type != null)
            {
                pinfo = type.GetProperty("Instance");

                if (pinfo != null)
                {
                    break;
                }

                type = type.BaseType;
            }

            if (pinfo == null)
            {
                continue;
            }

            MethodInfo instMethod = pinfo.GetGetMethod();
            if (instMethod == null)
            {
                continue;
            }

            System.Object tblMgrInst = instMethod.Invoke(null, null);
            if (tblMgrInst == null)
            {
                continue;
            }

            //TODO:加载完成回调
            Delegate dele = Delegate.CreateDelegate(typeof(OnLoaded), tblMgrInst, "OnResourceLoaded");
            loaded = (OnLoaded)dele;
            loaded(tex);
            //res.onLoaded += (Resource.OnLoaded)dele;
        }
    }
}

/// <summary>
/// 表格管理
/// </summary>
/// <typeparam name="TableArrayT">表组</typeparam>
/// <typeparam name="T">表</typeparam>
/// <typeparam name="K">键值</typeparam>
/// <typeparam name="T_1">具体表管理器类名</typeparam>
public abstract class TableManager<TableArrayT, T, K, T_1> : Singleton<T_1>, IEnumerable
{
    /// <summary>
    /// 表组
    /// </summary>
    public TableArrayT array;

    /// <summary>
    /// 键
    /// </summary>
    public K key;

    /// <summary>
    /// 数据
    /// </summary>
    public readonly Dictionary<K, T> dic = new Dictionary<K, T>();

    /// <summary>
    /// 获得枚举器
    /// </summary>
    /// <returns></returns>
    public IEnumerator GetEnumerator()
    {
        return dic.GetEnumerator();
    }

    /// <summary>
    /// 增加表
    /// </summary>
    /// <param name="table"></param>
    public void AddTable(T table)
    {
        K key = GetKey(table);

        if (dic.ContainsKey(key))
        {
            Debug.LogError(string.Format("{0}'s key {1} exist!", array, key));
        }
        else
        {
            dic.Add(key, table);
        }

        PostProcess(table);
    }

    /// <summary>
    /// 获取键值
    /// </summary>
    /// <param name="table"></param>
    /// <returns></returns>
    public abstract K GetKey(T table);

    /// <summary>
    /// 查表
    /// </summary>
    /// <param name="key">键值</param>
    /// <param name="tbl">返回的表</param>
    /// <returns></returns>
    public virtual bool TryGetValue(K key, out T tbl)
    {
        if (!dic.TryGetValue(key, out tbl))
        {
            return false;
        }

        return true;
    }

    /// <summary>
    /// 处理完一行数据
    /// </summary>
    /// <param name="table"></param>
    protected virtual void PostProcess(T table) { }

    /// <summary>
    /// 处理完所有行数据
    /// </summary>
    protected virtual void OnAllTablesLoaded() { }

    /// <summary>
    /// 表格加载成功回调
    /// </summary>
    /// <param name="res"></param>
    [System.Reflection.Obfuscation(Exclude = true, Feature = "renaming")]
    public void OnResourceLoaded(TextAsset res)
    {
        byte[] raw_data = res.bytes;

        byte[] data = new byte[raw_data.Length - 3];
        for (int i = 0, imax = raw_data.Length - 3; i < imax; data[i] = raw_data[i + 3], ++i) ;

        using (MemoryStream stream = new MemoryStream(data))
        {
            array = ProtoBuf.Serializer.Deserialize<TableArrayT>(stream);

            System.Type type = array.GetType();
            PropertyInfo pinfo = type.GetProperty("rows");
            if (pinfo != null)
            {
                MethodInfo mInfo = pinfo.GetGetMethod();
                if (mInfo != null)
                {
                    List<T> list = mInfo.Invoke(array, null) as List<T>;
                    if (list != null)
                    {
                        foreach (T table in list)
                        {
                            AddTable(table);
                        }
                    }
                }

                OnAllTablesLoaded();
            }
            else
            {
                Debug.LogError(string.Format("{0} does not has rows{1} exist!", array, key));
            }
        }
    }
}

/// <summary>
/// 场景表
/// </summary>
[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class SceneTableManager : TableManager<Table.scene_ARRAY, Table.scene, int, SceneTableManager>
{
    public override int GetKey(Table.scene table)
    {
        return table.id;
    }
}

[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestTableManager : TableManager<Table.test_ARRAY, Table.test, int, TestTableManager>
{
    public override int GetKey(Table.test table)
    {
        return table.id;
    }
}

[System.Reflection.Obfuscation(ApplyToMembers = false, Exclude = true, Feature = "renaming")]
public class TestaTableManager : TableManager<Table.testa_ARRAY, Table.testa, int, TestaTableManager>
{
    public override int GetKey(Table.testa table)
    {
        return table.id;
    }
}