if(typeof String.prototype.trim !== 'function') {
    String.prototype.trim = function() {
        return this.replace(/^\s+|\s+$/g, ''); 
    }
}

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

$('.x-play').click(function(){
    if(PVCC.getCookie('noads') != '1'){
        alert('您还没安装百度云-磁力助手插件，安装插件后即可在线观看本站资源。');
        $(this).attr('href', '/yunhelper/?fr=play');
    }else{
        $(this).attr('href', $(this).attr('data-url'));
    }
    return true;
});

function showAds(){
    var ua = navigator.userAgent;
    if(ua.indexOf('iP') > -1 || ua.indexOf('Android') > -1){ //移动端排版
    }else if(ua.indexOf('Safari') > -1 && ua.indexOf('Chrome') == -1){ //苹果
    }else if(ua.indexOf('bot') > -1){ //some bots
    }else if(PVCC.getCookie('noads') == ''){
        /*
        Ads here.    
        */
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
    setTimeout(function(){
        if($('#ssbc_helper_version').html() != ''){
            PVCC.setCookie('noads', '1');
        }
    },1000);
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

