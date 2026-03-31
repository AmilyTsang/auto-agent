from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from .tools import tools
import yaml
import os

class DataInsightAgent:
    def __init__(self, config_path="config/config.yaml"):
        # 加载配置
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            model=self.config["llm"]["model"],
            temperature=self.config["llm"]["temperature"],
            max_tokens=self.config["llm"]["max_tokens"],
            base_url=self.config["llm"]["base_url"],
            api_key=self.config["llm"]["api_key"]
        )
        
        # 创建提示模板
        tools_description = "\n".join([
            f"- {tool.name}: {tool.description}" 
            for tool in tools
        ])
        
        self.prompt_template = ChatPromptTemplate.from_template(
            f"""你是一个专业的数据分析助手，帮助用户分析数据并生成报告。

            对话历史：
            {{history}}

            用户问题：
            {{input}}
            
            可用工具：
            {tools_description}
            
            工具调用历史：
            {{agent_scratchpad}}
            
            如果用户的问题需要使用工具，请按照以下格式调用工具：
            工具名称: 参数
            
            例如：
            - 数据导入: data/sales.csv
            - 描述性分析: sales_data
            - 生成图表: sales_data,bar,销售数据趋势
            - 生成报告: analysis_results
            """
        )
        
        # 构建agent
        self.agent = create_tool_calling_agent(
            llm=self.llm,
            tools=tools,
            prompt=self.prompt_template
        )
        
        # 构建agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=tools,
            verbose=True
        )
        
        # 对话历史
        self.history = []
    
    def run(self, user_input):
        """运行agent，处理用户输入"""
        # 构建上下文
        history_str = "\n".join([f"用户: {h[0]}\n助手: {h[1]}" for h in self.history])
        
        # 调用agent
        response = self.agent_executor.invoke({
            "input": user_input,
            "history": history_str
        })
        
        # 更新对话历史
        self.history.append((user_input, response["output"]))
        
        return response["output"]
    
    def clear_history(self):
        """清空对话历史"""
        self.history = []
    
    def get_history(self):
        """获取对话历史"""
        return self.history
