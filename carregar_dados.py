from pathlib import Path
from database import cliente_supabase
from rag import criar_embedding

CAMINHO = Path(__file__).parent / "docs" / "conhecimento.txt"

def ler_documentos():
    texto = CAMINHO.read_text(encoding="utf-8")
    for bloco in texto.split("\n# "):
        bloco = bloco.strip().removeprefix("# ")
        if not bloco:
            continue
        titulo, separador, conteudo = bloco.partition("\n")
        if separador and conteudo.strip():
            yield titulo.strip(), conteudo.strip()

def main():
    banco = cliente_supabase()
    total = 0
    for titulo, conteudo in ler_documentos():
        banco.table("documentos_lumina").upsert(
            {"titulo": titulo, "conteudo": conteudo, "embedding": criar_embedding(conteudo)},
            on_conflict="titulo,conteudo"
        ).execute()
        total += 1
        print(f"[OK] {titulo}")
    print(f"\n{total} documentos enviados ao Supabase.")

if __name__ == "__main__":
    main()
