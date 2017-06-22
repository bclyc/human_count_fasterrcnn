
var points=new Array();
var cxt;  //画布函数
var img;
var sign=new Array();
var page = 0
var page_calibration = 0;
var NumPoint = 1;

function PrePage(){
    if(page <=0){
        //alert("已经到第一张了");
    }
    else{
        page =page-1;
        //a = points.join();
        //$.post("calibration.html?action=postpoints&points="+a,{});
        //loadurl(window.subpage,pagenum);
        drawImage();
        //drawlines();
    }

}

function AfterPage(){
    if(page >=sumpage-1){
       // alert("已经到最后一张了");
    }
    else{
        page =page+1;
        //sign[page] = 0;
        if (page_calibration<page)
        page_calibration=page;
        //$.post("calibration.html?action=postpoints&points="+a,{},);
        //loadurl(window.subpage,pagenum);
        drawImage();
        document.getElementById("num_frame").innerHTML=page_calibration;
        //drawlines();
    }
}


function loadurl(subpage){
    if(subpage==window.subpage){
        if(window.subpage == 0)
            window.open("calibration.html?subpage="+subpage,'_self');
        else(window.subpage == 1)
            window.open("calibration.html?subpage="+subpage,'_self');
        }
        //alert("biaoding.html?subpage="+subpage+"&pagenum="+pagenum+"&taskid="+taskid);
}

function SubmitPage(){
    var a = points.join();
    $.post("calibration.html?action=Calculation&subpage=0&configdir="+biaodingdir+"&points="+a,{});
    window.subpage = 0;
    loadurl(window.subpage);
        //function(data,status){
        //alert(data);
        //var arrayObj = new Array();
        //arrayObj =data.split(",");
        //document.getElementById("vanishing").innerHTML=arrayObj[0];
        //document.getElementById("rateing").innerHTML=arrayObj[1];
        //alert(arrayObj[1]);
    //}
}

function Recalibrate(){
}

//侧栏切换效果
$(document).ready(function(e) {
    subpage=window.subpage;
            $(".tabItemContainer>li>a").removeClass("tabItemCurrent");
			$(".tabBodyItem").removeClass("tabBodyCurrent");
    if(subpage==0){
			$($(".tabItemContainer>li")[0]).find("a").addClass("tabItemCurrent");
			$($(".tabBodyItem")[0]).addClass("tabBodyCurrent");

    }else if(subpage==1){
			$($(".tabItemContainer>li")[1]).find("a").addClass("tabItemCurrent");
			$($(".tabBodyItem")[1]).addClass("tabBodyCurrent");
			$(".subcamera_or_not").show();
    }
//    else if (subpage==2){
//			$($(".tabItemContainer>li")[2]).find("a").addClass("tabItemCurrent");
//			$($(".tabBodyItem")[1]).addClass("tabBodyCurrent");
//    }
});
//获取元素的纵坐标
function getTop(e){
    var offset=e.offsetTop;
    if(e.offsetParent!=null) offset+=getTop(e.offsetParent);
    return offset;
}
//获取元素的横坐标
function getLeft(e){
    var offset=e.offsetLeft;
    if(e.offsetParent!=null) offset+=getLeft(e.offsetParent);
    return offset;
}

//计算所画点的坐标并添加到数组
//	document.getElementById("myCanvas").onclick = function(){positionObj(event,"myCanvas")};

function getPositionObj(event,id){
    var thisX = getLeft(document.getElementById(id));
    var thisY = getTop(document.getElementById(id));
    subpage=window.subpage;

    x = event.clientX - thisX;
    y = event.clientY - thisY;
    return [x,y];
}


function positionObj(event,id){
    var thisX = getLeft(document.getElementById(id));
    var thisY = getTop(document.getElementById(id));
    subpage=window.subpage;

    x = event.clientX - thisX;
    y = event.clientY - thisY;
    //document.getElementById("signal_x").innerHTML=x;
    //document.getElementById("signal_y").innerHTML=y;
    points[page][sign[page]]= new Array();
    points[page][sign[page]][0]=x;
    points[page][sign[page]][1]=y;
    sign[page]+=1;
    if (window.subpage == 1){
        //drawpoints();
        drawlines();
    }
//		var imageData = cxt.getImageData(0,0,640,480);
//		var i=y*640*4+x*4;
//		imageData.data[i]=255;
//		imageData.data[i+1]=0;
//		imageData.data[i+2]=0;
//		imageData.data[i+3]=255;
//		cxt.putImageData(imageData,0,0);
}

