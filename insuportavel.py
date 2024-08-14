import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# Caminho para a imagem de fundo
background_image_path = "WhatsApp Image 2024-08-13 at 23.33.22.jpeg"

# Custom CSS styling para adicionar a imagem de fundo e estilizar o botão de download
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
    /* Manter a barra superior invisível */
    header {{visibility: hidden;}}
    body {{
        background-image: url('data:image/jpeg;base64,{base64.b64encode(open(background_image_path, "rb").read()).decode()}');
        background-size: cover;
        font-family: 'Montserrat', sans-serif;
        color: #FFFFFF;
    }}
    .stApp {{
        background: rgba(0, 0, 0, 0.7); /* Fundo escuro com transparência */
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px); /* Efeito de desfoque */
    }}
    h1 {{
        color: #f4f4f4;
        font-size: 3.5em;
        text-align: center;
        margin-bottom: 0.5em;
        text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.5);
    }}
    .welcome-message {{
        background-color: rgba(0, 0, 0, 0.7);
        color: white; /* Define todas as linhas como brancas */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        margin-bottom: 30px;
        animation: fadeIn 2s ease-in-out;
    }}
    h2 {{
        color: #EAEAEA; /* Título em branco suave */
        font-weight: 700;
    }}
    p {{
        color: #EAEAEA; /* Parágrafo em branco suave */
        font-size: 1.1em;
    }}
    .stButton>button {{
        background-color: #4CAF50;
        color: white;
        font-size: 1.3em;
        padding: 12px 24px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    .stButton>button:hover {{
        background-color: #45a049;
        transform: scale(1.05);
        color: black;
    }}
    .stDownloadButton > button {{
        background-color: white !important;
        color: black !important;
        font-size: 1.3em !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        border: none !important;
        cursor: pointer !important;
        transition: background-color 0.3s ease, transform 0.3s ease !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: #EAEAEA !important;
        color: black !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
    }}
    .stTextInput>div>div>input {{
        border: 2px solid #4CAF50;
        padding: 12px;
        border-radius: 10px;
        font-size: 1.2em;
        transition: border-color 0.3s ease;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: #45a049;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    }}
    .footer {{
        text-align: center;
        margin-top: 50px;
        color: #EAEAEA;
        font-size: 1.1em;
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    </style>
""", unsafe_allow_html=True)

# Mensagem de boas-vindas e propósito do projeto
st.markdown("""
<div class="welcome-message">
    <h2>Bem-vindo ao Criador de Paletas Personalizadas!</h2>
    <p>Com esta ferramenta, você pode criar suas próprias paletas de cores únicas. Insira os códigos HEX das suas cores favoritas,
    gere a paleta e até mesmo baixe-a como um arquivo PNG para seus projetos. Deixe sua criatividade brilhar!</p>
</div>
""", unsafe_allow_html=True)

# Função para plotar a paleta
def plot_palette(hex_colors):
    num_colors = len(hex_colors)
    width = 100 * num_colors
    height = 150  # Altura aumentada para acomodar o texto
    palette_image = Image.new('RGB', (width, height), "white")

    draw = ImageDraw.Draw(palette_image)

    # Carregar uma fonte padrão
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    for i, color in enumerate(hex_colors):
        # Desenhar o bloco de cor
        draw.rectangle([i * 100, 0, (i + 1) * 100, 100], fill=color)
        # Calcular a posição para centralizar o texto
        text_bbox = draw.textbbox((0, 0), color, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_position = ((i * 100) + (50 - text_width / 2), 110)
        draw.text(text_position, color, fill="black", font=font)

    return palette_image

# Entrada do usuário
st.title("Crie Sua Paleta")
user_input = st.text_input("Insira as cores para sua paleta (códigos HEX separados por vírgula):", "#FF5733, #33FF57, #3357FF")

if st.button("Gerar Paleta"):
    hex_colors = [color.strip() for color in user_input.split(',')]
    palette_image = plot_palette(hex_colors)
    
    # Exibir a paleta gerada na aplicação
    st.image(palette_image)
    st.write(f"Paleta Gerada: {hex_colors}")
    
    # Salvar a imagem em um objeto BytesIO
    buf = io.BytesIO()
    palette_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # Fornecer um botão de download estilizado com texto em preto e fundo branco
    st.download_button(
        label="Baixar Paleta como PNG",
        data=byte_im,
        file_name="paleta.png",
        mime="image/png"
    )

# Mensagem de rodapé
st.markdown("""
<div class="footer">
    <p>Criado com ❤ para a Beatriz.</p>
</div>
""", unsafe_allow_html=True)
