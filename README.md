��Ŀ | ����
---|---
���� | ProtobufTools
��ǩ | ProtobufTools��Protobuf��Unity�����
��ע | ��Unity������
������� | 2016-12-24 00:41:52

## ʹ��

��������£�
- table
    - output ����ļ�
        - table_cs �������࣬�ͱ���Ӧ
        - table_data ������ݣ��ͱ���Ӧ
        - common_cs ��������
    - proto
        - ����Զ�����
            - `c_table_xxx`�ͻ��˱�
            - `s_table_xxx`��������
        - ������
            - `common_xxx`Ҫ�ֶ�д
    - table ����ļ�
    - tools ����

�������裺
1. �½�һ��Excel���ŵ�table�ļ��У�������Ӣ������
    1. Excel�ļ�������Ǳ��ϣ�ͬϵͳ�ı���Է�һ��Excel�ļ�����ߵ�һ��Sheet����һ������ı�
    1. �½�һ��Sheet������Ϊ`xx_name`��`xx`��ֵ�����ǣ��������Ϲ����Ĭ����`none_name`����
        1. `all` �������Ϳͻ��˶���
        1. `client` ���ͻ�����
        1. `server` ����������
        1. `none` �����ɱ�������˵����ע��
    1. ���һ��Sheet����ʽ��`����:����ʽ` 
1. �ر�����Ҫ��ı����ڵ�Excel�ļ�
1. ����`tools\config.py`�е�
    1. `self.unity_table_cs_path`
    1. `self.unity_table_data_path`
    1. `self.unity_common_cs_path`
1. ����`tools\run_type-client_copy-1.py`��log��`table_tools.log`
    1. ����˵��
        1. type ������ͣ������ͻ��˱�
        1. copy �Ƿ񿽱���Unity���̣��������ã�`��`
    1. ��Ӧ�����ݾ���Unity������
    1. ��������Unity���`Assets/JerryTable`�µ�ָ��
1. ʹ��
    1. `TableDesc.cs`ע��һ���±�
    1. `GameApp.cs`��
        1. `LoadTables();` ���ر�������Զ���ѡ���ô�Resources��AssetBundle����
        1. ���ұ����������Լ����壬����������ϼ�

---

### ����:����ʽ

sint32 | `Common.EnumTest` | `List.uint32` | `Common.StructTest` | ˵��
---|---|---|---|---
id | `enum_test` | `ulist` | `struct_test` |   	
all | client | all | all | none
ID | ö�� | int�б� | �ṹ | ˵��
10000 | 1 | `1|2|3` | `{1^21}` | 
10001 | 2 | 1 | `{2^2}` | 

���ϱ�`Test.xlsx`->`all_TestA`����
- ��ͷ��ǰ4��
    - ��1�У�����
    - ��2�У����ƣ������Ľ������ж�Ӧ���ֶ���
    - ��3�У�ʹ�÷�Χ����Sheet����������һ��
    - ��4�У�һ�����Ǳ�ע����һ����Ҳ������Ϊ�������Ӧ�ֶε�ע��
- ���� 

���ͣ�
- ��ͨ���ͣ�
    - `sint32`
    - `uint32`
    - `string`
    - `float`
- �û��Զ��壺��Ҫ�Լ�дproto�ļ����ŵ�proto�ļ��У������壬����`tools/UserDefineType.xlsx`�Ǽ�
    - ö�٣����ϱ��`Common.DegreeType`����дintֵ
    - �ṹ�����ϱ��`Common.Effect`�������`{x^y}`�ṹ˳�����
- �б�
    - `List.type`�����ϱ��`List.uint32`���ṹ`x|y`

`UserDefineType.xlsx`��

���� | �����ļ� | Ĭ��ֵ | ˵��
---|---|---|---
Common.EnumTest | `common_test.proto` | `ENUM_TEST_INVALID` |
Common.StructTest | `common_test.proto` | |	

```
package Common;

enum EnumTest
{
    ENUM_TEST_INVALID	= 0;
    ENUM_TEST_A			= 1;
    ENUM_TEST_B			= 2;
}

message StructTest
{
    optional EnumTest type	= 1 [default = ENUM_TEST_INVALID];
    optional float    val	= 2;
}
```

˵����ö��ֵ��Ҫ��дĬ��ֵ