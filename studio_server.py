import os
import re
import sys
import json
import time
import asyncio
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn

# Suporte UTF-8 no terminal Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent

# Importa os serviços
sys.path.insert(0, str(BASE_DIR))
from services.content_generator_service import ContentGeneratorService
from services.social_scheduler_service import SocialSchedulerService
from scripts.gerador_videos_metanoia import (
    sintetizar_audio_e_ass,
    renderizar_video_completo,
    sanitizar_nome
)

content_service = ContentGeneratorService()
scheduler_service = SocialSchedulerService()

OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

class StudioRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Redirecionamento amigável para o Studio
        if path == "/studio" or path == "/studio/":
            self.path = "/studio/index.html"
            return super().do_GET()

        # API Endpoints
        if path == "/api/pilares":
            self._responder_json(content_service.listar_pilares())
            return

        if path == "/api/posts/fila":
            posts = scheduler_service.listar_posts()
            self._responder_json(posts)
            return

        # Arquivos estáticos normais (HTML, CSS, JS, MP4, PNG)
        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Lê o corpo JSON da requisição
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            dados = json.loads(body)
        except Exception:
            dados = {}

        # 1. Gerar Roteiro com IA (DevWorld)
        if path == "/api/roteiro/gerar":
            pilar_id = dados.get("pilar_id", "ordem_matinal")
            tom = dados.get("tom", "Confrontador e Sóbrio")
            modo = dados.get("modo_modelo", "alta_velocidade")
            
            roteiro = content_service.gerar_roteiro_ia(pilar_id, tom, modo)
            self._responder_json(roteiro)
            return

        # 2. Renderizar Vídeo em 9:16
        if path == "/api/video/renderizar":
            texto = dados.get("texto", "").strip()
            voz = dados.get("voz", "1")
            titulo = dados.get("titulo", "video_metanoia")
            pilar = dados.get("pilar", "Geral")

            if not texto:
                self._responder_json({"sucesso": False, "mensagem": "Texto não fornecido."}, status=400)
                return

            prefixo = f"studio_{sanitizar_nome(titulo)[:25]}_{int(time.time())}"
            temp_audio = OUTPUT_DIR / f"{prefixo}_audio.mp3"
            temp_ass = OUTPUT_DIR / f"{prefixo}_legendas.ass"
            video_final = OUTPUT_DIR / f"{prefixo}.mp4"

            try:
                # 1. Sintetiza áudio e gera legendas ASS
                duracao = asyncio.run(sintetizar_audio_e_ass(texto, temp_audio, temp_ass, voz_chave=voz))

                # 2. Renderiza vídeo com cortes a cada 2.5s e trilha sonora
                sucesso = renderizar_video_completo(temp_audio, temp_ass, video_final, duracao)

                if sucesso:
                    # Adiciona automaticamente à fila do SQLite como Renderizado
                    scheduler_service.adicionar_post(
                        titulo=titulo,
                        pilar=pilar,
                        roteiro_texto=texto,
                        video_path=f"output/{video_final.name}",
                        status="Renderizado"
                    )

                    self._responder_json({
                        "sucesso": True,
                        "video_arquivo": video_final.name,
                        "duracao": duracao,
                        "mensagem": "Vídeo renderizado com sucesso!"
                    })
                else:
                    self._responder_json({"sucesso": False, "mensagem": "Falha no FFmpeg."}, status=500)
            except Exception as e:
                self._responder_json({"sucesso": False, "mensagem": str(e)}, status=500)
            return

        # 3. Agendar Postagem
        if path == "/api/posts/agendar":
            titulo = dados.get("titulo", "Novo Vídeo")
            pilar = dados.get("pilar", "Geral")
            texto = dados.get("roteiro_texto", "")
            video_path = dados.get("video_path", "")
            redes = dados.get("redes", ["instagram", "youtube", "tiktok"])
            data_agendamento = dados.get("data_agendamento")

            pid = scheduler_service.adicionar_post(
                titulo=titulo,
                pilar=pilar,
                roteiro_texto=texto,
                video_path=video_path,
                redes=redes,
                data_agendamento=data_agendamento,
                status="Agendado"
            )
            self._responder_json({"sucesso": True, "id": pid, "mensagem": "Post agendado na fila com sucesso!"})
            return

        # 4. Publicar Agora
        if path == "/api/posts/publicar_agora":
            pid = dados.get("id")
            if not pid:
                self._responder_json({"sucesso": False, "mensagem": "ID do post não fornecido."}, status=400)
                return

            res = scheduler_service.publicar_agora(int(pid))
            self._responder_json(res)
            return

        self._responder_json({"erro": "Rota não encontrada"}, status=404)

    def _responder_json(self, dados, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(dados, ensure_ascii=False).encode("utf-8"))

def main():
    porta = 8585
    server_address = ("", porta)
    httpd = ThreadedHTTPServer(server_address, StudioRequestHandler)
    print("=" * 68)
    print(f"⚔️  METANOIA CONTENT STUDIO // SERVIDOR ATIVO NA PORTA {porta}")
    print("=" * 68)
    print(f"👉 Painel do Studio:    http://localhost:{porta}/studio")
    print(f"👉 Landing Page & Pix:  http://localhost:{porta}")
    print("Pressione Ctrl+C para encerrar o servidor.")
    print("=" * 68)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    main()
