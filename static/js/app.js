document.addEventListener("DOMContentLoaded", () => {
    fetchEvents();

    // Fetch and display all events
    function fetchEvents() {
        fetch("/get_events")
            .then(response => response.json())
            .then(events => {
                renderEvents("#event-list", events);
            });
    }

    // Render events dynamically
    function renderEvents(selector, events) {
        const container = document.querySelector(selector);
        container.innerHTML = events.map((event, index) => `
            <div class="event-card">
                <h3>${event.title}</h3>
                <p>Date: ${event.date}</p>
                <button onclick="deleteEvent(${index})">Delete</button>
                <button onclick="editEvent(${index})">Edit</button>
            </div>
        `).join("");
    }

    // Add event
    document.querySelector("#add-event-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const title = document.querySelector("#event-title").value;
        const date = document.querySelector("#event-date").value;

        fetch("/add_event", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title, date, type: "regular" }),
        }).then(() => fetchEvents());
    });

    // Delete event
    window.deleteEvent = (eventId) => {
        fetch(`/delete_event/${eventId}`, {
            method: "DELETE",
        }).then(() => fetchEvents());
    };

    // Edit event
    window.editEvent = (eventId) => {
        const title = prompt("Enter new title:");
        const date = prompt("Enter new date (YYYY-MM-DD):");

        if (title && date) {
            fetch(`/update_event/${eventId}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title, date, type: "regular" }),
            }).then(() => fetchEvents());
        }
    };
});


