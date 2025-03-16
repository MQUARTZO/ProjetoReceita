import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from community import community_louvain  # Biblioteca para detecção de comunidades

def detect_communities(df, output_folder):
    """Detecta comunidades na rede e salva os resultados."""
    # Cria o grafo bipartido
    G = nx.Graph()
    
    for _, row in df.iterrows():
        estado = row['UF']
        ano = row['Ano']
        arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
        G.add_node(estado, bipartite=0)
        G.add_node(ano, bipartite=1)
        G.add_edge(estado, ano, weight=arrecadacao)
    
    # Detecta comunidades usando o algoritmo de Louvain
    partition = community_louvain.best_partition(G)
    
    # Salva os resultados em um arquivo de texto
    output_path = os.path.join(output_folder, 'communities.txt')
    with open(output_path, 'w') as f:
        f.write("Comunidades Detectadas:\n")
        for node, community_id in partition.items():
            f.write(f"{node}: Comunidade {community_id}\n")
    
    # Gera uma visualização gráfica das comunidades
    plt.figure(figsize=(20, 15))  # Aumenta o tamanho da figura
    
    # Usa o layout spring_layout com parâmetros personalizados para espalhar os nós
    pos = nx.spring_layout(G, k=1.5, iterations=200)  # Aumenta k e iterations para espalhar mais
    
    # Desenha o grafo
    nx.draw_networkx_nodes(
        G, pos,
        node_size=1000,
        node_color=list(partition.values()),
        cmap=plt.cm.tab20,  # Usa um mapa de cores com 20 cores distintas
        alpha=0.8
    )
    
    # Desenha as arestas
    nx.draw_networkx_edges(
        G, pos,
        width=1.0,
        edge_color='gray',
        alpha=0.5
    )
    
    # Desenha os rótulos dos nós
    nx.draw_networkx_labels(
        G, pos,
        font_size=12,
        font_weight='bold',
        font_color='black'
    )
    
    # Adiciona título e remove eixos
    plt.title("Comunidades Detectadas na Rede", fontsize=24)
    plt.axis('off')  # Remove os eixos
    
    # Salva a imagem
    plt.savefig(os.path.join(output_folder, 'communities.png'), bbox_inches='tight', dpi=300)
    plt.close()
    
    print(f"Comunidades detectadas salvas em {output_path} e visualização salva em {output_folder}/communities.png")

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_folder = 'C:/Users/Mateus/ProjetoReceita/images/community_detection'
    
    # Verifica se a pasta de saída existe, caso contrário, cria-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Carrega os dados processados
    df = pd.read_csv(processed_file)
    
    # Realiza a detecção de comunidades
    detect_communities(df, output_folder)
    print("Detecção de comunidades concluída!")