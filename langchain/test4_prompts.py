
from langchain.prompts import ChatPromptTemplate


# 1、定义模板
template_string="""把由三个反引号分隔的文本\
翻译成一种{style}风格。\
文本：```{text}```
"""
# 将template_string转换为prompt_template
prompt_template=ChatPromptTemplate.from_template(template_string)

# [HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['style', 'text'], input_types={}, partial_variables={}, template='把由三个反引号分隔的文本翻译成一种{style}风格。文本：```{text}```\n'), additional_kwargs={})]
print("\n", prompt_template.messages)

# input_variables=['style', 'text'] input_types={} partial_variables={} template='把由三个反引号分隔的文本翻译成一种{style}风格。文本：```{text}```\n'
print("\n", prompt_template.messages[0].prompt)


# 2、格式化消息
customer_email="""
嗯呐，我现在可是火冒三丈，我那个搅拌机盖子竞然飞了出去，把我厨房的墙壁都溅上了果汁！
更糟糕的是，保修条款可不包括清理我厨房的费用。
伙计，赶紧给我过来！
"""

customer_style="""正式普通话 \
用一个平静、尊敬的语气
"""

customer_messages = prompt_template.format_messages(
    style=customer_style, 
    text=customer_email)


# 客户消息类型： <class 'list'>
print("客户消息类型：", type(customer_messages), "\n")


# 第一个客户消息类型： <class 'langchain_core.messages.human.HumanMessage'> 
print("第一个客户消息类型：", type(customer_messages[0]), "\n")


# 第一个客户消息： content='把由三个反引号分隔的文本翻译成一种正式普通话 用一个平静、尊敬的语气\n风格。文本：```\n嗯呐，我现在可是火冒三丈，我那个
# 搅拌机盖子竞然飞了出去，把我厨房的墙壁都溅上了果汁！\n更糟糕的是，保修条款可不包括清理我厨房的费用。\n伙计，赶紧给我过来！\n```\n' additional_kwargs={} response_metadata={}
print("第一个客户消息：", customer_messages[0], "\n")
