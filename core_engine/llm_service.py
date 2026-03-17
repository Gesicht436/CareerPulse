from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from typing import Dict, Any, List

class LLMService:
    def __init__(self, model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
        """
        Initializes a local LLM for explainable analysis.
        We use Qwen 1.5B by default as it's lightweight and excellent at following instructions.
        """
        print(f"DEBUG: Initializing LLMService with {model_name}...")
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto" if self.device == "cuda" else None
        ).to(self.device if self.device == "cpu" else "cuda")
        
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else -1
        )
        print(f"DEBUG: LLMService ready on {self.device}")

    async def generate_career_advice(self, resume_text: str, jd_text: str, score: float) -> Dict[str, Any]:
        """
        Generates natural language justification and actionable advice using the LLM.
        """
        # Truncate text to avoid context window issues in this prototype
        resume_snippet = resume_text[:1500]
        jd_snippet = jd_text[:1500]
        
        prompt = f"""
        You are a Career Expert and ATS Optimization specialist. 
        A candidate has a resume that matches a Job Description with a semantic score of {score}%.
        
        RESUME:
        {resume_snippet}
        
        JOB DESCRIPTION:
        {jd_snippet}
        
        Provide a JSON response with the following keys:
        - justification: A list of 2-3 bullet points explaining the match strength.
        - matched_skills: A list of specific technical skills found in both.
        - missing_skills: A list of key missing technical skills from the JD.
        - recommendations: 3 actionable career steps to bridge the gap.
        
        Output ONLY the JSON.
        """

        messages = [
            {"role": "system", "content": "You are a professional ATS analyzer that outputs strictly valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        # Generate response
        output = self.generator(
            messages,
            max_new_tokens=500,
            temperature=0.1, # Keep it deterministic
            do_sample=False
        )
        
        response_text = output[0]['generated_text'][-1]['content']
        
        # Attempt to parse JSON
        try:
            # Clean response text in case the LLM added markdown backticks
            cleaned_json = re.sub(r'```json\n|\n```', '', response_text).strip()
            return json.loads(cleaned_json)
        except Exception as e:
            print(f"DEBUG ERROR: LLM failed to return valid JSON. Error: {e}")
            # Fallback to a structured response if LLM fails
            return {
                "justification": [f"The system detected a {score}% semantic alignment in core competencies."],
                "matched_skills": ["Consult detailed report"],
                "missing_skills": ["Further analysis required"],
                "recommendations": ["Optimize your resume for the specific job requirements."]
            }

# Singleton instance
# Note: Initializing this may take a few minutes on first run to download the weights (~3GB)
llm_service = LLMService()
