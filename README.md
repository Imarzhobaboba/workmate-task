![Скриншот интерфейса](screenshots/screen1.png)  
*Пример интерфейса приложения*
![Скриншот интерфейса](screenshots/screen22.png)  
*Пример интерфейса приложения*

Можете протестировать вручную. Например, так: 
```Bash
pytest
python main.py --file products.csv --aggregate "price=avg"
python main.py --file products.csv --where "price>300" --aggregate "price=avg"
python main.py --file products.csv --where "brand>apple"
```