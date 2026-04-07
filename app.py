from flask import Flask, render_template, request, jsonify
import pygame
import random
import threading

app = Flask(__name__)

# --- ЛОГІКА СОРТУВАННЯ (Твій код) ---

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

# --- ВІЗУАЛІЗАЦІЯ PYGAME ---

def run_pygame_visual(numbers):
    """Функція для запуску вікна Pygame в окремому потоці"""
    pygame.init()
    
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Візуалізація сортування (Pygame)")
    
    # Налаштування кольорів та стовпців
    BLUE = (52, 152, 219)
    RED = (231, 76, 60)
    GREEN = (46, 204, 113)
    BLACK = (44, 62, 80)
    
    n = len(numbers)
    if n == 0: return
    bar_width = WIDTH // n
    max_val = max(numbers)
    
    def draw_bars(current_arr, highlights=None, finished=False):
        screen.fill(BLACK)
        for idx, val in enumerate(current_arr):
            # Пропорційна висота
            bar_height = (val / max_val) * (HEIGHT - 50)
            color = BLUE
            if highlights and idx in highlights:
                color = RED
            if finished:
                color = GREEN
            
            pygame.draw.rect(screen, color, (idx * bar_width, HEIGHT - bar_height, bar_width - 2, bar_height))
        pygame.display.update()

    # Алгоритм візуальної бульбашки
    arr = numbers.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            # Обробка виходу з вікна
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            
            draw_bars(arr, highlights=[j, j+1])
            pygame.time.delay(50) # Швидкість анімації

    draw_bars(arr, finished=True)
    
    # Тримаємо вікно відкритим після завершення
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()

# --- МАРШРУТИ FLASK ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort_numbers():
    data = request.get_json()
    raw_numbers = data.get('numbers', '')
    method = data.get('method', 'bubble')
    visualize = data.get('visualize', False) # Нове поле

    try:
        numbers = [int(n.strip()) for n in raw_numbers.split(',') if n.strip()]
        if not numbers:
            return jsonify({'error': 'Список порожній'}), 400

        # Якщо натиснуто кнопку візуалізації — запускаємо Pygame
        if visualize:
            # Запускаємо в окремому потоці, щоб Flask не "завис"
            threading.Thread(target=run_pygame_visual, args=(numbers,)).start()
            return jsonify({'message': 'Візуалізація запущена на вашому комп\'ютері!'})

        if method == 'bubble':
            result = bubble_sort(numbers.copy())
            name = "Бульбашка"
        elif method == 'quick':
            result = quick_sort(numbers.copy())
            name = "Швидке сортування"
        else:
            result = sorted(numbers.copy())
            name = "Стандартне"

        return jsonify({
            'result': result,
            'method_name': name
        })

    except ValueError:
        return jsonify({'error': 'Вводь тільки числа через кому!'}), 400

if __name__ == '__main__':
    # Вмикаємо debug=True для зручної розробки
    app.run(debug=True, port=5001)