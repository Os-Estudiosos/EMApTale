import os
from config import GET_PROJECT_PATH


class FontManager:
    """Classe responsável por armazenas o caminho de todas as fontes
    (Não carrega a fonte direto pois eu posso querer usar várias cores, tamanhos e etc.)
    """
    fonts = {
        'Game-Font': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Game-Font.ttf'),
        'Gamer': os.path.join(GET_PROJECT_PATH(), 'fonts', 'Gamer.ttf'),
        'Mettaton': os.path.join(GET_PROJECT_PATH(), 'fonts', 'mettaton-ex.ttf'),
        'VCR': os.path.join(GET_PROJECT_PATH(), 'fonts', 'VCR_OSD_MONO_1.001.ttf'),
        'Pixel': os.path.join(GET_PROJECT_PATH(), 'fonts', 'PixelOperator8.ttf'),
        'PixelB': os.path.join(GET_PROJECT_PATH(), 'fonts', 'PixelOperator8-Bold.ttf'),
    }
