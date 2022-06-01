Array.from(document.querySelectorAll('option')).forEach((elem) => {
    elem.innerHTML = elem.value;
})