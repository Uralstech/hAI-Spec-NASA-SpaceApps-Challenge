# I have not confirmed that this works yet.
from transformers import LlamaTokenizer, LlamaForCausalLM, pipeline
import torch

REPO_ID: str = "uralstech/hAI-Spec-Merged"

model = LlamaForCausalLM.from_pretrained(
	REPO_ID,
	load_in_4bit=True,
	torch_dtype=torch.float16,
	device_map="auto"
)

tokenizer = LlamaTokenizer.from_pretrained(REPO_ID)

prompt: str = "### Instruction:\nPurpose\nThe purpose of this standard is to establish the nondestructive evaluation (NDE) requirements for\nany NASA system or component, flight or ground, where fracture control is a requirement.  This\nstandard defines the primary requirements for NDE in support of NASA-STD-5019, Fracture\nControl Requirements for Spaceflight Hardware.  NDE applied in-process for purposes of process\ncontrol is not addressed in this document.\nIt is the policy of NASA to produce aerospace flight systems with a high degree of reliability and\nsafety.  This is accomplished through good design, manufacturing, test, and operational practices\nincluding the judicious choice of materials, detailed analysis, appropriate factors of safety, rigorous\ntesting and control of hardware, and reliable inspection.  NASA fracture control requirements\nstipulate that all aerospace flight systems be subjected to fracture control procedures to preclude\ncatastrophic failure.  Those procedures frequently rely on NDE to ensure that significant crack-like\nflaws are not present in critical areas.\na.  NDE processes shall meet the requirements in this standard to screen hardware reliably\nfor the presence of crack-like flaws.\nb.  Nothing in this document shall be construed as requiring duplication of effort dictated by\nother contract provisions.\nc.  Conversely, provisions stated herein shall not be interpreted to preclude compliance with\nrequirements invoked by other provisions.\n### Output:\n"

pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.float16,
    device_map="auto",
)

sequences = pipeline(
    prompt,
    do_sample=True,
    top_k=50,
    top_p = 0.9,
    num_return_sequences=1,
    repetition_penalty=1.1,
    max_new_tokens=1024,
)
for seq in sequences:
    print(f"Result: {seq['generated_text']}")
