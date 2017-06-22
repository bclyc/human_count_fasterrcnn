
function submitCheck(){
	var reg = new RegExp("^([0-2][0-9][0-5][0-9]-[0-2][0-9][0-5][0-9],{0,1}){1,}$");
	if(document.myform.camera.value==""){
		alert("未选择相机！");
		return false;
	}else if(document.myform.plan_name.value==""){
		alert("未输入预案名称！");
		return false;
	}else if(!reg.test(document.myform.run_time.value)){
		alert("时间段格式不正确！");
		return false;
	}else{
		var runtimeString = document.myform.run_time.value;
		var run_time_list=runtimeString.split(',');
		console.log(run_time_list);
		for(var i=0;i<run_time_list.length;i++){
			var starttime=run_time_list[i].substring(0,4);
			var endtime=run_time_list[i].substring(5,9);
			if(starttime>endtime){
				alert("时间段的开始时间"+starttime+"要小于结束时间"+endtime+"！");
				return false;
			}else if(starttime.substring(0,1)=="2"&&starttime.substring(1,2)>3){
				alert("开始时间"+starttime+"有误！");
				return false;
			}else if(endtime.substring(0,1)=="2"&&endtime.substring(1,2)>3){
				alert("结束时间"+endtime+"有误！");
				return false;
			}
		}
		alert("设置成功！");
		return true;
	}
}

function radiofn(){
	var radio=document.getElementsByName("radiocheck");

	for(var i=0;i<radio.length;i++){
		if(radio[i].checked){
			document.getElementById("mode_name").value=radio[i].value;
			alert("删除成功！");
			return true;
		}	
	}
	return false;
}




