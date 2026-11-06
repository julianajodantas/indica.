// Pequena interação: confirma ações de remoção dos favoritos.
document.querySelectorAll('form[action*="desfavoritar"]').forEach((formulario) => {
    formulario.addEventListener('submit', (evento) => {
        const confirmar = window.confirm('Deseja remover esta indicação dos seus favoritos?');
        if (!confirmar) evento.preventDefault();
    });
});
