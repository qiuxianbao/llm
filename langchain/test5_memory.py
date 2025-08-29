
# eg.1 对话缓存存储
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()

# print(memory.buffer)

# <bound method ConversationBufferMemory.load_memory_variables of ConversationBufferMemory(chat_memory=InMemoryChatMessageHistory(messages=[]))>   
# print(memory.load_memory_variables)

# 直接添加内容到存储缓存
memory.save_context({"input": "你好，我是皮皮鲁"}, {"output": "你好呀，我是鲁西西"})
# {'history': 'Human: 你好，我是皮皮鲁\nAI: 你好呀，我是鲁西西'}
# print(memory.load_memory_variables({}))


# ===========================================================================================================
# eg.2 对话缓存窗口存储（只保存最近 n 次交互，用于保持最近交互的滑动窗口，以便缓冲区不会过大）
from langchain.memory import ConversationBufferWindowMemory
memory = ConversationBufferWindowMemory(k=1)
memory.save_context({"input": "你好，我是皮皮鲁"}, {"output": "你好呀，我是鲁西西"})
memory.save_context({"input": "很高兴和你成为朋友"}, {"output": "是的，让我们一起去冒险吧！"})

# {'history': 'Human: 很高兴和你成为朋友\nAI: 是的，让我们一起去冒险吧！'}
# print(memory.load_memory_variables({}))


# ===========================================================================================================
# eg.3 对话令牌缓存存储
from langchain.memory import ConversationTokenBufferMemory



# ===========================================================================================================
# eg.4 对话摘要缓存存储
from langchain.memory import ConversationSummaryBufferMemory

#
# # eg.
# import datetime
# current_date = datetime.datetime.now().date()
# if current_date < datetime.date(2023, 9, 2):
#     llm_name = "gpt-3.5-turbo-0301"
# else:
#     llm_name = "gpt-3.5-turbo"
#
# # 1.加载向量数据库
# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
#
# persist_directory_chinese = 'data/chroma/matplotlib/'
# embedding = OpenAIEmbeddings()
# vectordb = Chroma(persist_directory=persist_directory_chinese, embedding_function=embedding)
#
# # 2.进行向量检索
# question = "这节课的主要话题是什么"
# docs = vectordb.similarity_search(question, k=3)
# len(docs)
#
# # 3.创建llm
# from langchain.chat_models import ChatOpenAI
# llm = ChatOpenAI(model_name=llm_name, temperature=0)
# llm.predict("你好")
#
# # 4.创建基于模板的检索问答链
# from langchain.prompts import PromptTemplate
# # 构建prompt
# template="""使用以下上下文片段来回答最后的问题。如果你不知道答案，只需说不知道，不要试图编造
# 答案。答案最多使用三个句子。尽量简明扼要地回答。在回答的最后一定要说“感谢您的提问！”
# {context}
# 问题：{question}
# 有用的回答："""
# QA_CHAT_PROMPT = PromptTemplate.format_prompt(
#     input_variables=["context", "question"],
#     template=template,
# )
#
# from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
# qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
#     llm,
#     retriever=vectordb.as_retriever(),
#     return_source_documents=True,
#     chain_type_kwargs={"prompt": QA_CHAT_PROMPT}
# )
# result = qa_chain({"query": question})
#
# # 5.存储
# from langchain.memory import ConversationBufferMemory
#
# memory = ConversationBufferMemory(
#     # 与prompt的输入变量保持一致
#     memory_key="chat_history",
#     # 以消息列表的方式返回聊天记录，而不是单个字符串
#     return_messages=True
# )
#
# # 6.对话检索链
# # 在QA的基础上，增加了处理对话历史的能力
# # from langchain.chains import conversationalRetrievalChain
# from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
#
# qa = ConversationalRetrievalChain.from_llm(llm, retriever=vectordb.as_retriever(), memory=memory)
# result = qa_chain({"query": question})
# print(result['answer'])

