# *_*coding:utf-8 *_*
import re
import execjs
import xmltodict
import yq_worker.utils.tools as tools
js_info = r'''
var ptv_domain = "haiwainet.cn";
function getDecoderVideo(str,isImage){
	var newstr="";
	if(!str || str=="") return newstr;
	if(str.indexOf("http://")!=0){
		var offset=3,pos=0,index=0;
		while(pos<str.length){
			var ch1=str.charCodeAt(pos++);
			var ch2=str.charCodeAt(pos++);
			newstr=newstr.concat(String.fromCharCode(ch2-offset));
			newstr=newstr.concat(String.fromCharCode(ch1-offset));
		}
	}else{
		newstr=str;
	}
	newstr=trimString(newstr);
	if(isImage) return newstr;
	var cdns=newstr.substr(7,4).toLowerCase();
	var fpxs=newstr.substr(-3).toLowerCase();
	if(cdns=="flv2"&&(fpxs=="mp4"||fpxs=="f4v")){
		var fn=newstr.substring(newstr.lastIndexOf("/")+1,newstr.lastIndexOf("."));
		var pt=newstr.substring(0,newstr.lastIndexOf("/")+1);
		newstr=pt+fn+".ssm/"+fn+".m3u8";
	}else if(cdns=="flv."&&fpxs=="mp4"){
	}else{
		newstr="ERROR";
	}
	return newstr;
}

function getDecoderVideoForMP4(str,videoType,isImage){
	var newstr="";
	if(!str || str=="") return newstr;
	if(str.indexOf("http://")!=0){
		var offset=3,pos=0,index=0;
		while(pos<str.length){
			var ch1=str.charCodeAt(pos++);
			var ch2=str.charCodeAt(pos++);
			newstr=newstr.concat(String.fromCharCode(ch2-offset));
			newstr=newstr.concat(String.fromCharCode(ch1-offset));
		}
	}else{
		newstr=str;
	}
	newstr=trimString(newstr);
	if(isImage) return newstr;
	var cdns=newstr.substr(7,4).toLowerCase();
	var fpxs=newstr.substr(-3).toLowerCase();
	if(cdns=="flv2"&&(fpxs=="mp4"||fpxs=="f4v")){
		if(videoType == 3){
			newstr = joinForMP4(newstr);
		}else{
			var fn=newstr.substring(newstr.lastIndexOf("/")+1,newstr.lastIndexOf("."));
			var pt=newstr.substring(0,newstr.lastIndexOf("/")+1);
			newstr=pt+fn+".ssm/"+fn+".m3u8";
		}
	}else if(cdns=="flv."&&fpxs=="mp4"){
		if(videoType == 3){
			newstr = joinForMP4(newstr);
		}
	}else{
		if(videoType == 3){
			newstr = joinForMP4(newstr);
		}else{
			newstr="ERROR";
		}
	}
	return newstr;
}

function joinForMP4(newstr){
	var pos = newstr.indexOf(ptv_domain)+ptv_domain.length+1;
	newstr = newstr.substring(0,pos)+"hls-vod"+"/"+newstr.substring(pos)+".m3u8";
	return newstr;
}

function trimString(str){
	str=str.replace(/^(\s|\u00A0)+/,'');
	for(var i=str.length-1;i>=0;i--){
		if(/\S/.test(str.charAt(i))){
			str=str.substring(0,i+1);
			break;
		}
	}
	return str;
};
'''
def get_video_info(html):
    regx = r'showPlayer\(\{id:\"(.*?)\"'
    xml_info = re.search(regx, html).group(1)
    xml_url = 'http://pvmsxml.haiwainet.cn' + xml_info
    xml_content = requests.get(xml_url).text
    content = xmltodict.parse(xml_content)
    video = content["root"]["video"]["item"]
    img = content["root"]["image"]
    node = execjs.get()
    ctx = node.compile(js_info)
    result = ctx.call('getDecoderVideoForMP4', video, 3, True)
    image_url = ctx.call("getDecoderVideo", img, "true")
    if result:
        print(result)
        return True
if __name__ == '__main__':
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    url = 'http://v.haiwainet.cn/n/2018/1207/c3541972-31454703.html'
    content = requests.get(url, headers=headers).text
    result = get_video_info(content)
    if result:
        print("我是视频哦")
