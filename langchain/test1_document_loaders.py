
# pip install openai
# pip install python-dotenv
# pip install langchain
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI #open ai模型

# from langchain.document_loaders import CSVLoader #文档加载器，采用csv格式存储
from langchain_community.document_loaders import CSVLoader

# from langchain.vectorstores import DocArrayInMemorySearch #向量存储
from langchain_community.vectorstores import DocArrayInMemorySearch

# 报错No module named IPython的所有解决方法
# https://blog.csdn.net/weixin_39585934/article/details/90384019
# pip install notebook
# pip install ipython
# pip install jupyter
from IPython.display import display, Markdown #在jupyter显示信息的工具

import pandas as pd

from langchain.chains import RetrievalQA #检索QA链，在文档上进行检索
import os


# eg.1加载csv
# file = 'C:/VsCode/llm/langchain/data/t_elec_ap_code.csv'
# loader =  CSVLoader(file_path=file)

# data = pd.read_csv(file, skiprows=0)

# data = pd.read_csv(file,usecols=[1,2,3,4])
#             type  code  byte_value  description
# 0  charge_finish    64          40            1
# 1  charge_finish    65          41            2
# 2  charge_finish   132          84            3
# 3  charge_finish   133          85            4
# 4  charge_finish   134          86            5
# print(data.head())


# 向量存储，Vector Stores
# from langchain.indexes import VectorstoreIndexCreator
# 基于文档加载器创建向量存储
# index = VectorstoreIndexCreator(vectorstore_cls=DocArrayInMemorySearch).from_loaders([loader])

# 直接查询向量存储
# query = "1"
# response = index.query(query)
# display(Markdown(response))


# 向量嵌入，Embedding Models\
# 通过csv格式加载
# docs = loader.load()

# 查看单个文档，每个文档对应CSV的一行数据
# page_content='
# id: 1
# type: charge_finish
# code: 64
# byte_value: 40
# description: 1
# ' metadata={'source': 'C:/VsCode/llm/langchain/data/t_elec_ap_code.csv', 'row': 0}
# print(docs[0])

# from langchain.embeddings import OpenAIEmbeddings
# embeddings = OpenAIEmbeddings()

# embed = embeddings.embed_query("你好呀，我的名字叫小可爱")
# print("向量表征的长度：", len(embed))
# print("向量表征前5个元素", embed[:5])

# 基于向量表征创建并查询向量存储
# db = DocArrayInMemorySearch.from_documents(docs, embeddings)
# query = "请推荐一件具有防晒功能的衬衣"
# docs = db.similarity_search(query)

# print("返回文档的个数\n" + len(docs))
# print("第一个文档\n" + docs[0])

#
import langchain
langchain.debug=True


# eg.2 加载pdf
# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader

# loader = PyPDFLoader("data/test.pdf")
# pages = loader.load()

# 1
# print(len(pages))   # pdf的页数

# <class 'list'>
# print(type(pages))

# <class 'langchain_core.documents.base.Document'>
# print(type(pages[0]))

# [Document(metadata={
# 'producer': '', 'creator': 'WPS 文字', 'creationdate': '2025-04-01T14:05:06+08:00',
# 'author': 'admin', 'comments': '', 'company': '', 'keywords': '',
# 'moddate': '2025-04-01T14:05:06+08:00', 'sourcemodified': "D:20250401140506+08'00'", 'subject': '', 'title': '',
# 'trapped': '/False', 'source': 'data/test.pdf', 'total_pages': 1, 'page': 0, 'page_label': '1'
# },
# page_content='测试文档\n要打开附加到一个电子邮件的 PDF 文档，可打开电子邮件，然后双击 PDF 图标。 要打开\n链接到已打开网页的 PDF，请单击 PDF 文件链接。 通常在网络浏览器内打开 PDF。 请双\n击文件系统中的 PDF 文件图标。 注意: 在 Mac OS 中，您有时无法通过双击图标打开在\nWindows 中创建的 PDF。 取而代之，请选择“文件”>“打开方式”>“Acrobat”。Acrobat 是一\n款软件 ，它可以用来查看、创建以及编辑 PDF 文件；Acrobat Reader 则是它的免费版，只\n能用于查看以及创建简单的 PDF 文件。 PDF 则是一种文档格式，它由 Adobe 公司发明。\nPDF 全称「Portable Document Format 便携式文档格式」，\n由 Adobe 的联合创始人 John Warnock 于 1991 正式发布，距今已有 25 年历史。最常用也\n是最直接的方式当然是使用 PDF 阅读器，我们可以下载安装极速 PDF 阅读器后，在 PDF 文\n档处右击选择以极速 PDF 阅读器打开即可。 （也可将其设置为默认打开方式，下次直接双\n击即可打开 PDF 文档） 同时还能一边阅读 PDF 文档，\n一边在重点内容上做相应的批注，点击导航栏中的“注释”切换到注释页面，点击工具栏的注\n释工具即可操作。')
# ]
# print(pages)

