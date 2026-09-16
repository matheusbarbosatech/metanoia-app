"""
Configurações Globais e Constantes do METANOIA.
"""
from pathlib import Path

APP_NAME = "METANOIA"
APP_TAGLINE = "Ordem Interior. Honra Diária. Comunhão no Secreto."
APP_VERSION = "1.0.0"

# Caminhos
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "metanoia.db"

# Faixa Etária e Posicionamento
TARGET_AUDIENCE = "Homens de 18 a 35 anos"
TARGET_PILLARS = [
    "01. A Ordem Matinal (Protocolo 7 Minutos)",
    "02. A Sentinela (Protocolo SOS Anti-Recaída)",
    "03. A Aliança (Pacto de Honra 1-to-1)",
    "04. O Conselheiro (Neurociência & Graça)"
]
