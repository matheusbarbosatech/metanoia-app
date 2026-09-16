import os
import sys
import json
import urllib.parse
import urllib.request
from pathlib import Path

# Suporte UTF-8 no Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
VIDEOS_DIR = BASE_DIR / "assets" / "videos_fundo"

def carregar_env():
    """Carrega variáveis do arquivo .env sem expor segredos"""
    env = {}
    p = BASE_DIR / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

class VideoBankService:
    """
    Serviço unificado de Banco de Vídeos Cinemáticos:
    - Pexels API (Clipes 4K/HD ultrarrealistas)
    - Pixabay API (Backup com clipes HD gratuitos)
    """
    def __init__(self):
        self.env = carregar_env()
        self.pexels_key = self.env.get("PEXELS_API_KEY", "")
        self.pixabay_key = self.env.get("PIXABAY_API_KEY", "")
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    def listar_videos_locais(self):
        """Retorna lista de vídeos já baixados e prontos em assets/videos_fundo/"""
        return list(VIDEOS_DIR.glob("*.mp4"))

    def baixar_do_pexels(self, termo: str, min_duracao: int = 15) -> Path:
        """Busca e baixa vídeo em alta definição da Pexels API"""
        if not self.pexels_key:
            return None

        query = urllib.parse.quote(termo)
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=8&orientation=portrait"
        
        # Se não achar em portrait, busca geral
        for orient in ["orientation=portrait", ""]:
            sep = "&" if orient else ""
            req_url = f"https://api.pexels.com/videos/search?query={query}&per_page=8{sep}{orient}"
            headers = {
                "Authorization": self.pexels_key,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }
            try:
                req = urllib.request.Request(req_url, headers=headers)
                with urllib.request.urlopen(req, timeout=12) as resp:
                    if resp.status != 200:
                        continue
                    data = json.loads(resp.read().decode("utf-8"))
                    videos = data.get("videos", [])
                    if not videos:
                        continue

                    # Filtra por duração
                    candidatos = [v for v in videos if v.get("duration", 0) >= min_duracao]
                    alvo = candidatos[0] if candidatos else videos[0]
                    v_id = alvo["id"]
                    
                    dest_file = VIDEOS_DIR / f"pexels_{v_id}_{termo.replace(' ', '_')}.mp4"
                    if dest_file.exists() and dest_file.stat().st_size > 100_000:
                        print(f"  ✅ [Pexels] Vídeo já em cache: {dest_file.name}")
                        return dest_file

                    # Escolhe arquivo HD ou UHD
                    arquivos = alvo.get("video_files", [])
                    # Prioriza HD (1080p ou 720p vertical)
                    hd_files = [f for f in arquivos if f.get("width", 0) >= 1080 or f.get("height", 0) >= 1080]
                    escolhido = hd_files[0] if hd_files else (arquivos[0] if arquivos else None)
                    
                    if not escolhido or not escolhido.get("link"):
                        continue

                    download_url = escolhido["link"]
                    print(f"  📥 [Pexels] Baixando ID {v_id} ({escolhido.get('width')}x{escolhido.get('height')}, {alvo.get('duration')}s)...")
                    
                    dl_req = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(dl_req, timeout=30) as dl_resp, open(dest_file, "wb") as f_out:
                        f_out.write(dl_resp.read())

                    print(f"  🎉 [Pexels] Salvo: {dest_file.name} ({dest_file.stat().st_size / (1024*1024):.2f} MB)")
                    return dest_file
            except Exception as e:
                # Continua para fallback
                pass

        return None

    def baixar_do_pixabay(self, termo: str, min_duracao: int = 15) -> Path:
        """Busca e baixa vídeo em alta definição do Pixabay"""
        if not self.pixabay_key:
            return None

        termo_busca = urllib.parse.quote(termo)
        url = f"https://pixabay.com/api/videos/?key={self.pixabay_key}&q={termo_busca}&video_type=film&per_page=10"
        
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                hits = data.get("hits", [])
                if not hits:
                    return None

                bons = [h for h in hits if h.get("duration", 0) >= min_duracao]
                alvo = bons[0] if bons else hits[0]
                video_id = alvo["id"]
                dest_file = VIDEOS_DIR / f"pixabay_{video_id}_{termo.replace(' ', '_')}.mp4"

                if dest_file.exists() and dest_file.stat().st_size > 100_000:
                    print(f"  ✅ [Pixabay] Vídeo já em cache: {dest_file.name}")
                    return dest_file

                streams = alvo.get("videos", {})
                stream = streams.get("large") or streams.get("medium") or streams.get("small")
                if not stream or not stream.get("url"):
                    return None

                print(f"  📥 [Pixabay] Baixando ID {video_id} ({stream.get('width')}x{stream.get('height')}, {alvo.get('duration')}s)...")
                v_req = urllib.request.Request(stream["url"], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(v_req, timeout=30) as v_resp, open(dest_file, "wb") as f_out:
                    f_out.write(v_resp.read())

                print(f"  🎉 [Pixabay] Salvo: {dest_file.name} ({dest_file.stat().st_size / (1024*1024):.2f} MB)")
                return dest_file
        except Exception as e:
            return None

    def obter_video_para_tema(self, tema: str = "blacksmith") -> Path:
        """
        Obtém vídeo adequado:
        1. Tenta baixar clipe de alta qualidade do Pexels
        2. Tenta Pixabay se Pexels falhar
        3. Recorre aos vídeos locais em cache
        """
        print(f"🔍 Buscando clipe cinemático para o tema '{tema}'...")
        
        # 1. Pexels
        v = self.baixar_do_pexels(tema)
        if v and v.exists():
            return v
            
        # 2. Pixabay
        v = self.baixar_do_pixabay(tema)
        if v and v.exists():
            return v

        # 3. Cache local existente
        locais = self.listar_videos_locais()
        if locais:
            print(f"  🔄 Usando clipe existente do acervo local: {locais[0].name}")
            return locais[0]

        return None
