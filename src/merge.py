import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

base_model_path = "abhishek/llama-2-7b-hf-small-shards"
adapter_path = "./hAI-Spec-Nasa-SpaceApps-Challenge/"
target_model_path = "./hAI-Spec-Nasa-SpaceApps-Challenge-Merged/"

model = AutoModelForCausalLM.from_pretrained(
    base_model_path,
    torch_dtype=torch.float16,
    low_cpu_mem_usage=True,
)

model = PeftModel.from_pretrained(model, adapter_path)
tokenizer = AutoTokenizer.from_pretrained(base_model_path)
model = model.merge_and_unload()

model.save_pretrained(target_model_path)
tokenizer.save_pretrained(target_model_path)