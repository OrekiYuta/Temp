    let ws; //websocket 连接对象
    let ws_url = 'ws://localhost:8000/';
    let chat_main = document.getElementsByClassName('chat-main')[0];
    let user ;
    window.onload = function(){
        let nickname = localStorage.getItem('nickname');
        user=nickname;
        if(nickname){
            document.getElementById('user').innerText = nickname + ", 欢迎进入聊天室！"

            ws = new WebSocket(ws_url);
            ws.onopen = function (e) {
                console.log('websocket建立连接成功')
                historyMessage('系统通知:和服务器建立连接成功')
            }
            ws.onmessage = function (e) {
                console.log('websocket收到消息:', e.data)
                historyMessage('收到消息:'+ e.data)
            }
            ws.onclose = function (e) {
                console.log('websocket连接断开')
                historyMessage('系统通知:和服务器断开连接')
            }
            ws.onerror = function (e) {
                console.log('websocket产生错误',e)
                historyMessage('系统通知:发送错误,连接中断')
            }
        }else{
            window.location.href = '/';
        }

    }

    function sendMessage(text) {
        if(!ws){return false;}
        if (ws.readyState != ws.OPEN){return false;}
        if (text == ''){return false;}
        ws.send(text)
        return true;
    }

    function sendMessageBtn() {
        let chat_input = document.getElementsByClassName('chat-input')[0];
        let text = chat_input.value;

        let result = sendMessage(text);
        if (result){
            historyMessage(text)
            chat_input.value = '';
        }
    }

    function historyMessage(text) {

        let history = document.createElement('p');
        history.innerText = text;
        chat_main.appendChild(history);
    }

    function quit() {
        // 关闭websocket
        if (ws){
            if (ws.readyState == ws.OPEN){
                ws.close();
            }
        }
        localStorage.removeItem('nickname');
        window.location.href = '/';
    }


    function inputKeyDown(event) {

        // console.log(e)
        //判断是否按下回车键
        if(event.keyCode == 13){
            let input = event.target;
            let text = input.value;

            if (event.ctrlKey){
            //    Ctrl + Enter 换行
                input.value = text + '\n';
            }else {
            //    阻止默认行为
                event.preventDefault();
            //    Enter 发送消息

                let result = sendMessage(text);
                if (result){
                    historyMessage(text)
                    input.value = '';
                }
            }
        }
    }