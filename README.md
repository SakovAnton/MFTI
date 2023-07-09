# MFTI

Это заданин по курсу: https://stepik.org/lesson/884392/step/1?unit=889040

Был выбран продуктовый трек.

Проблема: 
В моей работе я предлагаю автоматизировать процесс выставления коммерческого предложения для маленьких бригад или небольших ИП занимающихся электромонтажными работами в частных квартирах.

Обоснование актуальности проблемы :
1. В малом бизнесе, когда многофункций выполняется однми чеовеком. Большой экономический эффект имеют различные инструменты которые автоматизируют рктинные процессы.
2. В большинстве случаев их работа заключается в монтаже различных эдектророзеток и выключателей. Для того чтобы выставить комерческое предложение (КП) клиенту (таких предложений выставляется в день до нескольких десятков). Для такой работы в штате нужно держать как минимум одного менеджера. Процесс работы над составлением КП состоит из изучения присланных дизайнером или самим клиентом планов электромонтажа (фактически посчитать в ручную все условные обозначения на планах). Потом расчёт сметы по полученным данным и отправка клиенту, для ознакомления.
3. Малый бизнес не может сам инвестировать в разработку. Однако в легко доступном формате Телеграм бота, такое решение в полне может прижиться на рынке.

Модель:
Поиск готовой модели не привел к успеху. В итоге было решено взять YOLOv8l от ultralytics
https://docs.ultralytics.com/models/yolov8/
Обучение было проведено в Google Colab на GPU количество эпох составило 300 время обучения примерно 5 часов.
Датасет был собран в размечен в рамках данной работы при помощи CVAT (app.cvat.ai)
Размеченный датасет находиться в папке dataset 

Продукт:
Продукт был реализован форме Telegram бота. Такой формат наиболее легко можно продвинуть у целевой аудитории частные прорабы небольшие ИП. Чаще всего мелкие строительные объекты ведуться в Telegramm, с помощью создания групп объетка, поэтому телеграм бот максимально органичная и полнятная форма для целевой аудитории.




