
function setCleanflag(flag){
	
	$.post("mainpage.html?action=setCleanflag&flag="+flag,{});	
}

function setHidenotrunningflag(flag){
	
	$.post("mainpage.html?action=setHidenotrunningflag&flag="+flag,{});	
}

function postMainpage(url){

	$.post(url,{});

}