//画点程序
/*function drawpoints(){
    var notRun=true;
    if(notRun)
    return;
    cxt.fillStyle="ffffff";
    cxt.fillRect(0,0,window.width,window.height);
    cxt.drawImage(img,0,0);
    for(var j=0;j<points.length;j++){
        if(j == page){
            for(var i=0;i<points[j].length;i++){
                cxt.beginPath();
                cxt.fillStyle="#FF0000";
                cxt.arc(points[j][i][0],points[j][i][1],10,0,Math.PI*2,true);
                cxt.closePath();
                cxt.fill();
            }
        }
    }
}*/

//画线程序
function drawlines(){
    cxt.fillStyle="ffffff";
    cxt.fillRect(0,0,window.width,window.height);
    cxt.drawImage(img,0,0);
     for(var j=0;j<points.length;j++){
            if(j == page){
                for(var i=0;i<sign[page];i++){
                    drawOne(points[j][i],points[j][i+1]);
                        i += 1;
                }
            }
      }
}
var beginToDrawTempLine=false;
var currentBeginPoint=[0,0];

function drawImage(){
//    points[page] = new Array();
//    sign[page]=0;
    img=new Image()
    img.src=IImagePaths[page];
    img.onload=function(){
        drawlines();
        //cxt.drawImage(img,0,0);
    }

}
function drawOne(point1,point2){
            cxt.beginPath();
            cxt.fillStyle="#FF0000";
            cxt.strokeRect(point1[0],point1[1],point2[0]-point1[0],point2[1]-point1[1]);
            cxt.strokeStyle = "red";
/*            cxt.moveTo(point1[0],point1[1]);
            cxt.lineTo(point2[0],point2[1]);
            cxt.lineWidth = 2;
            cxt.strokeStyle="red";
            cxt.stroke();*/
}
function drawOne2(point1,point2){
                cxt.beginPath();
            cxt.fillStyle="#FF0000";
            cxt.moveTo(point1[0],point1[1]);
            cxt.lineTo(point2[0],point2[1]);
            cxt.lineWidth = 2;
            cxt.strokeStyle="red";
            cxt.stroke();
}

window.onload = function(){
    c=document.getElementById("myCanvas");
    cxt=c.getContext("2d");
    for(var i=0;i<sumpage;i++){
        points[i] = new Array();
        sign[i] = 0;
    }
    if (window.subpage == 1){
        //drawlines();
        drawImage();
    }
    document.getElementById("num_frame").innerHTML=page_calibration;
//    img=new Image()
//    img.src=window.IImagePath;
    /*img.src = "http://localhost:8080/static/data/malldata/seq_000003.jpg";*/
    //img.src="static/data/1.jpg";
//    img.onload=function(){
//        cxt.drawImage(img,0,0);
//   }

    //？？？
    document.oncontextmenu = function(event){
           event.preventDefault();
    };

    //左键，右键单击事件流
    document.getElementById("myCanvas").onmousedown = function(event){
        subpage=window.subpage;
        if(event.button == 2)
        {
        if(!beginToDrawTempLine){
            sign[page]-=2;
            if(sign[page]<0)
             sign[page]=0;
        }else{
            beginToDrawTempLine=false;
            currentBeginPoint=[0,0];
        }
            if (window.subpage == 1){
                //drawpoints();
                drawlines();
            }
//            if (window.subpage == 1){
//               drawpoints();
//               drawlines();
//            }

        }else if(event.button == 0){
                if(!beginToDrawTempLine){
        beginToDrawTempLine=true;
        currentBeginPoint=getPositionObj(event,'myCanvas');

        }else{
            beginToDrawTempLine=false;
            var realEndPoint=getPositionObj(event,'myCanvas');
            points[page][sign[page]]= new Array();
            points[page][sign[page]][0]=currentBeginPoint[0];
            points[page][sign[page]][1]=currentBeginPoint[1];
            sign[page]+=1;
            points[page][sign[page]]= new Array();
            points[page][sign[page]][0]=realEndPoint[0];
            points[page][sign[page]][1]=realEndPoint[1];
            sign[page]+=1;
            if (window.subpage == 1){
                //drawpoints();
                drawlines();
            }
        }

//            positionObj(event,"myCanvas");
        }
        return true;
    }
    document.getElementById("myCanvas").onmousemove= function(event){
        if(beginToDrawTempLine){
            currentEndPoint=getPositionObj(event,'myCanvas');
            if (window.subpage == 1){
                //drawpoints();
                drawlines();
            }
            drawOne(currentBeginPoint,currentEndPoint);


        }
    }
}


