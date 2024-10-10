import pandas as pd
from rakam_systems.components.agents.agents import Agent
from rakam_systems.components.agents.actions import ClassifyQuery


class SimpleAgent(Agent):
    def choose_action(self, input: str, state: dict):
        """
        Selects an action based on the input query.
        """
        return self.actions.get("classify_query")


# Initialize the agent
agent = SimpleAgent(
    model="gpt-3.5-turbo",
    api_key="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",
)

# Define trigger queries and corresponding class names
trigger_queries = pd.Series(["search", "retrieve", "classify"])
class_names = pd.Series(["SearchAction", "RetrieveAction", "ClassifyAction"])

# Add a classification action to the agent
classify_action = ClassifyQuery(
    agent,
    trigger_queries=trigger_queries,
    class_names=class_names,
)
agent.add_action("classify_query", classify_action)

# Input query from the user
input_query = "I want to retrieve some information."

# Execute the action based on the input query
chosen_action = agent.choose_action(input_query, state={})
result_class_name, result_trigger_query = chosen_action.execute(input_query)

# Output the result
print(f"Action: {result_class_name}, Trigger Query: {result_trigger_query}")
