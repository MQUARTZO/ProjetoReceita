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
            ipi_fumo = row['IPI - FUMO']
            ipi_bebidas = row['IPI - BEBIDAS']
            ipi_automoveis = row['IPI - AUTOMÓVEIS']  # Nome corrigido
            ipi_outros = row['IPI - OUTROS']
            
            # Soma os valores de IPI para o estado
            total_ipi = ipi_fumo + ipi_bebidas + ipi_automoveis + ipi_outros
            
            # Adiciona o nó do estado com o total de IPI
            G.add_node(estado, bipartite=0, total_ipi=total_ipi, ipi_fumo=ipi_fumo, ipi_bebidas=ipi_bebidas, ipi_automoveis=ipi_automoveis, ipi_outros=ipi_outros)
            G.add_node(ano, bipartite=1)
            G.add_edge(estado, ano, weight=total_ipi)
        
        # Ordena os estados por total de IPI (decrescente)
        estados_ordenados = sorted(df_ano['UF'], key=lambda x: df_ano[df_ano['UF'] == x]['IMPOSTO SOBRE IMPORTAÇÃO'].values[0], reverse=True)
        
        # Define posições dos nós em espiral
        pos = nx.spiral_layout(G)  # Layout em espiral
        
        # Detecta comunidades usando o algoritmo de Louvain
        partition = community_louvain.best_partition(G)
        
        # Salva os resultados em um arquivo de texto
        output_path = os.path.join(output_folder, f'communities_{ano}.txt')
        with open(output_path, 'w') as f:
            f.write(f"Comunidades Detectadas no Ano {ano}:\n")
            for node, community_id in partition.items():
                f.write(f"{node}: Comunidade {community_id}\n")
        
        # Gera uma visualização gráfica do grafo
        plt.figure(figsize=(12, 8))
        
        # Desenha os nós com cores diferentes para cada tipo de IPI
        for estado in G.nodes:
            if estado != ano:  # Ignora o nó do ano
                ipi_fumo = G.nodes[estado]['ipi_fumo']
                ipi_bebidas = G.nodes[estado]['ipi_bebidas']
                ipi_automoveis = G.nodes[estado]['ipi_automoveis']
                ipi_outros = G.nodes[estado]['ipi_outros']
                
                # Define a cor com base no maior valor de IPI
                max_ipi = max(ipi_fumo, ipi_bebidas, ipi_automoveis, ipi_outros)
                if max_ipi == ipi_fumo:
                    color = 'red'  # Fumo
                elif max_ipi == ipi_bebidas:
                    color = 'blue'  # Bebidas
                elif max_ipi == ipi_automoveis:
                    color = 'green'  # Automóveis
                else:
                    color = 'orange'  # Outros
                
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=[estado],
                    node_size=1000,
                    node_color=color,
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
            font_color='black',
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
    
    # Verifica os nomes das colunas no DataFrame
    print("Colunas disponíveis no DataFrame:", df.columns)
    
    # Realiza a detecção de comunidades
    detect_communities(df, output_folder)
    print("Detecção de comunidades concluída!")