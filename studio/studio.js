/* ==========================================================================
   METANOIA CONTENT STUDIO // JAVASCRIPT CONTROLLER
   ========================================================================== */

let estadoApp = {
  pilarSelecionado: "ordem_matinal",
  roteiroAtual: null,
  videoRenderizado: null,
  pilares: []
};

document.addEventListener("DOMContentLoaded", () => {
  carregarPilares();
  carregarFilaPosts();
  inicializarDataAgendamento();
  carregarConfigWebhook();
});

function switchTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-view").forEach(view => view.classList.remove("active"));

  document.getElementById(`tab-${tabId}-btn`).classList.add("active");
  document.getElementById(`view-${tabId}`).classList.add("active");
}

async function carregarPilares() {
  try {
    const res = await fetch("/api/pilares");
    if (res.ok) {
      estadoApp.pilares = await res.json();
      renderizarPilares();
    }
  } catch (e) {
    console.warn("Usando pilares padrão em cache.");
    renderizarPilaresPadrao();
  }
}

function renderizarPilaresPadrao() {
  estadoApp.pilares = [
    { id: "ordem_matinal", nome: "Ordem Matinal das 06h", icone: "🌅", foco: "Acordar sem tela, oração, banho frio e quebra da preguiça." },
    { id: "dopamina_telas", nome: "Vício em Dopamina & Celular", icone: "🧠", foco: "Cérebro frito, feed infinito, cansaço crônico e foco." },
    { id: "alianca_zap", nome: "Aliança de Honra no WhatsApp", icone: "🛡️", foco: "Fim da solidão, sabatina às 21h30, Provérbios 27:17." },
    { id: "sacerdocio_lar", nome: "Sacerdócio do Lar & Casamento", icone: "💍", foco: "Honra à esposa, liderança espiritual e exemplo aos filhos." },
    { id: "sala_emergencia", nome: "A Sala de Emergência (Anti-Porn)", icone: "⚔️", foco: "A batalha das 23h, choque vagal e teologia da graça." },
    { id: "governo_financeiro", nome: "Governo Financeiro & Fim das Bets", icone: "🪙", foco: "Fim das apostas e impulsos, trabalho duro e provisão." },
    { id: "tempera_guerreiro", nome: "A Têmpera do Guerreiro & Jejum", icone: "🔥", foco: "Jejum bíblico, disciplina militar e 1 João 2:14." }
  ];
  renderizarPilares();
}

function renderizarPilares() {
  const container = document.getElementById("pillars-container");
  if (!container) return;

  container.innerHTML = "";
  estadoApp.pilares.forEach((p, idx) => {
    const card = document.createElement("div");
    card.className = `pillar-card ${p.id === estadoApp.pilarSelecionado ? "active" : ""}`;
    card.onclick = () => selecionarPilar(p.id);
    card.innerHTML = `
      <div class="pillar-icon">${p.icone}</div>
      <div class="pillar-info">
        <strong>${p.nome}</strong>
        <span>${p.foco}</span>
      </div>
    `;
    container.appendChild(card);
  });
}

function selecionarPilar(id) {
  estadoApp.pilarSelecionado = id;
  document.querySelectorAll(".pillar-card").forEach(c => c.classList.remove("active"));
  event.currentTarget.classList.add("active");
}

async function gerarRoteiroComIA() {
  const btn = document.getElementById("btn-generate-script");
  const loading = document.getElementById("script-loading");
  const editor = document.getElementById("script-editor-container");
  const modelSelect = document.getElementById("ai-model-select").value;
  const toneSelect = document.getElementById("ai-tone-select").value;

  btn.disabled = true;
  loading.style.display = "flex";
  editor.style.opacity = "0.3";

  try {
    const res = await fetch("/api/roteiro/gerar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonPayload({
        pilar_id: estadoApp.pilarSelecionado,
        tom: toneSelect,
        modo_modelo: modelSelect
      })
    });

    if (res.ok) {
      const data = await res.json();
      estadoApp.roteiroAtual = data;
      preencherRoteiro(data);
    } else {
      alert("Erro ao conectar à API da DevWorld. Usando roteiro mestre da Forja.");
    }
  } catch (e) {
    console.error(e);
  } finally {
    btn.disabled = false;
    loading.style.display = "none";
    editor.style.opacity = "1";
  }
}

