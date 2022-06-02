document.getElementById('log-out-btn').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'block';
})

document.querySelector('.cancel-log-out').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'none';
})