# page_content='测试文档
# 要打开附加到一个电子邮件的 PDF 文档，可打开电子邮件，然后双击 PDF 图标。 要打开
# 链接到已打开网页的 PDF，请单击 PDF 文件链接。 通常在网络浏览器内打开 PDF。 请双
# 击文件系统中的 PDF 文件图标。 注意: 在 Mac OS 中，您有时无法通过双击图标打开在
# Windows 中创建的 PDF。 取而代之，请选择“文件”>“打开方式”>“Acrobat”。Acrobat 是一
# 款软件 ，它可以用来查看、创建以及编辑 PDF 文件；Acrobat Reader 则是它的免费版，只
# 能用于查看以及创建简单的 PDF 文件。 PDF 则是一种文档格式，它由 Adobe 公司发明。
# PDF 全称「Portable Document Format 便携式文档格式」，
# 由 Adobe 的联合创始人 John Warnock 于 1991 正式发布，距今已有 25 年历史。最常用也
# 是最直接的方式当然是使用 PDF 阅读器，我们可以下载安装极速 PDF 阅读器后，在 PDF 文
# 档处右击选择以极速 PDF 阅读器打开即可。 （也可将其设置为默认打开方式，下次直接双
# 击即可打开 PDF 文档） 同时还能一边阅读 PDF 文档，
# 一边在重点内容上做相应的批注，点击导航栏中的“注释”切换到注释页面，点击工具栏的注
# 释工具即可操作。
# ' metadata={'producer': '', 'creator': 'WPS 文字', 'creationdate': '2025-04-01T14:05:06+08:00', 'author': 'admin', 'comments': '', 'company': '', 'keywords': '', 'moddate': '2025-04-01T14:05:06+08:00', 'sourcemodified': "D:20250401140506+08'00'", 'subject': '', 'title': '', 'trapped': '/False',
# 'source': 'data/test.pdf', 'total_pages': 1, 'page': 0, 'page_label': '1'}
# page = pages[0]
# print(page)


# eg.3 加载网页内容
# from langchain.document_loaders import WebBaseLoader
from langchain_community.document_loaders import WebBaseLoader

# url = "https://github.com/datawhalechina/d2l-ai-solutions-manual/blob/master/docs/README.md"
# loader = WebBaseLoader(web_path=url)
# pages = loader.load()
# Type of Pages: <class 'list'>
# print("Type of Pages:", type(pages))
# Length of Pages: 1
# print("Length of Pages:", len(pages))

# page = pages[0]
# print("Page_content:", page.page_content)
# Meta_Data: {'source': 'https://github.com/datawhalechina/d2l-ai-solutions-manual/blob/master/docs/README.md', 'title': 'd2l-ai-solutions-manual/docs/README.md at master · datawhalechina/d2l-ai-solutions-manual · GitHub', 'description': '《动手学深度学习》习题解答，在线阅读地址如下：. Contribute to datawhalechina/d2l-ai-solutions-manual development by creating an account on GitHub.', 'language': 'en'}
# print("Meta_Data:", page.metadata)


# 提取有用的json，去除冗余信息
import json
#
# page_content = """
# {
# 	"state": 0,
# 	"desc": "成功",
# 	"value": {
# 		"deptProjectId": "1869751603304575087",
# 		"deptId": "1",
# 		"deptName": "爱充电"
# 	}
# }
# """
# convert_to_json = json.loads(page_content)
# # <class 'dict'>
# print(type(convert_to_json))
#
# extracted_json = convert_to_json['value']['deptName']
# print(extracted_json)

