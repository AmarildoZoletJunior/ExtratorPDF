import io
import os
import shutil
import PyPDF2
import re
import base64

def extrair_pagina_com_texto(base64String, texto_desejado):
    caminho_Pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pastaPdfs')
    if os.path.exists(caminho_Pasta):
            print("Ja encontrou")
    else:
            os.makedirs(caminho_Pasta)
            print("Criou")

    CaminhoPastaComArquivo = os.path.join(caminho_Pasta, 'PdfInicial.pdf')
    CaminhoPastaComPdfUnitario = os.path.join(caminho_Pasta,'PdfExtraido.pdf')
    conteudo_binario = base64.b64decode(base64String) ##Cria um código binário do base64 recebido
    with open(CaminhoPastaComArquivo, "wb") as arquivo_pdf: ##Inserir arquivo binário já como pdf com o conteúdo dentro.
         arquivo_pdf.write(conteudo_binario)

    with open(CaminhoPastaComArquivo, 'rb') as arquivo_pdf:
        leitor = PyPDF2.PdfReader(arquivo_pdf)
        for numero_pagina in range(len(leitor.pages)):
            pagina = leitor.pages[numero_pagina]
            texto = pagina.extract_text().replace("-","")
            if texto_desejado in texto:
                print("Achou")
                novo_documento = PyPDF2.PdfWriter()
                pagina = leitor.pages[numero_pagina]
                with open(CaminhoPastaComPdfUnitario, "wb") as arquivo_pdf: ##Inserir pdf já unitário
                    novo_documento.add_page(pagina)
                    novo_documento.write(arquivo_pdf)
                stringBase64 = converter_pdf_para_base64(CaminhoPastaComPdfUnitario)
    if os.path.exists(caminho_Pasta):
                     for arquivo in os.listdir(caminho_Pasta):
                        urlPasta = os.path.join(caminho_Pasta,arquivo)
                        os.remove(urlPasta)
    return print(stringBase64)

def converter_pdf_para_base64(nome_arquivo):
    with open(nome_arquivo, 'rb') as arquivo_pdf:
        conteudo_pdf = arquivo_pdf.read()
        base64_pdf = base64.b64encode(conteudo_pdf).decode('utf-8')
        return base64_pdf

extrair_pagina_com_texto('base 64','texto desejado')