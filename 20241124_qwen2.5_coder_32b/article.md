# Get your own SOTA code inference server with Qwen2.5-Coder-32B at 0.3 $/hour

## Introduction

The landscape of AI coding assistants has dramatically shifted with the release of [Qwen2.5-Coder](https://arxiv.org/html/2409.12186v3), an open-source model that not only matches but often outperforms commercial solutions like GPT-4o. This breakthrough enables developers to build powerful, private AI development environments with complete control over their data and infrastructure.

Qwen2.5-Coder-32B represents the current state-of-the-art in open-source coding models. With its 32-billion parameters and impressive 130k token context window, this model from Alibaba's Qwen Research team has demonstrated remarkable capabilities, positioning itself competitively between GPT-4o and Claude 3.5 Sonnet:

![qwen2.5 coder benchmark performance](images/qwen2.5_benchmark.png)

While the 32 billions parameters might seem daunting for local deployment, recent advances in quantization have made it surprisingly accessible. Through efficient compression techniques, it can now run on a single consumer-grade RTX 4090 GPU with a 15k token context window — making what once seemed impossible, entirely doable.

For developers who don't want to invest in high-end hardware, vast.ai offers an elegant solution: RTX 4090 GPU instances for just $0.3 per hour. This makes enterprise-grade AI capabilities accessible to individual developers and small teams.

This guide will walk you through creating your own state-of-the-art code inference server by combining:

* Qwen2.5-Coder 32B's state of the art coding capabilities
* Advanced quantization techniques for efficient deployment
* llama.cpp's high-performance inference server
* vast.ai's cost-effective GPU rentals

The result? A private code generation server capable of producing 40 tokens per second — much faster than human reading speed — at a fraction of the cost of commercial solutions. We'll also show you how to integrate this server with pearAI, an open-source alternative to Cursor built on continue.dev, creating a seamless development experience.

## Prerequisites

Before getting started, ensure you have the following set up:

1. vast.ai Account
  * [Create a free account](https://cloud.vast.ai/create/)
  * This will be your gateway to accessing affordable GPU instances
2. Account Balance
  * [Add funds to your vast.ai account](https://cloud.vast.ai/billing/)
  * A small initial deposit ($5-10) is sufficient to get started
  * Instances cost approximately $0.3/hour
3. Optional: CLI Setup
  * If you plan to use our automated deployment script, install the [vast.ai CLI tool](https://cloud.vast.ai/cli/)
  * This enables programmatic instance management and deployment

## Deploying Qwen2.5-Coder-32B

We'll be deploying a highly optimized 4-bit quantized version of Qwen2.5-Coder-32B, created by Daniel Han (@unsloth.ai). The model is available in GGUF format—a self-contained binary format that packages both model weights and metadata for efficient deployment. The key advantage of this model is that it is just 20GB in size making it perfect for the 24GB VRAM on RTX 4090 GPUs.

**Model Details:**
- Source: [unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF](https://huggingface.co/unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF/blob/main/Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf)
- Format: GGUF (developed by @ggerganov for llama.cpp)
- Quantization: 4-bit for optimal performance/size balance

### Deployment Options

You have two methods to deploy the inference server via automated script (recommended) or via vast.ai manual UI.

#### Option 1: Automated Script Deployment (Recommended)

This is the fastest and most straightforward method, using our provided script to handle instance selection and deployment automatically.

1. Download the deployment script:

```bash
wget https://raw.githubusercontent.com/grll/articles/main/20241124_qwen2.5_coder_32b/vastai_search.py
```

2. Run the script (choose one method):

```bash
python vastai_search.py
```

or

```bash
chmod +x vastai_search.py
./vastai_search.py
```

The script will:
- Search for compatible instances
- Present the top 3 options based on price and performance
- Handle deployment after you select an instance
- Provide the inference server URL once ready

> Notes: 
> * Initial setup takes approximately 10 minutes while the model downloads to your instance.
> * The first query may take much longer to process the input text.

#### Option 2: Manual UI Deployment

For those who prefer direct control through the vast.ai interface:

1. **Template Setup**
   - Visit [vast.ai templates](https://cloud.vast.ai/templates/)
   - Either use our [pre-configured template](https://cloud.vast.ai/?ref_id=137438&template_id=6e39ce6b12abc8fcbf1f76350c99fc7c)
   - Or create your own with these specifications:
     - Base Image: `ggerganov/llama.cpp:server-cuda-b4154`
     - CUDA Version: 12.6+
     - Minimum CPU RAM: 20GB
     - Minimum GPU VRAM: 20GB
     - Disk Space: 30GB minimum

2. **Instance Selection**
   - Navigate to the vast.ai search page
   - Apply these filters:
     - RAM: ≥20GB
     - GPU: RTX 4090 (recommended)
     - CUDA: ≥12.6
     - Location: Choose based on your region
   - Sort by "price inc." for best deals
   - Review total costs (including download bandwidth for the 20GB model)
   - Click "Rent" on your chosen instance

## Monitoring your Qwen2.5-Coder-32B Inference Server

After deployment, monitoring your instance is crucial for optimal performance and cost management. All monitoring features are accessible through the [vast.ai instances dashboard](https://cloud.vast.ai/instances/).

### Key Monitoring Features

1. **System Metrics**
   - Real-time GPU utilization
   - RAM usage
   - CPU load
   - Disk space consumption
   - All viewable directly from the dashboard

2. **Remote Access**
   - SSH connectivity via the "Connect" button
   - Direct access to instance logs through the "Logs" button
   - Real-time debugging and troubleshooting capabilities

3. **Server Access Information**
   - Click the blue IP address button to view:
     - Public IP address
     - Port mapping (by default port mapping to 8081)
     - Connection details for your inference server

### Quick Reference

Your inference server will be accessible at:
```
http://<public_ip>:<port_mapping>
```
Where:
- `<public_ip>` is your instance's public IP address
- `<port_mapping>` is the mapped port (typically mapped to internal port 8081)

> Tip: Bookmark your server's URL for easy access, but remember that the IP and port may change if you stop and restart your instance.

## Using your Qwen2.5-Coder-32B Inference Server

There are two primary ways to interact with your inference server: through the web interface for direct interactions, or by integrating it into your development environment for a more streamlined coding experience.

### Web Interface Access

llama.cpp provides a built-in web interface for immediate model interaction:

```
http://<public_ip>:<port_mapping>/
```

This interface offers:
- Direct text input/output
- Real-time response streaming
- Basic parameter adjustment
- Simple prompt testing

### IDE Integration

For a more powerful development experience, you can integrate the server directly into your IDE through pearAI or continue.dev, creating a Cursor-like experience.

#### Configuration Setup

1. Locate your pearAI configuration file:

   ```
   ~/.pearai/config.json
   ```

2. Add the following configuration block:

   ```json
   {
     "title": "Qwen2.5-Coder-32B (llama.cpp Q4_K_M on vast.ai)",
     "provider": "llama.cpp",
     "model": "Qwen2.5-Coder-32B",
     "apiBase": "http://<public_ip>:<port_mapping>"
   }
   ```

#### Available IDE Commands

After configuration, you can use these keyboard shortcuts (with PearAI or continue.dev):
- `Ctrl+L`: Open interaction panel (chat)
- `Ctrl+I`: Trigger inline code editing

The newly created model will be available in the `Model` dropdown both in the panel and in the inline editor.

## Conclusion

This guide demonstrates a significant milestone in AI coding assistance. Open source models are finally catching up to become a viable alternative for coding tasks. 

By leveraging several key technologies:

* Qwen2.5-Coder-32B's powerful language model
* Quantization techniques
* llama.cpp's efficient inference server
* vast.ai's affordable GPU infrastructure

You can now deploy a private code generation system that:

* Rivals GPT-4o in coding performance
* Operates at 40 tokens per second
* Costs only $0.3 per hour
* Maintains complete privacy and control
* Runs on a single GPU

This brings what previously was enterprise-grade LLM capabilites at individual developer costs with full control, no dependency on commercial API providers and with a privacy first approach that every individuals and companies can adopt safely.

## References & Acknowledgements

* Qwen2 team for the impressive Qwen2.5-Coder open source release see [technical report](https://arxiv.org/html/2409.12186v3).
* [llama.cpp](https://github.com/ggerganov/llama.cpp) for providing a simple way to create an efficient LLM inference server.
* Daniel Han at [unsloth ai](https://unsloth.ai) for quantizing the model and making it available on [Hugging Face](https://huggingface.co/unsloth/Qwen2.5-Coder-32B-Instruct-128K-GGUF/blob/main/Qwen2.5-Coder-32B-Instruct-Q4_K_M.gguf).
* [vast.ai](https://vast.ai) for providing a simple and easy to use API for GPU instances as well as extremly competitive prices.
* [pearAI](https://trypear.ai/) / [continue.dev](https://www.continue.dev/) for an open source alternative to Cursor that supports local model.