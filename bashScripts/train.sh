autotrain llm --train --project_name hAI-Spec-Nasa-SpaceApps-Challenge --data_path ./Data/ --model abhishek/llama-2-7b-hf-small-shards --learning_rate 2e-4 --num_train_epochs 3 --train_batch_size 4 --gradient_accumulation_steps 16 --optimizer adamw_bnb_8bit --weight_decay 0.01 --use_peft --fp16 --use_int4 --trainer sft --text_column Text --model_max_length 8100

#########################################################################################
# Training info                                                                         #
# {'loss': 0.9599, 'learning_rate': 0.0002, 'epoch': 1.0}                               #                               
# {'loss': 0.7396, 'learning_rate': 0.0001, 'epoch': 1.78}                              #                               
# {'loss': 0.2175, 'learning_rate': 0.0, 'epoch': 2.0}                                  #                              
# {'train_runtime': 156.4467, 'train_samples_per_second': 0.633,                        #
# 'train_steps_per_second': 0.019, 'train_loss': 0.6390099873145422, 'epoch': 2.0}      #
#########################################################################################