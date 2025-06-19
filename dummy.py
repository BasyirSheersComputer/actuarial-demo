import pandas as pd
import random
from faker import Faker

fake = Faker()

def generate_fake_actuarial_data(n=1000):
    data = []
    for _ in range(n):
        record = {
            "PolicyID": fake.uuid4(),
            "CustomerName": fake.name(),
            "CustomerAge": random.randint(18, 75),
            "SumAssured": round(random.uniform(50000, 1000000), 2),
            "AnnualPremium": round(random.uniform(1000, 10000), 2),
            "PolicyTerm": random.choice([10, 15, 20, 25]),
            "RiskScore": round(random.uniform(0, 1), 2),
            "ClaimMade": random.choice(["Yes", "No"]),
            "ClaimAmount": round(random.uniform(0, 50000), 2),
            "Projection10Y": round(random.uniform(1.05, 2.0), 2),
        }
        data.append(record)
    return pd.DataFrame(data)

df = generate_fake_actuarial_data()
df.to_csv("policy_data.csv", index=False)
# This code generates a CSV file with fake actuarial data for insurance policies.
# The data includes policy ID, customer name, age, sum assured, annual premium,