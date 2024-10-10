from utils.config_manager import ConfigManager
from agents.manager_agent import ManagerAgent
from agents.architecture_agent import ArchitectureAgent
from agents.performance_agent import PerformanceAgent
from agents.static_agent import StaticAgent
from agents.code_quality_agent import CodeQualityAgent
from agents.dependency_agent import DependencyAgent

class ButterflyCore:
    def __init__(self):
        self.config = ConfigManager()
        self.api_key = self.config.get_openai_api_key()

    def run_analysis(self):
        manager_agent = ManagerAgent(self.api_key, self.config.get_manager_prompt())
        architecture_agent = ArchitectureAgent(self.api_key, self.config.get_architecture_prompt())
        performance_agent = PerformanceAgent(self.api_key, self.config.get_performance_prompt())
        static_agent = StaticAgent(self.api_key, self.config.get_static_prompt())
        code_quality_agent = CodeQualityAgent(self.api_key, self.config.get_code_quality_prompt())
        dependency_agent = DependencyAgent(self.api_key, self.config.get_dependency_prompt())

        # Run the analysis using the agents
        manager_agent.analyze()
        architecture_agent.analyze()
        performance_agent.analyze()
        static_agent.analyze()
        code_quality_agent.analyze()
        dependency_agent.analyze()

        # Compile and return the results
        return self.compile_results()

    def compile_results(self):
        # Implement the logic to compile results from all agents
        pass

def run():
    core = ButterflyCore()
    return core.run_analysis()