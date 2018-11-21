call_order = ["text", "link", "image"];
	// console.log(call_order.length); 

function multi_stage_download(file_type_index){
	if (!(file_type_index < call_order.length))
		return false;

	file_type = call_order[file_type_index];
	console.log("Starting download of " + file_type + "s...");
	if(file_type == "image")
		data = {"image": 1};
	else if(file_type == "link")
		data = {"link": 1};
	else
		data = {"text": 1};

	$.ajax({
		method: "GET",
		type: "json",
		data: data,
		url: "/fetch_multistage",
		success: function(data){
			// console.log(data);
			json = JSON.parse(data);
			// console.log(json);
			for(i = 0; i < json[file_type].length; i++){
				// console.log(json["images"][i]);
				if(file_type == "image")
					$('#images-box').append("<img src='" + json[file_type][i] + "' class='col-md-4' style='height: 350px;'>");
				else if(file_type == "link")
					$("#links-box").append("<a  href='" + json[file_type][i] + "' class='col-md-6'>" + json["link_text"][i] + "</a>");
				else
					$("#text-box").append("<span class='col-md-12'>" + json[file_type][i] + "</span>");
			}
		},
		error: function(data){
			console.log("An error has occured...");
		}
	});
	setTimeout(multi_stage_download, 5000, file_type_index+1);
}

$(document).ready(function(){
	setTimeout(multi_stage_download, 3000, 0);
});

setInterval(function(){
	$.ajax({
		method: "GET",
		url: "https://api.openweathermap.org/data/2.5/weather",
		data: {"q":"Bangalore,IN", "appid":"ab0ecdd945b8aeb75f2a91b4f2008c29", "units":"metric"},
		type: "json",
		success: function(response) {
			console.log(response);
			console.log(new Date().toLocaleString());
			$("#lastmodified").text(new Date().toLocaleString());
			$("#temp").text(response["main"]["temp"]);
			$("#humidity").text(response["main"]["humidity"]);
			$("#location").text(innerHTML = response["name"]);
		},
		error: function(response) {
			console.log("error in api response");
		}
	});
}, 5000)

// var myApp = angular.module("myApp", []);
// // myApp.controller("RegisterCtrl", ['$scope',function ($scope,$http) {
// // 	$scope

// // }]);

// myApp.controller('RegisterCtrl', ['$scope', '$http',function($scope,$http) {
//       $scope.user = {};
//         $scope.submitForm = function() {
//         $http({
//           method  : 'POST',
//           url     : 'http://localhost:5000/login',
//           data    : $scope.user,
//           headers : { 'Content-Type': 'application/x-www-form-urlencoded' } 
//          })
//         // var userInput = $scope.register
//         // console.log(userInput)
//         // $http.post('/login',{"url": userInput})
//           .success(function(data) {
//             if (data.errors) {
//               // $scope.errorName = data.errors.name;
//               // $scope.errorUserName = data.errors.username;
//               // $scope.errorEmail = data.errors.email;
//             } else {
//               $scope.message = data.message;
//             }
//           });
//         };
//     }]);
