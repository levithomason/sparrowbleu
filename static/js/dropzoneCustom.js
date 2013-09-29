$(document).ready(function(){
	// "myAwesomeDropzone" is the camelized version of the HTML element's ID
	Dropzone.options.myAwesomeDropzone = {
	  paramName: "image", // The name that will be used to transfer the file
	  acceptedFiles: (
	  	'*.jpg, *.jpeg, *.png, *.gif'
	  ),
	  url: "/new-gallery-image",
	  method: "POST",
	};
});
