const emailField = document.getElementById('email');
const charCount = document.getElementById('charCount');
const clearBtn = document.getElementById('clearBtn');
const exampleButtons = document.querySelectorAll('.example-chip');
const confidenceBar = document.querySelector('.confidence-bar');

function updateCharacterCount() {
    const count = emailField.value.trim().length;
    charCount.textContent = `${count} character${count === 1 ? '' : 's'}`;
}

if (emailField && charCount) {
    updateCharacterCount();
    emailField.addEventListener('input', updateCharacterCount);
}

if (clearBtn && emailField) {
    clearBtn.addEventListener('click', () => {
        emailField.value = '';
        emailField.focus();
        updateCharacterCount();
    });
}

exampleButtons.forEach((button) => {
    button.addEventListener('click', () => {
        emailField.value = button.dataset.example || '';
        emailField.focus();
        updateCharacterCount();
        emailField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
});

if (confidenceBar) {
    const fill = confidenceBar.querySelector('span');
    const confidence = Number(confidenceBar.dataset.confidence || 0);

    if (fill) {
        fill.style.width = `${Math.max(0, Math.min(confidence, 100))}%`;
    }
}
