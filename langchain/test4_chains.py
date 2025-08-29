
# 简单顺序链（一个输入和一个输出）

# 顺序链（多个输入和多个输出）

# 路由器
# 路由链（Router Chain）：路由器链本身，负责选择要调用的下一个链
# 目标链（Destination Chains）：路由器可以路由到的链
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import PromptTemplate
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain_community.callbacks.fiddler_callback import MODEL_NAME

# 1、定义提示模板
#第一个提示适合回答物理问题
physics_template="""你是一个非常聪明的物理专家。\
你擅长用一种简洁并且易于理解的方式去回答问题。\
当你不知道问题的答案时，你承认\
你不知道

这是一个问题：
{input}"""


#第二个提示适合回答数学问题
math_template="""你是一个非常优秀的数学家。\
你擅长回答数学问题。\
你之所以如此优秀，\
是因为你能够将棘手的问题分解为组成部分，\
回答组成部分，然后将它们组合在一起，回答更广泛的问题。

这是一个问题：
{input}"""


#第三个适合回答历史问题
history_template="""你是以为非常优秀的历史学家。\
你对一系列历史时期的人物、事件和背景有着极好的学识和理解\
你有能力思考、反思、辩证、讨论和评估过去。\
你尊重历史证据，并有能力利用它来支持你的解释和判断。\

这是一个问题：
{input}"""


#第四个适合回答计算机问题
computerscience_template="""你是一个成功的计算机科学专家。\
你有创造力、协作精神、\
前瞻性思维、自信、解决问题的能力、\
对理论和算法的理解以及出色的沟通技巧。\
你非常擅长回答编程问题。\
你之所以如此优秀，是因为你知道\
如何通过以机器可以轻松解释的命令式步骤描述解决方案来解决问题，\
并且你知道如何选择在时间复杂性和空间复杂性之间取得良好平衡的解决方案。\

这还是一个输入：
{input}"""

# 2、对提示模板进行命名和描述
prompt_infos= [
    {
        "名字": "物理学",
        "描述": "擅长回答关于物理学的问题",
        "提示模板": physics_template
    },
    {
        "名字": "数学",
        "描述": "擅长回答数学问题",
        "提示模板": math_template
    },
    {
        "名字": "历史",
        "描述": "擅长回答历史问题",
        "提示模板": history_template
    },
    {
        "名字": "计算机科学",
        "描述": "擅长回答计算机科学问题",
        "提示模板": computerscience_template
    }
]


# 3、创建目标链

# 构建名字和链的关系
destination_chains = {}
for p_info in prompt_infos: 
    name = p_info["名字"]
    prompt_template = p_info["提示模板"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    # chain = LLMChain(llm=llm, prompt=prompt)
    # destination_chains[name] = chain


# 构建名字和描述的关系
# ['物理学:擅长回答关于物理学的问题', '数学:擅长回答数学问题', '历史:擅长回答历史问题', '计算机科学:擅长回答计算机科学问题']
destinations = [f"{p['名字']}:{p['描述']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

# 4、创建默认目标连
# 当路由器无法决定使用哪个子链时调用的链
default_prompt = ChatPromptTemplate.from_template("{input}")
# default_chain = LLMChain(llm=llm, prompt=default_prompt)


# 5、定义不同链之间的路由模板

# 多提示路由模板
MULTI_PROMPT_ROUTER_TEMPLATE = """给语言模型一个原始文本输入，\
让其选择最适合输入的模型提示。\
系统将为您提供可用提示的名称以及最适合改提示的描述。\
如果你认为修改原始输入最终会导致语言模型做出更好的响应，\
你也可以修改原始输入。


<< 格式 >>
返回一个带有JSON对象的markdown代码片段，该JSON对象的格式如下：
```json
{{{{
    "destination"：字符串\使用的提示名字或者使用"DEFAULT"
    "next_inputs"：字符串\原始输入的改进版本
}}}}



记住："destination"必须是下面指定的候选提示名称之一，\
或者如果输入不太适合任何候选提示，\
则可以是"DEFAULT"。
记住：如果您认为不需要任何修改，
则"next_inputs"可以只是原始输入。

<< 候选提示 >>
{destinations}

<< 输入 >>
{{input}}

<< 输出（记得要包含```json) >>

样例：
<< 输入 >>
"什么是黑体辐射？"
<< 输出 >>
```json
{{{{
    "destination"：字符串\使用的提示名字或者使用"DEFAULT"
    "next_inputs"：字符串\原始输入的改进版本
}}}}

"""

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(destinations=destinations_str)
# print(router_template)

router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

# router_chain = LLMRouterChain.from_llm(llm, router_prompt)
# chain = MultiPromptChain(router_chain=router_chain, 
#                          destination_chains=destination_chains, 
#                          default_chain=default_chain, 
#                          verbose=True)
