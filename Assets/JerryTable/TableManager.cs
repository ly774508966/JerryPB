using UnityEngine;
using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace Jerry
{
    public class TableLoader : TableSingleton<TableLoader>
    {
        public delegate void OnLoaded(TextAsset res);

        public OnLoaded LoadTable(string tableName)
        {
            if (string.IsNullOrEmpty(tableName))
            {
                return null;
            }

            string tableMgrName = tableName + "TableManager";
            Type type = Type.GetType(tableMgrName);
            if (type == null)
            {
                Debug.LogError(string.Format("{0} is Not Defined!", tableMgrName));
                return null;
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
                return null;
            }

            MethodInfo instMethod = pinfo.GetGetMethod();
            if (instMethod == null)
            {
                return null;
            }

            System.Object tblMgrInst = instMethod.Invoke(null, null);
            if (tblMgrInst == null)
            {
                return null;
            }

            Delegate dele = Delegate.CreateDelegate(typeof(OnLoaded), tblMgrInst, "OnResourceLoaded");
            return (OnLoaded)dele;
        }
    }

    /// <summary>
    /// 表格管理
    /// </summary>
    /// <typeparam name="TableArrayT">表组</typeparam>
    /// <typeparam name="T">表</typeparam>
    /// <typeparam name="K">键值</typeparam>
    /// <typeparam name="T_1">具体表管理器类名</typeparam>
    public abstract class TableManager<TableArrayT, T, K, T_1> : TableSingleton<T_1>, IEnumerable
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
}