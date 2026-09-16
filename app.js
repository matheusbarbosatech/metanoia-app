// METANOIA — Interações da Landing Page, Simulador SOS e Engrenagem de Vendas Pix

// 1. FAQ Accordion
document.querySelectorAll('.faq-question').forEach(q => {
  q.addEventListener('click', () => {
    const item = q.parentElement;
    item.classList.toggle('active');
    const span = q.querySelector('span');
    span.textContent = item.classList.contains('active') ? '−' : '+';
  });
});

// 2. Simulador Interativo do Protocolo SOS
let timerInterval = null;
let secondsLeft = 180;
const timerEl = document.getElementById('demo-timer');
const instructionEl = document.getElementById('demo-instruction');
const btnIniciar = document.getElementById('btn-iniciar-contagem');
const btnAbrirDemo = document.getElementById('btn-abrir-demo-sos');

if (btnAbrirDemo) {
  btnAbrirDemo.addEventListener('click', () => {
    document.getElementById('sos-demo').scrollIntoView({ behavior: 'smooth' });
    iniciarProtocoloSOS();
  });
}

if (btnIniciar) {
  btnIniciar.addEventListener('click', () => {
    iniciarProtocoloSOS();
  });
}

function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
}

function iniciarProtocoloSOS() {
  if (timerInterval) clearInterval(timerInterval);
  secondsLeft = 180;
  timerEl.textContent = formatTime(secondsLeft);
  btnIniciar.textContent = "PROTOCOLO EM EXECUÇÃO...";
  btnIniciar.disabled = true;

  timerInterval = setInterval(() => {
    secondsLeft--;
    timerEl.textContent = formatTime(secondsLeft);

    // Instruções sincronizadas com a quebra da onda de dopamina
    if (secondsLeft > 150) {
      instructionEl.textContent = "PULSO 1: Respire fundo pelo nariz por 4 segundos. Encha os pulmões... Segure.";
    } else if (secondsLeft > 120) {
      instructionEl.textContent = "PULSO 2: Solte o ar lentamente pela boca por 8 segundos. Vá até a pia e lave o rosto com água fria.";
    } else if (secondsLeft > 90) {
      instructionEl.textContent = "PULSO 3: O reflexo de mergulho vagal desacelera seu coração. A fissura está perdendo força. Não negocie.";
    } else if (secondsLeft > 45) {
      instructionEl.textContent = "PULSO 4: Faça 15 flexões no chão agora. O sangue precisa sair da região genital e ir para os músculos.";
    } else if (secondsLeft > 0) {
      instructionEl.textContent = "PULSO 5: A onda química de 3 minutos passou. Você é um homem livre. Agradeça a Deus.";
    } else {
      clearInterval(timerInterval);
      instructionEl.innerHTML = "<strong style='color: var(--success-green);'>VITÓRIA! Honra preservada e onda quebrada com sucesso.</strong>";
      btnIniciar.textContent = "⚡ SIMULAR NOVAMENTE";
      btnIniciar.disabled = false;
    }
  }, 1000);
}

// 3. ENGRENAGEM DE VENDAS // MODAL DE CHECKOUT PIX & ONBOARDING
const modal = document.getElementById('checkout-modal');
let pixCountdownInterval = null;
let currentPixPayload = "";
let currentCustomer = { name: "", email: "", phone: "", plan: "", price: "" };

function abrirCheckout(plano, preco) {
  currentCustomer.plan = plano;
  currentCustomer.price = preco;

  document.getElementById('modal-plano-nome').textContent = plano;
  document.getElementById('modal-plano-preco').textContent = `R$ ${preco}`;
  
  // Reseta estados
  document.getElementById('checkout-form').style.display = 'block';
  document.getElementById('pix-area').style.display = 'none';
  document.getElementById('pix-success-area').style.display = 'none';
  if (pixCountdownInterval) clearInterval(pixCountdownInterval);

  modal.style.display = 'flex';
}

function fecharCheckout() {
  if (pixCountdownInterval) clearInterval(pixCountdownInterval);
  modal.style.display = 'none';
}

