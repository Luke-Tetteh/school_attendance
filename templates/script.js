// Add your JavaScript code here
document.addEventListener('DOMContentLoaded', function() {
    // Code to run after the page has loaded
    // Access and manipulate HTML elements as needed
     // Example: Change the background color of the student detail section
    var studentDetail = document.getElementById('student-detail');
    studentDetail.style.backgroundColor = 'lightblue';

    // Example: Add a click event listener to a button
    var submitButton = document.getElementById('submit-button');
    submitButton.addEventListener('click', function(event) {
        event.preventDefault();
        alert('Button clicked!');
    
    });
});



// Get the submit button element
var submitButton = document.getElementById('submit-button');

// Add a click event listener to the submit button
submitButton.addEventListener('click', function() {
    // Get all the attendance checkboxes
    var checkboxes = document.getElementsByClassName('attendance-checkbox');
    
    // Create an array to store the attendance data
    var attendanceData = [];

    // Iterate through the checkboxes and get the attendance data
    for (var i = 0; i < checkboxes.length; i++) {
        var checkbox = checkboxes[i];
        var studentId = checkbox.id.split('-')[1];
        var isPresent = checkbox.checked;
        var attendance = {
            studentId: studentId,
            isPresent: isPresent
        };
        attendanceData.push(attendance);
    }

    // Perform any necessary actions with the attendance data
    console.log(attendanceData);
});
