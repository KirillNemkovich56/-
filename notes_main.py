#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout 

import json

app = QApplication([])


notes_win = QWidget()
notes_win.setWindowTitle('Заметки')
notes_win.resize(900, 600)

list_notes = QListWidget()
list_notes_label = QLabel('Список')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить')

field_tag = QLineEdit()
field_tag.setPlaceholderText('Введитк тег')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Удалить из заметок')
button_tag_search = QPushButton('Искать заметку по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)
row1 = QHBoxLayout()
row1.addWidget(button_note_create)
row1.addWidget(button_note_del)
row2 = QHBoxLayout()
row2.addWidget(button_note_save)
col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)
row3 = QHBoxLayout()
row3.addWidget(button_tag_add)
row3.addWidget(button_tag_del)
row4 = QHBoxLayout()
row4.addWidget(button_tag_search)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch = 2)
layout_notes.addLayout(col2, stretch = 1)
notes_win.setLayout(layout_notes)

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'добввить заметку', 'название заметки')
    if ok and note_name != '' :
        notes[note_name] = {'tekct': '', 'tegi' : []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['tegi'])
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]['tekct'])
    list_tags.clear()
    list_tags.addItems(notes[key]['tegi'])

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['tekct'] = field_text.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('вы не выбрали заметку!')


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w')as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii = False)
        print(notes)
    else:
        print('заметка для удаления не выбранна!')


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['tegi']:
            notes[key]['tegi'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана')


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['tegi'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['tegi'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('тег для удаления не выбран')

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == 'Искать заметки по тегу' and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes:
                notes_filtered[note] = notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_tags.clear()
        list_notes.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
        print(button_tag_search.text())
    else:
        pass



button_note_create.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)





notes_win.show()

with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)
app.exec_()

