from mistralai import Mistral
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, CollectionInfo
from sentence_transformers import SentenceTransformer
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import uuid

qdrant_client = QdrantClient(
    url="https://20b229ef-c75d-4eba-81f9-faebc9841da7.europe-west3-0.gcp.cloud.qdrant.io", 
    api_key="ZAq0hJMzBhjTzXtXul0lQeispRmVmVe1vPx5G4WwUikPocHOCrnmlg",
    timeout=30
)

def create_mistral_agent(api_key = "qIzgJeXyROO9gZ6AIHWsgQKCYh5jgOCd"):
    return Mistral(api_key=api_key)

client = create_mistral_agent()

def ai_agent(question: str) -> str:
    chat_response = client.agents.complete(
    agent_id="ag:edc8f481:20250131:clear-text:ba9a032b",
    messages=[
        {
            "role": "user",
            "content": str(question),
        },
        
    ],
)
    return chat_response.choices[0].message.content

def add_vector(title: str, text: str, collection_name="news_collection", model_name='all-MiniLM-L6-v2'):
    # Создаем SentenceTransformer для получения эмбеддингов
    embedder = SentenceTransformer(model_name)
    title_vector = embedder.encode(title).tolist()
    text_vector = embedder.encode(text).tolist()

    title_vector_size = len(title_vector)
    text_vector_size = len(text_vector)
    
    # Проверяем, существует ли коллекция
    if collection_name not in [col.name for col in qdrant_client.get_collections().collections]:
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config={
                "title_vector": VectorParams(size=title_vector_size, distance=Distance.COSINE),
                "text_vector": VectorParams(size=text_vector_size, distance=Distance.COSINE),
            },
        )
        print(f"Collection '{collection_name}' created successfully.")
    
    document_id = str(uuid.uuid4())
    
    # Создаем документ для вставки
    document = {
        "id": document_id,  # Уникальный идентификатор документа
        "payload": {
            "title": title,
            "text": text,
        },
        "vector": {
            "title_vector": title_vector,
            "text_vector": text_vector,
        },
    }

    # Добавляем документ в коллекцию
    qdrant_client.upsert(
        collection_name=collection_name,
        points=[document],
    )
    
    print(f"Document with ID {document_id} added to collection '{collection_name}'.")

def parse_website(url, depth=5, visited=None, max_depth=5):
    if visited is None:
        visited = set()
    if depth <= 0 or depth > max_depth or url in visited:
        return {}
    
    visited.add(url)
    headers = {'User-Agent': 'Mozilla/5.0'}  # Добавляем заголовок User-Agent
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    

    headers = {f'h{i}': [tag.text.strip() for tag in soup.find_all(f'h{i}')] for i in range(1, 4)}
    
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    
    paragraphs = [p.text.strip() for p in soup.find_all('p') if p.text.strip()]

    try:
        clear_text = ai_agent(str(paragraphs))
    except Exception as e:
        print(f"Ошибка чистки для {response.url}: {e}")

    print(url)
    print(clear_text)
    add_vector(title = str(url), text = str(clear_text))
    data = {
        'url': url,
        'headers': headers,
        'links': links,
        'text': paragraphs
    }
    
    for link in links:
        if link not in visited:
            try:
                data[link] = parse_website(link, depth - 1, visited, max_depth)
            except Exception as e:
                print(f"Ошибка коннекта для {response.url}: {e}")
    
    return data

if __name__ == "__main__":
    url = input("Введите URL: ")
    result = parse_website(url, 5)
    if result:
        print("Результат парсинга:", result)