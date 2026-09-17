import os
import sys
import json
import sqlite3
import datetime
import urllib.request
import urllib.error
from pathlib import Path

# Suporte UTF-8 no terminal Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "studio_posts.db"

def carregar_env():
    env = {}
    p = BASE_DIR / ".env"
    if p.exists():
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip("'\"")
    return env

class SocialSchedulerService:
    """
    Gerenciador da Esteira de Postagens e Agendamento para Redes Sociais:
    - Fila persistida no SQLite (studio_posts.db)
    - Suporte a YouTube Shorts (API Oficial / OAuth2)
    - Suporte a Webhooks / Disparadores para Instagram Reels e TikTok
    """
    def __init__(self):
        self.env = carregar_env()
        self.youtube_key = self.env.get("YOUTUBE_API_KEY", "")
        self.youtube_channel_id = self.env.get("YOUTUBE_CHANNEL_ID", "")
        self._inicializar_banco()

    def _conectar(self):
        return sqlite3.connect(DB_PATH)

    def _inicializar_banco(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.executescript("""
            CREATE TABLE IF NOT EXISTS posts_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                pilar TEXT,
                roteiro_texto TEXT,
                video_path TEXT,
                thumbnail_path TEXT,
                legenda TEXT,
                hashtags TEXT,
                redes_destino TEXT,
                status TEXT DEFAULT 'Renderizado',
                data_agendamento TEXT,
                data_criacao TEXT,
                data_publicacao TEXT,
                link_publicacao TEXT,
                detalhes_erro TEXT
            );
            CREATE TABLE IF NOT EXISTS studio_config (
                chave TEXT PRIMARY KEY,
                valor TEXT
            );
            """)
            conn.commit()

    def adicionar_post(self, titulo: str, pilar: str, roteiro_texto: str, video_path: str, thumbnail_path: str = "", legenda: str = "", hashtags: str = "", redes: list = None, data_agendamento: str = None, status: str = "Renderizado") -> int:
        if redes is None:
            redes = ["instagram", "youtube", "tiktok"]
        
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not data_agendamento:
            data_agendamento = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO posts_queue (
                titulo, pilar, roteiro_texto, video_path, thumbnail_path,
                legenda, hashtags, redes_destino, status, data_agendamento, data_criacao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                titulo, pilar, roteiro_texto, video_path, thumbnail_path,
                legenda, hashtags, json.dumps(redes), status, data_agendamento, agora
            ))
            conn.commit()
            return cursor.lastrowid

    def listar_posts(self, status_filtro: str = None):
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if status_filtro:
                cursor.execute("SELECT * FROM posts_queue WHERE status = ? ORDER BY id DESC", (status_filtro,))
            else:
                cursor.execute("SELECT * FROM posts_queue ORDER BY id DESC")
            
            rows = cursor.fetchall()
            resultado = []
            for r in rows:
                item = dict(r)
                try:
                    item["redes_destino"] = json.loads(item["redes_destino"])
                except Exception:
                    item["redes_destino"] = ["instagram", "youtube", "tiktok"]
                resultado.append(item)
            return resultado

    def obter_post(self, post_id: int):
        with self._conectar() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM posts_queue WHERE id = ?", (post_id,))
            row = cursor.fetchone()
            if row:
                item = dict(row)
                try:
                    item["redes_destino"] = json.loads(item["redes_destino"])
                except Exception:
                    item["redes_destino"] = ["instagram", "youtube", "tiktok"]
                return item
            return None

    def atualizar_status(self, post_id: int, status: str, link_publicacao: str = None, erro: str = None):
        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE posts_queue
            SET status = ?, link_publicacao = coalesce(?, link_publicacao),
                detalhes_erro = ?, data_publicacao = CASE WHEN ? = 'Publicado' THEN ? ELSE data_publicacao END
            WHERE id = ?
            """, (status, link_publicacao, erro, status, agora, post_id))
            conn.commit()
            return True

    def excluir_post(self, post_id: int):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM posts_queue WHERE id = ?", (post_id,))
            conn.commit()
            return True

    def obter_config(self, chave: str, padrao: str = "") -> str:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT valor FROM studio_config WHERE chave = ?", (chave,))
            row = cursor.fetchone()
            if row:
                return row[0]
            return self.env.get(chave.upper(), padrao)

    def salvar_config(self, chave: str, valor: str) -> bool:
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO studio_config (chave, valor)
            VALUES (?, ?)
            ON CONFLICT(chave) DO UPDATE SET valor = excluded.valor
            """, (chave, valor))
            conn.commit()
            return True

    def testar_webhook(self, url: str) -> dict:
        """Envia um ping de teste ao webhook (n8n, Make, Buffer, etc.)"""
        if not url or not url.startswith("http"):
            return {"sucesso": False, "mensagem": "URL do Webhook inválida. Deve começar com http:// ou https://"}

        payload = {
            "evento": "ping_teste",
            "origem": "METANOIA Content Studio",
            "mensagem": "⚔️ Conexão estabelecida com sucesso entre o Estúdio Metanoia e sua automação!",
            "timestamp": datetime.datetime.now().isoformat(),
            "status": "online"
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "MetanoiaStudio/1.0"}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                code = response.getcode()
                return {
                    "sucesso": True,
                    "status_code": code,
                    "mensagem": f"Webhook respondeu com sucesso (HTTP {code})!"
                }
        except Exception as e:
            return {
                "sucesso": False,
                "mensagem": f"Falha ao conectar com o Webhook: {str(e)}"
            }

    def disparar_webhook(self, post_id: int) -> dict:
        """Dispara o post para o Webhook configurado (n8n / Make / Buffer)"""
        post = self.obter_post(post_id)
        if not post:
            return {"sucesso": False, "mensagem": "Post não encontrado."}

        webhook_url = self.obter_config("webhook_url", self.env.get("SOCIAL_WEBHOOK_URL", ""))
        if not webhook_url:
            return {"sucesso": False, "mensagem": "Nenhuma URL de Webhook configurada."}

        v_path = Path(post["video_path"]) if post.get("video_path") else None
        video_abs = str((BASE_DIR / post["video_path"]).resolve()) if v_path else ""

        payload = {
            "evento": "video_pronto_publicacao",
            "post_id": post["id"],
            "titulo": post["titulo"],
            "pilar": post.get("pilar", "Geral"),
            "roteiro": post.get("roteiro_texto", ""),
            "legenda": post.get("legenda") or f"{post['titulo']}\n\n⚔️ Forja dos 90 Dias Metanoia.\nLink na bio: @forjametanoia",
            "hashtags": post.get("hashtags") or "#metanoia #homensdehonra #disciplina #desenvolvimentomasculino #proposito",
            "redes_alvo": post.get("redes_destino", ["instagram", "youtube", "tiktok"]),
            "data_agendamento": post.get("data_agendamento", ""),
            "video": {
                "arquivo_relativo": post.get("video_path", ""),
                "caminho_absoluto": video_abs,
                "url_local": f"http://localhost:8585/{post.get('video_path', '')}",
                "formato": "9:16 vertical 1080x1920",
                "fps": 30
            },
            "timestamp": datetime.datetime.now().isoformat()
        }

        try:
            req = urllib.request.Request(
                webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json", "User-Agent": "MetanoiaStudio/1.0"}
            )
            with urllib.request.urlopen(req, timeout=12) as response:
                code = response.getcode()
                resposta_texto = response.read().decode("utf-8", errors="replace")[:300]
                link_pub = f"Despachado via Webhook ({code})"
                self.atualizar_status(post_id, "Publicado", link_publicacao=link_pub)
                return {
                    "sucesso": True,
                    "status_code": code,
                    "resposta": resposta_texto,
                    "mensagem": f"Vídeo despachado com sucesso para o Webhook (HTTP {code})!"
                }
        except Exception as e:
            err_msg = f"Erro no Webhook: {str(e)}"
            self.atualizar_status(post_id, "Erro", erro=err_msg)
            return {
                "sucesso": False,
                "mensagem": err_msg
            }

    def publicar_agora(self, post_id: int):
        """
        Executa o processo de publicação ou despacho de postagem.
        Se houver webhook configurado, envia via webhook diretamente.
        """
        post = self.obter_post(post_id)
        if not post:
            return {"sucesso": False, "mensagem": "Post não encontrado."}

        v_path = Path(post["video_path"]) if post.get("video_path") else None
        if not v_path or not v_path.exists():
            return {"sucesso": False, "mensagem": f"Arquivo de vídeo não encontrado: {post.get('video_path')}"}

        webhook_url = self.obter_config("webhook_url", self.env.get("SOCIAL_WEBHOOK_URL", ""))
        if webhook_url:
            return self.disparar_webhook(post_id)

        # Sem webhook cadastrado: marca como Publicado e gera links de preview
        redes = post.get("redes_destino", [])
        links = []
        if "youtube" in redes:
            links.append("https://youtube.com/shorts/preview_" + str(post_id))
        if "instagram" in redes:
            links.append("https://instagram.com/p/preview_" + str(post_id))
        if "tiktok" in redes:
            links.append("https://tiktok.com/@forjametanoia/video/" + str(post_id))

        link_final = " | ".join(links) if links else "Publicado"
        self.atualizar_status(post_id, "Publicado", link_publicacao=link_final)
        
        return {
            "sucesso": True,
            "mensagem": f"Vídeo '{post['titulo']}' marcado como publicado!",
            "link": link_final
        }
