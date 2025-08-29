
from langchain.prompts import ChatPromptTemplate

# 1、定义模板
review_template_2="""
对于以下文本，请从中提取以下信息：：

礼物：该商品是作为礼物送给别人的吗？
如果是，则回答是的：如果否或未知，则回答不是。

交货天数：产品到达需要多少天？如果没有找到该信息，则输出-1。

价钱：提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表。

文本：{text}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template=review_template_2)

# input_variables=['format_instructions', 'text'] 
# input_types={} partial_variables={} 
# template='\n对于以下文本，请从中提取以下信息：：\n\n礼物：该商品是作为礼物送给别人的吗？\n如果是，则回答是的：如果否或未知，则回答不
# 是。\n\n交货天数：产品到达需要多少天？如果没有找到该信息，则输出-1。\n\n价钱：提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表。\n\n
# 文本：{text}\n\n{format_instructions}\n'
print(prompt.messages[0].prompt)


from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser



# 2、定义输出结构
gift_schema = ResponseSchema(name="礼物",
    description="这件物品是作为礼物送给别人的吗？\
    如果是，则回答是的，\
    如果否或未知，则回答不是。")

delivery_days_schema=ResponseSchema(name="交货天数",
    description="产品需要多少天才能到达？\
    如果没有找到该信息，则输出-1。")

price_value_schema=ResponseSchema(name="价钱",
    description="提取有关价值或价格的任何句子，\
    并将它们输出为逗号分隔的Python列表")

response_schema = [gift_schema, 
                   delivery_days_schema, 
                   price_value_schema]

output_parser = StructuredOutputParser.from_response_schemas(response_schema)
format_instructions = output_parser.get_format_instructions();

# 输出格式规定： The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

# ```json
# {
#         "礼物": string  // 这件物品是作为礼物送给别人的吗？    如果是，则回答是的，    如果否或未知，则回答不是。
#         "交货天数": string  // 产品需要多少天才能到达？    如果没有找到该信息，则输出-1。
#         "价钱": string  // 提取有关价值或价格的任何句子，    并将它们输出为逗号分隔的Python列表
# }
# ```
print("输出格式规定：", format_instructions)



customer_review="""
这款吹叶机非常神奇。它有四个设置：\
吹蜡烛、微风、风城、龙卷风。\
两天后就到了，正好赶上我妻子的\
周年纪念礼物。\
我想我的妻子会喜欢它到说不出话来。\
到目前为止，我是唯一一个使用它的人，而且我一直\
每隔一天早上用它来清理草坪上的叶子。\
它比其他吹叶机稍微贵一点，\
但我认为它的额外功能是值得的。\
"""
messages = prompt.format_messages(text=customer_review, 
                       format_instructions=format_instructions)


# 第一条客户消息： 
# 对于以下文本，请从中提取以下信息：：

# 礼物：该商品是作为礼物送给别人的吗？
# 如果是，则回答是的：如果否或未知，则回答不是。

# 交货天数：产品到达需要多少天？如果没有找到该信息，则输出-1。

# 价钱：提取有关价值或价格的任何句子，并将它们输出为逗号分隔的 Python 列表。

# 文本：
# 这款吹叶机非常神奇。它有四个设置：吹蜡烛、微风、风城、龙卷风。两天后就到了，正好赶上我妻子的周年纪念礼物。我想我的妻子会喜欢它到说不出话来。到目前为止，我是唯一一个使用它的人，而且我一直每隔一天早上用它来清理草坪上的 
# 叶子。它比其他吹叶机稍微贵一点，但我认为它的额外功能是值得的。

# The output should be a markdown code snippet formatted in the following schema, including the leading and trailing "```json" and "```":

# ```json
# {
#         "礼物": string  // 这件物品是作为礼物送给别人的吗？    如果是，则回答是的，    如果否或未知，则回答不是。
#         "交货天数": string  // 产品需要多少天才能到达？    如果没有找到该信息，则输出-1。
#         "价钱": string  // 提取有关价值或价格的任何句子，    并将它们输出为逗号分隔的Python列表
# }
# ```
print("第一条客户消息：", messages[0].content)


