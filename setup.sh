sudo apt install libxext-dev -y

pip install autotrain-advanced
pip install -r requirements.txt

autotrain setup --update-torch
pip install trl peft

huggingface-cli login