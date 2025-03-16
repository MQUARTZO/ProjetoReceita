import pandas as pd
import networkx as nx
import os

def calculate_shortest_paths(df, output_folder):
    """Calcula os caminhos mais curtos entre todos os pares de nós e salva os resultados."""
    # Cria o grafo bipartido
    G = nx.Graph()
    
    for _, row in df.iterrows():
        estado = row['UF']
        ano = row['Ano']
        arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
        G.add_node(estado, bipartite=0)
        G.add_node(ano, bipartite=1)
        G.add_edge(estado, ano, weight=arrecadacao)
    
    # Calcula os caminhos mais curtos
    shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
    
    # Salva os resultados em um arquivo de texto
    output_path = os.path.join(output_folder, 'shortest_paths.txt')
    with open(output_path, 'w') as f:
        f.write("Caminhos Mais Curtos:\n")
        for source, paths in shortest_paths.items():
            for target, length in paths.items():
                f.write(f"{source} -> {target}: {length}\n")
    
    print(f"Caminhos mais curtos salvos em {output_path}")

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_folder = 'C:/Users/Mateus/ProjetoReceita/images/shortest_paths_analysis'
    
    # Verifica se a pasta de saída existe, caso contrário, cria-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Carrega os dados processados
    df = pd.read_csv(processed_file)
    
    # Realiza a análise de caminhos mais curtos
    calculate_shortest_paths(df, output_folder)
    print("Análise de caminhos mais curtos concluída!")