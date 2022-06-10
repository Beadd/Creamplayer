//document.getElementById("imputMusicId")
// res.className = ("beadd");
res = document.getElementById("inputMusicId");
player = document.getElementById("musicPlayer");
function GetMusic(){
	console.log(res.value)
	music163Id = res.value;
	player.setAttribute("src",
	"https://api.injahow.cn/meting/?type=url&id="+music163Id);
}
