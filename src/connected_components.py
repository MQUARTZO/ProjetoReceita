import pandas as pd
import networkx as nx
import os

def find_connected_components(df, output_folder):
    """Identifica componentes conexas na rede e salva os resultados."""
    # Cria o grafo bipartido
    G = nx.Graph()
    
    for _, row in df.iterrows():
        estado = row['UF']
        ano = row['Ano']
        arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
        G.add_node(estado, bipartite=0)
        G.add_node(ano, bipartite=1)
        G.add_edge(estado, ano, weight=arrecadacao)
    
    # Encontra as componentes conexas
    components = list(nx.connected_components(G))
    
    # Salva os resultados em um arquivo de texto
    output_path = os.path.join(output_folder, 'connected_components.txt')
    with open(output_path, 'w') as f:
        f.write("Componentes Conexas:\n")
        for i, component in enumerate(components):
            f.write(f"Componente {i + 1}: {component}\n")
    
    print(f"Componentes conexas salvas em {output_path}")

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_folder = 'C:/Users/Mateus/ProjetoReceita/images/connected_components_analysis'
    
    # Verifica se a pasta de saída existe, caso contrário, cria-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Carrega os dados processados
    df = pd.read_csv(processed_file)
    
    # Realiza a análise de componentes conexas
    find_connected_components(df, output_folder)
    print("Análise de componentes conexas concluída!")