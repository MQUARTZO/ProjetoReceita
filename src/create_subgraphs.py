import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

def create_subgraphs(df, output_folder):
    """Cria subgrafos para cada ano e salva as imagens."""
    anos = df['Ano'].unique()
    
    # Verifica se a pasta de saída existe, caso contrário, cria-a
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for ano in anos:
        df_ano = df[df['Ano'] == ano]
        
        # Ordena os estados por arrecadação (IMPOSTO SOBRE IMPORTAÇÃO) em ordem decrescente
        df_ano = df_ano.sort_values(by='IMPOSTO SOBRE IMPORTAÇÃO', ascending=False)
        
        G = nx.Graph()
        
        for _, row in df_ano.iterrows():
            estado = row['UF']
            arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
            G.add_node(estado, bipartite=0)
            G.add_node(ano, bipartite=1)
            G.add_edge(estado, ano, weight=arrecadacao)
        
        # Define o layout bipartido
        pos = nx.bipartite_layout(G, nodes=[ano], align='vertical')
        
        # Ajusta a posição dos nós para centralizar o ano
        pos[ano] = (0.5, 0.5)  # Centraliza o nó do ano
        
        # Desenha o grafo
        plt.figure(figsize=(12, 8))
        
        # Desenha os nós dos estados
        nx.draw_networkx_nodes(G, pos, nodelist=df_ano['UF'].unique(), node_size=3000, node_color='skyblue', label='Estados')
        
        # Desenha o nó do ano
        nx.draw_networkx_nodes(G, pos, nodelist=[ano], node_size=5000, node_color='orange', label='Ano')
        
        # Desenha as arestas
        nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.6)
        
        # Desenha os rótulos
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Adiciona título e legenda
        plt.title(f'Arrecadação por Estado no Ano {ano}', fontsize=16)
        plt.legend(scatterpoints=1, frameon=False, fontsize=12)
        
        # Remove eixos
        plt.axis('off')
        
        # Salva a imagem
        output_path = os.path.join(output_folder, f'subgraph_{ano}.png')
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        plt.close()

if __name__ == "__main__":
    # Caminho para o arquivo de dados processados
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_folder = 'C:/Users/Mateus/ProjetoReceita/images/subgraphs'
    
    # Carrega os dados processados
    df = pd.read_csv(processed_file)
    
    # Cria e salva os subgrafos
    create_subgraphs(df, output_folder)
    print("Subgrafos criados e salvos com sucesso!")