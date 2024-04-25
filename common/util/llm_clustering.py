import pandas as pd
from openai import OpenAI
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from preprocessing_data.extract_ctr import *
from common.static.config import config
from preprocessing_data.utils import *
from load_dataset import load_data
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
model = "gpt-3.5-turbo"
openai_api_key = config['KEY']['openai_api_key']
client= OpenAI(api_key=openai_api_key)
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__4aba590bc7184265b424dceb302ece55"

def return_samename(names , total_name):
    system_prompt = """
        You are a helpful assistant for comparing names.
        i'll give you 'input some names' those can be separated with '|', and your job is find if name is in 'total_name'.
        For example, if I give input some names : [Ju Hwi LEE|Krishna T.  Malladi|Oscar P. Pinto], and total_name : ['유경인', '유경탁', '유광선', '크리슈나 T. 말라디', '유근영', '유동근', '오스카 P. 핀토'], you should answer [False, True, True].
        Never answer anything else except 'True' or 'False'.
        """
    input_prompt = """
        Given input some names is [SOME_NAME].
        Given total_name is [TOTAL_NAME].
        """
    input_prompt = input_prompt.replace("[SOME_NAME]", str(names)).replace("[TOTAL_NAME]", str(total_name))
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_prompt}
        ]
    )
    return completion.choices[0].message.content

def langchain_rag(retriever, name):
    # ex_prompt = """
    #     You are a helpful assistant for comparing names.
    #     i'll give you 'input name' and your job is find if name is in 'total_name'.
    #     If there is no name in 'total_name', answer 'False'.
        
    #     Given input some names is [SOME_NAME].
    #     """
    # # For example, if I give input some names : [Ju Hwi LEE|Krishna T.  Malladi|Oscar P. Pinto], and total_name : ['유경인', '유경탁', '유광선', '유근영', '유동근', '오스카 P. 핀토'], you should answer ['오스카 P. 핀토']].
    # ex_prompt=ex_prompt.replace("[SOME_NAME]",name)
    search_result = retriever.get_relevant_documents(name)
    return search_result[0]
def main():
    trans_df = pd.read_csv("./../dataset/for_inv_trans_claude_sonnet_withoutsame.csv")
    
    name_list = trans_df["translated"].to_list()
    
    # loader = CSVLoader(file_path="./../dataset/result.csv")
    # data = loader.load()
    # text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=20)
    # texts = text_splitter.split_documents(data)
    embeddings = OpenAIEmbeddings(api_key=openai_api_key)
    # db = FAISS.from_documents(texts, embeddings)
    # db.save_local("./../model/faiss_index")
    db = FAISS.load_local("./../model/faiss_index", embeddings, allow_dangerous_deserialization = True)
    threshold = 0.75
    retriever = db.as_retriever(
        search_type="similarity_score_threshold", search_kwargs={"k":1,"score_threshold": threshold}
    )
    result_list =[]
    name_list2=[]
    for name in name_list:
        if len(name)>3:
            result = langchain_rag(retriever, name)
            name_list2.append(name)
            result_list.append(result)
    result_df = pd.DataFrame()
    result_df["names"] = name_list2
    result_df["search_result"] = result_list
    result_df.to_csv(f"./../dataset/result/langchain_rag_with_trans_{str(threshold)}.csv",index=False)
# def main():  
#     split_same_notsame()
    # df2.to_csv("./../dataset/for_inv_trans_claude_sonnet_explode.csv", index=False)
    # name_list= df["name"].to_list()
    
    # trans_list = df2["translated"].to_list()
    # result_list =[]
    # result_list2 =[]
    # for trans in trans_list:
    #     trans = trans.split("|")
    #     for tran in trans:
    #         if tran not in name_list:
    #             result_list.append(tran)
    #         else :
    #             result_list2.append(tran)
            
    
    # df_result = pd.DataFrame()
    # df_result["trans"] = df2["translated"]
    # df_result["tf"] = result_list
    # df_result.to_csv("./../dataset/result/llm_result.csv", index=False)


if __name__ == "__main__":
    main()
