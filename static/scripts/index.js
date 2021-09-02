const hi = document.getElementById('Hello-World')
let x = 0;
hi.style.position = 'absolute';

setInterval(() => {
    x++;
    hi.style.left = `${x}px`;
    hi.style.top = `${x}px`;
}, 50);