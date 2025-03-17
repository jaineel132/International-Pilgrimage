document.addEventListener("DOMContentLoaded", () => {
  // Search Functionality
  const searchInput = document.getElementById("search");
  const pilgrimagesContainer = document.getElementById("pilgrimages-container"); // Corrected ID

  if (searchInput && pilgrimagesContainer) {
    searchInput.addEventListener("input", async (e) => {
      const query = e.target.value.trim(); // Trim whitespace

      if (query.length > 2) {
        try {
          // Show loading state
          pilgrimagesContainer.innerHTML =
            '<p class="text-center">Loading...</p>';

          // Fetch results from the API
          const response = await fetch(
            `/api/search?q=${encodeURIComponent(query)}`
          );
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const results = await response.json();

          // Update the pilgrimages
          updatePilgrimages(results);
        } catch (error) {
          console.error("Error:", error);
          pilgrimagesContainer.innerHTML =
            '<p class="text-center text-danger">Failed to load results. Please try again.</p>';
        }
      } else if (query.length === 0) {
        // Reload the page if the search query is empty
        location.reload();
      }
    });
  }

  function updatePilgrimages(pilgrimages) {
    pilgrimagesContainer.innerHTML = "";

    if (pilgrimages.length === 0) {
      // Show empty state
      pilgrimagesContainer.innerHTML =
        '<p class="text-center">No pilgrimages found.</p>';
      return;
    }

    // Display the pilgrimages
    pilgrimages.forEach((pilgrimage) => {
      const card = document.createElement("div");
      card.className = "col";
      card.innerHTML = `
                <div class="card h-100 shadow-sm">
                    <img src="${
                      pilgrimage.image_url || "/static/images/placeholder.jpg"
                    }" class="card-img-top" alt="${pilgrimage.name}">
                    <div class="card-body">
                        <h5 class="card-title">${pilgrimage.name}</h5>
                        <p class="card-text text-muted">${
                          pilgrimage.location
                        }</p>
                        <a href="/pilgrimage/${
                          pilgrimage.id
                        }" class="btn btn-primary">Learn More</a>
                    </div>
                </div>
            `;
      pilgrimagesContainer.appendChild(card);
    });
  }

  // Delete Functionality
  const deleteButtons = document.querySelectorAll(".delete-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", async (event) => {
      const itemId = event.target.dataset.id; // Get the item ID
      const itemType = event.target.dataset.type; // Get the item type

      // Confirm deletion
      const confirmDelete = confirm(
        `Are you sure you want to delete this ${itemType}?`
      );
      if (!confirmDelete) return;

      try {
        // Send DELETE request to the backend
        const response = await fetch(`/delete/${itemType}/${itemId}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
        });

        const result = await response.json();

        if (result.success) {
          // Remove the row from the DOM with animation
          const row = event.target.closest("tr");
          row.classList.add("animate__animated", "animate__fadeOut");
          setTimeout(() => row.remove(), 500); // Wait for animation to finish
          alert(result.message); // Show success message
        } else {
          alert(`Error: ${result.message}`); // Show error message
        }
      } catch (error) {
        console.error("Error deleting item:", error);
        alert("An unexpected error occurred.");
      }
    });
  });

  //-----------------------------
  //FIXED: Chatbot Integration
  document.addEventListener("DOMContentLoaded", function () {
    // Create chat button
    const chatButton = document.createElement("div");
    chatButton.id = "chatbot-btn";

    // Create an image element
    const chatImage = document.createElement("img");
    chatImage.src = "/static/images/chat-icon.png"; // Ensure the correct path
    chatImage.alt = "Chat AI";

    // Append image to the button
    chatButton.appendChild(chatImage);
    document.body.appendChild(chatButton);

    // Create chat container
    const chatContainer = document.createElement("div");
    chatContainer.id = "chat-container";
    chatContainer.classList.add("hidden"); // Initially hidden
    chatContainer.innerHTML = `
        <div id="chatbox"></div>
        <input type="text" id="userInput" placeholder="Type a message...">
        <button id="sendBtn">Send</button>
    `;
    document.body.appendChild(chatContainer);

    // Toggle chat window when button is clicked
    chatButton.addEventListener("click", function () {
      chatContainer.classList.toggle("hidden");
    });

    console.log("Chatbot button created:", chatButton);
    console.log("Chatbot button HTML:", chatButton.innerHTML);
  });

  const apiKey = "AIzaSyBLAA104lEZqNAkGBNbRhh49WW7kjCcH9w"; // Replace with your actual API key
  const model = "gemini-1.5-pro";
  const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`;

  if (!document.getElementById("chat-container")) {
    const chatContainer = document.createElement("div");
    chatContainer.id = "chat-container";
    chatContainer.classList.add("hidden");
    document.body.appendChild(chatContainer);

    chatContainer.innerHTML = `
      <div id="chatbox"></div>
      <input type="text" id="userInput" placeholder="Ask a query..">
      <button id="sendBtn">Send</button>
    `;

    const chatbotBtn = document.createElement("button");
    chatbotBtn.id = "chatbot-btn";
    chatbotBtn.innerText = "💬 Chat with AI";
    document.body.appendChild(chatbotBtn);

    chatbotBtn.addEventListener("click", () =>
      chatContainer.classList.toggle("hidden")
    );
    document.getElementById("sendBtn").addEventListener("click", sendMessage);
  }

  async function sendMessage() {
    const userInputField = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const userInput = userInputField.value.trim();

    if (!userInput) return;

    chatbox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
    userInputField.value = "";

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


🔹 User Query: ${userInput}`,
                },
              ],
            },
          ],
        }),
      });

      const data = await response.json();
      console.log("🔥 API Response:", data);

      let botReply = "Sorry, I didn't understand that.";
      if (data.candidates && data.candidates.length > 0) {
        botReply = data.candidates[0]?.content?.parts?.[0]?.text || botReply;
      }

      chatbox.innerHTML += `<p><strong>TravelPal:</strong> ${botReply}</p>`;
    } catch (error) {
      console.error("🔥 Chatbot API Error:", error);
      chatbox.innerHTML += `<p><strong>Bot:</strong> Error fetching response. Please try again.</p>`;
    }

    chatbox.scrollTop = chatbox.scrollHeight;
  }
});
