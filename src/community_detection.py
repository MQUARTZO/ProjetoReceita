import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
from community import community_louvain  # Biblioteca para detecção de comunidades

def detect_communities(df, output_folder):
    """Detecta comunidades na rede e salva os resultados."""
    anos = df['Ano'].unique()
    
    for ano in anos:
        df_ano = df[df['Ano'] == ano]
        G = nx.Graph()
        
        # Adiciona nós e arestas ao grafo
        for _, row in df_ano.iterrows():
            estado = row['UF']
            arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
            
            # Garante que o valor do imposto seja positivo
            if arrecadacao < 0:
                arrecadacao = 0  # Define como zero se for negativo
            
            G.add_node(estado, bipartite=0)
            G.add_node(ano, bipartite=1)
            G.add_edge(estado, ano, weight=arrecadacao)
        
        # Ordena os estados por valor de imposto sobre importação (decrescente)
        estados_ordenados = sorted(df_ano['UF'], key=lambda x: df_ano[df_ano['UF'] == x]['IMPOSTO SOBRE IMPORTAÇÃO'].values[0], reverse=True)
        
        # Define posições dos nós manualmente
        pos = {}
        pos[ano] = (0, 0)  # Ano no centro
        for i, estado in enumerate(estados_ordenados):
            pos[estado] = (1, i)  # Estados à direita, ordenados
        
        # Detecta comunidades usando o algoritmo de Louvain
        try:
            partition = community_louvain.best_partition(G, weight='weight')
        except ValueError as e:
            print(f"Erro ao detectar comunidades no ano {ano}: {e}")
            continue  # Pula para o próximo ano se houver erro
        
        # Salva os resultados em um arquivo de texto
        output_path = os.path.join(output_folder, f'communities_{ano}.txt')
        with open(output_path, 'w') as f:
            f.write(f"Comunidades Detectadas no Ano {ano}:\n")
            for node, community_id in partition.items():
                f.write(f"{node}: Comunidade {community_id}\n")
        
        # Gera uma visualização gráfica do grafo
        plt.figure(figsize=(12, 8))
        
        # Desenha os nós com cores diferentes para cada comunidade
        nx.draw_networkx_nodes(
            G, pos,
            node_size=1000,
            node_color=list(partition.values()),
            cmap=plt.cm.tab20,  # Mapa de cores para diferenciar comunidades
            alpha=0.8
        )
        
        # Desenha as arestas
        edges = nx.draw_networkx_edges(
            G, pos,
            width=1.0,
            edge_color='gray',
            alpha=0.5
        )
        
        # Desenha os rótulos das arestas
        edge_labels = {(estado, ano): f"{G.edges[estado, ano]['weight']:.2f}" for estado in estados_ordenados}
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=8,
            font_color='red',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)  # Fundo branco para melhor legibilidade
        )
        
        # Desenha os rótulos dos nós
        nx.draw_networkx_labels(
            G, pos,
            font_size=10,
            font_weight='bold',
            font_color='black'
        )
        
        # Adiciona título e remove eixos
        plt.title(f"Comunidades Detectadas no Ano {ano}", fontsize=16)
        plt.axis('off')  # Remove os eixos
        
        # Salva a imagem
        plt.savefig(os.path.join(output_folder, f'communities_graph_{ano}.png'), bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"Comunidades detectadas no ano {ano} salvas em {output_path} e visualização salva em {output_folder}/communities_graph_{ano}.png")

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