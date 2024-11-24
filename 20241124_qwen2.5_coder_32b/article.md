# Deploying your own SOTA code inference server with Qwen2.5-Coder-32B on Vast.ai

## Introduction

Open source models like Qwen2.5-Coder are now matching and sometimes surpassing commercial models like GPT-4o, enabling powerful local AI development with full privacy and control.

The best coding open source model to date is the Qwen2.5-Coder-32B which is a 32B parameters model with a context length of up to 130k tokens developed by Alibaba's Qwen Research team. The model has shown some impressive benchmark performance often seating between GPT-4o and Claude 3.5 sonnet:

![qwen2.5 coder benchmark performance](images/qwen2.5_benchmark.png)

If you are like most (me included) your hardware do not allow to run a model of that size at a decent speed.

Thanks to quantization the requirement to run such a model are drastically reduced and as it turns out it can even run on a single consumer grade GPU (RTX 4090) if we limit the context length to 15k tokens.

Buying a GPU of that size is still an expensive investment however thanks to vast.ai we can easily rent a (RTX 4090) GPU for only 0.3 $/hour.

In this technical article, I will show you how to combine the power of Qwen2.5-Coder 32B, the efficient compression of quantization, the inference speed of llama.cpp server and the cheap price of vast.ai to run your very own fully private SOTA code inference server at only 0.3 $/hour. You will be able to generate code at 40 tokens per second surpassing typical reading speeds. We will finish by integrating the inference server into pearAI a Cursor open source alternative based on continue.dev.

## Prerequisites

To follow along you need a vast.ai account that can be created for free here:
https://cloud.vast.ai/create/

Then you need to topup your account with a few dollars to cover the costs of the GPUs (0.3 $/hour).:
https://cloud.vast.ai/billing/

If you want to leverage the CLI script that comes with this article you also need vastAI CLI tool:
https://cloud.vast.ai/cli/

## Deploying Qwen2.5-Coder-32B

We will deploy a 4 bit quantized version of the model provided by Daniel Han (@unsloth.ai) in GGUF format on hugging face: https://huggingface.co/unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF/blob/main/Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf. The GGUF format https://huggingface.co/docs/hub/gguf is a popular self contained binary format that contains all the necessary information to run the model (both metadata and weigths). It was created by @ggerganov the author of lamma.cpp from which we will also borrow the inference server code to deploy.

I provided 2 options to deploy the inference server: semi-automated via a script that will look at compatible instances on vast.ai, let you select among the best 3 options and then deploy the server for you. The other option consist in create a template in vast.ai UI and searching an instance manually. 

### option 1: one-script deployment (recommended)

The fastest way to get your code inference up and running is through the vastai_search script. 



### option 2: manual deployment in vast.ai UI




It's unbelievable how open source models are now catching up with commercial models in terms of performances.


* Qwen2.5-Coder-32B is bringing open source models to a complete new level of performance often beating even commercial models like openAI gpt-4o: https://qwenlm.github.io/blog/qwen2.5-coder-family/
![alt text](images/qwen2.5_benchmark.png)
* this changes the game where we can actually use these models in our daily coding life bringing the following key advantages:
  * full privacy (local inferences)
  * cheap alternative as it can run quantized on a single GPU for 0.3 $/hour

In this technical article I will show you how to deploy your own inference server with Qwen2.5-Coder-32B.

thanks and references:
* Qwen2 team for releasing Qwen2.5-Coder-32B open source see technical report https://arxiv.org/html/2409.12186v3
* llama.cpp for providing a simple way to create an inference server.
* Daniel Han at unsloth ai for quantizing the model and making it available on HF
* vast.ai for providing a simple and easy to use API for GPU instances as well as extremly competitive prices 
* pearAI / continue.dev for an open source alternative to Cursor