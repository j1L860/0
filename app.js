// app.js

async function processFile() {
    const inputFileElement = document.getElementById('inputFile');
    const file = inputFileElement.files[0];
    if (!file) {
        alert('Please upload a file.');
        return;
    }

    // 	https://github.com/j1L860/7/blob/main/

    // Read the file
    const fileContent = await file.text();

    // Fetch reference data from GitHub
    const refDataUrl = 'https://github.com/j1L860/7/blob/main/j_hg38_ref.txt';
    const refResponse = await fetch(refDataUrl);
    const referenceData = await refResponse.text();

    // Process the file content (simplified processing here)
    let processedContent = fileContent.split('\n').map(line => {
        if (line.startsWith('#')) return null;
        return line.replace(/[/->"]/g, '').replace('ALLELE', 'RESULT');
    }).filter(line => line !== null).join('\n');

    // Create updated_input.txt
    const updatedFile = new Blob([processedContent], { type: 'text/plain' });
    const updatedFileUrl = URL.createObjectURL(updatedFile);

    // Optionally, save the file to GitHub (requires token)
    const uploadSuccess = await uploadToGitHub(updatedFile);
    if (uploadSuccess) {
        alert('File processed and uploaded successfully.');
    } else {
        alert('File processed, but upload failed.');
    }

    // Show the result to the user
    const outputDiv = document.getElementById('output');
    outputDiv.innerHTML = `<a href="${updatedFileUrl}" download="updated_input.txt">Download updated_input.txt</a>`;
}

async function uploadToGitHub(fileBlob) {
    const token = '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';  // Replace with a GitHub token
    const username = 'j1l860';
    const repo = '7';
    const path = '/j1L860/7/blob/main/updated_input.txt';
    const message = 'Upload updated_input.txt';

    const base64File = await blobToBase64(fileBlob);

    const url = `https://api.github.com/repos/${username}/${repo}/contents/${path}`;
    const response = await fetch(url, {
        method: 'PUT',
        headers: {
            'Authorization': `token ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            content: base64File
        })
    });

    return response.ok;
}

function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result.split(',')[1]);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}
