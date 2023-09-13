// Add your JavaScript code here
// You can define event listeners and functions to handle client-side interactions

// Example: Submit the attendance form
document.getElementById('attendanceForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
  
    // Retrieve the selected attendance data and course ID
    const attendanceIds = Array.from(document.querySelectorAll('input[name="attendance[]"]:checked')).map(input => input.value);
    const courseId = document.getElementById('courseId').value;
  
    // Create a data object to send in the request body
    const data = {
      attendance: attendanceIds,
      course_id: courseId
    };
  
    // Make a POST request to the server to record the attendance
    fetch('/attendance', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        // Process the response or show a success message
        console.log(result);
        alert('Attendance recorded successfully!');
      })
      .catch(error => {
        // Handle any errors
        console.error('Error:', error);
      });
  });
  