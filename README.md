# geekshop-server
Учебный проект по Django, Интернет-магазин

Для запуска в терминале:
1. установите git (если не установлен), примеры установки для основных ОС:
   <https://gist.github.com/derhuerst/1b15ff4652a867391f03>
2. Клонируйте проект на свой компьютер:
```
cd [путь до папки где хотите хранить проект]
git clone https://github.com/Sin93/geekshop-server
```
   Если нужна определённая ветка:
```
git fetch
git checkout [название ветки]
```
3. Я использую virtualenv, для управления виртуальным окружением. 
   На остальных проект не тестировался, по этому лучше использовать его.
   ***
   В следующих командах:
   ***
   #### Для Linux чаще всего необходимо использовать python3 и pip3
   ***
   #### Для Windows python и pip
   ***
   Возможны и другие варианты, по этому используйте тот, который подходит вам.
   ***
```
pip3 install virtualenv
pyhton3 -m venv venv
```
4. Активируйте виртуальную среду и установите зависимости
```
В Linux:    . ./venv/bin/activate
в Windows:  venv/Scripts/activate

pip install -r requirements.txt
```
5. Перейдите в папку с проектом
```
cd geekshop-server
```
6. Примените миграции
```
python manage.py migrate
```
7. Импортируйте демонстрационные данные в базу данных
```
python manage.py import
```
8. Запустите проект
```
python manage.py runserver
```