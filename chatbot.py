import tkinter as tk
from tkinter import scrolledtext
import requests
import threading
import time

# API 配置（请替换为实际的API Token）
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_TOKEN = "sk-wtzaawrhxlrmbhowrafnuurmowbfyjrqrutsejdpnitvyfxh"  # 请替换为你的 SiliconFlow API token

# 发送消息到API并获取回复
def call_api(message):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": message}],
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        print(f"API Status Code: {response.status_code}")  # 调试：状态码
        print(f"API Response: {response.text}")  # 调试：完整响应
        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                return response_data["choices"][0]["message"]["content"]
            else:
                return "未收到模型回复，API返回数据异常"
        else:
            if response.status_code == 401:
                return "API Token 无效，请检查 Token 是否正确或联系 SiliconFlow 支持！"
            return f"API 请求失败，状态码: {response.status_code}"
    except requests.exceptions.Timeout:
        return "请求超时，请检查网络连接"
    except requests.exceptions.RequestException as e:
        return f"请求发生错误: {e}"

# 发送消息的函数
def send_message():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        # 显示用户消息
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, user_input + "\n", "user")
        chat_display.see(tk.END)
        chat_display.config(state=tk.DISABLED)
        input_text.delete("1.0", tk.END)
        send_button.config(state=tk.DISABLED)

        # 显示“正在思考...”提示
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "正在思考...\n", "thinking")
        chat_display.see(tk.END)
        chat_display.config(state=tk.DISABLED)

        # 在线程中调用API
        threading.Thread(target=handle_api_response, args=(user_input,), daemon=True).start()

# 处理API响应
def handle_api_response(user_message):
    reply = call_api(user_message)
    print(f"Received reply: {reply}")  # 调试：打印回复内容
    root.after(0, lambda: display_reply(reply))

# 显示模型回复并替换“正在思考...”
def display_reply(reply):
    chat_display.config(state=tk.NORMAL)
    # 获取“thinking”标签的范围，如果没有则跳过
    thinking_ranges = chat_display.tag_ranges("thinking")
    if thinking_ranges:  # 确保有范围
        for i in range(0, len(thinking_ranges), 2):  # 每次取两个元素（起始和结束）
            start = thinking_ranges[i]
            end = thinking_ranges[i + 1]
            chat_display.delete(start, end)
    # 插入实际回复
    chat_display.insert(tk.END, reply + "\n", "robot")
    chat_display.see(tk.END)
    chat_display.config(state=tk.DISABLED)
    send_button.config(state=tk.NORMAL)

# 创建主窗口
root = tk.Tk()
root.title("聊天机器人")
root.geometry("600x700")

# 创建聊天记录显示区域
chat_display = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD, borderwidth=2, relief="groove")
chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
chat_display.config(state=tk.DISABLED)

# 设置消息样式
chat_display.tag_config("user", foreground="blue", justify="right", background="lightblue", 
                        relief="raised", borderwidth=1, lmargin1=50, rmargin=10)
chat_display.tag_config("robot", foreground="green", justify="left", background="lightgreen", 
                        relief="raised", borderwidth=1, lmargin1=10, rmargin=50)
chat_display.tag_config("thinking", foreground="gray", justify="left")

# 创建输入框
input_text = scrolledtext.ScrolledText(root, width=40, height=5, wrap=tk.WORD)
input_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# 创建发送按钮
send_button = tk.Button(root, text="发送", width=10, command=send_message)
send_button.grid(row=1, column=1, padx=10, pady=10, sticky="e")

# 绑定回车键事件
input_text.bind("<Return>", lambda event: send_message())

# 设置行列权重
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# 启动Tkinter事件循环
root.mainloop()