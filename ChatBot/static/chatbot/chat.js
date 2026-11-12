const textarea = document.getElementById("message");
const button = document.getElementById("send");
const chatbot = document.getElementById("chatbot");
const sendUrl = chatbot.dataset.sendUrl;                                                // the .dataset.sendUrl reads the data-send-url attribute found on the chatbot tag in the HTML
const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;           // finds the "secret stamp"

let messages = [];                                                                      // creates an empty array to contain the text

button.addEventListener("click", function() {                                           // creates a button/event listener
    const message = textarea.value;                                                     // creates a variable message that will contain the value that was input by the user in the text area        
    
    textarea.value = "";                                                                // clears the text box  

    messages.push({                                                                     // appends the user's messages to the "messages" array
    role: "user",                                                                       // defines "who is speaking"
    content: message                                                                    // contains the text from the variable "message"
    }); 

    const userBubble = document.createElement("div");                                   // creates a chat bubble that will contain a single user input / also creates a "div" element

    userBubble.classList.add("chat");                                                  // adds the created userBubble to a class called "chat"
    userBubble.innerHTML = "You: " + message ;                                         // sets the HTML inside the element user bubble, containing the text that was previously in text box

    chatbot.appendChild(userBubble)                                                    // adds a child element (userBubble) to the chatbot id or class

    fetch(sendUrl, {                                                                   //                                                 
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
            messages: messages
        })
    })
    .then(res => res.text())
    .then(data => {

        messages.push({
            role: "assistant",
            content: data
        });

        const responseBubble = document.createElement("div");

        responseBubble.classList.add("response");
        responseBubble.innerHTML = "Bot: " + marked.parseInline(data);

        chatbot.appendChild(responseBubble);
    });
});
