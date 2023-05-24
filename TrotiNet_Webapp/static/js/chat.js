$(document).ready(function () {
    let update_view = 0;

    function makeMessagediv(message, img_path, sender) {
        let ret = '';
        if (sender == 'admin') {
            ret +=
                `<div class="d-flex flex-row justify-content-start mb-4 align-items-center">
                            <i class="bi bi-person-gear" style="font-size: 35px;"></i>
                            <div id="chat_message" class="p-3 ms-3 border"
                                style="border-radius: 15px; background-color: rgb(255, 255, 255); max-width:80%;">
                                <p class="small mb-0">${message}
                                </p>
                            </div>
                        </div>`
        } else {
            ret += `<div class="d-flex flex-row justify-content-end mb-4 align-items-center">
                            <div id="chat_message" class="p-3 me-3 border" style="border-radius: 15px; background-color: #ffffff; max-width:80%;">
                                <p class="small mb-0">${message}</p>
                            </div>
                            <img src="${img_path}" class="rounded-circle" alt="Something went wrong!"
                                style="height: 45px; width: 45px;">
                        </div>`
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
                    fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: message,
                            sender: userId,
                            receiver: "admin"
                        })
                    })
                        .then(response => {
                            if (response.ok) {
                                // Request was successful 
                                fetch('/get_user_img_path', {
                                    method: 'GET',
                                    credentials: 'include'  // Include cookies or authentication tokens in the request
                                })
                                    .then(response => response.json())
                                    .then(user_data => {
                                        const user_img_path = user_data.img_path;
                                        // Make an HTTP POST request to Flask
                                        let toAppend = makeMessagediv(message, user_img_path, userId);
                                        $("#chatting").append(toAppend);
                                        $("#chatting").animate({ scrollTop: $('#chatting').prop("scrollHeight") }, 700);
                                    })
                                    .catch(error => {
                                        console.error('Error:', error);
                                    });
                                console.log('Message sent successfully');
                            } else {
                                // Request failed 
                                console.error('Failed to send message');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        };
        document.getElementById("text_message").value = ''
    });

    let no_new_message = 0;
    function fetchEndpoint() {
        // Update the message container with the fetched messages
        fetch('/get_user_img_path', {
            method: 'GET',
            credentials: 'include'  // Include cookies or authentication tokens in the request
        })
            .then(response => response.json())
            .then(data => {
                const user_img_path = data.img_path;
                // Make an HTTP POST request to Flask
                let has_admin_message = 0;
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
                            to_append += makeMessagediv(message.message, user_img_path, message.sender);
                            if (message.sender == "admin") {
                                has_admin_message += 1;
                            }
                        });
                        $("#chatting").empty();
                        $("#chatting").append(to_append);

                        if (has_admin_message != no_new_message) {
                            var chatDiv = document.getElementById('chatting');
                            chatDiv.scrollTop = chatDiv.scrollHeight;
                        }
                        no_new_message = has_admin_message;

                        // Scroll to the bottom of the chat container just in the first fecthEndpoint() call
                        if (update_view == 0) {
                            var chatDiv = document.getElementById('chatting');
                            chatDiv.scrollTop = chatDiv.scrollHeight;
                            update_view = 1;
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
    fetchEndpoint();
    // Call the fetchEndpoint function every 2 seconds
    setInterval(fetchEndpoint, 3000);
});