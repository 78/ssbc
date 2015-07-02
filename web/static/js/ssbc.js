var PVCC = PVCC || {
    setCookie: function(cname,cvalue,exsecs)
    {   
        var d = new Date();
        d.setTime(d.getTime()+(exsecs*1000));
        var expires = "expires="+d.toGMTString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    },  
    getCookie: function(cname)
    {   
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) 
        {   
            var c = ca[i].trim();
            if (c.indexOf(name)==0) return c.substring(name.length,c.length);
        }   
        return ""; 
    },
    getVar: function(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
};

$('.x-sform').submit(function(e){
    e.preventDefault();
    var kw = $('.x-kw').val();
    if(!kw){
        $('.x-kw').focus();
        return false;
    }
    var url = '/search/' + encodeURIComponent(kw) + '/';
    window.location = url;
    return false;
});

function showAds(){
    var ua = navigator.userAgent;
    if(ua.indexOf('iP') > -1 || ua.indexOf('Android') > -1){ //移动端排版
    }else if(ua.indexOf('Apple1') > -1 && window.location.pathname=='/'){ //苹果
    }else{
        if(window.location.href.indexOf('/h/') > -1 || window.location.href.indexOf('/search/') > -1){
            //document.write('<script type="text/javascript" src="http://cip2.czpush.com/promote.php?id=100072"><\/script>');
            document.write('<script type="text/javascript">u_a_client="16664";u_a_width="0";u_a_height="0";u_a_zones="47635";u_a_type="1";<\/script><script src="http://e4.6dad.com/i.js"><\/script>');
        }
    }

}

$(function(){
    var ref = document.referrer;
    if(ref && ref.indexOf('shousibaocai') == -1){
        PVCC.setCookie('ref', 'somewhere');
    }else if(!ref){
        PVCC.setCookie('ref', 'direct');
    }
    if(PVCC.getCookie('ref') == 'somewhere'){
    }
});

showAds();


$(".x-kw").typeahead({
    onSelect: function(item) {
        console.log(item);
    },
    ajax: {
        url: "/suggest",
        timeout: 500,
        displayField: "suggestion",
        triggerLength: 1,
        method: "get",
        preProcess: function (data) {
            if (data.error) {
                // Hide the list, there was some error
                return false;
            }
            // We good!
            return data.suggest.suggestions;
        }
    }
});

