import pandas as pd
import yaml
from environment import Environment
from collections import Counter

with open("config.yaml") as f:
    config = yaml.safe_load(f)

env = Environment(config)

data = []

for step in range(config["timesteps"]):

    env.step()

    population = len(env.population)
    resource = env.resource

    genotypes = [b.genotype for b in env.population]
    counts = Counter(genotypes)

    mutation_frequency = len(counts)

    cooperation_index = population * 0.01
    competition_index = population * 0.02

    row = {
        "time_step": step,
        "total_population": population,
        "resource_concentration": resource,
        "mutation_frequency": mutation_frequency,
        "cooperation_index": cooperation_index,
        "competition_index": competition_index
    }

    for g, c in counts.items():
        row[f"genotype_{g}_density"] = c / population

    data.append(row)

df = pd.DataFrame(data)
df.to_csv("simulation_metrics.csv", index=False)

print("Simulation completed.")