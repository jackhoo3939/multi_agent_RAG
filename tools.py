"""
Custom Tools for Multi-Agent System
1. DuckDuckGo Search Tool
2. Salary Predictor Tool
"""
import os
import joblib
from typing import Optional, Type
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field


class DuckDuckGoSearchInput(BaseModel):
    """Input schema for DuckDuckGo search"""
    query: str = Field(description="Search query string")


class DuckDuckGoSearchTool(BaseTool):
    """Tool for searching the web using DuckDuckGo"""
    name: str = "duckduckgo_search"
    description: str = (
        "Search the web using DuckDuckGo. "
        "Useful for finding current information, news, or general knowledge. "
        "Input should be a search query string."
    )
    args_schema: Type[BaseModel] = DuckDuckGoSearchInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Execute the search"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))

            if not results:
                return "No results found."

            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(
                    f"{i}. {result['title']}\n"
                    f"   {result['body']}\n"
                    f"   URL: {result['href']}\n"
                )

            return "\n".join(formatted_results)
        except Exception as e:
            return f"Error performing search: {str(e)}"


class SalaryPredictorInput(BaseModel):
    """Input schema for salary prediction"""
    years_experience: float = Field(description="Years of work experience")
    education_level: int = Field(
        description="Education level (1=High School, 2=Bachelor's, 3=Master's, 4=PhD)"
    )
    job_title: str = Field(description="Job title or role")


class SalaryPredictorTool(BaseTool):
    """Tool for predicting salary based on experience and education"""
    name: str = "salary_predictor"
    description: str = (
        "Predict salary based on years of experience, education level, and job title. "
        "Input: years_experience (float), education_level (1-4), job_title (string). "
        "Returns estimated salary range."
    )
    args_schema: Type[BaseModel] = SalaryPredictorInput
    model_path: str = "./salary_model.joblib"

    def _run(
        self,
        years_experience: float,
        education_level: int,
        job_title: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Predict salary"""
        try:
            if not os.path.exists(self.model_path):
                return f"Error: Salary model not found at {self.model_path}"

            model = joblib.load(self.model_path)

            features = [[years_experience, education_level]]
            predicted_salary = model.predict(features)[0]

            return (
                f"Salary Prediction for {job_title}:\n"
                f"- Years of Experience: {years_experience}\n"
                f"- Education Level: {education_level}\n"
                f"- Estimated Salary: ${predicted_salary:,.2f} per year\n"
                f"- Salary Range: ${predicted_salary * 0.9:,.2f} - ${predicted_salary * 1.1:,.2f}"
            )
        except Exception as e:
            return f"Error predicting salary: {str(e)}"


def get_tools():
    """Return list of all available tools"""
    return [
        DuckDuckGoSearchTool(),
        SalaryPredictorTool()
    ]

