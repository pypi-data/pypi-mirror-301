# FPowerKit 配电网运算组件
- 依赖于feasytools和gurobipy: `pip install feasytools,gurobipy`（请自行安装Gurobi并申请许可证）
- 包含电网的描述(含母线、发电机、线路等)和基于gurobipy的配电网求解
- 内含IEEE 33节点配电网DistFlow模型
- 优化目标为“发电成本最小”。发电成本模型为二次函数$f(x)=ax^2+bx+c$。

## 使用

输入以下命令开始仿真:
```bash
python main.py -g cases/ieee33.grid.zip
```
`ieee33`描述了IEEE 33节点配电网模型。换成`nodes3`则是一个极简版3节点辐射形配电网模型，结构如下：

```
G0  G1
|   |
B0->B1->B2
    |   |
    L1  L2
```

您也换成自己的`.zip`文件来仿真，例如`python main.py -g path/to/your_zipfile.zip`

## 文件格式
若要配置您自己的`.zip`文件来仿真，您需要确保该zip压缩文件**有且仅有**如下文件(区分大小写)，不能包含任何文件夹：
```
<your_file>.zip
    info.txt
    buses.csv
    lines.csv
    gens.csv
```

具体范例参见`PowerKit/cases/nodes3.zip`。

#### info.txt
该文件示例如下：

```
S_base_MVA: 10
U_base_kV: 10
buses_loop: 86400, 8
buses_unit: MVA
lines_unit: ohm
gens_unit: MVA
```

`S_base_MVA`表示复功率标幺值，单位为MVA；
`U_base_kV`表示电压标幺值，单位为kV；
`buses_loop`表示buses.csv中功率的循环周期(秒)和循环次数；
`buses_unit`表示buses.csv中功率值的单位，可选pu(标幺值),kVA,MVA；
`lines_unit`表示lines.csv中功率值的单位，可选pu(标幺值),ohm；
`gens_unit`表示gens.csv中功率值的单位，可选pu(标幺值),kVA,MVA；

#### buses.csv
该文件示例如下：

```
time,0
B0,0|0
B1,10.2|3.2
B2,3.8|0.7
```

首行表示时间线，内容用英文逗号分隔。第1个内容必定是小写`time`，从第2个内容开始为整数，表示从这一**秒**开始的负载功率；
从第2行开始，每行的第1个内容表示母线名称，从第二个内容开始表示复功率，以`有功功率|无功功率`的形式出现，单位为`info.txt`中的指定值。

#### gens.csv
该文件示例如下：

```
time,0
G0|B0|0.002|0.3|5,0|100|-100|100
G1|B1|0.0025|0.4|15,0|100|-100|100
```

首行表示时间线，内容用英文逗号分隔。第1个内容必定是小写`time`，从第2个内容开始为整数，表示从这一**秒**开始的发电功率最值；
从第2行开始，每行的第1个内容为`发电机ID|所在母线|成本系数a|成本系数b|成本系数c`，从第二个内容开始表示发电功率最值，以`最小有功功率|最大有功功率|最小无功功率|最大无功功率`的形式出现，单位为`info.txt`中的指定值。

#### lines.csv
该文件示例如下：
```
id,fBus,tBus,R,X
L0-1,B0,B1,0.08,0.2
L1-2,B1,B2,0.06,0.12
```
首行内容必须是`id,fBus,tBus,R,X`，区分大小写；
从第2行开始，每行的内容为`线路名称,起始母线,终止母线,线路电阻,线路电抗`。请注意线路功率的正方向为“起始母线->终止母线”，填反有可能需要在仿真时修改边界条件。