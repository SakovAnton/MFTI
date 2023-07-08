import os
import telebot
import locale
import urllib
import google.colab
from ultralytics import YOLO, checks, hub
from PIL import Image
from urllib.request import urlopen
from google.colab.patches import cv2_imshow
from openpyxl import Workbook
from openpyxl.styles import Font, Color, Alignment
from google.colab.patches import cv2
from google.colab import drive

drive.mount('/content/drive')

message_instruction = ' Я бот, который умеет на основе нейросети искать на плане электромонтажа условные обозначения розеток и формировать коммерческое предложние на их монтаж.'
message_instruction_2 = ' Если вы мне пришлёте лист с проектом на которм отображён план размещения розеток,то я с удовольствием расчитаю стоимость работ по их монтажу.'
message_instruction_3 = ' Большая просьба прислать мне скрин с вашего дизайн проекта в хорошем качестве, фото сделанное телефоном я тоже понимаю, но пока значительно хуже (я только учусь). '

model = YOLO('/content/drive/MyDrive/YOLO/Y15/detect/train3/weights/best.pt')

def answer (ans):
  answer = f'Я насчитал на вашем плане {ans} розеток. Я отметил на вашем плане найденные мной розетки.'
  return answer

def generate_offer (path, count):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Смета"
    #sheet.freeze_panes = row_to_freeze
    headers = ["поз", "вид работ", "расценка" ,"кол-во", "ед.изм.", "итого"]
    font = Font(name='Calibri',
                 size=12,
                 bold=True,
                 italic=False,
                 vertAlign=None,
                 underline='none',
                 strike=False,
                 color='000000FF')
    
    alignment=Alignment(horizontal='general',
                     vertical='bottom',
                     text_rotation=0,
                     wrap_text=False,
                     shrink_to_fit=False,
                     indent=0)
    
    sheet["A1"] = headers[0]
    sheet["A1"].font = font
    sheet["B1"] = headers[1]
    sheet["B1"].font = font
    sheet["C1"] = headers[2]
    sheet["C1"].font = font
    sheet["D1"] = headers[3]
    sheet["D1"].font = font
    sheet["E1"] = headers[4]
    sheet["E1"].font = font
    sheet["F1"] = headers[5]
    sheet["F1"].font = font

    sheet.column_dimensions['B'].width = 45
    sheet.column_dimensions['C'].width = 15

    data = [dict(zip(headers, (1 , "сверление отверстия для подрозетника", 200, count,"шт.", count*200))),
            dict(zip(headers, (2 , "монтаж подрозетника", 100, count,"шт.", count*100))),
            dict(zip(headers, (3 , "монтаж механизма розетки", 150, count,"шт.", count*150)))     
            ]

    row = 3
    for d in data:
        sheet[f'A{row}'] = d["поз"]
        sheet[f'B{row}'] = d["вид работ"]
        sheet[f'C{row}'] = d["расценка"]
        sheet[f'D{row}'] = d["кол-во"]
        sheet[f'E{row}'] = d["ед.изм."]
        sheet[f'F{row}'] = d["итого"]

        row += 1
    
    sheet["E7"] = "ВСЕГО"
    sheet["E7"].font = font 
    sheet["F7"] = "=SUM(F3:F5)"
    sheet["F7"].font = font 

    workbook.save(path)


token = '6389699537:AAEZWRjf-FyQTiKbX-1gpKKvBKB0bS-TGa0'
bot=telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id, message_instruction)
        bot.send_message(message.chat.id, message_instruction_2)
        bot.send_message(message.chat.id, message_instruction_3)

@bot.message_handler(content_types=['document'])
def handle_docs_audio(message):
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    file_path = '/content/drive/MyDrive/YOLO/pic.jpg'
    
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{token}/{file_info.file_path}', file_path)

    image_path = '/content/drive/MyDrive/YOLO/pic.jpg'

    image = Image.open(image_path)

    res = model(image)

    image_path = '/content/drive/MyDrive/YOLO/pic.jpg'

    image = Image.open(image_path)

    res = model(image)

    bot.send_message(message.chat.id, answer(len(res[0])))

    res_plotted = res[0].plot()
    file = cv2_imshow(res_plotted)
    image_res_path = '/content/drive/MyDrive/YOLO/doc_res.jpg'

    cv2.imwrite('/content/drive/MyDrive/YOLO/doc_res.jpg', res_plotted)

    file = open(image_res_path, 'rb')
    bot.send_photo(message.chat.id, file)

    smeta_path = '/content/drive/MyDrive/YOLO/smeta.xlsx'
    generate_offer (smeta_path, len(res[0]))
    bot.send_document(message.chat.id, open(smeta_path, 'rb'))


@bot.message_handler(content_types=['photo'])
def handle_photos(message):
    # Обработка фото
    file_path = '/content/drive/MyDrive/YOLO/foto.jpg'
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{token}/{file_info.file_path}', file_path)
    # Дополнительные действия с фото

    image_path = '/content/drive/MyDrive/YOLO/foto.jpg'

    image = Image.open(image_path)

    res = model(image)

    image_path = '/content/drive/MyDrive/YOLO/foto.jpg'

    image = Image.open(image_path)

    res = model(image)


    bot.send_message(message.chat.id, answer(len(res[0])))

    res_plotted = res[0].plot()
    file = cv2_imshow(res_plotted)
    image_res_path = '/content/drive/MyDrive/YOLO/foto_res.jpg'

    cv2.imwrite('/content/drive/MyDrive/YOLO/foto_res.jpg', res_plotted)

    file = open(image_res_path, 'rb')
    bot.send_photo(message.chat.id, file)

    smeta_path = '/content/drive/MyDrive/YOLO/smeta.xlsx'
    generate_offer (smeta_path, len(res[0]))
    bot.send_document(message.chat.id, open(smeta_path, 'rb'))


if __name__ == '__main__':
    print('Bot is staring...')
    bot.infinity_polling() # запускаем бота, чтоб он работал вечно
