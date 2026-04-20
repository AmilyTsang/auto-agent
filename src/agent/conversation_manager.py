import json
import os
from datetime import datetime

class ConversationManager:
    """对话管理模块"""
    
    def __init__(self, storage_dir="conversations"):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.current_conversation_id = None
        self.conversations = {}
        self.load_conversations()
    
    def load_conversations(self):
        """加载对话历史"""
        for file_name in os.listdir(self.storage_dir):
            if file_name.endswith(".json"):
                conversation_id = file_name[:-5]  # 移除.json后缀
                file_path = os.path.join(self.storage_dir, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        self.conversations[conversation_id] = json.load(f)
                except Exception as e:
                    print(f"加载对话 {conversation_id} 失败: {e}")
    
    def create_conversation(self):
        """创建新对话"""
        conversation_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.conversations[conversation_id] = {
            "id": conversation_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "messages": []
        }
        self.current_conversation_id = conversation_id
        self.save_conversation(conversation_id)
        return conversation_id
    
    def get_current_conversation(self):
        """获取当前对话"""
        if not self.current_conversation_id:
            return self.create_conversation()
        return self.current_conversation_id
    
    def set_current_conversation(self, conversation_id):
        """设置当前对话"""
        if conversation_id in self.conversations:
            self.current_conversation_id = conversation_id
            return True
        return False
    
    def add_message(self, role, content):
        """添加消息到当前对话"""
        conversation_id = self.get_current_conversation()
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversations[conversation_id]["messages"].append(message)
        self.conversations[conversation_id]["last_updated"] = datetime.now().isoformat()
        self.save_conversation(conversation_id)
        return message
    
    def get_messages(self, conversation_id=None):
        """获取对话消息"""
        if not conversation_id:
            conversation_id = self.get_current_conversation()
        if conversation_id in self.conversations:
            return self.conversations[conversation_id]["messages"]
        return []
    
    def get_conversation_history(self, conversation_id=None):
        """获取对话历史（用于Agent）"""
        messages = self.get_messages(conversation_id)
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return history_str
    
    def save_conversation(self, conversation_id):
        """保存对话"""
        if conversation_id in self.conversations:
            file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(self.conversations[conversation_id], f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存对话 {conversation_id} 失败: {e}")
    
    def delete_conversation(self, conversation_id):
        """删除对话"""
        if conversation_id in self.conversations:
            file_path = os.path.join(self.storage_dir, f"{conversation_id}.json")
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"删除对话文件 {conversation_id} 失败: {e}")
            del self.conversations[conversation_id]
            if self.current_conversation_id == conversation_id:
                self.current_conversation_id = None
            return True
        return False
    
    def list_conversations(self):
        """列出所有对话"""
        return [
            {
                "id": conv["id"],
                "created_at": conv["created_at"],
                "last_updated": conv["last_updated"],
                "message_count": len(conv["messages"]),
                "preview": conv["messages"][-1]["content"] if conv["messages"] else ""
            }
            for conv in self.conversations.values()
        ]
