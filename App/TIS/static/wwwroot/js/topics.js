document.getElementById('log-out-btn').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'block';
})

document.getElementById('cancel-log-out').addEventListener('click', () => {
    document.querySelector('.confirm-log-out__wrapper').style.display = 'none';
})