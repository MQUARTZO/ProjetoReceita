from process_data import load_data, preprocess_data, save_processed_data
from create_graphs import create_bipartite_graph, draw_graph
from analyze_graphs import analyze_graph

def main():
    # Caminho para o arquivo de dados
    input_file = 'C:/Users/Mateus/ProjetoReceita/data/arrecadacao-estado.csv'
    processed_file = 'C:/Users/Mateus/ProjetoReceita/data/processed_arrecadacao.csv'
    output_image = 'C:/Users/Mateus/ProjetoReceita/images/bipartite_graph.png'
    output_folder_subgraphs = 'C:/Users/Mateus/ProjetoReceita/images/subgraphs'
    
    # Carrega e processa os dados
    df = load_data(input_file)
    df_processed = preprocess_data(df)
    save_processed_data(df_processed, processed_file)
    
    # Cria o grafo bipartido
    G = create_bipartite_graph(df_processed)
    
    # Desenha e salva o grafo
    draw_graph(G, output_image)
    
    # Realiza análises no grafo
    analyze_graph(G)
    

    # Cria e salva os subgrafos
    create_subgraphs(df_processed, output_folder_subgraphs)


if __name__ == "__main__":
    main()