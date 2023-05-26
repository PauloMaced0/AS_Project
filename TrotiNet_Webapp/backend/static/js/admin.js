$(document).ready(function () {
    let update_view = 0;
    function makeMessagediv(message, sender) {
        let ret = '';
        if (sender != 'admin') {
            ret += `<li class="clearfix">
                        <div class="message my-message text-justify" style="max-width:80%;">${message}
                        </div>
                    </li>`
        } else {
            ret += `<li class="clearfix d-flex justify-content-end" >
                        <div class="message other-message text-justify"style="max-width:80%;">${message}    
                        </div>
                    </li>`
        }
        return ret;
    }

    let send = document.getElementById("send_message");

    send.addEventListener('click', () => {
        let message = document.getElementById("text_message").value;
        document.getElementById("text_message").focus();

        if (message.trim().length) {
            fetch('/get_user_id', {
                method: 'GET',
                credentials: 'include'  // Include cookies or authentication tokens in the request
            })
                .then(response => response.json())
                .then(data => {
                    const userId = data.userId;
                    // Make an HTTP POST request to Flask
                    fetch('/chat/admin', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: message,
                            sender: "admin",
                            receiver: userId
                        })
                    })
                        .then(response => {
                            if (response.ok) {
                                // Request was successful 
                                let toAppend = makeMessagediv(message, "admin");
                                $("#chat_content").append(toAppend);
                                $("#chat_content").animate({ scrollTop: $('#chat_content').prop("scrollHeight") }, 700);

                                console.log('Message sent successfully');
                            } else {
                                // Request failed 
                                console.error('Failed to send message');
                            }
                        });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
        document.getElementById("text_message").value = ''
    });

    let no_new_message = 0;
    function fetchEndpoint() {
        // Make an HTTP POST request to Flask
        let new_user_message = 0;
        fetch("/get_messages")
            .then(function (response) {
                if (!response.ok) {
                    throw new Error("Failed to fetch messages");
                }
                return response.json();
            })
            .then(function (message_data) {
                message_data.messages.sort(function (a, b) {
                    return new Date(a.date) - new Date(b.date);
                });
                let to_append = ""
                message_data.messages.forEach(function (message) {
                    to_append += makeMessagediv(message.message, message.sender);
                    if (message.sender != "admin") {
                        new_user_message += 1;
                    }
                });

                $("#chat_content").empty();
                $("#chat_content").append(to_append);

                if (new_user_message != no_new_message) {
                    var chatDiv = document.getElementById('chat_content');
                    chatDiv.scrollTop = chatDiv.scrollHeight;
                }
                no_new_message = new_user_message;

                // Scroll to the bottom of the chat container just in the first fecthEndpoint() call
                if (update_view == 0) {
                    var chatDiv = document.getElementById('chat_content');
                    chatDiv.scrollTop = chatDiv.scrollHeight;
                    update_view = 1;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    fetchEndpoint();
    // Call the fetchEndpoint function every 2 seconds
    setInterval(fetchEndpoint, 3000);
});