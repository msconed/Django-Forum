//NavBar
function hideIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:none;");
    navigation.classList.remove("hide");
}

function showIconBar(){
    var iconBar = document.getElementById("iconBar");
    var navigation = document.getElementById("navigation");
    iconBar.setAttribute("style", "display:block;");
    navigation.classList.add("hide");
}

//Comment
function showComment() {
    var commentArea = document.getElementById("comment-area");
    if (commentArea.classList.contains("hide")) {
        commentArea.classList.remove("hide");
    } else {
        commentArea.classList.add("hide");
    }
}

//Reply
function showReplies(id){
    var replyArea = document.getElementById(id);
    if (replyArea.classList.contains("hide")) {
        replyArea.classList.remove("hide");
    } else {
        replyArea.classList.add("hide");
    }
    
}

