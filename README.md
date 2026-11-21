# ✦ Lúmina — Assistente Virtual Acadêmico

Projeto desenvolvido por **Ronald Machado**, na disciplina **Projeto de Banco de Dados**, ministrada pelo professor **Anderson Soares**.

## Sobre o projeto

A Lúmina é uma assistente virtual que ajuda estudantes a consultar informações sobre matrícula, avaliações, biblioteca e documentos acadêmicos. Ela utiliza uma base própria de conhecimento, armazenada no Supabase, e o Gemini para formular respostas a partir das informações recuperadas.

Os conteúdos acadêmicos incluídos são **fictícios e usados apenas na demonstração**.

## Tecnologias

- Python e Streamlit: aplicação e interface.
- Supabase (PostgreSQL + pgvector): armazenamento e busca por similaridade.
- SentenceTransformers (`all-MiniLM-L6-v2`): embeddings de 384 dimensões.
- Google AI Studio / Gemini: geração das respostas contextualizadas.

## Como funciona o RAG

1. O arquivo `docs/conhecimento.txt` contém os textos da base de conhecimento.
2. `carregar_dados.py` transforma cada texto em embedding e o salva no Supabase.
3. Quando o usuário faz uma pergunta, `rag.py` gera o embedding dessa pergunta.
4. O Supabase executa a função `buscar_documentos_lumina`, ordenando os resultados pela similaridade do cosseno.
5. O Gemini recebe a pergunta e os trechos recuperados e gera a resposta.
6. A interface mostra a resposta e permite conferir os documentos encontrados e suas similaridades.

## Como executar

### 1. Baixar e preparar o projeto

Clone o repositório ou extraia o ZIP e abra a pasta no VS Code.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se a ativação estiver bloqueada no PowerShell, use diretamente `.\.venv\Scripts\python.exe` e `.\.venv\Scripts\streamlit.exe` nos comandos seguintes.

### 2. Criar o banco no Supabase

Crie um projeto no [Supabase](https://supabase.com/). Abra **SQL Editor**, copie o conteúdo de `docs/banco.sql` e execute. O script ativa o pgvector, cria a tabela e a função de busca.

### 3. Configurar as chaves

Crie uma chave no [Google AI Studio](https://aistudio.google.com/apikey). No Supabase, abra as configurações de API do projeto e copie a URL e uma **chave de servidor `service_role`** (ou a chave secreta equivalente com acesso ao banco). Nunca publique essa chave.

No terminal:

```powershell
Copy-Item .env.example .env
```

Edite `.env` com suas próprias credenciais. O arquivo está no `.gitignore` e não deve ser enviado ao GitHub. A aplicação foi projetada para execução local com chave de servidor; não publique essa chave em aplicações client-side.

### 4. Inserir os documentos

```powershell
python carregar_dados.py
```

O primeiro uso pode baixar o modelo de embeddings. Confira no Supabase se a tabela `documentos_lumina` recebeu os seis documentos.

### 5. Iniciar a interface

```powershell
streamlit run app.py
```

Abra o endereço local mostrado no terminal, normalmente `http://localhost:8501`.

## Testes sugeridos

- **Como faço para renovar minha matrícula?** — deve recuperar o conteúdo de Matrículas.
- **Como posso pegar livros emprestados?** — deve recuperar Biblioteca.
- **Onde solicito declaração de matrícula?** — deve recuperar Documentos.
- **Qual é o telefone da secretaria?** — não deve inventar um número inexistente na base.

Abra **Fontes recuperadas** abaixo das respostas para demonstrar o resultado da busca semântica e o valor de similaridade.

## Personalização dos dados

Edite `docs/conhecimento.txt` mantendo cada assunto iniciado por `# Título`. Execute novamente `python carregar_dados.py` para enviar conteúdos novos. Registros antigos não são apagados automaticamente: se substituir um conteúdo, remova a versão antiga no Supabase para evitar duplicidades. Para documentos maiores, é recomendável dividir o texto em trechos antes de gerar embeddings.

## Capturas de tela

Adicione as imagens na pasta `docs/` e substitua os caminhos abaixo pelos nomes utilizados.

**Tela inicial**

<!-- Adicione aqui: ![Tela inicial](docs/tela-inicial.png) -->

**Conversa com o assistente**

<!-- Adicione aqui: ![Conversa](docs/conversa.png) -->

**Consulta vetorial no Supabase**

<!-- Adicione aqui: ![Supabase](docs/supabase.png) -->

## Vídeo demonstrativo

**Link do vídeo:** [Adicionar link aqui](https://example.com)

No vídeo, apresentar a interface, uma pergunta, os documentos recuperados com similaridade, a resposta do Gemini e a tabela vetorial no Supabase.

## Repositório

**GitHub:** [Adicionar link do repositório aqui](https://github.com/)

## Observações

O Gemini precisa de conexão com a internet e de uma chave de API válida. O acesso pode estar sujeito a limites e custos do provedor. Este projeto não utiliza n8n, portanto não reivindica o bônus opcional.
