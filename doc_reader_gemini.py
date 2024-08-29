import os
import google.generativeai as genai
from google.api_core import retry
from dotenv import load_dotenv
load_dotenv()
import docx2txt
import time


file_path = input("Enter the Path: ")
print(file_path)

# Extract the Text:

text = docx2txt.process(file_path)
print(text)

# Configuring the Gemini Model

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instruction = "Behave like the best pdf reader and data scrapper. Give the final data as like in the pdf strictly. Dont assign anything unrelated strictly."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config=genai.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type='text/plain',
), system_instruction=instruction, safety_settings=safety)

input_prompt = "What is the name of the person mentioned in the text extracted. What are all the educational institutions he studied, What courses he studied in each educational institutions. Tell me the name of the projects he worked strictly. Dont assign anything other than that compulsorily. Dont give the data in json format and Give the data section wise strictly. Dont need any table format strictly."

prompt = f"""
Text Extracted: {text}

Prompt: {input_prompt}
"""
def get_response(prompt):
    response = model.generate_content(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    return response.text

start_time = time.time()
print(start_time)

data = get_response(prompt)
data = data.replace("**","").replace("#","").replace("*","")
print(data)

end_time = time.time()
print(end_time)

duration = end_time - start_time
print(duration)