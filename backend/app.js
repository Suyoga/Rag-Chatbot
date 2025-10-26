const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(sender, text, color) {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'mb-2';
  msgDiv.innerHTML = `<strong class="${color}">${sender}:</strong> ${text}`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const query = userInput.value.trim();
  if (!query) return;

  appendMessage('You', query, 'text-blue-600');
  userInput.value = '';

  try {
    const res = await fetch('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query, top_k: 3 })
    });

    const data = await res.json();
    if (data.answer) {
      appendMessage('Bot', data.answer, 'text-green-700');
    } else {
      appendMessage('Bot', data.error || 'No response from backend.', 'text-red-500');
    }
  } catch (err) {
    appendMessage('Bot', `⚠️ ${err.message}`, 'text-red-500');
  }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') sendMessage();
});
