import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from .architecture_agent import ArchitectureAgent
from .static_agent import StaticAgent
from .code_quality_agent import CodeQualityAgent
from .dependency_agent import DependencyAgent
from .performance_agent import PerformanceAgent

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load the system prompt from .env
MANAGER_SYS_PROMPT = os.getenv("MANAGER_SYS_PROMPT")

class ManagerAgent:
    def __init__(self):
        self.client = client
        self.system_prompt = MANAGER_SYS_PROMPT

    def generate_report(self, agent_outputs):
        """
        Generate a report based on the outputs of specialized agents.
        
        :param agent_outputs: A dictionary containing the outputs from each specialized agent
        :return: A dictionary containing the compiled report
        """
        compiled_report = {
            "ARCHITECTURE_ANALYSIS": agent_outputs.get("ARCHITECTURE_ANALYSIS"),
            "CODE_QUALITY_ANALYSIS": agent_outputs.get("CODE_QUALITY_ANALYSIS"),
            "DEPENDENCY_AUDIT": agent_outputs.get("DEPENDENCY_AUDIT"),
            "PERFORMANCE_ANALYSIS": agent_outputs.get("PERFORMANCE_ANALYSIS"),
            "STATIC_CODE_ANALYSIS": agent_outputs.get("STATIC_CODE_ANALYSIS"),
        }

        # Use OpenAI to generate an overall summary and project health assessment
        prompt = f"""
        Based on the following analysis results, provide an overall summary of the project's health and key recommendations:

        Architecture Analysis:
        {compiled_report['ARCHITECTURE_ANALYSIS']}

        Code Quality Analysis:
        {compiled_report['CODE_QUALITY_ANALYSIS']}

        Dependency Audit:
        {compiled_report['DEPENDENCY_AUDIT']}

        Performance Analysis:
        {compiled_report['PERFORMANCE_ANALYSIS']}

        Static Code Analysis:
        {compiled_report['STATIC_CODE_ANALYSIS']}

        Please provide:
        1. An overall project health assessment (Healthy, Stable, or At Risk)
        2. A brief summary of the key findings
        3. Top 3-5 recommendations for improvement
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ]
        )

        ai_summary = response.choices[0].message.content

        compiled_report["OVERALL_SUMMARY"] = ai_summary

        return compiled_report

    def analyze_codebase(self):
        """
        Analyze the codebase using all specialized agents and generate a report.
        """
        # Initialize all agents
        architecture_agent = ArchitectureAgent()
        static_analysis_agent = StaticAgent()
        code_quality_agent = CodeQualityAgent()
        dependency_agent = DependencyAgent()
        performance_agent = PerformanceAgent()

        # Perform analyses
        architecture_results = architecture_agent.analyze_codebase_architecture()
        static_analysis_results = static_analysis_agent.analyze_codebase_static()
        code_quality_results = code_quality_agent.analyze_codebase_quality()
        dependency_results = dependency_agent.analyze_codebase_dependencies()
        performance_results = performance_agent.analyze_codebase_performance()

        # Combine all results
        agent_outputs = {
            "ARCHITECTURE_ANALYSIS": architecture_results,
            "STATIC_CODE_ANALYSIS": static_analysis_results,
            "CODE_QUALITY_ANALYSIS": code_quality_results,
            "DEPENDENCY_AUDIT": dependency_results,
            "PERFORMANCE_ANALYSIS": performance_results
        }

        # Generate report
        return self.generate_report(agent_outputs)

    def main(self):
        report = self.analyze_codebase()
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    manager_agent = ManagerAgent()  # Create an instance of ManagerAgent
    manager_agent.main()  # Call the main method on the instance
