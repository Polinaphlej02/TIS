document.getElementById('log-in-btn').addEventListener('click', () => {
    document.getElementById('zatemnenie').style.display = 'block';
});

document.querySelector('.close').addEventListener('click', () => {
    document.getElementById('zatemnenie').style.display = 'none';
});