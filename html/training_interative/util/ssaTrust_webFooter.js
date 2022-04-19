//$(document).ready(function(){
	
// Capture ALL Clicks
// From https://stackoverflow.com/questions/8492344/javascript-attach-an-onclick-event-to-all-links
function clickCaptureCallbacky(e) {
	var e = window.e || e;

	if (e.target.tagName !== 'A')
		return;

	// Do something
	clickCaptureOverlayOn();
}

if (document.addEventListener)
	// document.addEventListener('click', clickCaptureCallbacky, true);

	document.addEventListener("click", function (e) {
	  e.preventDefault();         // Comment this line to enable the link tag again.
	  clickCaptureOverlayOn();
	});
else
	document.attachEvent('onclick', clickCaptureCallbacky);
	
	

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
			var overlays = document.querySelectorAll(".overlay");
			overlays.forEach((overlay)=>{
				overlay.style.display = "flex";
			});
		}


//});
