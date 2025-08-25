import requests
from fastapi import FastAPI

app = FastAPI() # cria a aplicação e será o ponto central das rotas


@app.get("/products") # Requisição GET com URL "/products" 
def buscar_produtos(): # Função que implementa a requisição
    
    url = f"https://dummyjson.com/products/" # URL da API externa para pegar os dados
    
    response = requests.get(url) # Faz a requisição GET para a API externa e armazena o resultado em response.
    
    return response.json() # Retorna para quem chamou nossa API o resultado em response convertido para JSON
