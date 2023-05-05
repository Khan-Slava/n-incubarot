import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

import programmLogic as logic

# Функция, вызываемая при нажатии на кнопку "Generate"
def generate_name():
    
    # получаем элементы таблицы и удаляем их(нужно, чтобы биграммы с прошлого имени не сохранялись)
    tree_children = tree.get_children()
    for items in tree_children:
        tree.delete(items)
    
    #получаем данные с programmLogic 
    global current_name
    all_bigrams = defaultdict
    all_bigrams =  logic.build_bigram("names.txt")
    bigram_probabilities_list = logic.create_new_name(all_bigrams)
    current_name = bigram_probabilities_list["current_name"]
    
    #записываю в имя и заполняю таблицу с вероятностями 
    text.config(text= f'Name: {current_name}')
    for bigram, probabilities in bigram_probabilities_list.items():
        if bigram != 'current_name':
            tree.insert('','end',text=bigram,values=probabilities)

# Функция, вызываемая при нажатии на кнопку "Create"
def create_image():
    global current_name
    # Создаем изображение и настраиваем его размеры
    image = Image.new('RGB', (500, 500))
    draw = ImageDraw.Draw(image)
    
    # Рисуем заголовки таблицы
    draw.text((50, 50), 'Bigram', font=ImageFont.truetype('arial.ttf', 12))
    draw.text((300, 50), 'Probability', font=ImageFont.truetype('arial.ttf', 12))
    
    # Рисуем строки таблицы
    y_offset = 70
    for item in tree.get_children():
        bigram = tree.item(item, 'text')
        probability = tree.item(item, 'values')[0]
        print(bigram)
        print (probability)
        draw.text((50, y_offset), bigram, font=ImageFont.truetype('arial.ttf', 10))
        draw.text((300, y_offset), probability, font=ImageFont.truetype('arial.ttf', 10))
        y_offset += 20
    
    # Сохраняем изображение в формате PNG
    image.save(current_name+'.png', 'PNG')
    messagebox.showinfo("Success", "Table image created!")




current_name = ""
# Создаем окно
root = tk.Tk()
root.geometry("500x500")

root.title("Bigram Language Model")


for c in range(2): root.columnconfigure(index=c, weight=1)
for r in range(6): root.rowconfigure(index=r, weight=1)

# Создаем кнопку "Generate" и привязываем ее к функции generate_name
generate_name_button = tk.Button(root, text="Generate Name", command=generate_name)
generate_name_button.grid(row=0,column=0)

# Создаем кнопку "Create" и привязываем ее к функции create_image
create_button = tk.Button(root, text="Create image", command=create_image)
create_button.grid(row=0,column=1)

# Создаем текстовое поле, где отображается текст с новым именем
text = tk.Label(text=f"Name: {current_name}" ,font=("Cambria", 20))
text.grid(row=1,column=0)

# Создаем таблицу
tree = ttk.Treeview(root, columns=('probability'))
tree.heading('#0', text='Bigram')
tree.heading('probability', text='Probability')

tree.column('#0', stretch=False,width=50,anchor='w')
tree.column('probability', stretch=True ,width=250, anchor='center')
tree.grid(row=3,column=0,columnspan=2)

# Запускаем главный цикл обработки событий
root.mainloop()