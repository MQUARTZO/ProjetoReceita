# Projeto de Arrecadação de Impostos sobre importações: Uma Visão com Grafos

## 📌 Descrição
Este projeto utiliza **grafos** para analisar dados de arrecadação da Receita Federal, permitindo visualizar padrões de arrecadação por estado, identificar discrepâncias regionais e entender melhor a distribuição dos impostos.

## 🎯 Objetivos
- Criar um grafo representando a arrecadação dos estados brasileiros.
- Gerar subgrafos para destacar estados com **maior** e **menor** arrecadação.
- Analisar arrecadação por **Estados, utilizando todas as região geográfica** (Norte, Nordeste, Centro-Oeste, Sudeste, Sul).
- Produzir visualizações para facilitar a interpretação dos dados.

## 📂 Estrutura do Repositório

```
ProjetoReceita/
│── data/                   # Dados de arrecadação processados
│── images/                 # Imagens geradas dos grafos
│── src/                    # Código-fonte do projeto
│   ├── main.py             # Script principal para execução
│   ├── process_data.py      # Tratamento dos dados
│   ├── create_graphs.py     # Construção do grafo principal
│   ├── analyze_graphs.py    # Análise das métricas do grafo
│   ├── generate_subgraphs.py # Geração de subgrafos
│── README.md                # Documentação do projeto
│── requirements.txt         # Dependências do projeto
│── relatório.pdf            # Relatório final do projeto
```

## 🚀 Como Executar o Projeto

### **1️⃣ Instale as dependências**
Se ainda não tiver as bibliotecas instaladas, rode:
```bash
pip install -r requirements.txt
```

### **2️⃣ Execute o script principal**
```bash
python src/main.py
```

### **3️⃣ Gerar os subgrafos**
```bash
python src/generate_subgraphs.py
```

Os subgrafos serão salvos na pasta `images/`.

## 📊 Tecnologias Utilizadas
- **Python** 🐍
- **NetworkX** (para manipulação de grafos)
- **Pandas** (para processamento dos dados)
- **Matplotlib** (para visualização dos grafos)

## 🔍 Análises Realizadas
- **Estados com maior arrecadação** 💰
- **Estados com menor arrecadação** 📉
- **Distribuição da arrecadação por regiões** 🗺️
- **Centralidade e conexões entre estados** 🔗

## 🏗️ Melhorias Futuras
- Implementar métricas avançadas de análise de grafos.
- Adicionar novos dados para enriquecer a análise.
- Criar uma API para facilitar o acesso aos dados.

---
📌 **Mantenedor:** [MQUARTZO](https://github.com/MQUARTZO), [ROBSONLUAN95](https://github.com/robsonluan95)
📢 **Contribuições são bem-vindas!** Abra um Pull Request. 🚀

