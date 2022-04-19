window.onload = function() {
  jQuery(function ($) { 
    if(window.location.href.indexOf("fatcaFfiList") < 0){
      $("a").attr("href", function(index) {
         var inner_url = this.innerHTML;
         this.href = this.href.replace(/^http:\/\/www.irs.gov/, "https://www.irs.gov");
         this.href = this.href.replace(/^http:\/\/apps.irs.gov/, "https://apps.irs.gov");
	 this.innerHTML = inner_url;
      });
    }
  });
};
