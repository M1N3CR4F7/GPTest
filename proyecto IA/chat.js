// Elementos del DOM
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Función para mostrar los mensajes
function displayMessage(message, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = message;
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Mantiene el scroll al fondo
}

// Función de enviar mensaje
function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
        // Mostrar mensaje del usuario
        displayMessage(message, 'user-message');
        
        // Limpiar campo de entrada
        userInput.value = '';
        
        // Simular respuesta de la IA
        setTimeout(() => {
            const aiResponse = 'Respuesta simulada de la IA: ' + message;
            displayMessage(aiResponse, 'ai-message');
        }, 1000); // Simula un retraso de 1 segundo
    }
}

// Eventos
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
