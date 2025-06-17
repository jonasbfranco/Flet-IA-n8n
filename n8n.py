import flet as ft
import requests

# Configuração do n8n
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/aula-n8n-yt"


async def get_ai_response(user_message: str, page: ft.Page):
    try:
        # Enviar a mensagem do usuario para o webhook do n8n
        payload = {
            "message": user_message,
            "user_name": page.session.get('user_name')
        }

        response = requests.post(N8N_WEBHOOK_URL, json=payload)

        response_data = response.json()

        if response.status_code == 200:
            return response.json().get("output")
        else:
            return f"Erro ao conectar resposta da IA: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Erro ao conectar com n8n: {str(e)}"