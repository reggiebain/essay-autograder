import pandas as pd
import pickle
import matplotlib.pyplot as plt

# Load pickled results
with open("output/grading_results.pkl", "rb") as f:
    data = pickle.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Create column of total scores 
df['total_score'] = df['Accuracy_score'] + df['Argument_score'] + df['Conclusions & Extensions_score'] + df['Mechanics_score']
df[['last_name', 'first_name']] = df['student'].str.split('--', expand=True)
simple_df = df[['first_name', 'last_name', 'slo', 'total_score']]
simple_df.to_csv('output/simplified_results.csv')
