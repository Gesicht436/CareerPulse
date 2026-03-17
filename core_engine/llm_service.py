from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from typing import Dict, Any, List

class LLMService:
    """
    LLMService handles all natural language processing tasks for CareerPulse.
    It manages the local Large Language Model lifecycle, including initialization,
    device placement (GPU/CPU), and structured response generation.
    """

    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        """
        Initializes the local LLM using the highly efficient 1.5B parameter model.
        
        Model: Qwen 2.5 1.5B (Lightweight and fast for real-time applications).
        Acceleration: Automatically utilizes CUDA if a compatible NVIDIA GPU is detected.
        Memory: Fits comfortably in <4GB VRAM, ensuring peak performance on RTX 3060.
        """
        print(f"DEBUG: Starting initialization of LLMService with model: {model_name}")
        
        # Check for CUDA availability to leverage RTX 3060 hardware acceleration
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"DEBUG: Hardware detection completed. Target device: {self.device}")
        
        # Load the tokenizer responsible for converting text into model-readable tokens
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Load the model in full/half precision (torch_dtype="auto")
        # For a 1.5B model, we don't need 4-bit quantization, allowing for maximum speed.
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto", 
            device_map="auto" if self.device == "cuda" else None
        )
        
        # Initialize the high-level pipeline for text generation
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )
        print(f"DEBUG: LLMService is fully operational on {self.device} using {self.model.dtype}")

    async def generate_career_advice(self, resume_text: str, jd_text: str, score: float) -> Dict[str, Any]:
        """
        Generates expert career advice by analyzing the gap between a resume and a job description.
        """
        # Truncate input text to 1500 characters
        resume_snippet = resume_text[:1500]
        jd_snippet = jd_text[:1500]
        
        prompt = f"""
        You are a Career Expert. Analyze the match between this RESUME and JOB DESCRIPTION. 
        Match score: {score}%.
        
        RESUME:
        {resume_snippet}
        
        JOB DESCRIPTION:
        {jd_snippet}
        
        Provide a JSON response with:
        - justification: 3 bullet points explaining the match.
        - matched_skills: Technical skills found in both.
        - missing_skills: Key technical gaps.
        - recommendations: 3 actionable steps.
        
        Output ONLY raw JSON.
        """

        messages = [
            {"role": "system", "content": "You are a professional ATS analyzer that outputs strictly valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        print(f"DEBUG: Generating advice for a {score}% match...")
        
        output = self.generator(
            messages,
            max_new_tokens=500,
            temperature=0.1,
            do_sample=False
        )
        
        response_text = output[0]['generated_text'][-1]['content']
        
        try:
            # Robust JSON extraction
            cleaned_json = re.sub(r'```(?:json)?\n?|\n?```', '', response_text).strip()
            return json.loads(cleaned_json)
        except Exception as e:
            print(f"DEBUG ERROR: JSON Parse failed. Falling back to default.")
            return {
                "justification": [f"System detected a {score}% semantic match."],
                "matched_skills": ["Review full report"],
                "missing_skills": ["Analysis in progress"],
                "recommendations": ["Align resume keywords with the JD requirements."]
            }

# Singleton instance
llm_service = LLMService()
