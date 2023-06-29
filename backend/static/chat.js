const userId = JSON.parse(document.getElementById('user-id').textContent);
  
document.querySelector('#send').onclick = function(e){
  const messageInputDom = document.querySelector('#message');
  const message = messageInputDom.value;

  if (chatSocket.readyState === WebSocket.OPEN) {
      chatSocket.send(JSON.stringify({
          'message': message,
          'user_id':userId,
      }));
      messageInputDom.value = '';
  } else {
      console.error('WebSocket connection is not open.');
  }
}
const chatSocket = new WebSocket(
            'ws://' +
            window.location.host +
            '/ws/chat/' +
            userId +
            '/'
        );

        chatSocket.onmessage = function (e) {
            const data = JSON.parse(e.data);
            let reverse = true;

            if (data.sender_id == userId){
                console.log('reversed')
              reverse = false
            };
            createMessageContainer(data.sender_username, data.sender_image, data.message, reverse);
        };

        function createMessageContainer(senderUsername, senderImage, content, reverse) {
          const container = document.createElement('div');
            container.classList.add('chat__conversation-board__message-container');
          if (reverse == true){
            console.log('reverse is true')
            console.log(reverse)
            container.classList.add('reversed')
          }
          

          const html = `
              <div class="chat__conversation-board__message__person">
                <div class="chat__conversation-board__message__person__avatar">
                  <img src="${senderImage}" alt="${senderUsername}"/>
                </div>
                <span class="chat__conversation-board__message__person__nickname">${senderUsername}</span>
              </div>
              <div class="chat__conversation-board__message__context">
                <div class="chat__conversation-board__message__bubble">
                  <span>${content}</span>
                </div>
              </div>
              <div class="chat__conversation-board__message__options">
                <button class="btn-icon chat__conversation-board__message__option-button option-item emoji-button">
                  <svg class="feather feather-smile sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M8 14s1.5 2 4 2 4-2 4-2"></path>
                    <line x1="9" y1="9" x2="9.01" y2="9"></line>
                    <line x1="15" y1="9" x2="15.01" y2="9"></line>
                  </svg>
                </button>
                <button class="btn-icon chat__conversation-board__message__option-button option-item more-button">
                  <svg class="feather feather-more-horizontal sc-dnqmqq jxshSx" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                    <circle cx="12" cy="12" r="1"></circle>
                    <circle cx="19" cy="12" r="1"></circle>
                    <circle cx="5" cy="12" r="1"></circle>
                  </svg>
                </button>
              </div>
          `;
        
          container.innerHTML = html;
          const chatContainer = document.getElementById('chat-container');
          chatContainer.appendChild(container);
        
          return container;
        }  
