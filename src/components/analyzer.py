import os
from math import ceil
import urllib.request as request
import zipfile
import langchain
import os
from src import logger
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI, OpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
import pandas as pd
from pypdf import PdfReader
from pathlib import Path
from dotenv import load_dotenv
import os
from src.constants import dtype_map
from src.utils.common import read_file , create_directories
import json
from src.config.configuration import ResumeAnalyzeConfig

load_dotenv()  # Load environment variables from .env file

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")



## component-Data Ingestion
class AnalyzeResume:
    def __init__(self , config: ResumeAnalyzeConfig):
        pass
        self.config=config
    
    def extract_text_from_pdf(self,pdf_path) -> str:
        """
        Extracts text and hyperlinks from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file.

        Returns:
            str: Extracted text and hyperlinks formatted as a string.

        Example:
            pdf_text = extract_text_from_pdf("resume.pdf")
        """
        
        # creating a pdf reader object
        reader = PdfReader(pdf_path)
        logger.info("PDF file read successfully")

        # Initialize variables to store text and links from all pages
        all_text = ""
        all_links = []

        # Loop through all pages in the PDF
        for page_num, page in enumerate(reader.pages):
            # Extract text from the current page
            text = page.extract_text()
            if text:
                all_text += text

            # Extract links (annotations) from the current page
            if "/Annots" in page:
                annotations = page["/Annots"]
                for annot in annotations:
                    annotation_obj = annot.get_object()
                    if "/A" in annotation_obj and "/URI" in annotation_obj["/A"]:
                        link = annotation_obj["/A"]["/URI"]
                        all_links.append(f"{link}")

        # Create the formatted output in a new variable
        resume = all_text
        if all_links:
            resume += "\n\nExtracted links:\n"
            resume += "\n".join(all_links)
        
        logger.info("Extraction from PDF file done and successfull")



        return resume
    
    def update_or_create_excel(self,file_path, new_data):
        """
        Updates or creates an Excel file with the given data.

        Args:
            file_path (str): Path to the Excel file.
            new_data (dict): Data to add to the Excel file.
        """
        # Convert the new data into a DataFrame
        new_df = pd.DataFrame([new_data])

        for column, dtype in dtype_map.items():
            if column in new_df.columns:
                new_df[column] = new_df[column].astype(dtype)

        # Check if the file exists
        if os.path.exists(file_path):
            # Read the existing Excel file
            try:
                existing_df = pd.read_excel(file_path)
                # Append new data
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            except Exception as e:
                print(f"Error reading the existing file: {e}")
                print("Creating a new file instead.")
                updated_df = new_df
        else:
            # If the file doesn't exist, create a new DataFrame
            updated_df = new_df

        # Save the updated DataFrame back to the Excel file
        updated_df.to_excel(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
    
    
    
    def generate_json_data_from_resume(self , resume_pdf_path):
        """
        Generates JSON data from a resume PDF and updates the results in an Excel file.

        Args:
            resume_pdf_path (str): Path to the resume PDF file.

        Process:
            - Extracts text from the PDF.
            - Constructs a prompt using a system message template.
            - Utilizes an LLM to generate JSON-formatted data.
            - Appends the JSON data to an existing Excel file or creates a new one.

        Returns:
            None
        """

        logger.info("Extracting Text from PDF...")
        resume = self.extract_text_from_pdf(resume_pdf_path)

        #model = ChatOpenAI(model = self.config.model_name)
        model = ChatOpenAI(model = self.config.model_name)

        # Reading the system prompt
        system_prompt = read_file(Path(self.config.system_prompt_path))

        logger.info("System prompt read successfully")
        
        # Replacing these characters to avoid jinja2 issues
        #system_prompt = system_prompt.replace( '{#' , '[#') 

        # Creating the system message prompt from template
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            system_prompt,
            template_format="jinja2"
        )


        # Create the human message template
        human_template = f"""
        {resume}
        """
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template,
            template_format="jinja2"
        )

        # Combine into a ChatPromptTemplate
        chat_prompt = ChatPromptTemplate.from_messages([
            system_message_prompt,
            human_message_prompt
        ])


        parser = StrOutputParser()

        # Creating LCEL chain
        chain = chat_prompt | model | parser
        logger.info("Extracting Json data...")
        json_data = chain.invoke({
            "resume" : resume
        })

        logger.info("json data generated successfully!!")
        with open("test.txt", "a") as file:
            file.write(f"\n{json_data}")

    
        new_data = json.loads(json_data)
        self.update_or_create_excel(self.config.final_results_file_path , new_data)
        


    

    def analyze_resumes(self, batch_size=100):
        """
        Processes resumes in batches and generates structured data.

        Args:
            batch_size (int): Number of resumes to process in one batch. Default is 10.

        Returns:
            None
        """
        resume_folder_path = self.config.resume_folder_path
        all_resumes = [resume for resume in os.listdir(resume_folder_path) if resume.endswith(".pdf")]

        # Calculate the number of batches
        num_batches = ceil(len(all_resumes) / batch_size)

        # Process each batch of resumes
        for batch_num in range(num_batches):
            batch_resumes = all_resumes[batch_num * batch_size : (batch_num + 1) * batch_size]
            print(f"Processing batch {batch_num + 1} with {len(batch_resumes)} resumes.")

            # Process each resume in the batch
            i = 1
            for resume in batch_resumes:
                file_path = os.path.join(resume_folder_path, resume)
                

                logger.info(f"Processing resume number: {i} with name:{resume} and path: {file_path}")
                
                self.generate_json_data_from_resume(file_path)
        