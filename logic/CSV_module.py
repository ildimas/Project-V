import pandas as pd

class CSVreader:
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    def create_adjacency_list(self):
        graph = {}
        for _, row in self.df.iterrows():
            source, target = row['source'], row['target']
            if source in graph:
                graph[source].append(target)
            else:
                graph[source] = [target]
            if target not in graph:
                graph[target] = []
        return graph
if __name__ == "__main__":
# Create the adjacency list
    csv = CSVreader('test.csv')
    print(csv.create_adjacency_list())