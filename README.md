# Django Menu App
<img width="331" height="752" alt="image" src="https://github.com/user-attachments/assets/47eb3348-8cb0-47a4-a6f4-976ef65fd176" />


Django приложение для создания и отображения древовидных меню.

## Возможности

- ✅ Меню через template tag `{% draw_menu 'menu_name' %}`
- ✅ Автоматическое развертывание пути к активному пункту
- ✅ Хранение в БД, редактирование в админке Django
- ✅ Поддержка явных URL и named URLs
- ✅ Оптимизация: 1 запрос к БД на меню
- ✅ Несколько меню на одной странице

## Быстрый старт

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Использование

### 1. Создание меню в админке

1. Откройте `/admin/`
2. Создайте меню (например, `main_menu`)
3. Добавьте пункты меню:
   - **Название** - текст пункта
   - **Родитель** - для вложенности (оставьте пустым для корневого)
   - **URL** или **Named URL** - адрес страницы
   - **Порядок** - для сортировки

### 2. Использование в шаблонах

```django
{% load menu_tags %}
{% draw_menu 'main_menu' %}
```

### 3. Пример структуры

```
Техника
├── Телевизоры
│   └── LG
└── Телефоны
    └── Iphone 13
```

## Требования

- Django 3.2+
- Python 3.7+

## Структура проекта

```
menu/
├── models.py          # Модели Menu и MenuItem
├── admin.py           # Админка
├── templatetags/      # Template tag draw_menu
└── templates/         # Шаблоны меню
```

## Логика работы

- Активный пункт определяется по URL текущей страницы
- Все пункты над активным автоматически развернуты
- Первый уровень под активным также развернут
- Каждое меню загружается одним запросом к БД
