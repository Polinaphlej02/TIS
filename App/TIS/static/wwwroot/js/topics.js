document.getElementById('log-out-btn').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'flex';
    document.getElementById('zatemnenie').style.display = 'block';
})

document.querySelector('.cancel-log-out').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'none';
    document.getElementById('zatemnenie').style.display = 'none';
})

const pictures = document.querySelectorAll('.picture');
if (pictures.length) {
    Array.from(pictures).forEach((picture) => {
     picture.src = `/static/pictures/${picture.dataset.name}`;
    });
};

const topic = document.location.pathname.split('/');

if (!!topic[2]) {
    if (topic[2] < 3) {
        document.querySelector('.chapter-name-1').click();
    } else if (topic[2] >= 3 && topic[2] <= 5) {
        document.querySelector('.chapter-name-2').click();
        var list = document.querySelector('.list-2');
        document.querySelector('.topics-list ol').scrollTo(0, list.offsetTop - 20);
    } else if (topic[2] >= 6 && topic[2] <= 8) {
        document.querySelector('.chapter-name-3').click();
        var list = document.querySelector('.list-3');
        document.querySelector('.topics-list ol').scrollTo(0, list.offsetTop - 20);
    } 
}

const table = document.querySelector('.brsuka');

if (table) {
    for ( let i = 0; i < 4; i++ ) {
        table.removeChild(table.firstChild);
    }
}