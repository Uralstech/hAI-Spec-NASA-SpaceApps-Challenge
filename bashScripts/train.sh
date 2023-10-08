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

#####################################################################################
# New dataset w/ epochs = 40                                                        #
# {'loss': 0.9798, 'learning_rate': 5e-05, 'epoch': 1.0}                            #
# {'loss': 0.775, 'learning_rate': 0.0001, 'epoch': 1.78}                           #
# {'loss': 0.2044, 'learning_rate': 0.00015000000000000001, 'epoch': 2.0}           #
# {'loss': 0.9712, 'learning_rate': 0.0002, 'epoch': 3.0}                           #
# {'loss': 0.5159, 'learning_rate': 0.00019444444444444446, 'epoch': 3.56}          #
# {'loss': 0.4389, 'learning_rate': 0.00018888888888888888, 'epoch': 4.0}           #
# {'loss': 0.9312, 'learning_rate': 0.00018333333333333334, 'epoch': 5.0}           #
# {'loss': 0.3082, 'learning_rate': 0.00017777777777777779, 'epoch': 5.33}          #
# {'loss': 0.5977, 'learning_rate': 0.00017222222222222224, 'epoch': 6.0}           #
# {'loss': 0.8849, 'learning_rate': 0.0001666666666666667, 'epoch': 7.0}            #
# {'loss': 0.1016, 'learning_rate': 0.0001611111111111111, 'epoch': 7.11}           #
# {'loss': 0.7526, 'learning_rate': 0.00015555555555555556, 'epoch': 8.0}           #
# {'loss': 0.7471, 'learning_rate': 0.00015000000000000001, 'epoch': 8.89}          #
# {'loss': 0.0868, 'learning_rate': 0.00014444444444444444, 'epoch': 9.0}           #
# {'loss': 0.8041, 'learning_rate': 0.0001388888888888889, 'epoch': 10.0}           #
# {'loss': 0.5063, 'learning_rate': 0.00013333333333333334, 'epoch': 10.67}         #
# {'loss': 0.2782, 'learning_rate': 0.00012777777777777776, 'epoch': 11.0}          #
# {'loss': 0.7619, 'learning_rate': 0.00012222222222222224, 'epoch': 12.0}          #
# {'loss': 0.3356, 'learning_rate': 0.00011666666666666668, 'epoch': 12.44}         #
# {'loss': 0.4048, 'learning_rate': 0.00011111111111111112, 'epoch': 13.0}          #
# {'loss': 0.7221, 'learning_rate': 0.00010555555555555557, 'epoch': 14.0}          #
# {'loss': 0.1666, 'learning_rate': 0.0001, 'epoch': 14.22}                         #
# {'loss': 0.535, 'learning_rate': 9.444444444444444e-05, 'epoch': 15.0}            #
# {'loss': 0.6888, 'learning_rate': 8.888888888888889e-05, 'epoch': 16.0}           #
# {'loss': 0.6785, 'learning_rate': 8.333333333333334e-05, 'epoch': 17.0}           #
# {'loss': 0.5077, 'learning_rate': 7.777777777777778e-05, 'epoch': 17.78}          #
# {'loss': 0.1588, 'learning_rate': 7.222222222222222e-05, 'epoch': 18.0}           #
# {'loss': 0.6512, 'learning_rate': 6.666666666666667e-05, 'epoch': 19.0}           #
# {'loss': 0.3319, 'learning_rate': 6.111111111111112e-05, 'epoch': 19.56}          #
# {'loss': 0.3084, 'learning_rate': 5.555555555555556e-05, 'epoch': 20.0}           #
# {'loss': 0.629, 'learning_rate': 5e-05, 'epoch': 21.0}                            #
# {'loss': 0.1938, 'learning_rate': 4.4444444444444447e-05, 'epoch': 21.33}         #
# {'loss': 0.4255, 'learning_rate': 3.888888888888889e-05, 'epoch': 22.0}           #
# {'loss': 0.612, 'learning_rate': 3.3333333333333335e-05, 'epoch': 23.0}           #
# {'loss': 0.0628, 'learning_rate': 2.777777777777778e-05, 'epoch': 23.11}          #
# {'loss': 0.5411, 'learning_rate': 2.2222222222222223e-05, 'epoch': 24.0}          #
# {'loss': 0.5343, 'learning_rate': 1.6666666666666667e-05, 'epoch': 24.89}         #
# {'loss': 0.0656, 'learning_rate': 1.1111111111111112e-05, 'epoch': 25.0}          #
# {'loss': 0.5954, 'learning_rate': 5.555555555555556e-06, 'epoch': 26.0}           #
# {'loss': 0.3824, 'learning_rate': 0.0, 'epoch': 26.67}                            #
# {'train_runtime': 2192.9027, 'train_samples_per_second': 0.602,                   #
# 'train_steps_per_second': 0.018, 'train_loss': 0.5044329412281513,                #
# 'epoch': 26.67}                                                                   #
#####################################################################################