function preencherRoteiro(data) {
  document.getElementById("script-source-tag").innerText = data.fonte_ia || "DevWorld AI";
  document.getElementById("script-title-input").value = data.titulo || "";
  document.getElementById("script-hook-input").value = data.hook_3s || "";
  document.getElementById("script-text-input").value = data.texto_locucao || "";
  document.getElementById("script-caption-input").value = (data.legenda_post || "") + "\n\n" + (data.hashtags || "");

  // Tabela de Cenas
  const tbody = document.getElementById("scenes-table-body");
  tbody.innerHTML = "";
  if (data.cenas && data.cenas.length > 0) {
    data.cenas.forEach(c => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${c.tempo}</strong></td>
        <td>${c.fala}</td>
        <td>${c.visual}</td>
        <td><code>${c.broll_query_en}</code></td>
      `;
      tbody.appendChild(tr);
    });
  }

  // Preenche também a tela de vídeo
  document.getElementById("video-voice-text").value = data.texto_locucao || "";
  document.getElementById("sched-video-title").value = data.titulo || "";
}

function enviarParaEstudioVideo() {
  const texto = document.getElementById("script-text-input").value.trim();
  if (!texto) {
    alert("Gere ou escreva um roteiro primeiro!");
    return;
  }
  document.getElementById("video-voice-text").value = texto;
  switchTab("video");
}

async function iniciarRenderizacao() {
  const btn = document.getElementById("btn-render-video");
  const progress = document.getElementById("render-progress");
  const statusText = document.getElementById("render-status-text");
  const texto = document.getElementById("video-voice-text").value.trim();
  const voz = document.getElementById("voice-select").value;
  const musica = document.getElementById("music-select").value;
  const titulo = document.getElementById("script-title-input").value.trim() || "video_metanoia";

  if (!texto) {
    alert("Digite o texto da locução para renderizar!");
    return;
  }

  btn.disabled = true;
  progress.style.display = "flex";
  statusText.innerText = "⚡ Cortando B-rolls dinâmicos no Pexels e sintetizando áudio...";

  try {
    const res = await fetch("/api/video/renderizar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonPayload({
        texto: texto,
        voz: voz,
        musica: musica,
        titulo: titulo,
        pilar: estadoApp.pilarSelecionado
      })
    });

    if (res.ok) {
      const data = await res.json();
      statusText.innerText = "🎉 Vídeo concluído com sucesso!";
      
      // Atualiza o player de vídeo
      const player = document.getElementById("studio-video-player");
      const videoSrc = `/output/${data.video_arquivo}?t=${Date.now()}`;
      player.src = videoSrc;
      player.load();
      player.play();

      document.getElementById("btn-download-video").href = videoSrc;
      document.getElementById("btn-download-video").download = data.video_arquivo;

      estadoApp.videoRenderizado = data;
      document.getElementById("sched-video-title").value = titulo;
      carregarFilaPosts();
    } else {
      alert("Erro durante a renderização do vídeo.");
    }
  } catch (e) {
    console.error(e);
    alert("Erro de conexão com o servidor de renderização.");
  } finally {
    btn.disabled = false;
    setTimeout(() => { progress.style.display = "none"; }, 1500);
  }
}

function enviarParaAgendador() {
  switchTab("agenda");
}

function inicializarDataAgendamento() {
  const now = new Date();
  now.setHours(now.getHours() + 2);
  const isoStr = now.toISOString().slice(0, 16);
  const input = document.getElementById("sched-datetime");
  if (input) input.value = isoStr;
}

function setTimePreset(timeStr) {
  const [hours, minutes] = timeStr.split(":");
  const now = new Date();
  now.setHours(parseInt(hours), parseInt(minutes), 0, 0);
  if (now < new Date()) {
    now.setDate(now.getDate() + 1);
  }
  const isoStr = now.toISOString().slice(0, 16);
  document.getElementById("sched-datetime").value = isoStr;
}

async function salvarAgendamento() {
  const titulo = document.getElementById("sched-video-title").value.trim();
  const dataHora = document.getElementById("sched-datetime").value;
  const videoArquivo = estadoApp.videoRenderizado ? estadoApp.videoRenderizado.video_arquivo : "metanoia_roteiro_4_A_Alian_a_de_Honra_Ferro_.mp4";
  
  const canais = [];
  if (document.getElementById("chk-insta").checked) canais.push("instagram");
  if (document.getElementById("chk-yt").checked) canais.push("youtube");
  if (document.getElementById("chk-tiktok").checked) canais.push("tiktok");

  if (!titulo) {
    alert("Informe o título do vídeo!");
    return;
  }

  try {
    const res = await fetch("/api/posts/agendar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonPayload({
        titulo: titulo,
        pilar: estadoApp.pilarSelecionado,
        roteiro_texto: document.getElementById("video-voice-text").value,
        video_path: `output/${videoArquivo}`,
        redes: canais,
        data_agendamento: dataHora
      })
    });

    if (res.ok) {
      alert("✅ Vídeo adicionado à Esteira de Postagens com sucesso!");
      carregarFilaPosts();
    }
  } catch (e) {
    console.error(e);
  }
}

async function carregarFilaPosts() {
  try {
    const res = await fetch("/api/posts/fila");
    if (res.ok) {
      const posts = await res.json();
      renderizarFilaTabela(posts);
    }
  } catch (e) {
    console.error(e);
  }
}

function renderizarFilaTabela(posts) {
  const tbody = document.getElementById("queue-table-body");
  if (!tbody) return;
  tbody.innerHTML = "";

  if (posts.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">Nenhum post na fila no momento.</td></tr>`;
    return;
  }

  posts.forEach(p => {
    const tr = document.createElement("tr");
    
    let statusClass = "rendered";
    if (p.status === "Publicado") statusClass = "published";
    if (p.status === "Agendado") statusClass = "scheduled";

    const canaisBadges = (p.redes_destino || []).map(c => {
      if (c === "instagram") return "📸 Insta";
      if (c === "youtube") return "▶️ YT";
      if (c === "tiktok") return "🎵 TikTok";
      return c;
    }).join(" ");

    tr.innerHTML = `
      <td>#${p.id}</td>
      <td><strong>${p.titulo}</strong></td>
      <td>${p.pilar || "Geral"}</td>
      <td>${canaisBadges}</td>
      <td>${p.data_agendamento || "Hoje"}</td>
      <td><span class="status-pill ${statusClass}">${p.status}</span></td>
      <td>
        ${p.status !== "Publicado" ? `<button class="btn btn-gold" style="padding: 4px 8px; font-size: 0.75rem;" onclick="publicarAgora(${p.id})">🚀 Postar</button>` : `<a href="${p.link_publicacao || '#'}" target="_blank" style="color: #10b981; font-size: 0.75rem;">Ver Link</a>`}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function publicarAgora(id) {
  if (!confirm("Deseja despachar e publicar este vídeo nas redes agora?")) return;
  try {
    const res = await fetch(`/api/posts/publicar_agora`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: jsonPayload({ id: id })
    });
    if (res.ok) {
      const data = await res.json();
      alert(data.mensagem || "Publicado com sucesso!");
      carregarFilaPosts();
    }
  } catch (e) {
    alert("Erro ao despachar publicação.");
  }
}

function jsonPayload(obj) {
  return JSON.stringify(obj);
}

/* ==========================================================================
   WEBHOOK & AUTOMAÇÃO CONTROLLER
   ========================================================================== */

async function carregarConfigWebhook() {
  try {
    const res = await fetch("/api/config/webhook");
    if (res.ok) {
      const data = await res.json();
      const input = document.getElementById("webhook-url-input");
      const toggle = document.getElementById("webhook-auto-toggle");
      const badge = document.getElementById("webhook-badge");
      const badgeText = document.getElementById("webhook-badge-text");

      if (input) input.value = data.webhook_url || "";
      if (toggle) toggle.checked = !!data.auto_disparo;

      if (data.webhook_url) {
        badge.classList.add("active");
        badgeText.innerText = "Conectado";
      } else {
        badge.classList.remove("active");
        badgeText.innerText = "Desconectado";
      }
    }
  } catch (e) {
    console.error("Erro ao carregar webhook:", e);
  }
}

async function salvarConfigWebhook() {
  const url = document.getElementById("webhook-url-input").value.trim();
  const auto = document.getElementById("webhook-auto-toggle").checked;

  try {
    const res = await fetch("/api/config/webhook", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ webhook_url: url, auto_disparo: auto })
    });
    if (res.ok) {
      alert("✅ Configurações de Webhook salvas com sucesso!");
      carregarConfigWebhook();
    }
  } catch (e) {
    alert("Erro ao salvar configurações do Webhook.");
  }
}

async function testarConexaoWebhook() {
  const url = document.getElementById("webhook-url-input").value.trim();
  const resultBox = document.getElementById("webhook-test-result");

  if (!url) {
    alert("Informe a URL do Webhook antes de testar!");
    return;
  }

  resultBox.style.display = "block";
  resultBox.className = "webhook-result-box";
  resultBox.innerText = "Enviando sinal de teste para o Webhook...";

  try {
    const res = await fetch("/api/config/webhook/testar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ webhook_url: url })
    });
    const data = await res.json();
    if (data.sucesso) {
      resultBox.className = "webhook-result-box success";
      resultBox.innerText = `✅ Sucesso! O Webhook respondeu com status HTTP ${data.status_code}. Conexão operacional!`;
    } else {
      resultBox.className = "webhook-result-box error";
      resultBox.innerText = `❌ Falha: ${data.mensagem}`;
    }
  } catch (e) {
    resultBox.className = "webhook-result-box error";
    resultBox.innerText = `❌ Erro de requisição ao testar Webhook.`;
  }
}

