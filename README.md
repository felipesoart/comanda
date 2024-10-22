# Sistema de Pedidos com Django e CSV

Este é um projeto de sistema de pedidos, desenvolvido em Django, que utiliza arquivos CSV para armazenar os dados em vez de um banco de dados relacional. 
O sistema permite a criação de pedidos de venda, exibição de dados da empresa, listagem de produtos e operadores, e a geração de uma nota fiscal em formato de impressão.
O projeto também gera um relatório de venda para impressão, onde o cliente pode escolher imprimir ou salvar em PDF.

## Funcionalidades

- Adicionar produtos ao pedido
- Selecionar cliente e operador
- Calcular total da venda
- Finalizar o pedido com diferentes formas de pagamento
- Gerar uma nota pronta para impressão
- Persistir dados de pedidos e empresas em arquivos CSV

## Arquivos CSV Utilizados

O projeto trabalha com três arquivos CSV principais:

1. **produtos.csv**:
    - Contém as colunas: `DESCRICAO`, `VALOR`
    - Exemplo:
      ```csv
      DESCRICAO,VALOR
      "LINGUIÇA NOBRE",2.50
      "MEIO BAIÃO",3.00
      ```

2. **empresas.csv**:
    - Contém as colunas: `NOME_EMPRESA`, `CPF_CNPJ`, `OPERADORES`
    - Exemplo:
      ```csv
      NOME_EMPRESA,CPF_CNPJ,OPERADORES
      "GALETERIA CANTO DO FRANGO","12345678901234","CARLOS;FELIPE;JOSY"
      ```

3. **pedidos.csv**:
    - Contém as colunas: `DATA_HORA`, `CONTROLE_NUM`, `COMANDA`, `TOTAL`, `FORMA_PAGAMENTO`,`CLIENTE`,`OPERADOR`
    - Exemplo:
      ```csv
      DATA_HORA,CONTROLE_NUM,COMANDA,TOTAL,FORMA_PAGAMENTO,CLIENTE,OPERADOR
      2024-10-22 10:52:02,2,PRODUTO => LINGUIÇA NOBRE (UND => 1) VALOR => R$ 2.5 # PRODUTO => MEIO BAIÃO (UND => 1) VALOR => R$ 3,5.5,Dinheiro,felipe,CARLOS
      2024-10-22 12:19:45,14,PRODUTO => LINGUIÇA NOBRE (UND => 1) VALOR => R$ 2.5 # PRODUTO => LINGUIÇA NOBRE (UND => 2) VALOR => R$ 2.5,7.5,Dinheiro,,JOSY
      ```

## Pré-requisitos

Antes de rodar o projeto, certifique-se de ter as seguintes dependências instaladas:

- Python 3.9 ou superior
- Django 3.2 ou superior

Você pode instalar as dependências necessárias executando o seguinte comando:
(obs: antes crie o arquivo requirements.txt com o Django>=3.2 dentro)
```bash
pip install -r requirements.txt
```
ou 
```bash
pip install django
pip install django reportlab
```
## Como Rodar o Projeto
  1 Clone este repositório:
  ```bash
  git clone https://github.com/seu-usuario/seu-repositorio.git
  ```
 2 Navegue até a pasta do projeto
  ```bash
   cd nome-do-projeto
```
3 Crie um arquivo produtos.csv, empresas.csv e pedidos.csv conforme descrito acima.

4 Execute o servidor Django:
 ```bash
  python manage.py migrate
  python manage.py runserver
  ```
5 Acesse o projeto em seu navegador, no endereço: http://127.0.0.1:8000

## Observações
  • O projeto não utiliza um banco de dados tradicional, todos os dados são persistidos e manipulados através de arquivos CSV.
  • O layout de impressão foi otimizado para uma largura de 8cm, adequado para impressoras de recibo.

## Licença
  Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
