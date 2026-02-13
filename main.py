import base64
import json
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("OPENAI_API_KEY")

WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "https://webhook.site/SEU-LINK-AQUI") 

client = OpenAI(api_key=API_KEY)

def encode_image(image_path):
    """Converte a imagem para Base64 para enviar para a API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_cnh_data(image_path):
    """
    Simula um motor de IDP (Intelligent Document Processing).
    Usa Visão Computacional para ler dados não estruturados de uma CNH.
    """
    print(f" [IDP] Iniciando análise do documento: {image_path}...")
    
    base64_image = encode_image(image_path)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": (
                                "Você é um agente de extração de dados (IDP). "
                                "Analise esta CNH brasileira e extraia os seguintes dados em JSON estrito: "
                                "nome_completo, cpf, registro_cnh, validade, categoria. "
                                "Se algum campo estiver ilegível, retorne null. "
                                "Retorne APENAS o JSON, sem markdown."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ],
            max_tokens=300
        )
        
        
        content = response.choices[0].message.content.replace("```json", "").replace("```", "")
        data = json.loads(content)
        print("[IDP] Dados extraídos com sucesso!")
        return data

    except Exception as e:
        print(f"Erro na extração: {e}")
        return None

def send_to_automation(data):
    """
    Envia os dados estruturados para o fluxo de automação (RPA/n8n).
    """
    if not data:
        return

    print("[RPA] Enviando payload para o Webhook (N8N)...")
    try:
        
        response = requests.post(WEBHOOK_URL, json=data)
        print(f"STATUS WEBHOOK: {response.status_code}")
        print("Fluxo de Onboarding iniciado.")
    except Exception as e:
        print(f"Erro ao conectar com Webhook: {e}")

if __name__ == "__main__":
    
    IMAGE_FILE = "cnh_teste.jpg" 
    
    if os.path.exists(IMAGE_FILE):
        extracted_data = extract_cnh_data(IMAGE_FILE)
        print(json.dumps(extracted_data, indent=4, ensure_ascii=False))
        
        send_to_automation(extracted_data)
    else:
        print(f" Arquivo {IMAGE_FILE} não encontrado. Adicione uma imagem para testar.")