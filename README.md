# IDP Agent (Intelligent Document Processing)

Este projeto é um protótipo de **Onboarding Digital Automatizado** desenvolvido para uma plataforma de cadastro de CNHs. O objetivo é eliminar a digitação manual de dados de (CNH) utilizando **Visão Computacional** e **Automação de Processos (RPA)**.

## Objetivo de Negócio
Reduzir o tempo de cadastro de novos instrutores/alunos em 90%, substituindo a entrada manual de dados pela leitura automática de documentos (IDP) e integração direta com o banco de dados via Webhook.

## Stack Tecnológica
* **Python 3.12**: Script de orquestração e tratamento de dados.
* **OpenAI GPT-4o-mini (Vision)**: Motor de OCR inteligente e extração de entidades (NER).
* **Requests**: Integração via API REST.
* **RPA Concept**: O script foi desenhado para atuar como gatilho (Trigger) de um fluxo maior no **n8n**.

## Como funciona
1.  O script recebe a imagem de um documento (CNH).
2.  A imagem é convertida para Base64 e enviada para a API da OpenAI.
3.  O modelo de Visão Computacional extrai campos específicos: `Nome`, `CPF`, `Validade`, `Categoria`.
4.  O retorno é estruturado em **JSON** estrito.
5.  Os dados validados são enviados para um **Webhook (n8n)** que dispara o fluxo de cadastro no CRM.

## Como rodar

# Clone o repositório
git clone [https://github.com/SEU-USER/bepilot-idp-agent.git](https://github.com/SEU-USER/bepilot-idp-agent.git)

# Instale as dependências
pip install -r requirements.txt

# Configure a API KEY no arquivo .env
# Execute
python main.py