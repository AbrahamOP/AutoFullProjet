document.addEventListener('DOMContentLoaded', function () {
    const vmForm = document.getElementById('vmForm');
    if (vmForm) {
        vmForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const formData = new FormData(vmForm);
            const jsonFormData = JSON.stringify(Object.fromEntries(formData));

            try {
                const response = await fetch('/create-vm', {
                    method: 'POST',
                    body: jsonFormData,
                    headers: {'Content-Type': 'application/json'}
                });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to create VM');
            }
        });
    }
});