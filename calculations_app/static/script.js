fetch('/calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ expression: screen.innerText })
})
.then(response => response.json())
.then(data => {
    screen.innerText = data.result;
})
.catch(() => {
    screen.innerText = "Error";
});
