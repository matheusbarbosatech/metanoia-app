# ⚡ Guia de Integração de Webhooks // METANOIA Content Studio

O **METANOIA Content Studio** possui um despachador nativo de Webhooks. Isso significa que assim que um vídeo 9:16 for renderizado (ou quando você clicar no botão "🚀 Postar" na fila), um evento JSON completo com o vídeo, legendas, título e hashtags é enviado para a sua ferramenta de automação preferida (**n8n**, **Make.com**, **Buffer**, **Zapier** ou um bot próprio de Telegram/Discord).

---

## 🎯 1. O Que o Webhook Envia (Payload JSON)

Sempre que um vídeo é disparado, o Studio envia uma requisição `POST` com cabeçalho `Content-Type: application/json` contendo:

```json
{
  "evento": "video_pronto_publicacao",
  "post_id": 1,
  "titulo": "A Primeira Vitória do Dia",
  "pilar": "Ordem Matinal das 06h",
  "roteiro": "Se a primeira coisa que você toca de manhã é a tela do celular...",
  "legenda": "A Primeira Vitória do Dia\n\n⚔️ Forja dos 90 Dias Metanoia.\nLink na bio: @forjametanoia",
  "hashtags": "#metanoia #homensdehonra #disciplina #desenvolvimentomasculino #proposito",
  "redes_alvo": ["instagram", "youtube", "tiktok"],
  "data_agendamento": "2026-09-17 06:00",
  "video": {
    "arquivo_relativo": "output/metanoia_pilar_1_ordem_matinal.mp4",
    "caminho_absoluto": "C:\\Users\\matheus\\Desktop\\metanoia-app\\output\\metanoia_pilar_1_ordem_matinal.mp4",
    "url_local": "http://localhost:8585/output/metanoia_pilar_1_ordem_matinal.mp4",
    "formato": "9:16 vertical 1080x1920",
    "fps": 30
  },
  "timestamp": "2026-09-17T02:00:00.000000"
}
```

---

## 🛠️ 2. Como Configurar no n8n (Recomendado - 100% Grátis)

1. No seu **n8n** (seja self-hosted ou cloud), crie um novo workflow.
2. Adicione o nó **Webhook**:
   - HTTP Method: `POST`
   - Path: `metanoia-postagens`
   - Response Mode: `On Received` (retorna `HTTP 200` imediatamente)
3. Copie a URL do Webhook gerada (ex: `https://seu-n8n.com/webhook/metanoia-postagens`).
4. Abra o painel do Metanoia em **http://localhost:8585/studio**, vá na **Aba 3 (Fila & Agendador)**.
5. Cole a URL no campo **Endpoint do Webhook** e clique em **Testar Conexão Agora**.
6. No n8n, conecte os nós de publicação:
   - **Nó Instagram for Business**: Publica Reels usando o link do vídeo (`{{ $json.body.video.url_local }}`) ou upload de arquivo binário com a legenda `{{ $json.body.legenda }} {{ $json.body.hashtags }}`.
   - **Nó YouTube**: Usa o nó oficial do YouTube para criar YouTube Short.
   - **Nó Telegram / WhatsApp**: Envia uma notificação para você com o vídeo e a legenda caso prefira revisar antes do post público.

> 📁 Um template pronto para importar no n8n está disponível em [`automations/metanoia_n8n_template.json`](file:///C:/Users/matheus/Desktop/metanoia-app/automations/metanoia_n8n_template.json).

---

## 🔄 3. Como Configurar no Make.com (Integromat)

1. Crie um novo Scenario no **Make.com**.
2. Adicione o módulo **Custom Webhook**:
   - Clique em **Add** e nomeie como `Metanoia Studio`.
   - Copie o link (ex: `https://hook.eu1.make.com/abc123xyz...`).
3. Cole o link no Metanoia Studio e clique em **Testar Conexão Agora**.
4. No Make, adicione os módulos:
   - **Instagram for Business -> Create a Reel**
   - **YouTube -> Upload a Video (Shorts)**
   - **TikTok for Business -> Upload a Video**

---

## ⚡ 4. Ativação do Disparo Automático 100% Hands-Free

Se você quiser que todo vídeo renderizado vá automaticamente para as redes sem precisar nem entrar na Aba 3:
1. Marque a caixinha: **[x] Disparo Automático: Enviar via Webhook imediatamente após cada renderização**.
2. Clique em **Salvar Configurações**.
3. A partir de agora, qualquer vídeo renderizado pelo estúdio ou gerado em lote dispara o webhook instantaneamente!
