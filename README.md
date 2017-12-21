# Reinforcement learning for SLG game

麻辣星空的Agent工程，[seraphli][1]编写。

2017年12月21日由[seraphli][1]整理代码。

## 目录结构设置

agent: 存放agent相关代码

env: 对接游戏客户端,构建训练环境的代码

test: 功能测试代码,验证代码

code: 实际运行代码


## Prerequisite

1. Google Protobuf
2. Redis

Install Command
> pip install protobuf redis

## 安装

1. 克隆工程
2. 添加工程目录到环境变量PYTHONPATH中(可选)
3. 复制一份config文件夹中的config.example.json,改名为config.json,然后修改里面的参数

## 测试

### Windows

双击`run_all_test.bat`

### 其他环境

运行`python run_all_test.py`

[1]: https://github.com/Seraphli