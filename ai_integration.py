from openai import OpenAI
from google import genai

class AIPhysiologist:
    """Connects to an AI API to provide physiological insights."""
    
    def __init__(self, api_key, model_id="gemini-2.5-flash"):
        # The new SDK uses a Client object rather than a global configure
        self.client = genai.Client(api_key=api_key)
        self.model_id = model_id
        
    def analyze_test(self, athlete_name, wd, hrd, zones):
        """Sends data to AI and returns a coaching analysis."""
        
        # System instructions are now passed inside the generate_content call
        # or defined in a config object.
        prompt = f"""
        Analyze the following lactate performance test for {athlete_name}:
        - D-Max Threshold: {wd:.1f} Watts at {hrd:.0f} bpm.
        - Training Zones:
          {zones}

        Provide a professional coaching summary (max 150 words) including:
        1. An assessment of current fitness.
        2. Specific training advice to improve the threshold.
        3. Predictions for potential race performance (e.g. FTP estimation).
        Keep the tone professional and scientific.
        """

        try:
            # Using the modern SDK syntax: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    "system_instruction": "You are a world-class cycling coach and exercise physiologist.",
                    "temperature": 0.7
                }
            )
            return response.text
        except Exception as e:
            return f"AI Analysis unavailable: {str(e)}"