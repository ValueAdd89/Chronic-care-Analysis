
import luigi
import os
import subprocess
import pandas as pd
import torch
from torch import nn
from sklearn.model_selection import train_test_split
import mlflow

class RunDbtModels(luigi.Task):
    def output(self):
        return luigi.LocalTarget('models_run.txt')

    def run(self):
        subprocess.run(['dbt', 'run'], check=True)
        with self.output().open('w') as f:
            f.write("dbt models ran")

class TrainEngagementModel(luigi.Task):
    def requires(self):
        return RunDbtModels()

    def output(self):
        return luigi.LocalTarget('ml_model.pt')

    def run(self):
        df = pd.read_csv('data/ml_engagement_training_data.csv')
        X = df[['age', 'active_days', 'avg_steps']].values
        y = df['dropout_risk'].values.astype(float)
        X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2)

        class SimpleNN(nn.Module):
            def __init__(self):
                super().__init__()
                self.fc = nn.Sequential(
                    nn.Linear(3, 8),
                    nn.ReLU(),
                    nn.Linear(8, 1),
                    nn.Sigmoid()
                )

            def forward(self, x):
                return self.fc(x)

        model = SimpleNN()
        loss_fn = nn.BCELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

        X_tensor = torch.tensor(X_train, dtype=torch.float32)
        y_tensor = torch.tensor(y_train.reshape(-1, 1), dtype=torch.float32)

        with mlflow.start_run():
            for epoch in range(100):
                optimizer.zero_grad()
                output = model(X_tensor)
                loss = loss_fn(output, y_tensor)
                loss.backward()
                optimizer.step()

            mlflow.log_metric("final_loss", loss.item())
            torch.save(model.state_dict(), self.output().path)

class FullPipeline(luigi.WrapperTask):
    def requires(self):
        return TrainEngagementModel()
