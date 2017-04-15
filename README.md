��Ŀ | ����
---|---
���� | JerryPB
��ǩ | Protobuf��Unity�����
��ע | ��Unity��������[Github](https://github.com/laijingfeng/JerryPB)
���� | 2017-04-15 12:08:46

[TOC]

# ʹ��

## ʹ�ò��裺��������������̣�����DLL���̺�Դ�빤�̣�

- �ѹ��߷ŵ�`Assets`ƽ��Ŀ¼������˵����`����:����`
- `Unity`���̵�`Plugins`�����`JerryTable.dll`��`protobuf-net.dll`��`Singleton.dll`��������
- �½�һ��Excel���ŵ�table�ļ��У�������Ӣ������
    - Excel�ļ�������Ǳ��ϣ������Ķ���ı���Էŵ�һ��Excel�ļ�����ߵ�һ��Sheet����һ������ı�
    - �½�һ��Sheet������Ϊ`xx_name`��`xx`��ֵ�����ǣ��������Ϲ����Ĭ����`none_name`����
        - `all` �������Ϳͻ��˶���
        - `client` ���ͻ�����
        - `server` ����������
        - `none` �����ɱ�������˵����ע��
    - ���һ��Sheet����ʽ��`����:����ʽ` 
- �ر�����Ҫ��ı����ڵ�Excel�ļ�
- ����`tools\config.py`�е�
    - `self.unity_table_cs_path` Unity�б��CS�ļ��洢���·��
    - `self.unity_table_data_path` Unity�б��������ļ��洢���·��
    - `self.unity_common_cs_path` Unity�й���PB��CS�ļ��洢���·��
    - `self.unity_command_cs_path` Unity��Э��PB��CS�ļ��洢���·��
- ����Unity���`Assets/JerryTable`�µ�ָ����д�����Զ���������ӦĿ¼�������`����:ָ��ϸ��`
- ʹ�ã��ο�`GameApp.cs`��`MyTableLoader.cs`
    - `MyTableLoader.cs`ע���±�������أ�������Զ���ѡ���ô�Resources��AssetBundle���أ�
    - `GameApp.cs`��ʹ��
        - ���ұ����������Լ����壬����������ϼ�

---

## ����:����

����Ŀ¼���£�
- table
    - output ����ļ�
        - command_cs Э����
        - common_cs ��������
        - table_cs �������࣬�ͱ���Ӧ
        - table_data ������ݣ��ͱ���Ӧ
    - proto
        - ����Զ�����
            - `c_table_xxx.proto`�ͻ��˱�
            - `s_table_xxx.proto`��������
        - ������
            - `common_xxx.proto`Ҫ�ֶ�д
        - ��ע������`.py`��`.pyc`���ļ��ǹ������ɵı����ļ�
    - table ����ļ�
        - `XXX.xlsx` 
    - tools ����

## ����:����ʽ

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

˵����ö��������Ҫ��дĬ��ֵ

## ����:ָ��ϸ��

ָ�����е���`tools\run.py`�������ֶ����У�
- ����`tools\run_type-client_copy-0.py`��log��`table_tools.log`
    - ����˵��
        - type ������ͣ������ͻ��˱�
        - copy �Ƿ񿽱���Unity���̣��������ã�`��`
    - ��Ӧ�����ݾ���Unity������
