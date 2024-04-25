from langchain.retrievers.multi_vector import MultiVectorRetriever

from langchain.storage import InMemoryByteStore
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.extract_ctr import *
from common.static.config import config
model = "gpt-3.5-turbo"
openai_api_key = config['KEY']['openai_api_key']

loaders = [
    CSVLoader("./../dataset/result.csv"),
    CSVLoader("./../dataset/for_inv_trans_claude_sonnet.csv"),
]
docs = []
for loader in loaders:
    docs.extend(loader.load())
text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000)
docs = text_splitter.split_documents(docs)

vectorstore = Chroma(
    collection_name="full_documents", embedding_function=OpenAIEmbeddings(api_key=openai_api_key)
)
# The storage layer for the parent documents
store = InMemoryByteStore()
id_key = "doc_id"
# The retriever (empty to start)
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)
import uuid

doc_ids = [str(uuid.uuid4()) for _ in docs]
child_text_splitter = RecursiveCharacterTextSplitter(chunk_size=400)
sub_docs = []
for i, doc in enumerate(docs):
    _id = doc_ids[i]
    _sub_docs = child_text_splitter.split_documents([doc])
    for _doc in _sub_docs:
        _doc.metadata[id_key] = _id
    sub_docs.extend(_sub_docs)
retriever.vectorstore.add_documents(sub_docs)
retriever.docstore.mset(list(zip(doc_ids, docs)))
from langchain.retrievers.multi_vector import SearchType

retriever.search_type = SearchType.mmr
print(retriever.vectorstore.similarity_search("솜퐁 폴 올라리그")[0].page_content)