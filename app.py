
from pathlib import Path
import streamlit as st
from rag import responder

st.set_page_config(
    page_title="Lúmina | Assistente IA",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

caminho_css = Path(__file__).parent / "assets" / "style.css"

with open(caminho_css, encoding="utf-8") as arquivo:
    st.markdown(
        f"<style>{arquivo.read()}</style>",
        unsafe_allow_html=True
    )

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []


def mostrar_fontes(fontes):
    if not fontes:
        return

    with st.expander("🔎 Fontes recuperadas | Busca vetorial"):
        for documento in fontes:
            titulo = documento.get("titulo", "Documento")
            conteudo = documento.get("conteudo", "")
            similaridade = documento.get("similaridade")

            st.markdown(f"**📄 {titulo}**")

            if similaridade is not None:
                st.caption(
                    f"Similaridade semântica: {float(similaridade):.1%}"
                )

            st.write(conteudo)
            st.divider()


# Barra lateral
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="brand-icon">✦</div>
            <div class="brand-title">Lúmina<span>.</span></div>
            <div class="brand-description">
                Inteligência que ilumina ideias.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">SEU ESPAÇO</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-nav">
            <div class="nav-active">
                <span>✧</span> Assistente inteligente
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-section">CONVERSA</div>',
        unsafe_allow_html=True
    )

    if st.button(
        "＋ Nova conversa",
        use_container_width=True,
        key="nova_conversa"
    ):
        st.session_state.mensagens = []
        st.rerun()

    st.markdown(
        """
        <div class="sidebar-bottom">
            <div class="sidebar-info-icon">✦</div>
            <div>
                <div class="sidebar-info-title">Lúmina AI</div>
                <div class="sidebar-info-text">
                    Conhecimento e inteligência em um só lugar.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# Apresentação
st.markdown(
    """
    <div class="hero">
        <div class="hero-glow"></div>
        <div class="hero-content">
            <div class="hero-label">
                <span class="hero-dot"></span>
                SEU ESPAÇO INTELIGENTE
            </div>
            <h1>Olá, eu sou a <span>Lúmina.</span> ✦</h1>
            <p>
                Sua assistente de inteligência artificial.
                Explore ideias, tire dúvidas e encontre
                respostas de um jeito simples e inteligente.
            </p>
        </div>
        <div class="hero-decoration">✳</div>
    </div>
    """,
    unsafe_allow_html=True
)


# Cartões de apresentação
col1, col2, col3 = st.columns(3, gap="medium")

cartoes = [
    (
        col1,
        "✦",
        "Inteligência artificial",
        "Converse, explore assuntos e encontre novas respostas.",
        "purple"
    ),
    (
        col2,
        "◈",
        "Conhecimento conectado",
        "Informações acadêmicas recuperadas de uma base própria.",
        "yellow"
    ),
    (
        col3,
        "⌕",
        "Busca inteligente",
        "Pesquisa semântica para encontrar conteúdos relevantes.",
        "mint"
    )
]

for coluna, simbolo, titulo, descricao, cor in cartoes:
    with coluna:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-icon {cor}">
                    {simbolo}
                </div>
                <div class="feature-title">{titulo}</div>
                <div class="feature-description">{descricao}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# Área de conversa
st.markdown(
    """
    <div class="chat-heading">
        <div>
            <div class="chat-kicker">CONVERSE COM A IA</div>
            <h2>Como posso ajudar?</h2>
            <p>
                Pergunte o que quiser ou explore
                informações da base de conhecimento.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# Sugestões iniciais
if not st.session_state.mensagens:
    st.markdown(
        '<div class="suggestions-title">Experimente perguntar</div>',
        unsafe_allow_html=True
    )

    sugestoes = [
        "O que é inteligência artificial?",
        "Como faço para renovar minha matrícula?",
        "Como funciona o empréstimo de livros?"
    ]

    colunas = st.columns(3, gap="small")

    for coluna, sugestao in zip(colunas, sugestoes):
        with coluna:
            if st.button(
                sugestao,
                use_container_width=True,
                key=f"sugestao_{sugestao}"
            ):
                st.session_state.pergunta_sugerida = sugestao
                st.rerun()


# Histórico de mensagens
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["papel"]):
        st.markdown(mensagem["texto"])
        mostrar_fontes(mensagem.get("fontes", []))


# Entrada de perguntas
pergunta_digitada = st.chat_input(
    "Pergunte qualquer coisa à Lúmina..."
)

pergunta_sugerida = st.session_state.pop(
    "pergunta_sugerida", None
)

pergunta = pergunta_digitada or pergunta_sugerida

if pergunta:
    st.session_state.mensagens.append(
        {
            "papel": "user",
            "texto": pergunta,
            "fontes": []
        }
    )

    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        fontes = []

        with st.spinner("Lúmina está pensando..."):
            try:
                texto, fontes = responder(pergunta)

            except Exception as erro:
                texto = (
                    "Não consegui responder agora. "
                    "Verifique a conexão e tente novamente."
                )

                st.error(
                    f"Erro na consulta: {type(erro).__name__}"
                )
                st.exception(erro)

        st.markdown(texto)
        mostrar_fontes(fontes)

    st.session_state.mensagens.append(
        {
            "papel": "assistant",
            "texto": texto,
            "fontes": fontes
        }
    )
