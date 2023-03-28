const fsgaiHint = document.getElementById('fasgai-hint');
const hintButton = document.getElementById('hint-button');
document.addEventListener('DOMContentLoaded', () => {
    if (fsgaiHint) {
        fsgaiHint.style.display = 'none';
    }

    const stage = new NGL.Stage("viewport");
    stage.loadFile("/media/{{post.plik_hash}}/ala.mol2", {defaultRepresentation: true})
});
if (hintButton) {
    hintButton.addEventListener('click', () => {
        if (!fsgaiHint) {
            return;
        }
        if (fsgaiHint.style.display === 'none') {
            fsgaiHint.style.display = 'block';
        } else {
            fsgaiHint.style.display = 'none';
        }
    });
}