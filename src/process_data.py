import pandas as pd

def load_data(file_path):
    """Carrega os dados do arquivo CSV."""
    df = pd.read_csv(file_path, sep=';', encoding='latin1')
    return df

def preprocess_data(df):
    """Realiza o pré-processamento dos dados."""
    # Remove colunas desnecessárias ou com valores nulos
    df = df.dropna(axis=1, how='all')
    
    # Converte colunas de valores para numéricas
    for col in df.columns[3:]:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Agrupa por estado e ano, somando os valores
    df_grouped = df.groupby(['Ano', 'UF']).sum().reset_index()
    
    return df_grouped

def save_processed_data(df, output_path):
    """Salva os dados processados em um novo arquivo CSV."""
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    # Caminho para o arquivo de dados
    input_file = '../data/arrecadacao-estado.csv'
    output_file = '../data/processed_arrecadacao.csv'
    
    # Carrega e processa os dados
    df = load_data(input_file)
    df_processed = preprocess_data(df)
    
    # Salva os dados processados
    save_processed_data(df_processed, output_file)
    print("Dados processados e salvos com sucesso!")