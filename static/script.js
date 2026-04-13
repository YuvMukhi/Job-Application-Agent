const form = document.getElementById('applicationForm');

if (window.location.protocol === 'file:') {
    const error = document.getElementById('error');
    document.getElementById('errorMessage').textContent = 'Please open the site through the Flask server using `python web.py`, not by opening index.html directly.';
    error.style.display = 'block';
    form.querySelector('button[type="submit"]').disabled = true;
} else {
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(this);

        // Show loading
        document.getElementById('loading').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('error').style.display = 'none';

        try {
            const url = `${window.location.origin}/process`;
            const response = await fetch(url, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const text = await response.text();
                throw new Error(`Server error ${response.status}: ${text}`);
            }

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            // Display results
            document.getElementById('companyBrief').textContent = data.company_brief;
            document.getElementById('tailoredResume').textContent = data.tailored_resume;
            document.getElementById('coverLetter').textContent = data.cover_letter;

            document.getElementById('loading').style.display = 'none';
            document.getElementById('results').style.display = 'block';

        } catch (error) {
            console.error(error);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('errorMessage').textContent = error.message;
            document.getElementById('error').style.display = 'block';
        }
    });
}

// File upload feedback
document.getElementById('resume').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const label = e.target.nextElementSibling;
        label.textContent = `Selected: ${file.name}`;
        label.style.borderColor = '#48bb78';
        label.style.background = '#f0fff4';
    }
});