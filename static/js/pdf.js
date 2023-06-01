// // Wait for the DOM to be ready
// document.addEventListener("DOMContentLoaded", function () {
//     // Get all the PDF links
//     var pdfLinks = document.querySelectorAll(".pdf-link");

//     // Iterate over each PDF link
//     pdfLinks.forEach(function (link) {
//         // Get the data URL from the href attribute
//         var pdfUrl = link.getAttribute("href");
//         var canvas = document.getElementById(pdfUrl)
        
//         // Load the PDF document using PDF.js
//         pdfjsLib.getDocument(pdfUrl).promise.then(function (doc) {
//             pdfDoc = doc

//             // Rendering code for the PDF document
//             // ...
//         });
//     });
// });


document.addEventListener("DOMContentLoaded", function () {
  // Get all the PDF links
  var pdfLinks = document.querySelectorAll(".pdf-link");

  // Iterate over each PDF link
  pdfLinks.forEach(function (link) {
      // Get the data URL from the href attribute
      var pdfUrl = link.getAttribute("href");
      var canvas = document.getElementById(pdfUrl);
      
      // Load the PDF document using PDF.js
      pdfjsLib.getDocument(pdfUrl).promise.then(function (doc) {
          var pdfDoc = doc;

          // Rendering code for the PDF document
          // ...
      });
  });
});