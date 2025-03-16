import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

def calculate_shortest_paths(df, output_folder):
    """Calcula os caminhos mais curtos entre todos os pares de nós e salva os resultados."""
    anos = df['Ano'].unique()
    
    for ano in anos:
        df_ano = df[df['Ano'] == ano]
        G = nx.Graph()
        
        # Adiciona nós e arestas ao grafo
        for _, row in df_ano.iterrows():
            estado = row['UF']
            arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
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
        
        # Calcula os caminhos mais curtos
        shortest_paths = dict(nx.all_pairs_shortest_path_length(G))
        
        # Salva os resultados em um arquivo de texto
        output_path = os.path.join(output_folder, f'shortest_paths_{ano}.txt')
        with open(output_path, 'w') as f:
            f.write(f"Caminhos Mais Curtos no Ano {ano}:\n")
            for source, paths in shortest_paths.items():
                for target, length in paths.items():
                    f.write(f"{source} -> {target}: {length}\n")
        
        # Gera uma visualização gráfica do grafo
        plt.figure(figsize=(12, 8))
        
        # Desenha os nós
        nx.draw_networkx_nodes(
            G, pos,
            node_size=1000,
            node_color='skyblue',
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
        plt.title(f"Caminhos Mais Curtos no Ano {ano}", fontsize=16)
        plt.axis('off')  # Remove os eixos
        
        # Salva a imagem
        plt.savefig(os.path.join(output_folder, f'shortest_paths_graph_{ano}.png'), bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"Caminhos mais curtos no ano {ano} salvos em {output_path} e visualização salva em {output_folder}/shortest_paths_graph_{ano}.png")

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