partidas={"FÁCIL":(
),'MEDIO':(( 2, 25, 1, 2, 4 ),
( 2, 44, 1, 3, 8 ),
( 2, 20, 1, 5, 3 ),
( 2, 10, 1, 6, 3 ),
( 2, 39, 1, 8, 8 ),
( 2, 16, 1, 9, 2),
( 1, 10, 2, 1, 2 ),
( 1, 10, 2, 4, 2),
( 1, 8, 2, 7, 2),
(1, 16, 3, 1, 2),
),'DIFICIL':(),'EXPERTO':()}

import tkinter as tk
from random import randint
import webbrowser
import subprocess
import Juego

#Colores

gris_claro='#2F3136'
gris_oscuro='#252526'

#Configuracion

configuracion={'nivel':1,'reloj':1}

#Definiciones de ventana

win=tk.Tk()
win.title(f'Kakuro 1.0')
win.resizable(tk.FALSE,tk.FALSE)
win.geometry('800x500')
win.configure(bg=gris_claro)

# Obtiene las dimensiones de la pantalla
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

# Calcula las coordenadas para centrar la pantalla
x = (screen_width // 4) - (win.winfo_reqwidth() // 2)
y = (screen_height // 4) - (win.winfo_reqheight() // 2)

# Set the window position
win.geometry("+{}+{}".format(x, y))

#Evita que el menu se desacople de la vantana

win.option_add('*tearOff', tk.FALSE)


# Calcula el ancho y alto del canvas en función del número de filas y columnas
width_cuad = 9 * 40  # 9 columnas 
height_cuad = 9 * 40  # 9 filas
    
# contenedor de la cuadricula
cuadricula = tk.Canvas(win, width=width_cuad, height=height_cuad)


# mensaje inicial

start_label = tk.Label(win, text='\nKakuro\nSeleccione las opciones de la barra de menus',bg=gris_claro,fg='white')
start_label.place(relx=0.5,rely=0.4, anchor='center')


# creacion de cuadricula
def crear_cuadricula():
    
    # Establece las coordenadas x del canvas en el centro horizontal de la ventana
    cuadricula.place(x=(screen_width-400)/4, y=0)
    cuadricula.configure(bg=gris_claro)
    cuadricula.config(highlightbackground=gris_claro)
    #cuadricula.pack(side="top", padx=0, pady=0)  # Agrega padding para separar el canvas del borde de la ventana
    cuadricula.update()  # Actualiza el canvas para que tenga las dimensiones correctas
    
    squares = []
    
    for i in range(9):
        row = []
        for j in range(9): 
            square = tk.Entry(cuadricula, width=2, font=('Arial', 22))
            if j%2 == 0:
                
            
                texto = "15/56"
                label = tk.Label(square, text=texto, font=('Arial', 8))
                square.delete(0, tk.END) # Elimina cualquier contenido previo del Entry
                
                #square.insert(0, texto) # Inserta el texto en el Entry
                #square.configure(bg="red")
                #label.configure(bg='gray')
                square.config(state='disabled') # Deshabilita el Entry
                #label.config(state='disabled')
                # Calcula la posición x del cuadro centrado en la celda
                x = (j + 0.5) * 40 - square.winfo_reqwidth()/2
                
                # Calcula la posición y del cuadro centrado en la celda
                y = (i + 0.5) * 40 - square.winfo_reqheight()/2
                
                label.place(x=x, y=y)
                
            # Calcula la posición x del cuadro centrado en la celda
            x = (j + 0.5) * 40 - square.winfo_reqwidth()/2
                
            # Calcula la posición y del cuadro centrado en la celda
            y = (i + 0.5) * 40 - square.winfo_reqheight()/2
            
            cuadricula.create_window(x, y, anchor="nw", window=square)  # Agrega el cuadro al canvas
            row.append(square)
        
        squares.append(row)
    
#Botones de opcion jugar

boton_iniciar=tk.Button(win, text='INICIAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.iniciar_juego)

boton_deshacer=tk.Button(win, text='DESHACER JUGADA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.deshacer_jugada)
            
boton_rehacer=tk.Button(win,text='REHACER JUGADA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.rehacer_jugada)

boton_borrar_casilla=tk.Button(win,text='BORRAR CASILLA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.borrar_casilla)

boton_borrar_juego=tk.Button(win,text='BORRAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.borrar_juego)

boton_terminar=tk.Button(win,text='TERMINAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.terminar_juego)

boton_top=tk.Button(win,text='TOP 10', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.top_10)

boton_guardar=tk.Button(win, text='GUARDAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.guardar_juego)

boton_cargar=tk.Button(win, text='CARGAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=Juego.cargar_juego)

#Checkbuttons de configuracion

nivel_var=tk.IntVar()
nivel = tk.Label(win, text='Nivel',bg=gris_claro,fg='white', font='dubai 15')
nivel_ck1=tk.Checkbutton(win, text='Facil', variable=nivel_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=1)
nivel_ck2=tk.Checkbutton(win, text='Medio', variable=nivel_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=2)
nivel_ck3=tk.Checkbutton(win, text='Dificil', variable=nivel_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=3)
nivel_ck4=tk.Checkbutton(win, text='Experto', variable=nivel_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=4)
nivel_var.set(configuracion['nivel'])

reloj_var=tk.IntVar()
reloj= tk.Label(win, text='Tipo de Reloj',bg=gris_claro,fg='white', font='dubai 15')
reloj_ck1=tk.Checkbutton(win, text='Reloj Normal', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=1)
reloj_ck2=tk.Checkbutton(win, text='Sin Reloj', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=2)
reloj_ck3=tk.Checkbutton(win, text='Timer', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=3)

reloj_var.set(configuracion['reloj'])

#Creditos

acerca_label = tk.Label(win, text='\nKakuro\nVersion: 1.0\nFecha de Creacion: 24/05/2023\nAutor: Sebastián Guillén Guzmán',bg=gris_claro,fg='white')

#Funcion para aplicar configuracion

def aplicar_config():
    global configuracion
    configuracion['nivel']=nivel_var.get()
    configuracion['reloj']=reloj_var.get()
    print(configuracion)

#Boton para aplicar configuracion
boton_aplicar=tk.Button(win,text='APLICAR', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=aplicar_config)

def borrar_items():
    nivel.place_forget()
    nivel_ck1.place_forget()
    nivel_ck2.place_forget()
    nivel_ck3.place_forget()
    nivel_ck4.place_forget()   

    reloj.place_forget()
    reloj_ck1.place_forget()
    reloj_ck2.place_forget()
    reloj_ck3.place_forget()

    boton_aplicar.place_forget()

    acerca_label.place_forget()
    
    start_label.place_forget()
    
    boton_iniciar.place_forget()
    boton_deshacer.place_forget()
    boton_rehacer.place_forget()
    boton_borrar_casilla.place_forget()
    boton_borrar_juego.place_forget()
    boton_terminar.place_forget()
    boton_top.place_forget()
    boton_guardar.place_forget()
    boton_cargar.place_forget()
    

    ayuda_label.place_forget()
    navegador_boton.place_forget()
    archivo_boton.place_forget()
    
    
    cuadricula.pack()
    cuadricula.pack_forget()
    
    
        
        
#Funciones para abrir archivos ------------ AGREGAR LINK Y PATH AL TERMINAR

def abre_internet():
    try:
        path = 'agregar link'
        webbrowser.open_new(path)
    except:
        print('Ha ocurrido un error. Revise su conexion a internet')

def abre_explorador():
    try:
        path='manual_de_usuario_kakuro.pdf'
        subprocess.Popen([path], shell=True)
    except:
        print('ERROR: No se pudo encontrar el archivo')

#Ayuda Label y Botones

ayuda_label=tk.Label(win, text='DONDE DESEA DESPLEGAR EL MANUAL DE USUARIO?\n SI NO SUCEDE NADA REVISE LA CONSOLA PARA SABER QUE SUCEDIO',bg=gris_claro,fg='white')

navegador_boton=tk.Button(win, text='ABRIR POR INTERNET', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=abre_internet)

archivo_boton=tk.Button(win, text='ABRIR DESDE EXPLORADOR DE ARCHIVOS', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=abre_explorador)

#Funciones barra de menus

def jugar():
    borrar_items()
    boton_iniciar.place(relx=0.2, rely=0.77, anchor='center')
    boton_deshacer.place(relx=0.2, rely=0.87, anchor='center')
    boton_rehacer.place(relx=0.2, rely=0.97, anchor='center')
    boton_borrar_casilla.place(relx=0.5, rely=0.77, anchor='center')
    boton_borrar_juego.place(relx=0.5, rely=0.87, anchor='center')
    boton_terminar.place(relx=0.5, rely=0.97, anchor='center')
    boton_top.place(relx=0.8, rely=0.77, anchor='center')
    boton_guardar.place(relx=0.8, rely=0.87, anchor='center')
    boton_cargar.place(relx=0.8, rely=0.97, anchor='center')
        
    crear_cuadricula()
    
    print('jugar')

def config():
    borrar_items()

    boton_aplicar.place(relx=0.1, rely=0.9,anchor=tk.CENTER)

    nivel_var=tk.IntVar()
    nivel.place(relx=0.04,rely=0.05,anchor=tk.CENTER)
    nivel_ck1.place(relx=0.01,rely=0.1)
    nivel_ck2.place(relx=0.075,rely=0.1)
    nivel_ck3.place(relx=0.15,rely=0.1)
    nivel_ck4.place(relx=0.22,rely=0.1)
    

    reloj_var=tk.IntVar()
    reloj.place(relx=0.08,rely=0.2,anchor=tk.CENTER)
    reloj_ck1.place(relx=0.01,rely=0.25)
    reloj_ck2.place(relx=0.13,rely=0.25)
    reloj_ck3.place(relx=0.23,rely=0.25)

def acerca_de():
    borrar_items()

    acerca_label.place(relx=0.5,rely=0.4, anchor='center')
    

def ayuda():
    borrar_items()
    ayuda_label.place(relx=0.5,rely=0.3,anchor='center')
    navegador_boton.place(relx=0.3,rely=0.7,anchor='center')
    archivo_boton.place(relx=0.7,rely=0.7,anchor='center')
    print('manual')

def salir():
    win.quit()


# Crear una barra de menús.

barra = tk.Menu()
config_menu=tk.Menu(barra, tearoff=False)

#Se agregan las opciones
barra.add_command(label='Jugar',command=jugar)
barra.add_command(label='Configuracion',command=config)
barra.add_command(label='Acerca De',command=acerca_de)
barra.add_command(label='Ayuda',command=ayuda)
barra.add_command(label='Salir',command=salir)
jugar



# Insertarla en la ventana principal.
win.config(menu=barra)

win.mainloop()


