
// $(function(){
//     console.log("up to here");
//     $('#btnSignUp').click(function (){

//         var request = new XMLHttpRequest();

//         // This registers the python function here
//         request.open('POST', '/signUP');

//         // This registers the callback for when the python functions finishes
//         request.onload = function() {

//           console.log("up to here");
//           console.log(request.responseText);

//           if (request.status === 200 && request.responseText === 'User created successfully !') {
//             // Redirect to the url 
//             window.location = '/display';
//           } else {
//             // ops, we got an error from the server
//             alert('Something went wrong.');
//           }
//         };

//         // Registers callback if the python functions fails 
//         request.onerror = function() {
//           // ops, we got an error trying to talk to the server
//           alert('Something went wrong.');
//         };

//         // Now, this starts everything, the actual call. 
//         request.send($('form').serialize());

//     });
// });
