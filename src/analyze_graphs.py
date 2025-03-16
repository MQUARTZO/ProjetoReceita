import networkx as nx

def analyze_graph(G):
    """Realiza análises básicas no grafo."""
    print("Número de nós:", G.number_of_nodes())
    print("Número de arestas:", G.number_of_edges())
    
    # Calcula a centralidade de grau
    degree_centrality = nx.degree_centrality(G)
    print("Centralidade de grau:", degree_centrality)
    
    # Calcula a centralidade de intermediação
    betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
    print("Centralidade de intermediação:", betweenness_centrality)

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    input_file = '../data/processed_arrecadacao.csv'
    
    # Carrega os dados processados
    df = pd.read_csv(input_file)
    
    # Cria o grafo bipartido
    G = create_bipartite_graph(df)
    
    # Realiza análises no grafo
    analyze_graph(G)