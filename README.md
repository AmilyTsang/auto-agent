# Auto-Agent: 自动化数据分析与报告生成智能体

## 项目简介

Auto-Agent 是一个自动化数据分析与报告生成工具，能够帮助用户快速分析数据、生成可视化图表并自动生成专业报告。项目提供了直观的Web界面，支持本地使用，无需安装复杂依赖。

## 核心功能

- **智能数据分析**：自动识别数据类型，执行统计分析，发现数据中的模式和趋势
- **数据可视化**：生成多种类型的图表，包括柱状图、饼图、折线图、散点图等
- **自动报告生成**：基于分析结果生成结构化报告，支持多种格式
- **前端界面**：直观的Web界面，便于用户上传数据、查看分析结果
- **本地使用**：无需安装依赖，直接在浏览器中打开使用

## 技术栈

### 后端
- Python 3.9+
- FastAPI：构建高性能API服务
- LangChain：智能体框架
- pandas/numpy：数据处理
- scikit-learn：机器学习分析
- plotly/matplotlib：数据可视化
- Jinja2：报告模板

### 前端
- HTML5 + JavaScript
- Chart.js：数据可视化
- 原生CSS：样式设计

## 项目结构

```
auto-agent/
├── config/              # 配置文件
│   └── config.yaml      # 主配置文件
├── frontend/            # 前端代码
│   ├── public/          # 静态资源
│   ├── src/             # 源代码
│   │   ├── styles/      # 样式文件
│   │   ├── App.js       # 主应用组件
│   │   └── index.js     # 应用入口
│   ├── package.json     # 前端依赖
│   └── requirements.txt # 前端Python依赖
├── outputs/             # 生成的输出文件
├── src/                 # 后端源代码
│   ├── agent/           # 智能体模块
│   ├── analysis/        # 数据分析模块
│   ├── api/             # API服务模块
│   ├── data/            # 数据处理模块
│   ├── report/          # 报告生成模块
│   ├── visualization/   # 数据可视化模块
│   └── frontend/        # Gradio前端模块
├── uploads/             # 上传的文件
├── index.html           # 本地HTML前端页面
├── simple_gradio_app.py # 简化版Gradio应用
└── requirements.txt     # 后端依赖
```

## 使用方法

### 方法一：使用HTML前端页面（推荐）

1. 直接在浏览器中打开 `index.html` 文件
2. 点击"选择文件"按钮上传您的数据文件（支持CSV和JSON格式）
3. 点击"处理数据"按钮进行分析
4. 在"数据分析"标签页查看智能分析结果
5. 在"数据可视化"标签页选择图表类型和数据维度，查看生成的图表
6. 在"报告生成"标签页选择报告格式，生成并下载报告

### 方法二：使用Gradio应用（可选）

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 运行Gradio应用

```bash
python src/frontend/gradio_app.py
```

3. 在浏览器中访问生成的本地URL

### 方法三：使用API服务

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 配置环境变量

编辑 `config/config.yaml` 文件，设置您的智谱AI API密钥：

```yaml
llm:
  api_key: "您的智谱AI API密钥"
```

3. 启动API服务

```bash
cd src/api
uvicorn app:app --reload
```

API服务将在 http://localhost:8000 启动，可访问 http://localhost:8000/docs 查看交互式API文档。

## 支持的数据格式

- CSV
- JSON
- Excel (xlsx) - 需通过API服务使用
- TXT - 需通过API服务使用

## 报告输出格式

- HTML
- 文本文件
- PDF - 需通过API服务使用
- PPTX - 需通过API服务使用

## 功能特点

### 智能数据分析
- 自动识别数据类型（数值型、日期型、布尔型、文本型）
- 执行描述性统计分析
- 提供数据概览和详细统计信息

### 数据可视化
- 支持多种图表类型：柱状图、饼图、折线图、散点图
- 支持自定义X轴和Y轴数据
- 实时更新图表，提供直观的数据展示

### 自动报告生成
- 基于分析结果生成结构化报告
- 支持多种报告格式
- 包含数据概览、数据类型分析和数据预览

### 前端界面
- 直观的Web界面，采用标签页设计
- 响应式布局，美观易用
- 支持本地使用，无需安装依赖

## 示例

### 数据分析示例

1. 上传销售数据CSV文件
2. 系统自动识别数据结构，执行描述性统计分析
3. 生成销售趋势折线图和产品类别饼图
4. 生成包含分析结果和建议的HTML报告

## 配置说明

主要配置文件为 `config/config.yaml`，包含以下配置项：

- **llm**：大语言模型配置
- **data**：数据处理配置
- **analysis**：分析参数配置
- **visualization**：可视化配置
- **report**：报告生成配置
- **api**：API服务配置
- **storage**：存储配置

## 注意事项

1. HTML前端页面仅支持CSV和JSON文件格式
2. 上传的数据文件大小建议不超过10MB
3. 复杂的分析任务可能需要较长时间执行
4. 使用API服务时需要配置有效的智谱AI API密钥

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请联系项目维护者。