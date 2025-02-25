import requests
import time

# API 配置
url = "https://api.siliconflow.cn/v1/chat/completions"
token = ""  # 替换为你的实际 Token（不含 Bearer 前缀）
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "model": "deepseek-ai/DeepSeek-V3",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": False,
    "max_tokens": 512
}

# 发送请求并保存结果
try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)  # 添加10秒超时
    status_code = response.status_code
    response_text = response.text
    
    # 打印结果
    print(f"状态码: {status_code}")
    print(f"响应内容: {response_text}")
    
    # 保存到文件
    with open("api_test_result.txt", "w", encoding="utf-8") as f:
        f.write(f"状态码: {status_code}\n")
        f.write(f"响应内容: {response_text}\n")
    print("结果已保存到 'api_test_result.txt'")

except requests.exceptions.RequestException as e:
    error_msg = f"请求失败: {e}"
    print(error_msg)
    with open("api_test_result.txt", "w", encoding="utf-8") as f:
        f.write(error_msg + "\n")

# 等待用户查看结果
input("程序运行完成，按 Enter 键关闭...")