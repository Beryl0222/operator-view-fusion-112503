# 共享张量视图的激活融合与自动微分

本项目用于视图重叠、存储版本和原地写资格相关的Python模型计算。模型输入格式与外部调用语义见 [数据及数值约定](docs/contracts.md)。

目前代码提供合成资料读取与检查，数值运算和业务处理接口尚未提供。资料检查成功只表示数据可以读取。

使用 Python 3.11；依赖版本记录在 requirements.txt。独立环境安装：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m support.inspect_data
.venv/bin/python -m pytest -q
```

已经安装依赖的环境可直接运行 `python3 -m support.inspect_data` 和 `python3 -m pytest -q`。运行不需要联网服务、真实用户资料或额外模型下载。

data/catalog.json 引用各个张量文件；data/records.json 描述样本身份和调用参数；data/events.json 保存会作用于这些输入的合成事件。support 仅负责读取资料，tests 检查资料格式与引用。尚不存在的产品接口和测试用法应随产品实现另行记录。
