import openai
import os
import pandas as pd

class TaskExecutor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def run(self, task: str):
        """
        Executes a plain-English task using LLM + Python.
        """
        # For now, just simulate parsing the task
        if "sum" in task.lower():
            numbers = [int(n) for n in task.split() if n.isdigit()]
            return {"operation": "sum", "numbers": numbers, "result": sum(numbers)}

        # Default fallback (AI call)
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful data analyst assistant."},
                {"role": "user", "content": task},
            ],
        )
        return response.choices[0].message.content
