import gradio as gr
import pandas as pd
import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.data.data_processor import DataProcessor
from src.analysis.analyzer import Analyzer
from src.visualization.visualizer import Visualizer
from src.report.report_generator import ReportGenerator

class GradioApp:
    def __init__(self):
        self.data_processor = DataProcessor()
        self.analyzer = Analyzer()
        self.visualizer = Visualizer()
        self.report_generator = ReportGenerator()
        self.output_dir = "outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_data(self, file):
        if file is None:
            return "请上传数据文件", None, None
        
        try:
            # 处理上传的文件
            df = self.data_processor.load_data(file.name)
            
            # 基本统计信息
            stats = df.describe().to_string()
            
            # 生成基本可视化
            chart_path = os.path.join(self.output_dir, f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
            self.visualizer.create_bar_chart(df, chart_path)
            
            return f"数据加载成功！\n\n基本统计信息：\n{stats}", chart_path, df
        except Exception as e:
            return f"处理数据时出错：{str(e)}", None, None
    
    def generate_report(self, df, report_format):
        if df is None:
            return "请先上传并处理数据", None
        
        try:
            # 生成报告
            report_path = os.path.join(self.output_dir, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{report_format}")
            self.report_generator.generate_report(df, report_path, report_format)
            
            return f"报告生成成功！\n报告路径：{report_path}", report_path
        except Exception as e:
            return f"生成报告时出错：{str(e)}", None
    
    def run(self):
        with gr.Blocks(title="Auto-Agent: 自动化数据分析与报告生成") as app:
            gr.Markdown("# Auto-Agent 智能数据分析工具")
            gr.Markdown("上传数据文件，自动分析并生成报告")
            
            with gr.Row():
                with gr.Column():
                    file_input = gr.File(label="上传数据文件", file_types=[".csv", ".xlsx", ".json", ".txt"])
                    process_btn = gr.Button("处理数据")
                    report_format = gr.Dropdown(
                        label="报告格式",
                        choices=["pdf", "html", "pptx"],
                        value="html"
                    )
                    report_btn = gr.Button("生成报告")
                
                with gr.Column():
                    output_text = gr.Textbox(label="输出信息", lines=10)
                    chart_output = gr.HTML(label="数据可视化")
                    report_output = gr.File(label="生成的报告")
            
            # 存储数据的状态
            df_state = gr.State(None)
            chart_path_state = gr.State(None)
            
            # 处理数据按钮
            process_btn.click(
                fn=self.process_data,
                inputs=[file_input],
                outputs=[output_text, chart_path_state, df_state]
            )
            
            # 当chart_path_state更新时，显示图表
            chart_path_state.change(
                fn=lambda path: open(path, 'r').read() if path else "",
                inputs=[chart_path_state],
                outputs=[chart_output]
            )
            
            # 生成报告按钮
            report_btn.click(
                fn=self.generate_report,
                inputs=[df_state, report_format],
                outputs=[output_text, report_output]
            )
        
        app.launch(share=False, inbrowser=True)

if __name__ == "__main__":
    gradio_app = GradioApp()
    gradio_app.run()
