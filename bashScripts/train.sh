autotrain llm --train --project_name hAI-Spec-Nasa-SpaceApps-Challenge --data_path ./Data/ --model abhishek/llama-2-7b-hf-small-shards --learning_rate 2e-4 --num_train_epochs 3 --train_batch_size 4 --gradient_accumulation_steps 16 --optimizer adamw_bnb_8bit --weight_decay 0.01 --use_peft --fp16 --use_int4 --trainer sft --text_column Text --model_max_length 8100

#####################################################################################
# {'loss': 1.0893, 'learning_rate': 0.0002, 'epoch': 1.0}                           #
# {'loss': 0.8114, 'learning_rate': 0.00016, 'epoch': 1.78}                         #
# {'loss': 1.3399, 'learning_rate': 0.00012, 'epoch': 2.0}                          #
# {'loss': 0.5676, 'learning_rate': 8e-05, 'epoch': 2.56}                           #
# {'loss': 1.4913, 'learning_rate': 4e-05, 'epoch': 3.0}                            #
# {'loss': 0.3335, 'learning_rate': 0.0, 'epoch': 3.33}                             #
# {'train_runtime': 205.527, 'train_samples_per_second': 0.963,                     #
# 'train_steps_per_second': 0.029, 'train_loss': 0.938852588335673, 'epoch': 3.33}  #
#####################################################################################