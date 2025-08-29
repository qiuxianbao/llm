
from langchain.agents import load_tools, initialize_agent, AgentType
# from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI
from numpy.f2py.crackfortran import verbose


# # 新建llm
# llm = ChatOpenAI(temperature=0)
#
# # 初始化工具
# # llm-math 工具结合模型和计算器用来进行数学计算
# # wikipedia 通过API连接到wikipedia进行搜索查询
#  = load_tools(
#     ["llm-math", "wikipedia"],
#     llm=llm
# )
#
# # 生成代理
# agent = initialize_agent(
#     tools,
#     llm,
#     # chat 是针对对话优化的模型; zero_shot 仅在当前操作上起作用，没有记忆;
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 代理类型
#     handle_parsing_errors=True,  # 处理解析错误，当发生错误时，由大模型进行纠正
#     verbose=True  # 输出中间步骤
# )
#
# agent("计算300的25%")


# 定义自己的工具
# from langchain.agents import tool
# from datetime import date
#
# # @tool
# def time(text: str) -> str:
#     """
#     返回今天的日期，用于任何需要知道今天日期的问题。\
#     输入应该总是一个空字符串，\
#     这个函数将总是返回今天的日期，任何日期计算应该在这个函数之外进行。
#     """
#     return str(date.today())

# 生成代理
# agent = initialize_agent(
#     tools=[time],
#     llm,
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 代理类型
#     handle_parsing_errors=True,  # 处理解析错误，当发生错误时，由大模型进行纠正
#     verbose=True  # 输出中间步骤
# )




