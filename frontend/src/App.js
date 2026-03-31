import React, { useState, useRef } from 'react';
import './styles/App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [fileId, setFileId] = useState(null);
  const [activeTab, setActiveTab] = useState('chat');
  const chatEndRef = useRef(null);

  // 滚动到聊天底部
  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // 发送消息
  const handleSend = async () => {
    if (!input.trim()) return;

    // 添加用户消息
    setMessages([...messages, { type: 'user', text: input }]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'agent', text: data.response }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent', text: `错误: ${error.message}` }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  // 处理文件上传
  const handleFileUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setFileId(data.file_id);
      setMessages(prev => [...prev, { type: 'agent', text: `文件上传成功，文件ID: ${data.file_id}` }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent', text: `文件上传失败: ${error.message}` }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  // 分析数据
  const handleAnalyze = async (analysisType) => {
    if (!fileId) {
      setMessages(prev => [...prev, { type: 'agent', text: '请先上传文件' }]);
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file_id', fileId);
      formData.append('analysis_type', analysisType);

      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'agent', text: `分析结果: ${JSON.stringify(data, null, 2)}` }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent', text: `分析失败: ${error.message}` }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  // 生成图表
  const handleVisualize = async (chartType) => {
    if (!fileId) {
      setMessages(prev => [...prev, { type: 'agent', text: '请先上传文件' }]);
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file_id', fileId);
      formData.append('chart_type', chartType);

      const response = await fetch('http://localhost:8000/api/visualize', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'agent', text: `图表生成成功，路径: ${data.chart_path}` }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent', text: `图表生成失败: ${error.message}` }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  // 生成报告
  const handleGenerateReport = async (reportFormat) => {
    if (!fileId) {
      setMessages(prev => [...prev, { type: 'agent', text: '请先上传文件' }]);
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('file_id', fileId);
      formData.append('report_format', reportFormat);

      const response = await fetch('http://localhost:8000/api/generate_report', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setMessages(prev => [...prev, { type: 'agent', text: `报告生成成功，路径: ${data.report_path}` }]);
    } catch (error) {
      setMessages(prev => [...prev, { type: 'agent', text: `报告生成失败: ${error.message}` }]);
    } finally {
      setLoading(false);
      scrollToBottom();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航栏 */}
      <nav className="bg-blue-600 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Auto-Agent</h1>
          <div className="flex space-x-4">
            <button 
              className={`px-4 py-2 rounded ${activeTab === 'chat' ? 'bg-blue-700' : 'hover:bg-blue-700'}`}
              onClick={() => setActiveTab('chat')}
            >
              聊天
            </button>
            <button 
              className={`px-4 py-2 rounded ${activeTab === 'analysis' ? 'bg-blue-700' : 'hover:bg-blue-700'}`}
              onClick={() => setActiveTab('analysis')}
            >
              分析
            </button>
            <button 
              className={`px-4 py-2 rounded ${activeTab === 'visualization' ? 'bg-blue-700' : 'hover:bg-blue-700'}`}
              onClick={() => setActiveTab('visualization')}
            >
              可视化
            </button>
            <button 
              className={`px-4 py-2 rounded ${activeTab === 'report' ? 'bg-blue-700' : 'hover:bg-blue-700'}`}
              onClick={() => setActiveTab('report')}
            >
              报告
            </button>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <div className="container mx-auto p-4">
        {/* 文件上传区 */}
        <div className="mb-4">
          <div className="file-upload">
            <input 
              type="file" 
              className="hidden" 
              id="file-upload" 
              onChange={handleFileUpload}
            />
            <label htmlFor="file-upload" className="cursor-pointer">
              <div className="flex flex-col items-center justify-center">
                <svg className="w-12 h-12 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                <p className="text-gray-600">点击或拖拽文件到此处上传</p>
                {file && <p className="text-gray-500 text-sm mt-2">已选择: {file.name}</p>}
              </div>
            </label>
          </div>
        </div>

        {/* 聊天区 */}
        {activeTab === 'chat' && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            <div className="chat-container mb-4">
              {messages.map((message, index) => (
                <div 
                  key={index} 
                  className={`message ${message.type === 'user' ? 'user-message' : 'agent-message'}`}
                >
                  {message.text}
                </div>
              ))}
              {loading && (
                <div className="message agent-message">
                  <div className="loading"></div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="flex">
              <input
                type="text"
                className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                placeholder="输入消息..."
              />
              <button
                className="bg-blue-600 text-white px-4 py-2 rounded-r-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={handleSend}
              >
                发送
              </button>
            </div>
          </div>
        )}

        {/* 分析区 */}
        {activeTab === 'analysis' && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            <h2 className="text-xl font-bold mb-4">数据分析</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleAnalyze('descriptive')}
              >
                描述性分析
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleAnalyze('time_series')}
              >
                时间序列分析
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleAnalyze('clustering')}
              >
                聚类分析
              </button>
            </div>
          </div>
        )}

        {/* 可视化区 */}
        {activeTab === 'visualization' && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            <h2 className="text-xl font-bold mb-4">数据可视化</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleVisualize('bar')}
              >
                柱状图
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleVisualize('line')}
              >
                折线图
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleVisualize('scatter')}
              >
                散点图
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleVisualize('pie')}
              >
                饼图
              </button>
            </div>
          </div>
        )}

        {/* 报告区 */}
        {activeTab === 'report' && (
          <div className="bg-white rounded-lg shadow-lg p-4">
            <h2 className="text-xl font-bold mb-4">报告生成</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleGenerateReport('html')}
              >
                HTML报告
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleGenerateReport('pdf')}
              >
                PDF报告
              </button>
              <button 
                className="bg-blue-600 text-white p-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                onClick={() => handleGenerateReport('pptx')}
              >
                PowerPoint报告
              </button>
            </div>
          </div>
        )}
      </div>

      {/* 底部信息 */}
      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto text-center">
          <p>Auto-Agent © 2026</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
