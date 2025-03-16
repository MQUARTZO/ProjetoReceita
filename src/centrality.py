import pandas as pd
import networkx as nx
import os

def calculate_centrality(df, output_folder):
    """Calcula o grau de centralidade de cada nó e salva os resultados."""
    # Cria o grafo bipartido
    G = nx.Graph()
    
    for _, row in df.iterrows():
        estado = row['UF']
        ano = row['Ano']
        arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
        G.add_node(estado, bipartite=0)
        G.add_node(ano, bipartite=1)
        G.add_edge(estado, ano, weight=arrecadacao)
    
    # Calcula o grau de centralidade
    centrality = nx.degree_centrality(G)
    
    # Ordena os nós por centralidade (do maior para o menor)
    centrality_sorted = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    
    # Salva os resultados em um arquivo de texto
    output_path = os.path.join(output_folder, 'centrality.txt')
    with open(output_path, 'w') as f:
        f.write("Grau de Centralidade:\n")
        for node, value in centrality_sorted:
            f.write(f"{node}: {value:.4f}\n")
    
    print(f"Grau de centralidade salvo em {output_path}")

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_folder = 'C:/Users/Mateus/ProjetoReceita/images/centrality_analysis'
    
    # Verifica se a pasta de saída existe, caso contrário, cria-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Carrega os dados processados
    df = pd.read_csv(processed_file)
    
    # Realiza a análise de centralidade
    calculate_centrality(df, output_folder)
    print("Análise de centralidade concluída!")