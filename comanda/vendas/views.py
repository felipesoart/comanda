import csv
import json
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.http import JsonResponse
# Create your views here.


def pagina_inicial(request):
    produtos = ler_produtos()  # Função que lê o CSV de produtos
    operadores, dados_empresa = ler_dados_empresa()  # Função que lê o CSV de empresa e retorna operadores e dados
    #print(dados_empresa)
    return render(request, 'vendas/index.html', {'produtos': produtos, 'operadores': operadores, 'dados_empresa': dados_empresa})





def ler_produtos():
    with open('vendas/produtos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
   
def ler_dados_empresa():
    with open('vendas/empresa.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dados_empresa = list(reader)
        operadores = []
        for empresa in dados_empresa:
            operadores += empresa['OPERADOR'].split(';')
        return list(set(operadores)), dados_empresa  # Remove duplicatas






def calcular_total(produto, quantidade):
    produtos = ler_produtos()
    for item in produtos:
        if item['DESCRICAO'] == produto:
            return float(item['VALOR']) * quantidade




def processar_pedido(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        operador = request.POST.get('operador')
        forma_pagamento = request.POST.get('forma_pagamento')
        
        # Desserializa os produtos enviados como JSON
        produtos = json.loads(request.POST.get('produtos'))  # Recebe os produtos como JSON

        if not produtos:
            return HttpResponse("Nenhum produto foi adicionado ao pedido.", status=400)

        # Calcula o total
        total = sum(produto['valor'] * produto['quantidade'] for produto in produtos)

        # Cria a comanda (descrição do pedido)
        comanda = " # ".join([f"PRODUTO => {p['descricao']} (UND => {p['quantidade']}) VALOR => R$ {p['valor']}" for p in produtos])

        # Gera o número de controle
        controle_numero = controle_num()

         # Data e hora atual do pedido
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Escreve o pedido no CSV
        with open('vendas/pedidos.csv', 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([data_hora, controle_numero, comanda, total, forma_pagamento, cliente, operador])

        return HttpResponse("Pedido processado com sucesso!")


# Função para calcular o número de controle do pedido
def controle_num():
    try:
        with open('vendas/pedidos.csv', newline='', encoding='utf-8') as csvfile:
            return sum(1 for _ in csvfile) + 1
    except FileNotFoundError:
        return 1  # Se o arquivo não existir, começa do pedido número 1



def gerar_pdf(request, pedido_id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="pedido_{pedido_id}.pdf"'

    c = canvas.Canvas(response)

    # Informações do cabeçalho
    c.drawString(100, 750, "Recibo do Pedido")
    c.drawString(100, 730, f"Pedido Nº: {pedido_id}")

    # Aqui você pode usar as funções `ler_produtos` e `ler_dados_empresa` para puxar detalhes
    produtos = ler_produtos()  # Carrega os produtos
    dados_empresa = ler_dados_empresa()  # Carrega os dados da empresa

    # Exemplo de escrita de detalhes de produtos no PDF
    y = 700
    for produto in produtos:
        c.drawString(100, y, f"{produto['descricao']} - {produto['valor']}")
        y -= 20

    c.showPage()
    c.save()
    return response

def obter_ultimo_pedido_view(request):
    controle_num, data_hora = obter_ultimo_pedido()
    return JsonResponse({'controle_num': controle_num, 'data_hora': data_hora})

def obter_ultimo_pedido():
    print("inicio obter_ultimo_pedido")
    try:
        with open('vendas/pedidos.csv', 'r', encoding='utf-8') as csvfile:
            reader = list(csv.reader(csvfile))
            if reader:
                # Pega o último registro
                ultimo_registro = reader[-1]
                controle_num = ultimo_registro[1]  # Assume que CONTROLE_NUM está na segunda coluna
                data_hora = ultimo_registro[0]  # Assume que DATA_HORA está na primeira coluna
                return controle_num, data_hora
            else:
                return None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None, None