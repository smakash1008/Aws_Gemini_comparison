from dotenv import load_dotenv
load_dotenv()
import boto3
import json
import docx2txt
import time

file_path = input("Enter the Path: ")
print(file_path)

text = docx2txt.process(file_path)
print(text)

session = boto3.Session(aws_access_key_id="your_aws_access_key", aws_secret_access_key="your_aws_secret_access_key", region_name="us-west-2")

client = session.client("bedrock-runtime")

model_id = "ai21.j2-ultra-v1"

prompt = f"""What is the name of the person mentioned in the text extracted. What are all the educational institutions he studied, What courses he studied in each educational institutions. Tell me the name of the projects he worked strictly. Dont assign anything other than that compulsorily. Dont give the data in json format and Give the data section wise strictly. Dont need any table format strictly.

Text Extracted: {text}"""

native_request = {
    "prompt": prompt,
    "maxTokens": 512,
    "temperature": 0.5,
}


request = json.dumps(native_request)

start_time = time.time()
print(start_time)

response = client.invoke_model(modelId=model_id, body=request)


model_response = json.loads(response["body"].read())

response_text = model_response["completions"][0]["data"]["text"]
print(response_text)

end_time = time.time()
print(end_time)

duration = end_time - start_time
print(duration)