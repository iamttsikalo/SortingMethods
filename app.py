from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- Алгоритми сортування ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# --- Маршрути Flask ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_numbers():
    data = request.get_json()
    raw_numbers = data.get('numbers', '')
    method = data.get('method', 'bubble')

    try:
        # Перетворюємо рядок у список чисел
        numbers = [int(n.strip()) for n in raw_numbers.split(',') if n.strip()]
        
        if not numbers:
            return jsonify({'error': 'Список порожній'}), 400

        if method == 'bubble':
            result = bubble_sort(numbers)
            name = "Бульбашка"
        elif method == 'quick':
            result = quick_sort(numbers)
            name = "Швидке сортування"
        else:
            result = sorted(numbers)
            name = "Стандартне"

        return jsonify({
            'result': result,
            'method_name': name
        })

    except ValueError:
        return jsonify({'error': 'Вводь тільки числа через кому!'}), 400

# --- Блок запуску ---
if __name__ == '__main__':
    print("Сервер запускається на http://127.0.0.1:5000")
    app.run(debug=True, port=5000)