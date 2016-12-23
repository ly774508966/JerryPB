项目 | 内容
---|---
标题 | ProtobufTools
标签 | ProtobufTools、Protobuf、Unity、表格
备注 | 对Unity无依赖
最近更新 | 2016-12-24 00:41:52

## 使用

打表工具如下：
- table
    - output 输出文件
        - table_cs 表格解析类，和表格对应
        - table_data 表格数据，和表格对应
        - common_cs 公共库类
    - proto
        - 表格：自动生成
            - `c_table_xxx`客户端表
            - `s_table_xxx`服务器表
        - 公共库
            - `common_xxx`要手动写
    - table 表格文件
    - tools 工具

操作步骤：
1. 新建一个Excel表，放到table文件夹，建议用英文命名
    1. Excel文件代表的是表集合，同系统的表可以放一个Excel文件，里边的一个Sheet才是一个具体的表
    1. 新建一个Sheet，命名为`xx_name`，`xx`的值可以是（命名不合规则的默认是`none_name`）：
        1. `all` 服务器和客户端都用
        1. `client` 仅客户端用
        1. `server` 仅服务器用
        1. `none` 不会打成表，用来做说明备注的
    1. 填充一个Sheet，格式如`补充:表格格式` 
1. 关闭所有要打的表所在的Excel文件
1. 配置`tools\config.py`中的
    1. `self.unity_table_cs_path`
    1. `self.unity_table_data_path`
    1. `self.unity_common_cs_path`
1. 运行`tools\run_type-client_copy-1.py`，log在`table_tools.log`
    1. 参数说明
        1. type 打表类型，这里打客户端表
        1. copy 是否拷贝到Unity工程，这是设置：`是`
    1. 相应的数据就在Unity工程了
    1. 或者运行Unity里的`Assets/JerryTable`下的指令
1. 使用
    1. `TableDesc.cs`注册一个新表
    1. `GameApp.cs`里
        1. `LoadTables();` 加载表，你可以自定义选择用从Resources或AssetBundle加载
        1. 查找表，主键可以自己定义，单键或者组合键

---

### 补充:表格格式

sint32 | `Common.EnumTest` | `List.uint32` | `Common.StructTest` | 说明
---|---|---|---|---
id | `enum_test` | `ulist` | `struct_test` |   	
all | client | all | all | none
ID | 枚举 | int列表 | 结构 | 说明
10000 | 1 | `1|2|3` | `{1^21}` | 
10001 | 2 | 1 | `{2^2}` | 

如上表（`Test.xlsx`->`all_TestA`）：
- 表头：前4行
    - 第1行：类型
    - 第2行：名称，将来的解析类中对应的字段名
    - 第3行：使用范围，和Sheet命名规则含义一致
    - 第4行：一方面是备注，另一方面也讲生成为解析类对应字段的注释
- 内容 

类型：
- 普通类型：
    - `sint32`
    - `uint32`
    - `string`
    - `float`
- 用户自定义：需要自己写proto文件（放到proto文件夹）来定义，并在`tools/UserDefineType.xlsx`登记
    - 枚举：如上表的`Common.DegreeType`，填写int值
    - 结构：如上表的`Common.Effect`，按这个`{x^y}`结构顺序填充
- 列表：
    - `List.type`：如上表的`List.uint32`，结构`x|y`

`UserDefineType.xlsx`表：

类型 | 所在文件 | 默认值 | 说明
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

说明：枚举值需要填写默认值