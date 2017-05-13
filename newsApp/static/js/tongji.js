var second = 0;
window.setInterval(function () {
    second ++;
}, 1000);
var tjArr = localStorage.getItem("jsArr") ? localStorage.getItem("jsArr") : '[{}]';
$.cookie('tjRefer', getReferrer() ,{expires:1,path:'/'});

window.onbeforeunload = function() {
    debugger;
    if($.cookie('tjRefer') == ''){
        var tjT = eval('(' + localStorage.getItem("jsArr") + ')');
        if(tjT){
            tjT[tjT.length-1].time += second;
            var jsArr= JSON.stringify(tjT);
            localStorage.setItem("jsArr", jsArr);
        }
    } else {
        var tjArr = localStorage.getItem("jsArr") ? localStorage.getItem("jsArr") : '[{}]';
        var dataArr = {
            'url' : location.href,
            'time' : second,
            'refer' : getReferrer(),
            'timeIn' : Date.parse(new Date()),
            'timeOut' : Date.parse(new Date()) + (second * 1000)
        };
        tjArr = eval('(' + tjArr + ')');
        tjArr.push(dataArr);
        tjArr= JSON.stringify(tjArr);
        localStorage.setItem("jsArr", tjArr);
    }
     var tjlog = localStorage.getItem('jsArr');
    document.getElementById('time_input_id').value = tjlog;
    console.log(tjlog);
    // $;
    var username=$('#username_input_id').val();
    var article_id=$('#article_id_input_id').val();
    $.ajax({
        type:'POST',
        url:'../userlog/'+username+'/'+article_id,
        data:{
            timelog:tjlog
        },
    })
};
function getReferrer() {
    var referrer = '';
    try {
        referrer = window.top.document.referrer;
    } catch(e) {
        if(window.parent) {
            try {
                referrer = window.parent.document.referrer;
            } catch(e2) {
                referrer = '';
            }
        }
    }
    if(referrer === '') {
        referrer = document.referrer;
    }
    return referrer;
}