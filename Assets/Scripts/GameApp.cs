using UnityEngine;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        TableLoader.Instance.LoadTables();
    }

    void Start()
    {
        Table.Scene scene = null;

        if (SceneTableManager.Instance.TryGetValue(10000, out scene))
        {
            Debug.LogError(string.Format("id={0}", scene.id));
            Debug.LogError(string.Format("degree_type={0}", scene.degree_type));
            Debug.LogError(string.Format("effect.type={0}", scene.effect.type));
            Debug.LogError(string.Format("effect.val={0}", scene.effect.val));

            int idx = 0;
            foreach (uint i in scene.ulist)
            {
                Debug.LogError(string.Format("-{0}={1}", idx++, i));
            }
        }
        else
        {
            Debug.LogError("not exist");
        }
    }
}