import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def create_bipartite_graph(df):
    """Cria um grafo bipartido a partir dos dados."""
    G = nx.Graph()
    
    # Adiciona nós para estados e anos
    estados = df['UF'].unique()
    anos = df['Ano'].unique()
    
    G.add_nodes_from(estados, bipartite=0)
    G.add_nodes_from(anos, bipartite=1)
    
    # Adiciona arestas com pesos baseados na arrecadação total
    for _, row in df.iterrows():
        estado = row['UF']
        ano = row['Ano']
        arrecadacao_total = row.iloc[2:].sum()
        G.add_edge(estado, ano, weight=arrecadacao_total)
    
    return G

def draw_graph(G, output_path):
    """Desenha o grafo e salva a imagem."""
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))
    
    # Define cores para os nós
    color_map = []
    for node in G.nodes():
        if G.nodes[node]['bipartite'] == 0:
            color_map.append('blue')  # Estados
        else:
            color_map.append('green')  # Anos
    
    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=2000, font_size=10, font_weight='bold')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    input_file = 'C:/Users/Mateus/ProjetoReceita/data/arrecadacao-estado.csv'
    output_image = 'C:/Users/Mateus/ProjetoReceita/images/bipartite_graph.png'
    
    # Carrega os dados processados
    df = pd.read_csv(input_file)
    
    # Cria o grafo bipartido
    G = create_bipartite_graph(df)
    
    # Desenha e salva o grafo
    draw_graph(G, output_image)
    print("Grafo bipartido gerado e salvo com sucesso!")