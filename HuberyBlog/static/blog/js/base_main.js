 layui.use(['element'], function () {
    var element = layui.element; //导航的hover效果、二级菜单等功能，需要依赖element模块
    //监听导航点击
    element.on('nav(demo)', function (elem) {
        //console.log(elem)
        layer.msg(elem.text());
    });
});

$(function () {
    //为当前窗口添加滚动条滚动事件（适用于所有可滚动的元素和 window 对象（浏览器窗口））
    $(window).scroll(function () {
        //创建一个变量存储当前窗口下移的高度
        var scroTop = $(window).scrollTop();
        //判断当前窗口滚动高度
        //如果大于100，则显示顶部元素，否则隐藏顶部元素
        if (scroTop > 100) {
            $('.return_top').fadeIn(500);
        } else {
            $('.return_top').fadeOut(500);
        }
    });
    //为返回顶部元素添加点击事件
    $('.return_top').click(function () {
        //将当前窗口的内容区滚动高度改为0，即顶部
        $("html,body").animate({scrollTop: 0}, "fast");
    });
});


// 显示当前时间
var weeks=["日","一","二","三","四","五","六"];
setInterval(function(){
    var date=new Date();
    var y=date.getFullYear();
    var m=date.getMonth()+1;
    var d=date.getDate();
    var w=date.getDay();
    var h=date.getHours();
    var mi=date.getMinutes();
    var s=date.getSeconds();
    var ms=m<10?"0"+m:m;
    var ds=d<10?"0"+d:d;
    var hs=h<10?"0"+h:h;
    var mis=mi<10?"0"+mi:mi;
    var ss=s<10?"0"+s:s;
    var time=y+"年"+ms+"月"+ds+"日  "+hs+":"+mis+":"+ss+"  星期"+weeks[w];
    document.getElementById("div_time").innerText=time;
}, 1000);
