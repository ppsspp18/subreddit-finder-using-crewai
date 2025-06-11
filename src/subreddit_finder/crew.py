from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class SubredditFinder():
    """SubredditFinder crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def subreddit_discover_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['subreddit_discover_agent'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
        )
    @agent
    def fetch_posts_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['fetch_posts_agent'], # type: ignore[index]
            verbose=True,
            allow_delegation=False,
        )
    @agent
    def lead_detector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['lead_detector_agent'], # type: ignore[index] 
            verbose=True,
            allow_delegation=False,
        )
    @agent
    def csv_writer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['csv_writer_agent'], # type: ignore[index] 
            verbose=True,
            allow_delegation=False,
        )
    

    @task
    def subreddit_discover_task(self) -> Task:
        return Task(
            config=self.tasks_config['subreddit_discover_task'], # type: ignore[index]
            output_file='searched_reddit.md'
        )
    @task
    def fetch_posts_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_posts_task'], # type: ignore[index]
            output_file='posts_and_comments_report.md',
        )
    @task
    def lead_detection_task(self) -> Task:
        return Task(
            config=self.tasks_config['lead_detection_task'], # type: ignore[index]
        )
    @task
    def csv_writer_task(self) -> Task:
        return Task(
            config=self.tasks_config['csv_writer_task'], # type: ignore[index]
            output_file='leads.csv',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SubredditFinder crew"""

        selected_agents = []
        selected_tasks = []

        print("---------------------------------------------------------------\n")
        print("Select the option you want to perform:")
        print("1. Search for subreddits")
        print("2. Find posts and comments in a subreddit")
        print("3. Find Leaads in a subreddit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            selected_agents.append(self.subreddit_discover_agent())
            selected_tasks.append(self.subreddit_discover_task())
        elif choice == '2':
            selected_agents.append(self.fetch_posts_agent())
            selected_tasks.append(self.fetch_posts_task())
        elif choice == '3':
            selected_agents.append(self.lead_detector_agent())
            selected_tasks.append(self.lead_detection_task())
            selected_agents.append(self.csv_writer_agent())
            selected_tasks.append(self.csv_writer_task())

        return Crew(
            agents=selected_agents, # Automatically created by the @agent decorator
            tasks=selected_tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
