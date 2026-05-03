async function enviarPregunta() {
    const input = document.getElementById('chat-input');
    const box = document.getElementById('chat-box');
    const msg = input.value.trim();

    if (!msg) return;

    // Mostrar mensaje del usuario
    box.innerHTML += `
        <div class="user-msg">
            <strong>Vos:</strong><br>${msg}
        </div>
    `;
    input.value = '';
    box.scrollTop = box.scrollHeight;

    // Indicador de carga
    const tempId = "loading-" + Date.now();
    box.innerHTML += `<div id="${tempId}" style="color: #64748b; font-size: 12px; margin-bottom: 10px;">Analytixa está analizando...</div>`;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ msg: msg })
        });

        const data = await response.json();
        document.getElementById(tempId).remove();

        const respuestaIA = data.response && data.response !== "null" 
            ? data.response 
            : "No pude procesar la respuesta. ¿Podrías intentar de nuevo?";

        // RENDERIZAMOS EL MARKDOWN (Negritas, listas, etc.)
        const htmlFormateado = marked.parse(respuestaIA);

        box.innerHTML += `
            <div class="ai-reply">
                <strong style="color: #10b981;">Analytixa:</strong><br>
                ${htmlFormateado}
            </div>
        `;
    } catch (e) {
        if(document.getElementById(tempId)) document.getElementById(tempId).remove();
        box.innerHTML += `<div class="ai-reply" style="border-color: red;">Error de conexión.</div>`;
    }

    box.scrollTop = box.scrollHeight;
}

// Escuchar tecla Enter
document.getElementById('chat-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') enviarPregunta();
});