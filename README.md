项目 | 内容
---|---
标题 | ProtobufTools
标签 | ProtobufTools、Protobuf、Unity、表格
备注 | 对Unity无依赖
最近更新 | 2016-12-25 00:35:32

## 使用

使用步骤：（具体见样例工程，包括DLL工程和源码工程）
- 把工具放到`Assets`平行位置，工具说明见`补充:工具`
- `Unity`工程的`Plugins`里加入`JerryTable.dll`和`protobuf-net.dll`
- 新建一个Excel表，放到table文件夹，建议用英文命名
    - Excel文件代表的是表集合，同系统的表可以放一个Excel文件，里边的一个Sheet才是一个具体的表
    - 新建一个Sheet，命名为`xx_name`，`xx`的值可以是（命名不合规则的默认是`none_name`）：
        - `all` 服务器和客户端都用
        - `client` 仅客户端用
        - `server` 仅服务器用
        - `none` 不会打成表，用来做说明备注的
    - 填充一个Sheet，格式如`补充:表格格式` 
- 关闭所有要打的表所在的Excel文件
- 配置`tools\config.py`中的
    - `self.unity_table_cs_path`
    - `self.unity_table_data_path`
    - `self.unity_common_cs_path`
- 运行Unity里的`Assets/JerryTable`下的指令进行打表，会自动拷贝到相应目录，更多见`补充:指令细节`
- 使用：参考`GameApp.cs`和`MyTableLoader.cs`
    - `MyTableLoader.cs`注册新表，处理加载（你可以自定义选择用从Resources或AssetBundle加载）
    - `GameApp.cs`里使用
        - 查找表，主键可以自己定义，单键或者组合键

---

### 补充:工具

工具目录如下：
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

### 补充:指令细节

指令运行的是`tools\run.py`，可以手动运行：
- 运行`tools\run_type-client_copy--py`，log在`table_tools.log`
    - 参数说明
        - type 打表类型，这里打客户端表
        - copy 是否拷贝到Unity工程，这是设置：`是`
    - 相应的数据就在Unity工程了