document.addEventListener('DOMContentLoaded', function () {
    const lxcForm = document.getElementById('lxcForm');
    if (lxcForm) {
        lxcForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const formData = new FormData(lxcForm);
            const jsonFormData = JSON.stringify(Object.fromEntries(formData));

            try {
                const response = await fetch('/create-ct', {
                    method: 'POST',
                    body: jsonFormData,
                    headers: {'Content-Type': 'application/json'}
                });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                console.error('Error:', error);
                alert('Failed to create CT');
            }
        });
    }
});