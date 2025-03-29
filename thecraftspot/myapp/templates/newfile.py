<style>
    /* Chatbot Styles */
    #chatbot-container {
        position: fixed;
        bottom: 80px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        background: white;
        border-radius: 10px;
        box-shadow: 04px 8px rgba(0, 0, 0, 0.2);
        display: none;
        flex-direction: column;
    }
    #chat-header {
        background: #007bff;
        color: white;
        padding: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    #chat-header button {
        background: none;
        border: none;
        color: white;
        font-size: 16px;
        cursor: pointer;
    }
    #chat-body {
        padding: 10px;
        overflow-y: auto;
        flex: 1;
        height: 300px;
    }
    #chat-footer {
        display: flex;
        padding: 10px;
        border-top: 1px solid #ddd;
    }
    #chat-input {
        flex: 1;
        padding: 5px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    #send-btn, #clear-btn {
        background: #007bff;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        margin-left: 5px;
        cursor: pointer;
    }
    #close-btn {
        background: red;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 5px;
        cursor: pointer;
    }
    #chat-icon {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #007bff;
        color: white;
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 50%;
        cursor: pointer;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    }
</style>

<!-- Chatbot Icon -->
<div id="chat-icon">
    <i class="fas fa-comments"></i>
</div>

<!-- Chatbot Container -->
<div id="chatbot-container">
    <div id="chat-header">
        <span>Chatbot</span>
        <button id="close-btn">&times;</button>
    </div>
    <div id="chat-body"></div>
    <div id="chat-footer">
        <input type="text" id="chat-input" placeholder="Ask something...">
        <button id="send-btn">Send</button>
        <button id="clear-btn">Clear</button>
    </div>
</div>

<script>
    document.getElementById("chat-icon").addEventListener("click", function() {
        document.getElementById("chatbot-container").style.display = "flex";
    });

    document.getElementById("close-btn").addEventListener("click", function() {
        document.getElementById("chatbot-container").style.display = "none";
    });

    document.getElementById("clear-btn").addEventListener("click", function() {
        document.getElementById("chat-body").innerHTML = "";
    });

    document.getElementById("send-btn").addEventListener("click", function() {
        sendMessage();
    });

    document.getElementById("chat-input").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    function sendMessage() {
        let inputField = document.getElementById("chat-input");
        let userMessage = inputField.value.trim();
        if (userMessage === "") return;

        // Append user message
        let chatBody = document.getElementById("chat-body");
        chatBody.innerHTML += `<div><strong>You:</strong> ${userMessage}</div>`;

        // Call API
        fetch('/images/genai/?existing=' + encodeURIComponent(userMessage))
            .then(response => response.json())
            .then(data => {
                let botMessage = data.gallery_description || "No response received.";
                chatBody.innerHTML += `<div><strong>Bot:</strong> ${botMessage}</div>`;
                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                chatBody.innerHTML += `<div><strong>Bot:</strong> Error fetching response.</div>`;
            });

        inputField.value = "";
    }
</script>