async function sendToPython(method) {
    const inputElement = document.getElementById('numbersInput');
    const resultBox = document.getElementById('resultBox');
    const sortedResult = document.getElementById('sortedResult');
    const methodNameSpan = document.getElementById('methodName');

    const inputVal = inputElement.value;

    sortedResult.innerText = "Обробка...";

    try {
        const response = await fetch('/sort', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                numbers: inputVal,
                method: method
            })
        });

        const data = await response.json();

        if (response.ok) {
            resultBox.style.display = 'block';
            methodNameSpan.innerText = data.method_name;
            sortedResult.innerText = data.result.join(', ');
        } else {
            alert(data.error || "Помилка формату чисел");
            sortedResult.innerText = "";
        }
    } catch (error) {
        console.error("Помилка:", error);
        alert("Не вдалося зв'язатися з Python-сервером. Перевір, чи запущений app.py");
    }
}