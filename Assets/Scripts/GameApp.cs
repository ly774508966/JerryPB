using UnityEngine;
using System.Collections;

public class GameApp : MonoBehaviour
{
    void Awake()
    {
        TableLoader.Instance.LoadTables();
    }

    void Start()
    {
        Table.scene scene = null;

        if (SceneTableManager.Instance.TryGetValue(10000, out scene))
        {
            Debug.LogError(string.Format("id={0}", scene.id));
            Debug.LogError(string.Format("type={0}", scene.scene_type));
            Debug.LogError(string.Format("desc={0}", scene.des));
            Debug.LogError(string.Format("num_float={0}", scene.num_float));
            
            Debug.LogError(string.Format("num_uint32", scene.num_uint32));
            int idx = 0;
            foreach (uint i in scene.num_uint32)
            {
                Debug.LogError(string.Format("-{0}={1}", idx++, i));
            }

            Debug.LogError(string.Format("res_output"));
            
            Debug.LogError(string.Format("-type={0}", scene.res.type));
            Debug.LogError(string.Format("-des={0}", scene.res.des));
            Debug.LogError(string.Format("param_list"));
            idx = 0;
            foreach (long i in scene.res.param_list)
            {
                Debug.LogError(string.Format("--{0}={1}", idx++, i));
            }
        }
        else
        {
            Debug.LogError("not exist");
        }
    }
}
