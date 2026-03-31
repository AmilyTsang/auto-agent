# Auto-Agent: 自动化数据分析与报告生成智能体

## 项目简介

Auto-Agent 是一个基于大语言模型的自动化数据分析与报告生成智能体，能够帮助用户快速分析数据、生成可视化图表并自动生成专业报告。

## 核心功能

- **智能数据分析**：自动识别数据类型，执行统计分析，发现数据中的模式和趋势
- **数据可视化**：生成多种类型的图表，包括柱状图、饼图、折线图等
- **自动报告生成**：基于分析结果生成结构化报告，支持多种格式
- **API服务**：提供RESTful API接口，方便集成到其他系统
- **前端界面**：直观的Web界面，便于用户上传数据、查看分析结果

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
- React 18+
- Chart.js：前端数据可视化
- TailwindCSS：样式框架
- HeadlessUI：UI组件

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
│   └── visualization/   # 数据可视化模块
├── uploads/             # 上传的文件
└── requirements.txt     # 后端依赖
```

## 安装与部署

### 后端安装

1. 克隆项目到本地
2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置环境变量

编辑 `config/config.yaml` 文件，设置您的智谱AI API密钥：

```yaml
llm:
  api_key: "您的智谱AI API密钥"
```

4. 启动API服务

```bash
cd src/api
uvicorn app:app --reload
```

API服务将在 http://localhost:8000 启动

### 前端安装

1. 进入前端目录

```bash
cd frontend
```

2. 安装依赖

```bash
npm install
```

3. 启动前端开发服务器

```bash
npm start
```

前端应用将在 http://localhost:3000 启动

## 使用方法

### 1. 上传数据

通过前端界面上传CSV、Excel等格式的数据文件，或通过API接口上传。

### 2. 配置分析任务

设置分析目标、选择分析方法和可视化类型。

### 3. 执行分析

系统将自动执行数据分析，生成可视化图表。

### 4. 查看结果

在前端界面查看分析结果和生成的图表。

### 5. 生成报告

选择报告格式，系统将自动生成包含分析结果和图表的专业报告。

## API文档

启动API服务后，可以访问 http://localhost:8000/docs 查看交互式API文档。

## 支持的数据格式

- CSV
- Excel (xlsx)
- JSON
- TXT

## 报告输出格式

- PDF
- HTML
- PPTX

## 示例

### 数据分析示例

1. 上传销售数据CSV文件
2. 系统自动识别数据结构，执行描述性统计分析
3. 生成销售趋势折线图和产品类别饼图
4. 生成包含分析结果和建议的PDF报告

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

1. 使用前请确保配置了有效的智谱AI API密钥
2. 上传的数据文件大小建议不超过10MB
3. 复杂的分析任务可能需要较长时间执行

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 联系方式

如有问题或建议，请联系项目维护者。