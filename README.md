# Oficina-API

## Exercícios Práticos: Construindo uma API com FastAPI

#### Nessa atividade vocês irão testar o que foi apresentado na oficina.

Vocês irão fazer uma API que atua como uma intermediária (*wrapper*), consumindo e manipulando dados de uma API de e-commerce pública e de testes, a **[DummyJSON](https://dummyjson.com/)**.

O objetivo é construir uma API funcional com FastAPI que interage com um serviço externo. Ao final, você terá praticado:
* O uso dos principais métodos HTTP: `GET`, `POST` e `DELETE`.
* A construção de endpoints com **parâmetros de caminho** (ex: `/products/1`) e **parâmetros de consulta** (ex: `/search?q=phone`).
* O envio e recebimento de dados no formato `JSON`.
* A criação de uma pequena "automação", onde sua API consome outra para realizar uma tarefa.

### Construindo os Endpoints

Vamos construir nossa API passo a passo, adicionando um endpoint de cada vez.

#### Endpoint 1: Buscar um Produto Específico (GET)

O primeiro passo é criar um endpoint que busca um único produto pelo seu ID.

* **Descrição:** Este endpoint receberá um número (ID) na URL e o usará para buscar os detalhes de um produto específico na API DummyJSON.
* **Método HTTP:** `GET`
* **Caminho (Path):** `/products/{product_id}`

#### Endpoint 2: Pesquisar Produtos (GET com Parâmetro de Consulta)

Agora, vamos criar uma funcionalidade de busca.

* **Descrição:** Este endpoint permitirá que o usuário pesquise produtos enviando um termo de busca.
* **Método HTTP:** `GET`
* **Caminho (Path):** `/products/search/`
* **Parâmetro de Consulta (Query Parameter):** `q` (obrigatório)


#### Endpoint 3: Adicionar um Novo Produto (POST)

Vamos implementar a capacidade de criar novos recursos.

* **Descrição:** Este endpoint receberá os dados de um novo produto no corpo da requisição (`body`) e os enviará para a DummyJSON para criação.
* **Método HTTP:** `POST`
* **Caminho (Path):** `/products/add`

**Instruções:**
Este é um passo mais avançado. Usaremos o `Pydantic` (que já vem com o FastAPI) para validar os dados que recebemos e também definiremos um código de status de retorno (`201 Created`) para seguir as boas práticas.

```python
# Adicione estas importações no topo do seu arquivo main.py
from fastapi import status, Response
from pydantic import BaseModel

# Crie este "modelo" para validar os dados do produto que chegam na nossa API
class Produto(BaseModel):
    title: str
    price: float

# Adicione este novo endpoint
@app.post("/products/add")
def adicionar_produto(produto: Produto, response_api: Response):
    # 'produto: Produto' diz ao FastAPI para esperar um JSON com 'title' e 'price'
    url = "[https://dummyjson.com/products/add](https://dummyjson.com/products/add)"
    
    # .dict() converte o objeto Pydantic em um dicionário para enviar
    response_externa = requests.post(url, json=produto.dict())
    
    # Definimos o código de status da NOSSA API como 201 (Created)
    response_api.status_code = status.HTTP_201_CREATED
    
    return response_externa.json()
```

#### Endpoint 4: Deletar um Produto (DELETE)

Para completar as operações básicas, vamos criar a função de deletar.

* **Descrição:** Este endpoint receberá o ID de um produto na URL e enviará uma requisição para removê-lo.
* **Método HTTP:** `DELETE`
* **Caminho (Path):** `/products/delete/{product_id}`

**Instruções:**
A boa prática para uma operação `DELETE` bem-sucedida é retornar um status `204 No Content`, que indica sucesso sem retornar nenhum dado no corpo da resposta.

```python
# Adicione este endpoint ao final do seu arquivo
@app.delete("/products/delete/{product_id}")
def deletar_produto(product_id: int):
    url = f"[https://dummyjson.com/products/](https://dummyjson.com/products/){product_id}"
    
    response_externa = requests.delete(url)
    
    # Se a API externa confirmou a deleção (status 200),
    # nossa API retorna um status 204 para o cliente.
    if response_externa.status_code == 200:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        # Se deu erro (ex: produto não existe), repassamos a mensagem de erro
        return response_externa.json()
```

---

### ▶️ Como Executar e Testar sua API

1.  **Inicie o Servidor:** Com o arquivo `main.py` salvo, execute o seguinte comando no terminal:
    ```bash
    uvicorn main:app --reload
    ```
2.  **Acesse a Documentação Interativa:** Abra seu navegador e acesse a URL fornecida pelo Uvicorn, adicionando `/docs` ao final.
    * **Localmente:** `http://127.0.0.1:8000/docs`
    
3.  **Teste cada Endpoint:** Use a interface do `/docs` para testar cada um dos  endpoints que você criou e veja os resultados em tempo real!
