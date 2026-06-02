// Define o tamanho base padrão (16px)
let currentFontSize = 16;

// Função que aumenta ou diminui a fonte
function changeFontSize(step) {
    currentFontSize += step;

    // Criamos limites para a letra não ficar minúscula nem gigante a ponto de quebrar o site
    if (currentFontSize < 12) currentFontSize = 12;
    if (currentFontSize > 24) currentFontSize = 24;

    // Atualiza a variável CSS do seu tema em tempo real
    document.documentElement.style.setProperty('--font-size', currentFontSize + 'px');

    // Guarda a preferência no navegador do utilizador
    localStorage.setItem('userFontSize', currentFontSize);
}

// Assim que a página carrega, verifica se o utilizador já tinha alterado a fonte antes
document.addEventListener('DOMContentLoaded', () => {
    const savedSize = localStorage.getItem('userFontSize');
    
    if (savedSize) {
        currentFontSize = parseInt(savedSize);
        document.documentElement.style.setProperty('--font-size', currentFontSize + 'px');
    }
});

// ==========================================
// LEITURA DE TEXTO POR VOZ (TEXT-TO-SPEECH)
// ==========================================

let isReadingModeActive = false;
let hoveredElement = null;
let availableVoices = [];

// 1. Carregar as vozes do sistema
function loadVoices() {
    availableVoices = window.speechSynthesis.getVoices();
}
window.speechSynthesis.onvoiceschanged = loadVoices;

// 2. Função que liga e desliga o modo (acionada pelo botão)
function toggleReadingMode() {
    isReadingModeActive = !isReadingModeActive;
    
    // Guarda o novo estado no localStorage para persistir entre as páginas
    localStorage.setItem('readingModeActive', isReadingModeActive);

    applyReadingModeUI();

    if (isReadingModeActive) {
        speakText("Modo de leitura ativado.");
    } else {
        window.speechSynthesis.cancel();
        removeHighlight();
    }
}

// 3. Atualiza apenas o visual do botão (evita repetir código)
function applyReadingModeUI() {
    const btn = document.getElementById('btn-read-text');
    const textSpan = document.getElementById('text-read-text');

    // Segurança: se o utilizador estiver numa página que não tem o botão (ex: login/registo)
    if (!btn || !textSpan) return;

    if (isReadingModeActive) {
        textSpan.innerText = "Parar Leitura";
        btn.classList.add('ring-4', 'ring-red-500'); 
    } else {
        textSpan.innerText = "Ler Texto";
        btn.classList.remove('ring-4', 'ring-red-500');
    }
}

function speakText(text) {
    window.speechSynthesis.cancel(); 
    
    if (!text || text.trim() === '') return;

    const utterance = new SpeechSynthesisUtterance(text);
    
    const ptVoices = availableVoices.filter(voice => voice.lang.includes('pt-PT') || voice.lang.includes('pt-BR'));
    
    if (ptVoices.length > 0) {
        let bestVoice = ptVoices.find(voice => 
            voice.name.includes('Google') || 
            voice.name.includes('Premium') || 
            voice.name.includes('Natural') ||
            voice.name.includes('Online')
        );
        utterance.voice = bestVoice ? bestVoice : ptVoices[0];
    }

    utterance.lang = 'pt-PT'; 
    utterance.rate = 1.0;     
    
    window.speechSynthesis.speak(utterance);
}

// 4. VERIFICAÇÃO AO CARREGAR A PÁGINA: Mantém o estado ativo entre as páginas!
document.addEventListener('DOMContentLoaded', () => {
    // Carrega as vozes imediatamente
    loadVoices();

    // Recupera o estado salvo do modo de leitura
    const savedReadingState = localStorage.getItem('readingModeActive');
    
    if (savedReadingState === 'true') {
        isReadingModeActive = true;
        // Dá um pequeno tempo (100ms) para o navegador renderizar o HTML antes de aplicar o visual
        setTimeout(() => {
            applyReadingModeUI();
        }, 100);
    }
});

// --- Funções de Destaque Visual (Highlight) ---
function addHighlight(element) {
    removeHighlight();
    hoveredElement = element;
    element.classList.add('outline', 'outline-4', 'outline-yellow-400', 'rounded-md');
}

function removeHighlight() {
    if (hoveredElement) {
        hoveredElement.classList.remove('outline', 'outline-4', 'outline-yellow-400', 'rounded-md');
        hoveredElement = null;
    }
}

// --- Detetores de Rato (Mouseover / Mouseout) ---
document.addEventListener('mouseover', function(e) {
    if (!isReadingModeActive) return;
    
    const readableTags = ['P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'SPAN', 'A', 'BUTTON', 'LI'];

    if (readableTags.includes(e.target.tagName)) {
        if (e.target.closest('#btn-read-text')) return;

        const textToRead = e.target.innerText || e.target.textContent;
        addHighlight(e.target);
        speakText(textToRead);
    }
});

document.addEventListener('mouseout', function(e) {
    if (!isReadingModeActive) return;
    removeHighlight();
});