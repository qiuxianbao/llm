from ollama import Client
from ollama import ChatResponse

client = Client(host='http://10.100.16.88:11434', timeout= 5 * 60 * 1000)

# 
# [Model(model='deepseek-r1:7b', modified_at=datetime.datetime(2025, 3, 20, 15, 54, 21, 277973, tzinfo=TzInfo(+08:00)), digest='0a8c266910232fd3291e71e5ba1e058cc5af9d411192cf88b6d30e92b6e73163', size=4683075271, details=ModelDetails(parent_model='', format='gguf', family='qwen2', families=['qwen2'], parameter_size='7.6B', quantization_level='Q4_K_M'))]
# print(client.list())
# print(client.ps())

# 
# response: ChatResponse = client.chat(model='deepseek-r1:7b', messages=[
#   {
#     'role': 'user',
#     'content': '你是谁',
#     "stream": True,
#   },
# ])

response: ChatResponse = client.chat(model='deepseek-r1:7b', messages=[
  {
    'role': 'user',
    'content': '请生成包括书名、作者和类别的三本虚构的、非真实存在的中文书籍清单，并以JsoN格式提供，其中包含以下键：book_id、title、author、genre',
    "stream": True,
  },
])

print(response.message.content)


