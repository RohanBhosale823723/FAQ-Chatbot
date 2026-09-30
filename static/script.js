function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const question = input.value.trim();

    if (question === "") {
        return;
    }

    // Display user question
    const userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = question;
    chatBox.appendChild(userMessage);

    // Send question to Flask
    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {

        // Display chatbot answer
        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = data.answer;

        chatBox.appendChild(botMessage);

        // Scroll to latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => {
        console.error("Error:", error);

        const botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = "Sorry, something went wrong.";

        chatBox.appendChild(botMessage);
    });

    input.value = "";
    input.focus();
}


function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}