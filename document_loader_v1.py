# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import UnstructuredPDFLoader
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import os
from prompts import refine_template,p0_prompt_template,json_prompt_template,raw_text_template,json_prompt_template_p1
# #UnstructuredPDF
# loader_uns = UnstructuredPDFLoader("Data/Bryce-Hoffman-Transcript-WBECS-2022-Full-Summit.pdf",
#                                    mode="elements")
# data = loader_uns.load()
# data[0]

# PyPDF
loader = PyPDFLoader("Data/Bryce-Hoffman-Transcript-WBECS-2022-Full-Summit.pdf")
pages = loader.load_and_split()
data = loader.load()
data[0]


os.environ['OPENAI_API_KEY'] = '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'
llm = OpenAI(temperature=0)
chain = load_summarize_chain(llm, chain_type="refine")
chain.run(data)


class DocSummaryBot:
    def __init__(self,relative_doc_path):
        self.path = PyPDFLoader(relative_doc_path)
        self.refine_prompt = PromptTemplate(
    input_variables=["previous_page_HTML","raw_text_latest","json","page"],
    template=refine_template,
)
        self.PROMPT = PromptTemplate(template=p0_prompt_template, input_variables=["text"])
        self.PROMPT_JSON = PromptTemplate(template=json_prompt_template, input_variables=["text"])
        self.raw_PROMPT = PromptTemplate(template=raw_text_template, input_variables=["text"])
        self.PROMPT_JSON_P1 = PromptTemplate(
    input_variables=["text","json"],
    template=json_prompt_template_p1,
)
        
    def load_doc(self,doc_name):
        loader = PyPDFLoader(self.path +"/" +doc_name)
        pages = loader.load_and_split()
        self.data = loader.load()
        
    def init_llms(self):
        self.LLM_chain = LLMChain(
    llm=OpenAI(temperature=0,max_tokens=300), 
    prompt=self.PROMPT, 
    verbose=True, 
)
        self.LLM_chain_json = LLMChain(
    llm=OpenAI(temperature=0,max_tokens=300), 
    prompt=self.PROMPT_JSON, 
    verbose=True, 
)
        self.LLM_chain_raw = LLMChain(
    llm=OpenAI(temperature=0,model_name='gpt-3.5-turbo'), 
    prompt=self.raw_PROMPT, 
    verbose=True, 
)
        self.llm_chain_p1 = LLMChain(prompt=self.refine_prompt, llm=OpenAI(temperature=0))
        self.llm_json_p1 = LLMChain(prompt=self.PROMPT_JSON_P1, llm=OpenAI(temperature=0))
        
        
    def create_summary_pages(self):
        self.overall_summary = ''
        for page_num in range(len(self.data)):
            if page_num == 0:
                response = self.LLM_chain.predict(self.data[page_num].page_content)
                response_json = self.LLM_chain_json.predict(response)
                response_raw = self.LLM_chain_raw.predict(self.data[page_num].page_content)
                self.overall_summary += response + '\n'
            else:
                response = self.llm_chain_p1.predict(previous_page_HTML=response,
                    json=response_json,
                    raw_text_latest=response_raw,
                    page=self.data[page_num].page_content)
                response_raw = self.LLM_chain_raw.predict(self.data[page_num].page_content)
                response_json = self.LLM_json_p1.predict(response)
                self.overall_summary += response + '\n'
                
    def save_summary(self):
        with open("summary.html",'w') as file:
            file.write(self.overall_summary)
        
            

if __name__ == "__main__":
    doc_summary_bot = DocSummaryBot("Personal/NotesIT/Code/Data")
    doc_summary_bot.load_doc("Bryce-Hoffman-Transcript-WBECS-2022-Full-Summit.pdf")
    doc_summary_bot.init_llms()
    doc_summary_bot.create_summary_pages()
    doc_summary_bot.save_summary()    
            
        
        
        
        