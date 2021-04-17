# Лабораторная работа по ЭВМ

## Начало работы

Для начала работы необходимо иметь python версии 3.5 и выше. 
1.
    Поместить в файл data.csv свой вариант 
2. 
    Перейти в директорию с проектом:
    ```
    $ cd composition
    ```
3.
    Запустить программу:
    ```
    $ python3 .
    ```
3. 
    Радоваться выполненой лабораторной

## Структура программы

### containers_generator
Решение "комбинаторной" (на самом деле там жесть какая-то) задачи. По возможным размерам контейнера строит 
комбинации всех возжных контейнеров так, чтобы они без остатка вмещали заданное количество вершин графа.
Советую просто пользоваться и не забивать голову

### calculation
Собственно, здесь функции, которые  выполняют алгоритмы из методы по 
последовательной и итерационной компановке а также метод анализа количества внешних связей. 
В последней версии добален методы по размещению

### graph
Содержит в себе класс графа и класс вершины. По своей сути является также подграфом, 
который используется в процессе компоновки

### crystal
Там лежит класс платы для размещения. Не так удобно сделан, как graph, но что поделать? 

### main
Если не догадаетесь сами, то я не знаю, как вы дожили до 4 курса (хотя я как-то ведь дожил...)

## Полезное
Чтобы понять, как все это добро работает, нужно загрузить файл по ссылке
```
https://yadi.sk/i/PDwUKX-xFngNnw
```
И, заварив чая или чего по-крепче, начать чтиво сего дивного произведения с 51 страницы


## Важное
Хоть python я знаю хорошо, но с английским у меня большие проблемы, поэтому будте заранее готовы к 
кривым названиям переменных и методов. 
А вообще по всем вопросам пишите на почту molotkov.1997@mail.ru. 
Поддержать теплыми словами можно также через соцсеть https://vk.com/id241976031
