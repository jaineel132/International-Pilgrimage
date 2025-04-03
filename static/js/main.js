document.addEventListener("DOMContentLoaded", () => {
  // Initialize the chatbot
  initChatbot()

  // Add animation classes to elements
  addAnimationClasses()

  // Initialize date validation for trip planning
  initDateValidation()

  // Initialize dark mode toggle
  initDarkMode()

  
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
                    <img src="/static/images/chatbot-avatar.png" class="chatbot-avatar" alt="Assistant">
                    <div class="message-content">
                        Hello! I'm your Sacred Journeys assistant. How can I help you with your pilgrimage planning today?
                    </div>
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" placeholder="Type your message...">
                <button><i class="fas fa-paper-plane"></i></button>
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
    if (chatbotWindow.style.display === "flex") {
      chatbotInput.focus()
    }
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

    let messageHTML = ""

    if (sender === "bot") {
      messageHTML = `
      <img src="/static/images/chatbot-avatar.png" class="chatbot-avatar" alt="Assistant">
      <div class="message-content">${message}</div>
    `
    } else {
      messageHTML = `
      <div class="message-content">${message}</div>
    `
    }

    messageElement.innerHTML = messageHTML
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
      return "Prices vary depending on the pilgrimage, accommodation type, and services. You can see detailed pricing when you plan your trip. We offer options for all budgets!"
    } else if (message.includes("cancel") || message.includes("refund")) {
      return "For cancellations or refunds, please contact our support team at support@sacredjourneys.com or through your account dashboard. Cancellations made 30 days before departure are eligible for a full refund."
    } else if (message.includes("popular") || message.includes("recommend")) {
      return "Some of our most popular pilgrimages include Santiago de Compostela in Spain, Vatican City in Italy, and Jerusalem in Israel. Each offers unique spiritual experiences. Would you like more details about any of these?"
    } else if (message.includes("payment") || message.includes("pay")) {
      return "We accept all major credit cards, PayPal, and bank transfers. Your payment information is securely processed and we never store your card details. Need help with payment?"
    } else if (message.includes("thank")) {
      return "You're welcome! Is there anything else I can help you with? Feel free to ask about any aspect of your pilgrimage journey."
    } else {
      return "I'm not sure I understand. Could you please rephrase your question? You can ask about booking, prices, popular destinations, or specific pilgrimages. I'm here to help make your sacred journey memorable!"
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

// Dark mode toggle
function initDarkMode() {
  // Check for saved dark mode preference
  const darkModeEnabled = localStorage.getItem("darkMode") === "enabled"

  // Create dark mode toggle button
  const darkModeToggle = document.createElement("div")
  darkModeToggle.className = "dark-mode-toggle" + (darkModeEnabled ? " active" : "")
  darkModeToggle.title = "Toggle Dark Mode"

  // Add to navbar
  const navbarNav = document.querySelector(".navbar-nav.me-auto")
  if (navbarNav) {
    const darkModeItem = document.createElement("li")
    darkModeItem.className = "nav-item d-flex align-items-center ms-3"
    darkModeItem.appendChild(darkModeToggle)
    navbarNav.appendChild(darkModeItem)
  }

  // Apply dark mode if enabled
  if (darkModeEnabled) {
    document.body.classList.add("dark")
  }

  // Toggle dark mode on click
  darkModeToggle.addEventListener("click", () => {
    darkModeToggle.classList.toggle("active")
    document.body.classList.toggle("dark")

    // Save preference
    if (document.body.classList.contains("dark")) {
      localStorage.setItem("darkMode", "enabled")
    } else {
      localStorage.setItem("darkMode", "disabled")
    }
  })
}

