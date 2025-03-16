import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os

def find_connected_components(df, output_folder):
    """Identifica componentes conexas na rede e salva os resultados."""
    anos = df['Ano'].unique()
    
    for ano in anos:
        df_ano = df[df['Ano'] == ano]
        G = nx.Graph()
        
        for _, row in df_ano.iterrows():
            estado = row['UF']
            arrecadacao = row['IMPOSTO SOBRE IMPORTAÇÃO']
            G.add_node(estado, bipartite=0)
            G.add_node(ano, bipartite=1)
            G.add_edge(estado, ano, weight=arrecadacao)
        
        # Encontra as componentes conexas
        components = list(nx.connected_components(G))
        
        # Salva os resultados em um arquivo de texto
        output_path = os.path.join(output_folder, f'connected_components_{ano}.txt')
        with open(output_path, 'w') as f:
            f.write(f"Componentes Conexas no Ano {ano}:\n")
            for i, component in enumerate(components):
                f.write(f"Componente {i + 1}: {component}\n")
        
        # Gera uma visualização gráfica do grafo com componentes conexas destacadas
        plt.figure(figsize=(20, 15))  # Aumenta o tamanho da figura
        
        # Usa o layout spring_layout com parâmetros personalizados para espalhar os nós
        pos = nx.spring_layout(G, k=1.5, iterations=200)
        
        # Desenha os nós com cores diferentes para cada componente conexa
        colors = [i for i, component in enumerate(components) for node in component]
        nx.draw_networkx_nodes(
            G, pos,
            node_size=1000,
            node_color=colors,
            cmap=plt.cm.tab20,  # Mapa de cores para diferenciar componentes
            alpha=0.8
        )
        
        # Desenha as arestas com o valor do imposto no centro
        edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edges(
            G, pos,
            width=1.0,
            edge_color='gray',
            alpha=0.5
        )
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=edge_labels,
            font_size=10,
            font_color='red'
        )
        
        # Desenha os rótulos dos nós
        nx.draw_networkx_labels(
            G, pos,
            font_size=12,
            font_weight='bold',
            font_color='black'
        )
        
        # Adiciona título e remove eixos
        plt.title(f"Componentes Conexas no Ano {ano}", fontsize=24)
        plt.axis('off')  # Remove os eixos
        
        # Salva a imagem
        plt.savefig(os.path.join(output_folder, f'connected_components_graph_{ano}.png'), bbox_inches='tight', dpi=300)
        plt.close()
        
        print(f"Componentes conexas no ano {ano} salvas em {output_path} e visualização salva em {output_folder}/connected_components_graph_{ano}.png")

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