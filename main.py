#Importation des modules
import tkinter as tk
import qrcode
import os
from PIL import Image, ImageTk
from tkinter import filedialog
from io import BytesIO
import win32clipboard

#Configuration de tkinter
win = tk.Tk()
win.title("QR Code Generator")
win.geometry('320x600')
win.minsize(320,600)
win.maxsize(320,600)

#Fonction permettant de convertir un lien en un QR Code et d'afficher sur l'app avec les options de save et copy
def create_qrcode():
    global img,img2,img3
    if link.get() != "":
        img = qrcode.make(link.get())       #Création du QR Code
        img.save("tmp.png")                 #Save temporaire
        img2 = Image.open("tmp.png")        #Load de l'image avec le module PIL
        resize = img2.resize((250,250))     #Resize de l'image
        img3 = ImageTk.PhotoImage(resize)   #Création de l'image finale

        #Création des éléments du QR Code (Image, save, copy, nouveau)
        image_qr_code = tk.Label(win,image=img3)
        save_button = tk.Button(win, text="Save", font=('Segoe UI Black',"20"),command=save_img)
        copy_button = tk.Button(win, text="Copy", font=('Segoe UI Black',"20"),command=copy_img)

        #Affichage de ces éléments
        image_qr_code.grid(row=3, column=0, padx=0, pady=20, rowspan=1, columnspan=2)
        save_button.grid(row=4, column=0, padx=0, pady=0, rowspan=1, columnspan=1)
        copy_button.grid(row=4, column=1, padx=0, pady=0, rowspan=1, columnspan=1)

        #Supprime l'image sauvegardé temporairement
        os.remove("tmp.png")
    else:
        #Si l'entry ne contient aucun lien, on créée une fenêtre d'erreur
        win2 = tk.Toplevel(win)
        win2.title("ERREUR")
        #Création des éléments de la fenêtre d'erreur
        error_text = tk.Label(win2, text="ERREUR: Aucun lien",font=('Segoe UI Black',"20"))
        button_ok = tk.Button(win2, text="OK",font=('Segoe UI Black',"16"), command=win2.destroy)
        #Affichage des éléments de la fenêtre d'erreur
        error_text.grid(row=0, column=0, padx=7, pady=10, rowspan=1, columnspan=1)
        button_ok.grid(row=1, column=0, padx=0, pady=5, rowspan=1, columnspan=1)

#Fonction permettant de sauvegarder l'image du QR Code dans le dossier voulu
def save_img():
    file = filedialog.asksaveasfile(filetypes=[("PNG File",".png")],defaultextension=[("PNG File",".png")],mode='w')
    abs_path = os.path.abspath(file.name)
    img2.save(abs_path)

#Fonction permettant de copier l'image du QR Code dans le presse-papier
def copy_img():
    output = BytesIO()
    img2.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

#Création des éléments Tkinter
title = tk.Label(win, text = "Bienvenue sur \nQR Code Generator", font=('Segoe UI Black',"23"))
link = tk.StringVar()
entry = tk.Entry(win, font=('Segoe UI Black',"17"),textvariable=link)
button_generate = tk.Button(win, text="Générer QR Code", font=('Segoe UI Black',"23"), command = create_qrcode)

#Afficahge des éléments TKinter
title.grid(row=0, column=0, padx=10, pady=5, rowspan=1, columnspan=2)
entry.grid(row=1, column=0, padx=0, pady=5, rowspan=1, columnspan=2)
button_generate.grid(row=2, column=0, padx=0, pady=5, rowspan=1, columnspan=2)

#Lancement de l'application tkinter
win.mainloop()