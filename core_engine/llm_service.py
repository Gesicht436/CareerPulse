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

    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct", use_4bit: bool = False):
        """
        Initializes the local LLM.
        
        Model: Qwen 2.5 1.5B or 7B.
        Acceleration: Automatically utilizes CUDA if a compatible NVIDIA GPU is detected.
        Quantization: Optional 4-bit quantization using bitsandbytes.
        """
        print(f"DEBUG: Starting initialization of LLMService with model: {model_name}, Quantization: {use_4bit}")
        
        # Check for CUDA availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Configure model loading
        load_kwargs = {
            "torch_dtype": "auto",
            "device_map": "auto" if self.device == "cuda" else None
        }
        
        if use_4bit and self.device == "cuda":
            from transformers import BitsAndBytesConfig
            load_kwargs["quantization_config"] = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4"
            )
            print("DEBUG: 4-bit quantization enabled.")

        # Load the model
        self.model = AutoModelForCausalLM.from_pretrained(model_name, **load_kwargs)
        
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
        # Truncate input text to 4000 characters for comprehensive context
        resume_snippet = resume_text[:4000]
        jd_snippet = jd_text[:4000]
        
        prompt = f"""
        Analyze the match between this RESUME and JOB DESCRIPTION. 
        Match score: {score}%.
        
        RESUME:
        {resume_snippet}
        
        JOB DESCRIPTION:
        {jd_snippet}
        
        Provide a JSON response with these EXACT keys and types:
        - "justification": [string, string, string]
        - "matched_skills": [string, ...] (List ALL technical skills found in BOTH)
        - "missing_skills": [string, ...] (List ALL key technical gaps found in JD but NOT in resume)
        - "recommendations": [string, string, string]
        - "career_roadmap": [
            {{"week": "Week 1", "topic": "Name", "description": "Details"}},
            ...
          ]
        
        IMPORTANT: Be exhaustive in identifying skills. Do not put roadmap objects inside recommendations.
        Output ONLY raw JSON.
        """

        messages = [
            {"role": "system", "content": "You are a professional ATS analyzer that outputs strictly valid JSON. You never include conversational text before or after the JSON block."},
            {"role": "user", "content": prompt}
        ]
        
        print(f"DEBUG: Generating advice for a {score}% match...")
        
        output = self.generator(
            messages,
            max_new_tokens=600,
            temperature=0.1,
            do_sample=False
        )
        
        response_text = output[0]['generated_text'][-1]['content']
        
        try:
            # Robust JSON extraction
            match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if match:
                cleaned_json = match.group(0)
            else:
                cleaned_json = response_text
                
            data = json.loads(cleaned_json)
            
            # Defensive post-processing for Pydantic validation
            if "recommendations" in data:
                # Ensure all recommendations are strings. 
                # If LLM put a dict there, convert it to a string or remove it.
                sanitized_recs = []
                for item in data["recommendations"]:
                    if isinstance(item, dict):
                        # If it's a roadmap item misplaced here, flatten it
                        sanitized_recs.append(f"{item.get('topic', '')}: {item.get('description', '')}")
                    elif isinstance(item, str):
                        sanitized_recs.append(item)
                data["recommendations"] = sanitized_recs[:5] # Limit count
                
            return data
            
        except Exception as e:
            print(f"DEBUG ERROR: JSON Parse failed: {e}. Falling back to default.")
            return {
                "justification": [f"System detected a {score}% semantic match."],
                "matched_skills": ["Review full report"],
                "missing_skills": ["Analysis in progress"],
                "recommendations": ["Align resume keywords with the JD requirements."],
                "career_roadmap": []
            }

# Singleton instance
llm_service = LLMService()
