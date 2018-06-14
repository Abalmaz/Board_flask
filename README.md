# Доска объявлений

## Функционал:
1. Для зарегистированных пользователей отображает список всех объялений
2. Возможность оставлять комментарии и лайки под объявлением, только зарегистрированным пользователям и не более 5 в час

## Запуск:
### Создание БД:
1. flask db init
2. flask db migrate
3. flask db upgrade
### Запуск приложения
flask run

| Methods | URI | Action |
|---------|-----|--------|
|GET| http://127.0.0.1:5000| Show all boards name (if user authorized)|
|POST| http://127.0.0.1:5000/new_board| Create new board, send data in json format like {"board_name": "Name of new board"}, just for authorized user|
|GET| http://127.0.0.1:5000/<board_id>| Show all information about board: Creator, date create, all comments, count of likes, just for authorized user|
|POST| http://127.0.0.1:5000/<board_id>/add_comment| Add comment to board with id = board_id, data in json forman like {"comment":"Text of your comment"}, just for authorized user|
|POST| http://127.0.0.1:5000/<board_id>/likes_board| Add like to board (if user authorized)|
|GET| http://127.0.0.1:5000/login| Authorized user, send data in json format like {"username": "User", "password":"pass"}|
|POST| http://127.0.0.1:5000/register| Register user, send data in json format like {"username": "User", "password":"pass"}|
