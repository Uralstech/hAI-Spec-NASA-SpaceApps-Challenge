"""
Server code for inferencing hAI! Spec.
"""

from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
import torch

from fastapi import UploadFile
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from io import BytesIO

from ..Common.PDFFormatter import format_pdf

class ModelOutput(BaseModel):
    output: list[str]

REPO_ID: str = "uralstech/hAI-Spec-Merged"
model = LlamaForCausalLM.from_pretrained(
	REPO_ID,
	load_in_4bit=True,
	torch_dtype=torch.float16,
	device_map="auto"
)

tokenizer = LlamaTokenizer.from_pretrained(REPO_ID)
prompt_template: str = "Below is part of a document that needs to be reviewed. Review the text and suggest changes that can be made to improve accuracy, readability and relevency.\n### Instruction:\n{0}\n### Output:\n"

pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
)

app: FastAPI = FastAPI(title="hAI! Spec", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_methods=["*"], allow_origins=["*"])

@app.post("/api/instruct", response_model=ModelOutput)
def inference(file: UploadFile):
    print(f"Processing request!")

    file_bytes = BytesIO(file.file.read())
    data = format_pdf(file_bytes)
    output: list[str] = []
    for value in data.values():
        sequences = pipeline(
            str.format(prompt_template, value),
            num_return_sequences=1,
            max_new_tokens=4096,
        )

        output.append(sequences[0]['generated_text'])
    
    print("Sending request!")
    return output

if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8080)