document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search');
    const pilgrimagesContainer = document.getElementById('pilgrimages');

    if (searchInput) {
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value;
            if (query.length > 2) {
                const response = await fetch(`/api/search?q=${query}`);
                const results = await response.json();
                updatePilgrimages(results);
            } else if (query.length === 0) {
                location.reload();
            }
        });
    }

    function updatePilgrimages(pilgrimages) {
        pilgrimagesContainer.innerHTML = '';
        pilgrimages.forEach(pilgrimage => {
            const card = document.createElement('div');
            card.className = 'col';
            card.innerHTML = `
                <div class="card h-100">
                    <img src="/static/images/placeholder.jpg" class="card-img-top" alt="${pilgrimage.name}">
                    <div class="card-body">
                        <h5 class="card-title">${pilgrimage.name}</h5>
                        <p class="card-text">${pilgrimage.location}</p>
                        <a href="/pilgrimage/${pilgrimage.id}" class="btn btn-primary">Learn More</a>
                    </div>
                </div>
            `;
            pilgrimagesContainer.appendChild(card);
        });
    }
});
document.addEventListener("DOMContentLoaded", () => {
    // Initialize the chatbot
    initChatbot()
  
    // Add animation classes to elements
    addAnimationClasses()
  
    // Initialize date validation for trip planning
    initDateValidation()
  })
  
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
      `
  
    // Append chatbot to body
    document.body.insertAdjacentHTML("beforeend", chatbotHTML)
  
    // Get chatbot elements
    const chatbotButton = document.querySelector(".chatbot-button")
    const chatbotWindow = document.querySelector(".chatbot-window")
    const chatbotClose = document.querySelector(".chatbot-close")
    const chatbotInput = document.querySelector(".chatbot-input input")
    const chatbotSend = document.querySelector(".chatbot-input button")
    const chatbotMessages = document.querySelector(".chatbot-messages")
  
    // Toggle chatbot window
    chatbotButton.addEventListener("click", () => {
      chatbotWindow.style.display = chatbotWindow.style.display === "flex" ? "none" : "flex"
    })
  
    // Close chatbot window
    chatbotClose.addEventListener("click", () => {
      chatbotWindow.style.display = "none"
    })
  
    // Send message
    function sendMessage() {
      const message = chatbotInput.value.trim()
      if (message) {
        // Add user message
        addMessage(message, "user")
  
        // Clear input
        chatbotInput.value = ""
  
        // Get bot response
        setTimeout(() => {
          const response = getBotResponse(message)
          addMessage(response, "bot")
        }, 500)
      }
    }
  
    // Send message on button click
    chatbotSend.addEventListener("click", sendMessage)
  
    // Send message on Enter key
    chatbotInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        sendMessage()
      }
    })
  
    // Add message to chat
    function addMessage(message, sender) {
      const messageElement = document.createElement("div")
      messageElement.classList.add("message")
      messageElement.classList.add(sender + "-message")
      messageElement.textContent = message
  
      chatbotMessages.appendChild(messageElement)
  
      // Scroll to bottom
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight
    }
  
    // Get bot response based on user input
    function getBotResponse(message) {
      message = message.toLowerCase()
  
      if (message.includes("hello") || message.includes("hi") || message.includes("hey")) {
        return "Hello! How can I assist you with your pilgrimage planning?"
      } else if (message.includes("book") || message.includes("reservation")) {
        return "To book a pilgrimage, browse our collection and click on 'Learn More' for the one you're interested in. Then you can use the booking form or plan a detailed trip."
      } else if (message.includes("price") || message.includes("cost") || message.includes("fee")) {
        return "Prices vary depending on the pilgrimage, accommodation type, and services. You can see detailed pricing when you plan your trip."
      } else if (message.includes("cancel") || message.includes("refund")) {
        return "For cancellations or refunds, please contact our support team at support@sacredjourneys.com or through your account dashboard."
      } else if (message.includes("popular") || message.includes("recommend")) {
        return "Some of our most popular pilgrimages include Santiago de Compostela in Spain, Vatican City in Italy, and Jerusalem in Israel. Each offers unique spiritual experiences."
      } else if (message.includes("thank")) {
        return "You're welcome! Is there anything else I can help you with?"
      } else {
        return "I'm not sure I understand. Could you please rephrase your question? You can ask about booking, prices, popular destinations, or specific pilgrimages."
      }
    }
  }
  
  // Add animation classes to elements
  function addAnimationClasses() {
    const elements = document.querySelectorAll(".card, .jumbotron, .stats-card")
  
    // Create an observer
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("animated-fade-in")
            observer.unobserve(entry.target)
          }
        })
      },
      {
        threshold: 0.1,
      },
    )
  
    // Observe each element
    elements.forEach((element) => {
      observer.observe(element)
    })
  }
  
  // Date validation for trip planning
  function initDateValidation() {
    const startDateInput = document.querySelector('input[name="start_date"]')
    const endDateInput = document.querySelector('input[name="end_date"]')
  
    if (startDateInput && endDateInput) {
      // Set min date to today
      const today = new Date()
      const todayFormatted = today.toISOString().split("T")[0]
      startDateInput.min = todayFormatted
  
      // Update end date min when start date changes
      startDateInput.addEventListener("change", function () {
        endDateInput.min = this.value
  
        // If end date is before start date, update it
        if (endDateInput.value && endDateInput.value < this.value) {
          endDateInput.value = this.value
        }
      })
    }
  }
  
  