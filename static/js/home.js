// Show and Hide file content
const view = document.querySelectorAll(".view");
const viewDetails = document.querySelectorAll(".view-details");

view.forEach((link, index) => {
    link.addEventListener("click", function () {
        if (link.innerHTML == "Preview") {
            link.innerHTML = "Hide";
        } else {
            link.innerHTML = "Preview";
        }
        console.log(link);
        viewDetails[index].classList.toggle("active");
    });
});

// Handle download increment
// Get all the download links
var downloadLinks = document.querySelectorAll(".download-link");

// Iterate over each download link
downloadLinks.forEach(function (link) {
    // Add click event listener
    link.addEventListener("click", function (event) {
        

        // Get the file ID from the link's href attribute
        var fileID = link.getAttribute("data-file-id");

        // Call the increaseDownload view using AJAX
        fetch("/file/" + fileID + "/download/")
            .then(function (response) {
                if (response.ok) {
                    // Perform any additional actions after the download is incremented
                    // ...
                } else {
                    console.error("Error: " + response.status);
                }
            })
            .catch(function (error) {
                console.error("Error: " + error);
            });
    });
});
