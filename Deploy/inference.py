"""
Server code for inferencing hAI! Spec.
"""

from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
import torch

from fastapi import UploadFile
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Common.common import format_pdf

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

@app.post("/api/instruct/", response_model=ModelOutput)
async def inference(file: UploadFile):
    data = format_pdf(file)
    output: list[str] = []
    for value in data.values():
        sequences = pipeline(
            str.format(prompt_template, value),
            num_return_sequences=1,
            repetition_penalty=1.01,
            max_new_tokens=4096,
        )

        output.append(sequences['generated_text'])
    
    return output
