async function searchTopic() {

    const query = document.getElementById("searchInput").value;

    if (query.trim() === "") {
        alert("Please enter a topic");
        return;
    }

    try {

        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query
            })
        });

        const data = await response.json();

        document.getElementById("result").innerHTML = `
            <h2>${data.query}</h2>

            <h3>📝 Summary</h3>
            <p>${data.summary}</p>

            <h3>📚 Sections</h3>

            <ul>
                ${data.sections.map(section => `<li>${section}</li>`).join("")}
            </ul>
        `;

    } catch (error) {

        console.error(error);
        alert("Something went wrong");

    }
}