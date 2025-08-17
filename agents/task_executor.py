import openai
import os
import pandas as pd
import json
import base64
import io
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Union
from pathlib import Path

class TaskExecutor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.data_cache = {}

    def _load_data(self, file_path: str) -> Any:
        """Load data from various file formats"""
        if file_path in self.data_cache:
            return self.data_cache[file_path]
            
        _, ext = os.path.splitext(file_path.lower())
        try:
            if ext == '.csv':
                data = pd.read_csv(file_path)
            elif ext in ['.xls', '.xlsx']:
                data = pd.read_excel(file_path)
            elif ext == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
            elif ext in ['.png', '.jpg', '.jpeg']:
                with open(file_path, 'rb') as f:
                    data = f.read()
                return data
            else:  # For text files
                with open(file_path, 'r') as f:
                    data = f.read()
            
            self.data_cache[file_path] = data
            return data
            
        except Exception as e:
            raise ValueError(f"Error loading {file_path}: {str(e)}")

    def _generate_plot(self, data: pd.DataFrame, x_col: str, y_col: str, plot_type: str = 'scatter') -> str:
        """Generate a plot and return as base64 encoded image"""
        plt.figure(figsize=(10, 6))
        
        if plot_type == 'scatter':
            plt.scatter(data[x_col], data[y_col])
            # Add regression line
            z = np.polyfit(data[x_col], data[y_col], 1)
            p = np.poly1d(z)
            plt.plot(data[x_col], p(data[x_col]), 'r--')
        # Add more plot types as needed
        
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.title(f"{y_col} vs {x_col}")
        
        # Save to bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        
        # Convert to base64
        return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode('utf-8')}"

    def _analyze_with_openai(self, prompt: str, data: Dict[str, Any] = None) -> str:
        """Use OpenAI to analyze data based on the prompt"""
        try:
            messages = [
                {"role": "system", "content": "You are a helpful data analyst assistant. "
                                         "Provide clear, concise analysis and include relevant statistics."}
            ]
            
            if data:
                messages.append({
                    "role": "user",
                    "content": f"Data: {json.dumps(data, default=str)}\n\nQuestion: {prompt}"
                })
            else:
                messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3,
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error in analysis: {str(e)}"

    def run(self, task: str, file_paths: List[str] = None) -> Union[Dict, str]:
        """
        Execute a data analysis task with optional file inputs.
        
        Args:
            task: The analysis task or question
            file_paths: List of file paths to analyze
            
        Returns:
            Analysis results in a structured format
        """
        try:
            # Load all data files
            loaded_data = {}
            if file_paths:
                for file_path in file_paths:
                    try:
                        file_name = os.path.basename(file_path)
                        loaded_data[file_name] = self._load_data(file_path)
                    except Exception as e:
                        print(f"Warning: Could not load {file_path}: {str(e)}")
            
            # For now, return a simple response with the task and file info
            # In a real implementation, you would process the task and data here
            return {
                "status": "success",
                "task": task,
                "files_loaded": list(loaded_data.keys()),
                "analysis": self._analyze_with_openai(task, loaded_data)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "task": task
            }
