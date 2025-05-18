document.getElementById('idea-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const data = {
        project_type: document.getElementById('project_type').value,
        project_interest: document.getElementById('project_interest').value,
        project_technical: document.getElementById('project_technical').value,
        project_potential: document.getElementById('project_potential').value,
        project_additional: document.getElementById('project_additional').value
    };

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('output').textContent = result.ideas;
});
