
import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"

# 1.加载向量数据库
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

persist_directory_chinese = 'data/chroma/matplotlib/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory_chinese, embedding_function=embedding)

# 2.进行向量检索
question = "这节课的主要话题是什么"
docs = vectordb.similarity_search(question, k=3)
len(docs)

# 3.构建检索式问答链
from langchain.chat_models import ChatOpenAI
# from langchain.chains import RetrievalQA
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain

llm = ChatOpenAI(model_name=llm_name, temperature=0)
# 3.1定义一个检索问答链
qa_chain = RetrievalQAWithSourcesChain.from_chain_type(llm, retriever=vectordb.as_retriever())
result = qa_chain({"query": question})
print(result["result"])


# 3.2 基于模板构建检索问答链
from langchain.prompts import PromptTemplate
# 构建prompt
template="""使用以下上下文片段来回答最后的问题。如果你不知道答案，只需说不知道，不要试图编造
答案。答案最多使用三个句子。尽量简明扼要地回答。在回答的最后一定要说“感谢您的提问！”
{context}
问题：{question}
有用的回答："""
QA_CHAT_PROMPT = PromptTemplate.format_prompt(template)

qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAT_PROMPT}
)
result = qa_chain({"query": question})

# 3.3基于mapreduce/refine的检索式问答链
qa_chain_mr = RetrievalQAWithSourcesChain.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    # chain_type="map_reduce"
    chain_type="refine"
)
