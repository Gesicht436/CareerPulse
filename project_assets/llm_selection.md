# LLM Selection Report - CareerPulse

This document outlines the architectural and hardware-driven process I used to select the Large Language Model (LLM) for the CareerPulse core engine.

## 1. My Hardware Constraints

The choice of model was not just a preference but a strict requirement dictated by my local development hardware:

- **GPU:** NVIDIA GeForce RTX 3060 Laptop GPU
- **VRAM:** 6 GB GDDR6
- **Architecture:** Ampere (Supports BF16/FP16 and CUDA 13.0)
- **The "VRAM Wall":** On a Windows machine, the OS and display drivers consume roughly 0.8GB - 1.2GB of VRAM even at idle. This means my actual usable budget for an LLM is effectively **~4.8 GB**.

## 2. My Selection Criteria

I evaluated models based on three critical factors:

1. **VRAM Footprint & "The Headroom Rule":** The model must fit comfortably within that 4.8GB budget while leaving room for the **Embedding Model** and the **KV Cache**.
2. **Latency (Tokens/Sec):** For a web application, I need near-instant feedback. If a model takes 30 seconds to generate a response, the UX is ruined.
3. **Instruction Following:** The model must reliably output structured JSON for my frontend.

## 3. Options I Evaluated

| Model Family | Size | Precision | VRAM Req. | My Detailed Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **Qwen-2.5** | 1.5B | FP16 | **~3.5 GB** | **Final Selection:** It is incredibly fast and fits perfectly alongside my embedding model on the GPU. It follows instructions well enough for the current prototype. |
| **Llama-3.2** | 3B | FP16 | ~4.8 GB | **Strong Contender:** Offers GPT-3.5 level reasoning, but uses almost all available VRAM, making it tight for concurrent tasks. |
| **Qwen-2.5** | 7B | 4-bit | ~5.0 GB | **Rejected (Latency):** While smarter, the 4-bit quantization and high parameter count led to slow inference on my laptop hardware. |
| **Llama-3.1** | 8B | 4-bit | ~5.5 GB | **Rejected:** Too heavy for a 6GB card once Windows and background apps are factored in. |

## 4. Why I Chose 1.5B over 7B

Initially, I wanted the "smartest" model possible (7B/8B). However, during testing, I realized that for an ATS analysis tool:

- **Speed is King:** A 1.5B model generates advice in ~1 second. A 7B model takes ~5-10 seconds.
- **Resource Management:** By using a 1.5B model, I can keep my **Embedding model on the GPU** as well. This makes the initial semantic search much faster.
- **Accuracy:** The 1.5B Instruct-tuned models are surprisingly capable at basic extraction and summarization, which are our core needs.

## 5. My Final Decision: Qwen-2.5-1.5B-Instruct

**Selected Model:** `Qwen/Qwen2.5-1.5B-Instruct`

### **Why this is the best choice for my current machine:**

1. **Native Performance:** It runs in high precision (FP16) without the overhead of quantization.
2. **GPU Harmony:** I can run the LLM, the Embedding model, and the FastAPI server all on the RTX 3060 without hitting OOM (Out of Memory) errors.
3. **Development Velocity:** Faster load times and faster generation mean I can test my code changes much more quickly.

---
**Status:** Implementation complete in `core_engine/llm_service.py`.
