// Overlay type 1: Big Window that blocks everything when someone  clicks 

function clickCaptureOverlayOn() {
  document.getElementById("clickCaptureOverlay").style.display = "block";
  return false; // Used to override the link
}

function clickCaptureOverlayOff() {
  document.getElementById("clickCaptureOverlay").style.display = "none";
  return false;  // Used to override the link
}

function clickCaptureCallback(e) {
    var e = window.e || e;

    if (e.target.tagName !== 'A')
        return;

    // Do something
	clickCaptureOverlayOn()
}


// Hijack ALL clicks
//if (document.addEventListener)
//    document.addEventListener('click', clickCaptureCallback, false);
//else
//    document.attachEvent('onclick', clickCaptureCallback);


// Overlay type 2: A tip on the screen with info
function addOverlaysToBody(bodyWithTags){
	var result = bodyWithTags;
	var overlayComponent;
	const OverlayTexts = getAllTheOverlayTexts(bodyWithTags);
	OverlayTexts.forEach((element)=>{
			overlayComponent = getOverlayComponent(getTagText(element[0]))
			result = result.replace(element[0], overlayComponent);
		})

	return result;

}

function getAllTheOverlayTexts(bodyToOverlay){
	var regularExpression =  new RegExp("@@(.)+@@", "g");
	return [...bodyToOverlay.matchAll(regularExpression)]; 

}
function getTagText(tag){
	return tag.replaceAll('@@', '');
}
function getOverlayComponent(desiredText){
	return `<span class="body-overlay-wrapper"> <span class="overlay-inline overlay"><img class="body-overlay-image" src="./images/alert-triangle (1).svg"><span class="body-overlay-text">${desiredText}</span></span></span>`;
}



