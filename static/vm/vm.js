document.addEventListener('DOMContentLoaded', function () {
    const vmForm = document.getElementById('vmForm');
    const submitButton = document.querySelector('.bouton-droite');

    vmForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Désactiver le bouton pendant le traitement
        submitButton.disabled = true;
        submitButton.textContent = 'Création en cours...';

        // Récupérer les données du formulaire
        const formData = new FormData(vmForm);
        const jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        try {
            // Envoyer la requête POST au serveur Flask
            const response = await fetch('/create-vm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            // Gérer les erreurs de réponse
            if (!response.ok) {
                // Tenter de parser la réponse comme du JSON, même en cas d'erreur
                const errorData = await response.text().then(text => {
                    try {
                        return JSON.parse(text);
                    } catch (error) {
                        // Si le parsing échoue, renvoyer un objet d'erreur avec le texte brut
                        return { error: text };
                    }
                });
                
                // Lancer une erreur avec le message d'erreur du serveur
                throw new Error(errorData.error || 'Erreur serveur inconnue'); 
            }

            // Traiter la réponse JSON en cas de succès
            const result = await response.json();
            alert(result.message); // Afficher le message de succès

            // Réinitialiser le formulaire
            vmForm.reset();
        } catch (error) {
            // Gérer les erreurs de requête ou de parsing JSON
            console.error('Erreur lors de la création de la VM:', error);
            alert(error.message || 'La création de la VM a échoué. Veuillez réessayer plus tard.');
        } finally {
            // Réactiver le bouton et rétablir son texte d'origine
            submitButton.disabled = false;
            submitButton.textContent = 'Créer la VM';
        }
    });
});
