import os
import csv


class Logger:
    """
    Logger for metrics
    """
    def __init__(self):
        self.metrics = []
        """ list of metrics"""
        self.directory = 'logs'
        """ directory of the logs"""
        self.fields = ['episode', 'step', 'agent', 'action', 'reward']
        """ fields to log"""

        with open(os.path.join(self.directory, "metrics.tsv"), "a", newline='') as csvfile:
            logwriter = csv.DictWriter(csvfile, delimiter='\t', fieldnames=self.fields)
            logwriter.writeheader()

    def log_metrics(self, metrics: dict):
        """
        Log one row of metrics

        :param metrics: Dictionary containing 'episode', 'step', 'agent', 'action', 'reward' keys
        """
        with open(os.path.join(self.directory, "metrics.tsv"), "a", newline='') as csvfile:
            logwriter = csv.DictWriter(csvfile, delimiter='\t', fieldnames=self.fields)
            logwriter.writerow(metrics)
