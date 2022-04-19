 $(document).ready(function(){
			
		//ADDING THE PARAMETRIZED TEXT
		var data = JSON.parse(jsonData);

		document.getElementById("subject").innerText = data.Subject;
		
		if (data.Name.length > 0) {
			document.getElementById("name").innerText = data.Name;
		} else {
			document.getElementById("name").innerHTML =  " ".concat("&#60;", data.From, "&#62;");
		}

		document.getElementById("sender-top").innerHTML = " " // .concat("&#60;", data.From, "&#62;");;
		document.getElementById("date-left").innerHTML = data.Month.concat(" ", data.Day, ", ", data.Year,", ", data.Hour, " " );

		document.getElementById("date-right").innerHTML = data.Month.concat(" ", data.Day, ", ", data.Year,", ", data.Hour, " " );

		if (data.Name.length > 0) {
			document.getElementById("sender").innerHTML = data.Name.concat(" | ", data.From);
		} else {
			document.getElementById("sender").innerHTML = data.From;
		}
		document.getElementById("reply-to").innerHTML = data.Reply_to;
		document.getElementById("to").innerHTML = data.To;
		document.getElementById("date").innerHTML = data.Month.concat(" ", data.Day, ", ", data.Year,", ", data.Hour);
		document.getElementById("mailed-by").innerHTML = data.Mailed_by;
		console.log(addOverlaysToBody(data.Email_body));
		document.querySelector(".mail-text").innerHTML = addOverlaysToBody(data.Email_body);
		

		//ADDING THE SET OVERLAY MESSAGES
		const queryString = window.location.search;
		const urlParams = new URLSearchParams(queryString);
		// var params = window.location.search.substring(1);
		var displayTheOverlays = false;
		if (urlParams.has('showOverlays')) {
			var theParam = urlParams.get('showOverlays');
			if (theParam == 'true') {
				displayTheOverlays = true;
			}
		}
	   
		if(displayTheOverlays){
			document.querySelector(".toMe-arrow").classList.toggle("rotated");
			document.querySelector(".mail-box-table").classList.toggle("expanded");
			var overlays = document.querySelectorAll(".overlay");
			overlays.forEach((overlay)=>{
				overlay.style.display = "flex";
			});
		}

		var overlay_Messages = JSON.parse(overlayMessages);
		if(overlay_Messages.Subject == "" || overlay_Messages.Subject == null){
			document.querySelector(".overlay-subject").style.display = "none";
		}
		if(overlay_Messages.Date == "" || overlay_Messages.Date == null){
			document.querySelector(".overlay-date").style.display = "none";
			document.getElementById("overlay-hour-container").style.display = "none";
		}
		if(overlay_Messages.Name_Sender == "" || overlay_Messages.Name_Sender == null){
			document.querySelector(".overlay-name").style.display = "none";
		}
		if(overlay_Messages.toMe == "" || overlay_Messages.toMe == null){
			document.querySelector(".overlay-toMe").style.display = "none";
		}
		if(overlay_Messages.From == "" || overlay_Messages.From == null){
			document.querySelector(".overlay-from").style.display = "none";
		}
		if(overlay_Messages.Reply_to == "" || overlay_Messages.Reply_to == null){
			document.querySelector(".overlay-reply-to").style.display = "none";
		}
		if(overlay_Messages.To == "" || overlay_Messages.To == null){
			document.querySelector(".overlay-to").style.display = "none";
		}
		if(overlay_Messages.Mailed_by == "" || overlay_Messages.Mailed_by == null){
			document.querySelector(".overlay-mailed-by").style.display = "none";
		}

		document.querySelector("#Overlay-subject>p").innerHTML = overlay_Messages.Subject;
		document.querySelector("#Overlay-hour>p").innerHTML = overlay_Messages.Date;
		document.querySelector("#Overlay-name>p").innerHTML = overlay_Messages.Name_Sender;
		document.querySelector("#Overlay-toMe>p").innerHTML = overlay_Messages.toMe;
		document.querySelector("#Overlay-1>p").innerHTML = overlay_Messages.From;
		document.querySelector("#Overlay-2>p").innerHTML = overlay_Messages.Reply_to;
		document.querySelector("#Overlay-3>p").innerHTML = overlay_Messages.To;
		document.querySelector("#Overlay-4>p").innerHTML = overlay_Messages.Date;
		document.querySelector("#Overlay-5>p").innerHTML = overlay_Messages.Mailed_by;
		
		//THIS HIDES OR SHOWS ALL THE OVERLAYS
		//To hide include in the html url '?showOverlays=true'
		
		if (screen.width < 620) {
			document.querySelectorAll(`.overlay-text`).forEach((element) => element.classList.toggle("collapsed-horizontal"));
			document.querySelectorAll(`.overlay-text`).forEach((element) => element.classList.toggle("no-shadow"));
		}

		// Fill in the name, if there is a space for it & we have a name to put in
		const nameElement = document.getElementById('nametofill')
		if (nameElement && urlParams.has('name')) {
			var theNewName = urlParams.get('name');
			if (theNewName && theNewName.length > 1) {
				nameElement.textContent = theNewName;
			}
		}

});
	
function displayMailBoxTable(){
	
	document.querySelector(".toMe-arrow").classList.toggle("rotated");

	document.querySelector(".mail-box-table").classList.toggle("expanded");

}

        