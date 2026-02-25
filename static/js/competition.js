function saveSelection(path, value) {
  fetch(path, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ selection: value }),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      location.reload();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// competitions
document.addEventListener('DOMContentLoaded', function () {
  const competition = document.getElementById('comp-competition');
  competition.addEventListener('change', function () {
    saveSelection('/set_competition', this.value);
  });
});

// submissions
document.addEventListener('DOMContentLoaded', function () {
  const submission = document.getElementById('comp-submission');
  submission.addEventListener('change', function () {
    saveSelection('/set_submission', this.value);
  });
});
