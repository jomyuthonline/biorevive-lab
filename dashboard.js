document.addEventListener('DOMContentLoaded', () => {
    const noteInput = document.getElementById('note-input');
    const addNoteBtn = document.getElementById('add-note-btn');
    const noteList = document.getElementById('note-list');

    // Load existing notes
    let notes = JSON.parse(localStorage.getItem('biorevive_notes') || '[]');
    
    function renderNotes() {
        noteList.innerHTML = '';
        notes.forEach((note, index) => {
            const div = document.createElement('div');
            div.className = 'note-item';
            div.innerHTML = `
                <p>${note.text}</p>
                <div class="note-actions">
                    <button class="note-btn copy" onclick="copyNote(${index})"><i class="fa-solid fa-copy"></i> คัดลอก</button>
                    <button class="note-btn" onclick="deleteNote(${index})"><i class="fa-solid fa-trash"></i> ลบ</button>
                </div>
            `;
            noteList.appendChild(div);
        });
    }

    addNoteBtn.addEventListener('click', () => {
        const text = noteInput.value.trim();
        if (text) {
            notes.unshift({ text, date: new Date().toISOString() });
            localStorage.setItem('biorevive_notes', JSON.stringify(notes));
            noteInput.value = '';
            renderNotes();
        }
    });

    window.deleteNote = (index) => {
        notes.splice(index, 1);
        localStorage.setItem('biorevive_notes', JSON.stringify(notes));
        renderNotes();
    };

    window.copyNote = (index) => {
        const text = notes[index].text;
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.querySelectorAll('.note-btn.copy')[index];
            const originalText = btn.innerHTML;
            btn.innerHTML = '<i class="fa-solid fa-check"></i> คัดลอกแล้ว';
            setTimeout(() => { btn.innerHTML = originalText; }, 2000);
        });
    };

    renderNotes();
});
