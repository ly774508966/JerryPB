﻿using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Reflection;
using System;

namespace Jerry
{
    public class TableLoader : TableSingleton<TableLoader>
    {
        public delegate void OnLoaded(TextAsset res);

        public class Loader
        {
            public string resPath;
            public OnLoaded callBack;

            public Loader(string resPath, OnLoaded callBack, Action handleBack)
            {
                this.resPath = resPath;
                this.callBack = callBack;
                if (handleBack != null)
                {
                    handleBack();
                }
            }
        }

        public List<Loader> loaders = new List<Loader>();
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
        protected TableArrayT array;

        /// <summary>
        /// 键
        /// </summary>
        protected K key;

        /// <summary>
        /// 数据
        /// </summary>
        protected readonly Dictionary<K, T> dic = new Dictionary<K, T>();

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
        protected void AddTable(T table)
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
        protected abstract K GetKey(T table);

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

        public Action onTblComplete = null;

        /// <summary>
        /// 处理完一行数据
        /// </summary>
        /// <param name="table"></param>
        protected virtual void PostProcess(T table) { }

        /// <summary>
        /// 处理完所有行数据
        /// </summary>
        public virtual void OnTblComplete()
        {
            if (onTblComplete != null)
            {
                onTblComplete();
            }
        }

        /// <summary>
        /// 表格加载成功回调
        /// </summary>
        /// <param name="res"></param>
        public void OnResLoaded(TextAsset res)
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

                    OnTblComplete();
                }
                else
                {
                    Debug.LogError(string.Format("{0} does not has rows{1} exist!", array, key));
                }
            }
        }
    }
}