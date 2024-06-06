from CSV_module import CSVreader
class TarjanSCC:
    def __init__(self, graph):
        self.graph = graph  
        self.n = len(graph)  #!Количество вершин
        self.index = 0 #? low link number
        self.stack = []      #! Стэк
        self.in_stack = [False] * self.n #! Массив проверки на наличие вершины в стэке
        self.indices = [-1] * self.n #! Не посещенные вершины
        self.lowlink = [-1] * self.n #! Список low link элементов
        self.sccs = [] #! Список сильных компонент связанности

    def strong_connect(self, v):
        self.indices[v] = self.index #! устанавливаем посещение для вершины
        self.lowlink[v] = self.index #! устанавливаем low link number для вершины
        self.index += 1 
        self.stack.append(v) #! кладем в стэк командой put индекс нашей вершины
        self.in_stack[v] = True #! обозначаем что вершина в стэке

        for w in self.graph[v]: #! пробегаемся по всем соседям нашей вершины
            if self.indices[w] == -1: #! проверяем есть ли уже посещенные вершины
                self.strong_connect(w) #? РЕКУРСИЯ.....
                self.lowlink[v] = min(self.lowlink[v], self.lowlink[w]) #todo Устанавливаем значение low link для вершины выбирая между текущей и соседней
            elif self.in_stack[w]: #todo Если сосед уже был посещен и находится в стэке 
                self.lowlink[v] = min(self.lowlink[v], self.indices[w]) #! было найдено обратное ребро соединющее текущую вершину с более ранней

        #! Если вершина корневая, очищаем стэк и записываем сильный компонент связанности
        if self.lowlink[v] == self.indices[v]: #! смотрим если значение low link вершины == ее индексу и делаем вывод, что найден сильный компонент связанности
            scc = []
            while True:
                w = self.stack.pop()
                self.in_stack[w] = False
                scc.append(w)
                if w == v:
                    break
            self.sccs.append(scc)

    def get_sccs(self):
        for v in self.graph:
            if self.indices[v] == -1:
                self.strong_connect(v)
        with open('res/result.txt', 'w', encoding='utf-8') as file:
            for line in self.sccs:
                line_str = ""
                for char in line:
                    line_str += f"{char} "
                file.write(f"{line_str}\n")   
            file.close()
        return self.sccs


if __name__ == "__main__":
    csv_reader = CSVreader('test.csv')
    graph = csv_reader.create_adjacency_list()
    
    # Adjust the graph to ensure all nodes are present
    max_node = max(max(csv_reader.df['source']), max(csv_reader.df['target']))
    graph = {i: graph.get(i, []) for i in range(max_node + 1)}

    # Apply Tarjan's Algorithm
    tarjan = TarjanSCC(graph)
    sccs = tarjan.get_sccs()
    print("Strongly Connected Components:", sccs)
