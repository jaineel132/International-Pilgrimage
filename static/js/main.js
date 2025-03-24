document.addEventListener("DOMContentLoaded", () => {
  // Initialize the chatbot
  initChatbot();

  // Add animation classes to elements
  addAnimationClasses();

  // Initialize date validation for trip planning
  initDateValidation();
});

// Chatbot functionality
function initChatbot() {
  // Create chatbot HTML structure
  const chatbotHTML = `
        <div class="chatbot-container">
            <div class="chatbot-button">
                <i class="fas fa-comment"></i>
            </div>
            <div class="chatbot-window">
                <div class="chatbot-header">
                    <h5 class="m-0">Sacred Journeys Assistant</h5>
                    <span class="chatbot-close">&times;</span>
                </div>
                <div class="chatbot-messages">
                    <div class="message bot-message">
                        Hello! I'm your Sacred Journeys assistant. How can I help you with your pilgrimage planning today?
                    </div>
                </div>
                <div class="chatbot-input">
                    <input type="text" placeholder="Type your message...">
                    <button>Send</button>
                </div>
            </div>
        </div>
    `;

  // Append chatbot to body
  document.body.insertAdjacentHTML("beforeend", chatbotHTML);

  // Get chatbot elements
  const chatbotButton = document.querySelector(".chatbot-button");
  const chatbotWindow = document.querySelector(".chatbot-window");
  const chatbotClose = document.querySelector(".chatbot-close");
  const chatbotInput = document.querySelector(".chatbot-input input");
  const chatbotSend = document.querySelector(".chatbot-input button");
  const chatbotMessages = document.querySelector(".chatbot-messages");

  // Toggle chatbot window
  chatbotButton.addEventListener("click", () => {
    chatbotWindow.style.display =
      chatbotWindow.style.display === "flex" ? "none" : "flex";
  });

  // Close chatbot window
  chatbotClose.addEventListener("click", () => {
    chatbotWindow.style.display = "none";
  });

  // Send message
  function sendMessage() {
    const message = chatbotInput.value.trim();
    if (message) {
      // Add user message
      addMessage(message, "user");

      // Clear input
      chatbotInput.value = "";

      // Get bot response using API
      getBotResponse(message);
    }
  }

  // Send message on button click
  chatbotSend.addEventListener("click", sendMessage);

  // Send message on Enter key
  chatbotInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });

  // Add message to chat
  function addMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", `${sender}-message`);
    messageElement.textContent = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }

  // Get bot response using API with custom instructions
  async function getBotResponse(message) {
    const apiKey = "AIzaSyBLAA104lEZqNAkGBNbRhh49WW7kjCcH9w"; // Replace with your actual API key
    const model = "gemini-1.5-pro";
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

    try {
      const response = await fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              role: "user",
              parts: [
                {
                  text: `IMPORTANT: You are an AI that ONLY provides information about international pilgrimage sites. Follow these strict rules:

- Answer only questions about pilgrimage sites, rituals, traditions, and travel logistics.  
- If the user says "hi," "hello," or similar greetings, respond with:  
  - "Hello! How can I assist you with pilgrimage info?"  
  - "Hey there! Looking for details on a pilgrimage site?"  
- If asked about "places to visit" in a city, respond **only** with pilgrimage sites from that city.  
  - If there are known pilgrimage sites, **list them immediately**.  
  - If unsure, ask: "Are you looking for pilgrimage sites in [city]?"  
- **If the user confirms ("yes"),** immediately provide the pilgrimage sites.  
- **DO NOT ask "Would you like more details?" more than once.** If the user confirms, provide details directly.  
- **Never restart the conversation** after user confirmation.  
- DO NOT answer unrelated topics (e.g., general tourism, politics, entertainment). If asked, reply:  
  - "I can only provide information about pilgrimage-related topics."  
- Keep responses **short and to the point.**  
- Be respectful, neutral, and informative at all times.  

🔹 User Query: ${message}`,
                },
              ],
            },
          ],
        }),
      });

      const data = await response.json();
      let botReply = "Sorry, I didn't understand that.";
      if (data.candidates && data.candidates.length > 0) {
        botReply = data.candidates[0]?.content?.parts?.[0]?.text || botReply;
      }
      addMessage(botReply, "bot");
    } catch (error) {
      console.error("Chatbot API Error:", error);
      addMessage("Error fetching response. Please try again.", "bot");
    }
  }
}