function gerarPix(e) {
  e.preventDefault();
  
  const nome = document.getElementById('cust-name').value.trim();
  const email = document.getElementById('cust-email').value.trim();
  const tel = document.getElementById('cust-phone').value.trim();

  currentCustomer.name = nome;
  currentCustomer.email = email;
  currentCustomer.phone = tel;

  // Código Pix Padrão Banco Central do Brasil (EMV QRCPS)
  const valorCentavos = currentCustomer.price.replace(',', '.');
  currentPixPayload = `00020126580014br.gov.bcb.pix0136metanoia-pagamentos-oficial-18355204000053039865405${valorCentavos}5802BR5925METANOIA FORJA TECNOLOGIA6009SAO PAULO62070503***6304E8A2`;

  // Exibe o código no bloco
  document.getElementById('pix-code-text').textContent = currentPixPayload;

  // Gera o QR Code dinamicamente via API pública de alta velocidade
  const qrUrl = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&color=050505&bgcolor=FAFAFA&data=${encodeURIComponent(currentPixPayload)}`;
  const qrImg = document.getElementById('pix-qr-img');
  qrImg.src = qrUrl;

  // Inicia Timer de 15 Minutos (Gera Escassez e Urgência Real)
  let tempoRestante = 15 * 60;
  const timerEl = document.getElementById('pix-timer');
  
  if (pixCountdownInterval) clearInterval(pixCountdownInterval);
  pixCountdownInterval = setInterval(() => {
    tempoRestante--;
    const min = Math.floor(tempoRestante / 60);
    const sec = tempoRestante % 60;
    timerEl.textContent = `${min < 10 ? '0' : ''}${min}:${sec < 10 ? '0' : ''}${sec}`;

    if (tempoRestante <= 0) {
      clearInterval(pixCountdownInterval);
      timerEl.textContent = "EXPIRADO";
    }
  }, 1000);

  // Troca de tela
  document.getElementById('checkout-form').style.display = 'none';
  document.getElementById('pix-area').style.display = 'block';
}

function fallbackCopyText(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-999999px";
  textArea.style.top = "-999999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();
  try {
    document.execCommand('copy');
  } catch (err) {
    console.error('Erro ao executar fallback copy:', err);
  }
  document.body.removeChild(textArea);
}

function copiarPix() {
  if (!currentPixPayload) return;

  function notifyCopied() {
    const btn = document.getElementById('btn-copiar-pix');
    if (!btn) return;
    const txtOriginal = btn.textContent;
    btn.textContent = "✅ CÓDIGO PIX COPIADO!";
    btn.style.background = "var(--success-green)";
    btn.style.color = "#050505";
    setTimeout(() => {
      btn.textContent = txtOriginal;
      btn.style.background = "";
      btn.style.color = "";
    }, 3000);
  }

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(currentPixPayload)
      .then(notifyCopied)
      .catch(() => {
        fallbackCopyText(currentPixPayload);
        notifyCopied();
      });
  } else {
    fallbackCopyText(currentPixPayload);
    notifyCopied();
  }
}

function confirmarPix() {
  // Simula confirmação imediata de gateway e abre onboarding
  if (pixCountdownInterval) clearInterval(pixCountdownInterval);
  
  document.getElementById('conf-name').textContent = currentCustomer.name || "Guerreiro";
  document.getElementById('conf-email').textContent = currentCustomer.email || "seu-email@exemplo.com";

  document.getElementById('pix-area').style.display = 'none';
  document.getElementById('pix-success-area').style.display = 'block';
}

// Fechar modal ao clicar fora
window.addEventListener('click', (e) => {
  if (e.target === modal) fecharCheckout();
});

// Máscara automática no campo de telefone WhatsApp
const phoneInput = document.getElementById('cust-phone');
if (phoneInput) {
  phoneInput.addEventListener('input', (e) => {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length > 11) value = value.slice(0, 11);
    
    if (value.length > 6) {
      e.target.value = `(${value.slice(0, 2)}) ${value.slice(2, 7)}-${value.slice(7)}`;
    } else if (value.length > 2) {
      e.target.value = `(${value.slice(0, 2)}) ${value.slice(2)}`;
    } else if (value.length > 0) {
      e.target.value = `(${value}`;
    }
  });
}
