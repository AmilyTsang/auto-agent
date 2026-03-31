import gradio as gr
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

class SimpleGradioApp:
    def __init__(self):
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_data(self, file):
        if file is None:
            return "请上传数据文件", ""
        
        try:
            # 读取数据文件
            if file.name.endswith('.csv'):
                df = pd.read_csv(file.name)
            elif file.name.endswith('.xlsx'):
                df = pd.read_excel(file.name)
            elif file.name.endswith('.json'):
                df = pd.read_json(file.name)
            else:
                return "不支持的文件格式，请上传CSV、Excel或JSON文件", ""
            
            # 基本统计信息
            stats = df.describe().to_string()
            
            # 生成可视化图表
            chart_path = os.path.join(self.output_dir, f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            
            # 选择数值列进行可视化
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                fig = px.bar(df, x=df.index, y=numeric_cols[0])
                fig.write_html(chart_path)
                chart_html = open(chart_path, 'r').read()
            else:
                chart_html = "数据中没有数值列，无法生成可视化"
            
            return f"数据加载成功！\n\n基本统计信息：\n{stats}", chart_html
        except Exception as e:
            return f"处理数据时出错：{str(e)}", ""
    
    def run(self):
        with gr.Blocks(title="Auto-Agent: 自动化数据分析工具") as app:
            gr.Markdown("# Auto-Agent 智能数据分析工具")
            gr.Markdown("上传数据文件，自动分析并生成可视化")
            
            with gr.Row():
                with gr.Column():
                    file_input = gr.File(label="上传数据文件", file_types=[".csv", ".xlsx", ".json"])
                    process_btn = gr.Button("处理数据")
                
                with gr.Column():
                    output_text = gr.Textbox(label="输出信息", lines=10)
                    chart_output = gr.HTML(label="数据可视化")
            
            # 处理数据按钮
            process_btn.click(
                fn=self.process_data,
                inputs=[file_input],
                outputs=[output_text, chart_output]
            )
        
        app.launch(share=False, inbrowser=True)

if __name__ == "__main__":
    app = SimpleGradioApp()
    app.run()
