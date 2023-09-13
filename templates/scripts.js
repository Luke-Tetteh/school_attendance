function submitAttendance() {
    // Iterate through the checkboxes and get the attendance data
    var attendanceData = [];
    {% for student in students %}
    var presentCheckbox = document.getElementById('present-{{ student.id }}');
    var attendance = {
        studentId: {{ student.id }},
        present: presentCheckbox.checked
    };
    attendanceData.push(attendance);
    {% endfor %}

    // Perform any necessary actions with the attendance data
    console.log(attendanceData);
}
