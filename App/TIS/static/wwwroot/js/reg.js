Array.from(document.querySelectorAll('option')).forEach((elem) => {
    elem.innerHTML = elem.value;
})

const hideMessageBlock = () => {
    const msgs = document.querySelectorAll('.reg-error');

    Array.from(msgs).forEach((msg) => {
        if (msg.offsetHeight < 7) {
            msg.style.display = 'none';
        }
    });
}

window.addEventListener("load", () => hideMessageBlock());
document.querySelector('button').addEventListener('click', () => hideMessageBlock());