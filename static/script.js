document.getElementById('applicationForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const mainUI = document.getElementById('main-interface');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const statusText = document.getElementById('status-text');

    // UI State Management
    mainUI.style.display = 'none';
    loading.style.display = 'block';

    // Simulated status updates
    const steps = ["Parsing your resume...", "Researching company culture...", "Tailoring experience bullets...", "Writing cover letter..."];
    let stepIdx = 0;
    const interval = setInterval(() => {
        if (stepIdx < steps.length) {
            statusText.innerText = steps[stepIdx];
            stepIdx++;
        }
    }, 5000);

    // Function to handle the request with a retry for 503 errors
    async function processApplication(retries = 2) {
        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData
            });

            // Handle 503 Specific Logic
            if (response.status === 503 && retries > 0) {
                statusText.innerText = "AI is busy, retrying in 5 seconds...";
                await new Promise(resolve => setTimeout(resolve, 5000));
                return processApplication(retries - 1);
            }

            const data = await response.json();
            if (data.error) throw new Error(data.error);
            return data;

        } catch (error) {
            throw error;
        }
    }

    try {
        const data = await processApplication();
        clearInterval(interval);

        // Populate Content
        document.getElementById('companyBrief').textContent = data.company_brief;
        document.getElementById('tailoredResume').textContent = data.tailored_resume;
        document.getElementById('coverLetter').textContent = data.cover_letter;

        /** * FIX FOR DOWNLOAD LINKS:
         * Your packager.py creates files like 'tailored_resume_Company.docx'.
         * We extract the company name from the backend response context or 
         * assume the standard naming used in your download buttons.
         */
        const companySuffix = data.company_name ? `_${data.company_name.replace(/\s+/g, '_')}` : '';
        
        // Update download links to match the logic in packager.py
        document.getElementById('dl-resume').href = `/download/tailored_resume${companySuffix}.docx`;
        document.getElementById('dl-cover').href = `/download/cover_letter${companySuffix}.docx`;

        loading.style.display = 'none';
        results.style.display = 'block';

    } catch (error) {
        clearInterval(interval);
        // User-friendly error message for 503 spikes
        if (error.message.includes("503") || error.message.includes("UNAVAILABLE")) {
            alert("The AI service is currently overloaded. Please wait a moment and try again.");
        } else {
            alert("Error: " + error.message);
        }
        mainUI.style.display = 'block';
        loading.style.display = 'none';
    }
});

// Improved File Upload Visual
document.getElementById('resume').addEventListener('change', function(e) {
    const fileName = e.target.files[0]?.name;
    if (fileName) {
        const label = this.nextElementSibling;
        label.innerHTML = `<strong>File Selected:</strong><br>${fileName}`;
        label.style.borderColor = '#2563eb';
        label.style.background = '#eff6ff';
    }
});