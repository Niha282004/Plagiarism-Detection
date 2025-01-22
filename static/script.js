document.getElementById('plagiarism-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const resultDiv = document.getElementById('result');

    fetch('/doc/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerHTML = data.error;
        } else if (data.plagiarism_percentage === 'No files provided') {
            resultDiv.innerHTML = 'Please select both files to check for plagiarism.';
        } else {
            resultDiv.innerHTML = `Plagiarism percentage: ${data.plagiarism_percentage}%`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.innerHTML = 'An error occurred. Please try again.';
    });
});
