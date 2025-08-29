#
# # eg.1
# # 加载文档 & 分隔文本 & 存储向量
# # from langchain.document_loaders import PyPDFLoader
# # from langchain_community.document_loaders import PyPDFLoader
# #
# # loaders_pdfs = [
# #     # 测试添加重复文档
# #     PyPDFLoader("data/test.pdf"),
# #     PyPDFLoader("data/test.pdf"),
# #     PyPDFLoader("data/test2.pdf")
# # ]
# #
# # # 1.加载文档
# # docs = []
# # for loader in loaders_pdfs:
# #     docs.extend(loader.load())
# #
# # # 2.分隔文本
# # from langchain.text_splitter import RecursiveCharacterTextSplitter
# # r_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=15)
# # splits = r_splitter.split_documents(docs)
# #
# # # 15
# # # print(len(splits))
# #
# #
# # # from langchain.embeddings.openai import OpenAIEmbeddings
# # from langchain_community.embeddings import OpenAIEmbeddings
# #
# # # 3.1.词向量
# # embedding = OpenAIEmbeddings()
# #
# # # sentence1_zh = "我喜欢狗"
# # # sentence2_zh = "我喜欢犬科动物"
# # # sentence3_zh = "外面的天气很糟糕"
# # #
# # # embedding_sentence1 = embedding.embed_query(sentence1_zh)
# # # embedding_sentence2 = embedding.embed_query(sentence2_zh)
# # # embedding_sentence3 = embedding.embed_query(sentence3_zh)
# # #
# # # import numpy as np
# # # np.dot(embedding_sentence1, embedding_sentence2)
# # # np.dot(embedding_sentence1, embedding_sentence3)
# # # np.dot(embedding_sentence2, embedding_sentence3)
# #
# #
# # from langchain.vectorstores import Chroma
# # # 3.2.向量存储库
# # persist_directory_chinese = 'data/chroma/matplotlib'
# # vectordb_chinese = Chroma.from_documents(
# #     documents=splits,
# #     embedding=embedding,
# #     persist_directory=persist_directory_chinese  # 允许将persist_directory_chinese目录保存到磁盘上
# # )
# #
# # # 此处和 len(splits) 是一样的
# # print(vectordb_chinese._collection.count())
# #
# # # 相似性搜索
# # # 基本的相似性搜索很容易就能让你完成80%的工作，但是会出现一些相似性搜索失败的情况
# # question_chinese = "Matlablib是什么"
# # docs_chinese = vectordb_chinese.similarity_search(question_chinese)
# # print(len(docs_chinese))
# #
# # print(docs_chinese[0].page_content)
# #
# # # 持久化
# # vectordb_chinese.persist()
#
#
#
# # eg.2.1 基本语义相似度（Basic semantic similarity)
# # 加载向量数据库
# from langchain.vectorstores import Chroma
# from langchain.embeddings.openai import OpenAIEmbeddings
#
# persist_directory_chinese = 'data/chroma/matplotlib/'
# embedding = OpenAIEmbeddings()
# # 加载
# vectordb_chinese = Chroma(persist_directory=persist_directory_chinese, embedding_function=embedding)
# print(vectordb_chinese._collection.count())
#
# texts_chinese=[
#     """毒鹅膏菌（Amanita phalloides）具有大型且引人注目的地上（epigeous）子实体(basidiocarp)""",
#     """一种具有大型子实体的蘑菇是毒鹅膏菌（Amanita phalloides）。某些品种全白。""",
#     """A.phalloides，又名死亡帽，是已知所有蘑菇中最有毒的一种。""",
# ]
# # 存储文本
# smalldb_chinese = Chroma.from_texts(texts_chinese, embedding=embedding)
#
# question_chinese = "告诉我关于具有大型子实体的全白色蘑菇的信息"
#
# # 根据问题的语义去向量库搜索与之相关性最高的文档
# # k设置为0，只返回2个相关的文档
# # 存在一些问题：第1句和第2句含义非常接近，只返回一个就满足要求了，目前返回了2条，是一种资源的浪费
# smalldb_chinese.similarity_search(question_chinese,k=2)
#
#
# # eg.2.2 最大边际相关性（Maximum marginal relevance，MMR）
# question_chinese = "Matplotlib是什么？"
# docs_mmr_chinese = vectordb_chinese.max_marginal_relevance_search(question_chinese, k=3)
#
#
# # eg.2.3 使用元数据（Including Metadata）
# question_chinese = ""
# docs_chinese = vectordb_chinese.similarity_search(
#     question_chinese,
#     k=3,
#     # 不能没每次都采用手动的方式来解决这个问题
#     filter={"source": "data/test.pdf"}
# )
#
#
# # eg.2.4 LLM辅助检索（LLM Aided Retrieval
# # 如何自动从用户问题中提取过滤信息
# from langchain.llms import OpenAI
# from langchain.retrievers.self_query.base import SelfQueryRetriever
# from langchain.chains.query_constructor.base import AttributeInfo
#
# llm = OpenAI(temperature=0)
#
# medata_field_info_chinese = [
#     AttributeInfo(
#         # 告诉LLM我们想要的数据来源
#         name="source",
#         description="The lecture the chunk is from, should be one of 'data/test.pdf', 'data/test2.pdf'",
#         type="string",
#     ),
#     AttributeInfo(
#         # 告诉LLM我们需要提取相关的内容在原始文档的哪一页
#         name="page",
#         description="The page from lecture",
#         type="integer",
#     )
# ]
#
# document_content_description_chinese = "Matplotlib 课堂"
# retriever_chinese = SelfQueryRetriever.from_llm(
#     llm,
#     vectordb_chinese,
#     document_content_description_chinese,
#     medata_field_info_chinese,
#     verbose=True
# )
#
# query_chinese = "他们在第二讲中对Figure做了些什么"
# docs_chinese = retriever_chinese.get_relevant_documents(query_chinese)
# for d in docs_chinese:
#     print(d.metadata)
#
#
# # eg.2.5 压缩
# from langchain.retrievers import ContextualCompressionRetriever
# from langchain.retrievers.document_compressors import LLMChainExtractor
#
# llm=OpenAI(temperature=0)
# # 创建压缩器
# compressor = LLMChainExtractor.from_llm(llm)
#
# # 对源文档进行压缩
# compression_retriever_chinese = ContextualCompressionRetriever(
#     # 压缩器
#     base_compressor=compressor,
#     # 检索器
#     # base_retriever=vectordb_chinese.as_retriever()
#     base_retriever=vectordb_chinese.as_retriever(search_type="mmr")
# )
#
# question_chinese = "Matplotlib是什么"
# compressed_docs_chinese = compression_retriever_chinese.get_relevant_documents(query_chinese)
#
#
# # eg.2.6 其他类型的检索
# from langchain.retrievers import SVMRetriever
# from langchain.retrievers import TFIDFRetriever
# from langchain.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
#
# # 加载pdf
# loader_chinese = PyPDFLoader("data/test.pdf")
# pages_chinese = loader_chinese.load()
# # 数组
# all_page_text_chinese = [p.page_content for p in pages_chinese]
# # 将all_page_text_chinese 列表中的所有字符串通过空格" "连接成一个完整的字符串
# joined_page_text_chinese = " ".join(all_page_text_chinese)
#
# # 分隔文本
# text_splitter_chinese = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
# split_chinese = text_splitter_chinese.split_text(joined_page_text_chinese)
#
# # 检索
# svm_retriever = SVMRetriever.from_texts(split_chinese, embedding)
# tfidf_retriever = TFIDFRetriever.from_texts(split_chinese)
#
# question_chinese = "Matplotlib是什么"
# docs_svm_chinese = svm_retriever.get_relevant_documents(query_chinese)
# docs_tfidf_chinese = tfidf_retriever.get_relevant_documents(query_chinese)
