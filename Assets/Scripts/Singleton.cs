using UnityEngine;
using System.Collections;
using System;

/// <summary>
/// 单例类
/// </summary>
/// <typeparam name="T"></typeparam>
[System.Reflection.Obfuscation(ApplyToMembers = true, Exclude = true, Feature = "renaming")]
public class Singleton<T>
{
    /// <summary>
    /// 单例
    /// </summary>
    private static T m_instance = default(T);

    /// <summary>
    /// 单例
    /// </summary>
    public static T Instance
    {
        get
        {
            if (m_instance == null)
            {
                m_instance = (T)Activator.CreateInstance(typeof(T), true);
            }
            return m_instance;
        }
    }
}