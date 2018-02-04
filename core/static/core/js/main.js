$(function(){
	console.log("Ready");

});

let submitForm = function(){
	event.preventDefault();
	$("[type='submit']").prop('disabled', true);
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
	.then((response)=> {
		return response.json();
	})
	.catch(error => console.error('Error:', error))
	.then((data)=>{
		console.log(data);
		showRes(data["query_result"], data["csv_id"])
	});

}

let verifyForm = function(){
	console.log("Verify Form");
}

let showRes = function(result, downlink){
	$("#queryres").val(result);
	$("#result_holder").find("a").attr('href', '/queryfile?path='+downlink);
	$("#form_holder").slideUp();
	$("#result_holder").css('display', 'block');
}