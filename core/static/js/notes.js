// Mock storage for uploaded notes (no backend yet)
let notes = [];

// Upload form handler
document.getElementById("uploadForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const fileInput = document.getElementById("fileInput");
  const title = document.getElementById("noteTitle").value;
  const subject = document.getElementById("noteSubject").value;

  if (fileInput.files.length === 0) {
    alert("Please select a file!");
    return;
  }

  const file = fileInput.files[0];
  const uploader = "You"; // Later: real username
  const uploadDate = new Date().toLocaleDateString();

  const note = {
    title,
    subject,
    uploader,
    date: uploadDate,
    fileURL: URL.createObjectURL(file) // temporary link
  };

  notes.push(note);
  displayNotes(notes);

  // Reset form
  fileInput.value = "";
  document.getElementById("noteTitle").value = "";
  document.getElementById("noteSubject").value = "";
});

// Display notes
function displayNotes(notesList) {
  const container = document.getElementById("notesContainer");
  container.innerHTML = "";

  notesList.forEach((note) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <strong>${note.title}</strong> (${note.subject})<br>
      Uploaded by: ${note.uploader} on ${note.date}<br>
      <a href="${note.fileURL}" download="${note.title}">Download</a>
    `;
    container.appendChild(li);
  });
}

// Search/Filter
document.getElementById("searchInput").addEventListener("input", function(e) {
  const searchValue = e.target.value.toLowerCase();
  const filtered = notes.filter(note =>
    note.title.toLowerCase().includes(searchValue) ||
    note.uploader.toLowerCase().includes(searchValue)
  );
  displayNotes(filtered);
});
