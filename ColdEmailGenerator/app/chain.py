import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq( model = "llama-3.1-70b-versatile", temperature = 0, max_tokens= None,timeout= None,max_retries= 2,groq_api_key = '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')

    def extract_jobs(self , page_data):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            the scraped text is from career's page of a website
            your job is to extract the job postings and return then in JSON format containing the
            following keys: 'role' , 'experience' ,'skills' and 'description'.
            Only return the valid JSON
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={'page_data': page_data})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too large to parse jobs")
        return res if isinstance(res, list) else [res]

    def write_mail(self , job , links):
        prompt_email = PromptTemplate.from_template(
            """ 
            ### JOB DESCRIPTION
            (job_description)

            ###INSTRUCTION:
            Your name is Ali, you are a buisness development executive at NextSolution inc. NextSolution is an AI & Software consultant
            organization dedicated to provide seamless integrationof buisness process through automated tools.
            Over our experience , we have empowered numerous enterprises with tailored solutions fostering scalibility,
            procces optimization, cost reduction and heightened overall efficiency.
            your job is to write a cold email to client regarding the job mentioned above describing the capability of mentioned 
            above in a fulfilling their needs
            Also add the most relevant ones from the following links to showcase NextSolution's portfolio:{link_list}
            Remember you are Ali, BDE at NextSolution.
            Do not provide a preamble
            ###EMAIL (NO PREAMBLE)
            """
        )

        chain_extract = prompt_email | self.llm
        res = chain_extract.invoke(input={'job_description': str(job), "link_list": links})
        return res.content

if __name__ =='__main__':
    print(os.getenv("groq_api_key"))
