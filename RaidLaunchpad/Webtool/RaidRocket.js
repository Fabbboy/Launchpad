
        function ping_tokens() {

          const ping_tokens = get_data('ping-tokens')

        }

        function join_tokens() {
          const inviteLink = document.getElementById('invite').value;
          const errormsg = document.getElementById('error');
          if(!inviteLink){
           errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
          }else{
          const join = post_data('join-server', {
            'invite': inviteLink
          });
        }
        }

        function leave_tokens() {
         const errormsg = document.getElementById('error');
        if(!document.getElementById('leave').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
         const leave = get_data(`leave-server/${document.getElementById('leave').value}`);
         }
        }

        function nick_tokens() {
   const errormsg = document.getElementById('error');
        if(!document.getElementById('nickId').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
          if(!document.getElementById('nick').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
          const start = post_data(`change-nick/${document.getElementById('nickId').value}`, {
            'nick': document.getElementById('nick').value
          });
}}
        }

        function disguise_tokens() {

        const errormsg = document.getElementById('error');
        if(!document.getElementById('disId').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
          const hide = get_data(`disguise/${document.getElementById('disId').value}`)
}
        }

        function speak_tokens() {
   const errormsg = document.getElementById('error');
        if(!document.getElementById('sendId').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
              if(!document.getElementById('msg').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
          const speak = post_data(`speak/${document.getElementById('sendId').value}`, {
            'message_content': document.getElementById('msg').value
          });
}}
        }
/*
        function react_tokens() {

          const react = post_data(`react`, {
            'channel_id': document.getElementById('reactId').value,
            'message_id': document.getElementById('react').value,
            'emoji':  document.getElementById('emoji').value
          });

        }
*/
        function start_spam() {
           const errormsg = document.getElementById('error');
        if(!document.getElementById('SpamId').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
               if(!document.getElementById('SpamMsg').value){
            errormsg.style.visibility = "visible"

           setTimeout(function(){
            errormsg.style.visibility = "hidden"
            return
            }, 2000);
        return
        }else{
          const start = post_data(`spam/${document.getElementById('SpamId').value}`, {
            'channel_id': document.getElementById('SpamId').value,
            'message_content': document.getElementById('SpamMsg').value,
            'mode': "1"
          });
}}
        }

        function stop_spam() {

          stop_spam = get_data('stop-spam');

        }

        function notify(text){

          document.querySelector(".base-3dtUhz").insertAdjacentHTML("afterbegin", `<div class="notice-3bPHh-" style="background-color:#722fb5;color:white;">${text}</div>`);

          setTimeout(function() {
            document.querySelector("div[class='notice-3bPHh-']").remove();
          }, 5500);

        }

        function error(text){

           console.log(`%c${text}`,"color: #f7f7f7; padding: 10px; background-color: #7a183e; font-size: 20px;");

        }

        async function post_data(url, data = {}) {
          try {
              fetch(`http://127.0.0.1:4321/raidrocket/${url}`,{
                method: 'POST',
                cache: "no-cache",
                credentials: "same-origin",
                body: JSON.stringify(data),
                headers: {"Content-Type": "text/plain"}
              })
              .then(response => response.json())
              .then((json) => { BdApi.showToast(json["message"]) })
          } catch (err){
            error(`An error occured while sending a POST request to the RaidRocket: ${err}`)
          }
        }

        async function get_data(endpoint) {
          try {
            const response = await fetch(`http://127.0.0.1:4321/raidrocket/${endpoint}`)
            .then(response => response.json())
            BdApi.showToast(response["message"])
          } catch (err) {
            error(`An error occurred while sending a POST request to the RaidRocket: ${err}`)
          }
        }

        function get_url() {
          return window.location.href.split("/")
        }

        function get_text_data(){
          if(document.querySelector("span[data-slate-string='true']")){

            var text = document.querySelector("span[data-slate-string='true']");

            var raw_found_params = []
            var found_params = []

            var extracted = text.innerText;
            if (typeof extracted !== 'undefined'){
              raw_found_params = extracted.split(",")

              for(var i = 0; i < raw_found_params.length; ++i){
                found_params.push(raw_found_params[i].trim())
              }
            }

            return found_params

          } else {
             BdApi.showToast('You must give paramters in the Discord message bar.', {type: 'error', timeout: '5500'})
          }

        }






