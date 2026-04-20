# Auto-Agent: 自动化数据分析与报告生成智能体

## 项目简介

Auto-Agent 是一个自动化数据分析与报告生成工具，能够帮助用户快速分析数据、生成可视化图表并自动生成专业报告。项目提供了基于大语言模型的智能对话系统，支持通过自然语言指令进行数据分析和报告生成。

## 核心功能

- **对话式智能分析**：基于大语言模型的对话系统，支持多轮对话交互，可通过自然语言指令进行数据分析
- **智能数据分析**：自动识别数据类型，执行统计分析，发现数据中的模式和趋势
- **数据可视化**：生成多种类型的图表，包括柱状图、饼图、折线图、散点图等
- **自动报告生成**：基于分析结果生成结构化报告，支持多种格式
- **多对话管理**：支持创建、切换、删除多个对话，对话历史持久化保存
- **高性能API服务**：基于Flask构建，提供完整的RESTful接口
- **工具调用能力**：智能体可调用多种工具进行数据导入、分析、可视化和报告生成
- **Web前端界面**：直观的HTML界面，集成所有功能模块

## 技术栈

### 后端
- Python 3.9+
- Flask：构建高性能API服务
- LangChain：智能体框架
- pandas/numpy：数据处理
- scikit-learn：机器学习分析
- plotly/matplotlib：数据可视化
- Jinja2：报告模板

### 前端
- HTML5 + CSS3 + JavaScript
- 响应式设计，支持移动端
- 美观的用户界面

## 项目结构

```
auto-agent/
├── src/                 # 源代码
│   ├── agent/           # 智能体模块
│   │   ├── __init__.py
│   │   ├── agent.py              # DataInsightAgent核心类
│   │   ├── conversation_manager.py  # 对话管理模块
│   │   └── tools.py      # 工具定义
│   ├── analysis/        # 数据分析模块
│   │   ├── __init__.py
│   │   └── analyzer.py
│   ├── data/            # 数据处理模块
│   │   ├── __init__.py
│   │   └── data_processor.py
│   ├── report/          # 报告生成模块
│   │   ├── __init__.py
│   │   └── report_generator.py
│   └── visualization/   # 数据可视化模块
│       ├── __init__.py
│       └── visualizer.py
├── frontend/            # 前端文件
│   └── index.html       # Web前端界面
├── config/              # 配置文件
│   └── config.yaml      # 主配置文件
├── app.py               # Flask应用入口
├── requirements.txt     # 依赖列表
├── README.md
└── .gitignore
```

## 使用方法

### 快速启动

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置API密钥

编辑 `config/config.yaml` 文件，设置您的智谱AI API密钥：

```yaml
llm:
  api_key: "您的智谱AI API密钥"
  model: "glm-4"
  base_url: "https://open.bigmodel.cn/api/paas/v4/"
```

3. 启动服务

```bash
python app.py
```

4. 访问前端

在浏览器中打开 http://localhost:5000/

## 前端界面功能

### 对话式智能分析
- 通过自然语言与智能体交流
- 智能体自动调用工具进行数据分析
- 支持多轮对话，上下文中理解用户意图
- 提供详细的数据分析结果

### 文件上传
- 支持多种数据格式：CSV、Excel、JSON、TXT
- 拖拽或点击上传
- 文档列表管理

### 数据分析
- 描述性分析
- 时间序列分析
- 聚类分析
- 自动识别数据类型和模式

### 数据可视化
- 多种图表类型：柱状图、折线图、散点图、饼图
- 交互式图表展示
- 自动选择合适的可视化方式

### 报告生成
- 支持多种格式：HTML、PDF、PPTX
- 包含数据概览和统计分析
- 自动生成数据洞察

## API端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 访问前端界面 |
| `/frontend/<path>` | GET | 服务前端静态文件 |
| `/api/chat` | POST | 发送消息，获取智能体回复 |
| `/api/upload` | POST | 上传数据文件 |
| `/api/clear` | POST | 清空对话历史 |
| `/api/clear_docs` | POST | 清空上传的文档 |
| `/api/analyze` | POST | 分析数据 |
| `/api/visualize` | POST | 生成可视化图表 |
| `/api/generate_report` | POST | 生成分析报告 |

## 智能体工具

| 工具名称 | 功能描述 | 参数说明 |
|---------|---------|---------|
| 数据导入 | 导入数据文件并存储到数据存储中 | file_path: 数据文件路径 |
| 描述性分析 | 对数据进行描述性分析 | data_id: 数据ID |
| 生成图表 | 生成数据可视化图表 | data_id: 数据ID, chart_type: 图表类型, title: 图表标题 |
| 生成报告 | 生成分析报告 | analysis_id: 分析结果ID |

## 对话示例

**用户**：我有一个销售数据文件，请帮我分析一下

**助手**：我将帮您分析销售数据。首先，我需要导入数据文件。

工具调用：数据导入

**助手**：数据导入成功！现在我将对数据进行描述性分析。

**用户**：请生成一个销售趋势的折线图

**助手**：好的，我将生成销售趋势的折线图。

**用户**：请生成一份完整的分析报告

**助手**：报告生成成功！您的销售数据分析已完成。

## 支持的数据格式

- CSV
- JSON
- Excel (xlsx)
- TXT

## 报告输出格式

- HTML
- PDF
- PPTX

## 配置说明

主要配置文件为 `config/config.yaml`，包含以下配置项：

- **llm**：大语言模型配置（API密钥、模型、温度等）
- **data**：数据处理配置
- **analysis**：分析参数配置
- **visualization**：可视化配置
- **report**：报告生成配置

## 注意事项

1. 使用API服务时需要配置有效的智谱AI API密钥
2. 上传的数据文件大小建议不超过10MB
3. 复杂的分析任务可能需要较长时间执行
4. 对话历史保存在`conversations`目录中
5. 生成的图表和报告分别保存在`outputs`和`reports`目录中

## 技术特点

- **前后端分离架构**：前端使用HTML/CSS/JS，后端使用Flask
- **响应式设计**：支持桌面端和移动端
- **高性能API**：基于Flask构建的RESTful接口
- **智能对话系统**：基于LangChain的Agent执行框架
- **工具调用能力**：自动调用工具进行数据处理和分析
- **多对话管理**：支持多个并发对话会话

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请联系项目维护者。