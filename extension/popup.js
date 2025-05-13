document.getElementById("summarizeBtn").addEventListener("click", async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;

    fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("output").value = "Error: " + data.error;
        } else {
            const summary = `📌 Title: ${data.title}\n👤 Author: ${data.author}\n🗓️ Date: ${data.date}\n\n📝 Summary:\n${data.summary}`;
            document.getElementById("output").value = summary;
        }
    })
    .catch(error => {
        document.getElementById("output").value = "Request failed: " + error;
    });
});
