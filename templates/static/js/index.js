// Gerar csrftoken -> Fonte: doc do django 
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;}

// responsável por modificar o botão de like apos um click nele
function like(postId, userName) {
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);

    fetch(`/dashboard/like-post/${postId}/${userName}/`,{ method: "POST" ,credentials: 'same-origin',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        }})
      .then((res) => res.json())
      .then((data) => {
        likeCount.innerHTML = data["count_likes"];
        if (data["liked"] === true) {
          likeButton.className = "fas fa-thumbs-up";
        } else {
          likeButton.className = "far fa-thumbs-up";
        }
      })
      .catch((e) => alert(e));
  }

 
// Responsabel por mudar o status da notificação no banco de dados e no front-end
function changeVisualization(notification_id){
  const box = document.getElementById(`viewed-${notification_id}`)
  const value = document.getElementById(`value-checkbox-${notification_id}`)
  if (box.checked){
   value.innerHTML = "<b>Notification viewed</b>"
   fetch(`/dashboard/msg-viewed/${notification_id}/${true}`, { method: "GET" })
   .then((res) => res.json())
   .then((data) => {
     {}
   })
   .catch((e) => alert(e));
  }else{
   value.innerHTML = "<b>Notification wasn't viewed</b>"
   fetch(`/dashboard/msg-viewed/${notification_id}/${false}`, { method: "GET" })
   .then((res) => res.json())
   .then((data) => {})
   .catch((e) => alert(e));
  }
}