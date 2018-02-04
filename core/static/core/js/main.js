$(function(){
	console.log("Ready");

});

let submitForm = function(){
	event.preventDefault();
	console.log("Submit Form Clicked");
	var formData = new FormData();
	var fileField = document.querySelector("input[type='file']");

	formData.append('queryVar', document.getElementById('queryVar').value);
	formData.append('forYear', document.getElementById('year').value);
	formData.append('pdf_file', fileField.files[0]);
	formData.append('csrfmiddlewaretoken', document.getElementsByName("csrfmiddlewaretoken")[0].value);


	fetch('/queryfile', {
	  method: 'POST',
	  body: formData,
      credentials: 'same-origin',
	})
	.then(()=> {
		return response.json();
	})
	.catch(error => console.error('Error:', error))
	.then(function(data){
		console.log(data);
	});

}

let verifyForm = function(){
	console.log("Verify Form");
}

