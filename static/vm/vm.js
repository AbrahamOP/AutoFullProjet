document.addEventListener('DOMContentLoaded', function () {
    const vmForm = document.getElementById('vmForm');
    const submitButton = document.querySelector('.bouton-droite'); // Sélectionne le bouton de soumission

    vmForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Désactive le bouton de soumission pendant le traitement
        submitButton.disabled = true;
        submitButton.textContent = 'Création en cours...';

        const formData = new FormData(vmForm);
        const jsonFormData = JSON.stringify(Object.fromEntries(formData));

        try {
            const response = await fetch('/create-vm', {
                method: 'POST',
                body: jsonFormData,
                headers: { 'Content-Type': 'application/json' }
            });

            if (!response.ok) {
                const errorData = await response.json(); // Essaie de récupérer un message d'erreur du serveur
                throw new Error(errorData.message || 'Erreur lors de la création de la VM.');
            }

            const result = await response.json();
            alert(result.message); // Affiche le message de succès du serveur

            // Réinitialise le formulaire après la création réussie
            vmForm.reset();

        } catch (error) {
            console.error('Erreur lors de la création de la VM:', error);
            alert(error.message || 'La création de la VM a échoué. Veuillez réessayer plus tard.'); 
        } finally {
            // Réactive le bouton de soumission et rétablit son texte d'origine
            submitButton.disabled = false;
            submitButton.textContent = 'Créer la VM';
        }
    });
});
