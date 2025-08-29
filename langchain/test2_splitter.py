from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

# chunk_size = 20 #块大小
# chunk_overlap = 10 #设置块重叠大小

# eg.1
# 递归字符文本分隔器
# r_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#
# text="在AI的研究中，由于大模型规模非常大，模型参数很多，在大模型上跑完来验证参数好不好训练时间成本很高，所以一般会在小模型上做消融实验来验证哪些改进是有效的再去大模型上做实验。"
# r_splitter_split_text = r_splitter.split_text(text)
# ['在AI的研究中，由于大模型规模非常大，模',
#  '大模型规模非常大，模型参数很多，在大模型',
#  '型参数很多，在大模型上跑完来验证参数好不',
#  '上跑完来验证参数好不好训练时间成本很高，',
#  '好训练时间成本很高，所以一般会在小模型上',
#  '所以一般会在小模型上做消融实验来验证哪些',
#  '做消融实验来验证哪些改进是有效的再去大模',
#  '改进是有效的再去大模型上做实验。']
# print(r_splitter_split_text)

# eg.2
# 字符文本分割器，默认以换行符为分隔符
# c_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
# c_splitter_split_text = c_splitter.split_text(text)
# ['在AI的研究中，由于大模型规模非常大，模型参数很多，在大模型上跑完来验证参数好不好训练时间成本很高，所以一般会在小模型上做消融实验来验证哪些改进是有效的再去大模型上做实验。']
# print(c_splitter_split_text)


# 指定分隔符：以，进行分隔
# c_splitter = CharacterTextSplitter(
#     chunk_size=chunk_size,
#     chunk_overlap=chunk_overlap,
#     separator='，'
# )
# c_splitter_split_text = c_splitter.split_text(text)
# # ['在AI的研究中，由于大模型规模非常大',
# #  '由于大模型规模非常大，模型参数很多',
# #  '在大模型上跑完来验证参数好不好训练时间成本很高',
# #  '所以一般会在小模型上做消融实验来验证哪些改进是有效的再去大模型上做实验。']
# print(c_splitter_split_text)


# eg.3
# 长文本分隔
some_text="""在编写文档时，作者将使用文档结构对内容进行分组。 \
    这可以向读者传达哪些想法是相关的。 例如，密切相关的想法\
    是在句子中。类似的想法在段落中。 段落构成文档。 \n\n
    段落通常用一个或两个回车符分隔。 \
    回车符是您在该字符串中看到的嵌入的“反斜杠n”。 \
    句子末尾有一个句号，但也有一个空格。 \
    并目单词之间用空格分隔"""

# 177
# print(len(some_text))

# c_splitter = CharacterTextSplitter(chunk_size=80, chunk_overlap=0, separator=' ')
# c_splitter_split_text = c_splitter.split_text(some_text)
# ['在编写文档时，作者将使用文档结构对内容进行分组。 这可以向读者传达哪些想法是相关的。 例如，密切相关的想法 是在句子中。类似的想法在段落中。 段落构成文档。',
#  '段落通常用一个或两个回车符分隔。 回车符是您在该字符串中看到的嵌入的“反斜杠n”。 句子末尾有一个句号，但也有一个空格。 并目单词之间用空格分隔']
# print(c_splitter_split_text)

# r_splitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=0, separators=["\n\n", "\n", " ", ""])
# r_splitter_split_text = r_splitter.split_text(some_text)
# ['在编写文档时，作者将使用文档结构对内容进行分组。     这可以向读者传达哪些想法是相关的。 例如，密切相关的想法    是在句子中。类似的想法在段落中。',
# '段落构成文档。',
# '段落通常用一个或两个回车符分隔。     回车符是您在该字符串中看到的嵌入的“反斜杠n”。     句子末尾有一个句号，但也有一个空格。', '并目单词之间用空格分隔']
# print(r_splitter_split_text)


# eg.4
# 基于token分隔
from langchain.text_splitter import TokenTextSplitter
#
# text_splitter = TokenTextSplitter(chunk_size=1, chunk_overlap=0)
# text = "foo bar bazzyfoo"
# text_splitter_split_text = text_splitter.split_text(text)

# 对于英文输入，一个token一般对应4个字符或者四分之三个单词；
# 对于中文输入，一个token一般对应一个或半个词。
# ['foo', ' bar', ' b', 'az', 'zy', 'foo']
# print(text_splitter_split_text)


# eg.5
# 基于markdown分隔


markdown_document="""# TitTe\n\n \
## 第一章\n\n \
李白乘舟将欲行\n\n忽然岸上踏歌声\n\n \
### Section\n\n\ \
桃花潭水深千尺\n\n
## 第二章\n\n\ \
不及汪伦送我情"""

# #TitTe
#
# ##第一章
#
#
# 李白乘舟将欲行
#
# 忽然岸上踏歌声
#
# ###Section
#
# 桃花潭水深千尺
#
#
# ##第二章
#
# 不及汪伦送我情
# print(markdown_document)

from langchain.text_splitter import MarkdownHeaderTextSplitter
headers_to_split_on=[
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)

#
print(len(md_header_splits))
# page_content='李白乘舟将欲行
# 忽然岸上踏歌声' metadata={'Header 1': 'TitTe', 'Header 2': '第一章'}
# print(md_header_splits[0])

# page_content='\ 桃花潭水深千尺' metadata={'Header 1': 'TitTe', 'Header 2': '第一章', 'Header 3': 'Section'}
# print(md_header_splits[1])



