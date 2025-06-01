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
    const ideasText = result.ideas;

    const ideas = ideasText.split("Project Name:").slice(1); // remove empty string before first idea
    const outputDiv = document.getElementById('output');
    const submitBtn = document.getElementById('submit-selected-idea');
    document.getElementById('dislike-button').style.display = 'block';
    document.getElementById('generate-ideas').style.display = 'block';
    submitBtn.style.display = 'none';
    outputDiv.innerHTML = ''; // Clear previous

    let selectedButton = null;
    let selectedIdea = "";

    ideas.forEach((idea, idx) => {
        const button = document.createElement('button');
        button.textContent = "💡 Idea " + (idx + 1);
        button.style.display = 'block';
        button.style.margin = '10px 0';
        button.style.padding = '10px';
        button.style.width = '100%';
        button.style.textAlign = 'left';
        button.style.whiteSpace = 'pre-line';
        button.style.border = '1px solid #ccc';
        button.style.background = '#f9f9f9';
        button.style.cursor = 'pointer';
        button.innerText = "Project Name:" + idea.trim();

        button.addEventListener('click', () => {
            if (selectedButton) {
                selectedButton.style.background = '#f9f9f9';
                selectedButton.style.color = 'black';
            }

            button.style.background = '#007bff'; // Blue background
            button.style.color = 'white';
            selectedButton = button;
            selectedIdea = button.textContent;
            submitBtn.style.display = 'block';
        });


        outputDiv.appendChild(button);
    });

    submitBtn.onclick = () => {
        if (selectedIdea) {
            document.getElementById('thank-you-screen').style.display = 'block';
            document.getElementById('idea-form').style.display = 'none';
            document.getElementById('generate-ideas').style.display = 'none';
            outputDiv.style.display = 'none';
            submitBtn.style.display = 'none';

            document.getElementById('selected-idea-display').textContent = selectedIdea;
        }
    };

    document.getElementById('dislike').onclick = () => {
        // Simulate frontend trigger
        document.getElementById('chat').style.display = 'block';
        // Send POST to backend: { start_memory: true, idea_context: "..." }
    }
});
