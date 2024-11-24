#Criando um Tradutor Usando OpenAI e Azure

!pip install requests beautifulsoup4 openai langchain-openai
import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')
      for script_or_style in soup(["script", "style"]):
          script_or_style.decompose()
          texto = soup.get_text(separator= ' ')
          #limpar texto
          linhas = (line.strip() for line in texto.splitlines())
          parts = (phrase.strip() for line in linhas for phrase in line.split("  "))
          texto_limpo = '\n'.join(chunk for chunk in parts if chunk)
          return texto_limpo
    else:
        print(f"Failed to fetch URL: {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    return text

from langchain_openai.chat_models.azure import AzureChatOpenAI

##Adicione as credenciais do azure aqui:##

Client = AzureChatOpenAI(
    azure_endpoint= "",
    api_key= "",
    api_version= "",
    deployment_name= "",
    max_retries=0
)

def translate_article(text, lang):
  messages = [
      ("system",  "Você atua como tradutor de textos"),
      ("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
  ]

response = client.invoke(messages)
print(response.content)
return response.content

###Adicione a URL do artigo que você quer traduzir aqui:###

url = ''
text = extract_text_from_url(url)
article = translate_article(text, "pt-br")
print(article)
