document.addEventListener('DOMContentLoaded', function () {
    const lxcForm = document.getElementById('lxcForm');
    const submitButton = document.querySelector('.bouton-droite');

    lxcForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        submitButton.disabled = true;
        submitButton.textContent = 'Création en cours...';

        const formData = new FormData(lxcForm);
        const jsonFormData = JSON.stringify(Object.fromEntries(formData));

        try {
            const response = await fetch('/create-ct', {  
                method: 'POST',
                body: jsonFormData,
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                const errorData = await response.json(); 
                throw new Error(errorData.message || 'Erreur lors de la création du conteneur LXC.');
            }

            const result = await response.json();
            alert(result.message);

            lxcForm.reset();

        } catch (error) {
            console.error('Erreur lors de la création du conteneur LXC:', error);
            alert(error.message || 'La création du conteneur LXC a échoué. Veuillez réessayer plus tard.');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Créer le conteneur LXC'; 
        }
    });
});
