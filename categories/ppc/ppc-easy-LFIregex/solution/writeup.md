## Нашёл и посмотрел

| Событие | Название | Категория | Сложность |
| :------ | ---- | ---- | ---- |
| VKACTF 2025 | Архив полигона 9 | ppc web | easy |

  
### Описание


> Автор: one!tea
>
Мы получили доступ к просмотру архива полигона 9, осталось только понять, как же увидеть всё...


### Решение
Открываем страницу, где видим поиск по регулярным выражениям и список текстовых файлов. 

Один из файлов имеет наиболее интересное название `*** TOP SECRET ARCHIVE FILE ***`, он нам и нужен.

Пробуем разные выражения для получения результата. При помощи, например `file.*`, понимаем, что указанное название секретного файла ненастоящее.
 
Однако мы можем получить его имя при помощи перебора `часть_имени_файла_которую_мы_нашли.*` и предположения, что все файлы текстовые и на конце имеют `.txt`.

Получаем заветное название `filename_is_not_a_flag_I_L0V3_MY_D1R_4ND_ALL_MY_L0n6_F1L3s.txt`.

Также стоит заметить, что сайт написан на `aiohttp/3.9.1`. Быстрый поиск в интернете даёт нам понимание, что вероятно здесь есть LFI.

Смотрим в панеле разработчика, в какой директории хранятся статические файлы - это `front`.

Кнопка `Выполнить поиск в /archive` намекает на то, что директория архива имеет название `archive`. Пытаемся прочитать файл по пути `/front/../archive/filename_is_not_a_flag_I_L0V3_MY_D1R_4ND_ALL_MY_L0n6_F1L3s.txt`. Успех, флаг!

Пример сплойта [solution.py](./solution.py)

### Флаг

```
vka{easy_regex_search_and_lfi_read}
```
