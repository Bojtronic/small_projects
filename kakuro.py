import tkinter as tk
from random import randint
import webbrowser
import subprocess
from tkinter import messagebox
import time
import json


#Colores

gris_claro='#2F3136'
gris_oscuro='#252526'

#Configuracion

configuracion={'nivel':'Facil','reloj':1}

#Definiciones de ventana

win=tk.Tk()
win.title(f'Kakuro 1.0')
win.resizable(tk.FALSE,tk.FALSE)
win.geometry('800x600')
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

width_cuad = 9 * 40 # 9 columnas 
height_cuad = 9 * 40  # 9 filas
    
# contenedor de la cuadricula

cuadricula = tk.Canvas(win, width=width_cuad, height=height_cuad)

# entry y label nombre

nombre=tk.StringVar()
nombre_entry=tk.Entry(win,width=25,bg='white',text='Ingrese su nombre',fg='black',textvariable=nombre)
ingrese_nombre=tk.Label(win, font ='Consolas 10', text = 'Ingrese su nombre',fg='white',bg =gris_claro)
jugador_label=tk.Label(win,font='Consolas 10', text='Jugador:',fg='white',bg =gris_claro)
nombre_label=tk.Label(win,font='Consolas 10', textvariable= nombre,fg='white',bg =gris_claro)

# mensaje inicial

start_label = tk.Label(win, text='\nKakuro\nSeleccione las opciones de la barra de menus',bg=gris_claro,fg='white')
start_label.place(relx=0.5,rely=0.4, anchor='center')

#Labels Cronometro

label_cronometro = tk.Label(win, text="00:00:00", font=("Arial", 24),bg=gris_claro,fg='white')

#Total segundos

total_segundos=0

# Variable para almacenar el número seleccionado
numero_seleccionado = None

#Lista de botones de numeros

botones_numeros = []

#Lista de squares 

squares=[]

#Jugadas realizadas

jugadas_realizadas=[]

#Jugadas Deshecha

jugadas_deshechas=[]

# Función para obtener el estado actual del tablero
def obtener_estado_actual():
    estado = []
    # Obtener los valores de todas las casillas del tablero
    for fila in range(9):
        fila_estado = []
        for columna in range(9):
            casilla = obtener_casilla(fila, columna)
            valor = casilla.numero
            fila_estado.append(valor)
        estado.append(fila_estado)
    return estado

def obtener_casilla(fila, columna):
    return squares[fila][columna]

#Funciones seleccionar numero y casilla

def seleccionar_numero(numero):
    global numero_seleccionado
    numero_seleccionado = numero

def seleccionar_casilla(casilla):
    global numero_seleccionado
    if not casilla.numero and numero_seleccionado:
        casilla.config(text=str(numero_seleccionado),)
        casilla.numero = numero_seleccionado
        numero_seleccionado=None
        jugadas_realizadas.append(casilla)
        jugadas_deshechas.clear()
        
# obtener partida

def obtener_partida(nivel, numero_partida):
    try:
        with open('kakuro2023partidas.dat', 'r') as archivo:
            contenido = archivo.read()
            data = json.loads(contenido)

            if nivel in data and f"partida_{numero_partida}" in data[nivel]:
                partida = data[nivel][f"partida_{numero_partida}"]
                return partida
            else:
                print("No se encontró la partida especificada.")
    except:
        print("Ocurrió un error al leer el archivo.")

    return []

# creacion de cuadricula
def crear_cuadricula(nivel, numero_partida):
    global squares
    partida = obtener_partida(nivel, numero_partida)
    
    # Establece las coordenadas x del canvas en el centro horizontal de la ventana
    cuadricula.place(x=(screen_width-400)/4, y=0)
    cuadricula.configure(bg=gris_claro)
    cuadricula.config(highlightbackground=gris_claro)
    cuadricula.pack(side="top", padx=0, pady=20)  # Agrega padding para separar el canvas del borde de la ventana
    cuadricula.update()  # Actualiza el canvas para que tenga las dimensiones correctas
    
    squares = []
    
    for i in range(9):
        row = []
        for j in range(9): 
            square = tk.Button(cuadricula, width=2, font=('Arial', 20))
            x = ((j + 0.5) * 40 - square.winfo_reqwidth() / 2)
            y = ((i + 0.5) * 40 - square.winfo_reqheight() / 2)
            
            
            if partida[i][j] == 0:
                #square.delete(0, tk.END)  # Elimina cualquier contenido previo del Entry
                square.config(state='disabled')  # Deshabilita el Button
                square.configure(bg='#888888')
                #texto = ""
                #label_x = x + square.winfo_reqwidth() / 2
                #label_y = y + square.winfo_reqheight() / 2
                #label = tk.Label(cuadricula, text=texto, font=('Arial', 8))
                #label.place(x=label_x, y=label_y,anchor='center')
            
            
            if partida[i][j] == 1000: # 1000 indica una pista de columna
                square.config(state='disabled')  # Disable the button
                square.configure(bg='#888888')
                
                pista_columna = 0
                fila = i+1
                      
                while fila < len(partida) and ((partida[fila][j])!=1000 and (partida[fila][j])!=2000 and (partida[fila][j])!=3000):
                    pista_columna += partida[fila][j]
                    fila += 1
                         
                texto = str(pista_columna) + "\\"
                label_x = x + square.winfo_reqwidth() / 2
                label_y = y + square.winfo_reqheight() / 2
                label = tk.Label(cuadricula, text=texto, font=('Arial', 10, 'bold'), fg='green', bg='#888888')
                label.place(x=label_x, y=label_y, anchor='center')
                                    
            if partida[i][j] == 2000: # 2000 indicates a row clue
                square.config(state='disabled')  # Disable the button
                square.configure(bg='#888888')
                
                pista_fila = 0  
                col = j+1
                
                while col < len(partida) and ((partida[i][col])!=1000 and (partida[i][col])!=2000 and (partida[i][col])!=3000):
                    pista_fila += partida[i][col]
                    col += 1
                   

                texto = "\\" + str(pista_fila)
                label_x = x + square.winfo_reqwidth() / 2
                label_y = y + square.winfo_reqheight() / 2
                label = tk.Label(cuadricula, text=texto, font=('Arial', 10, 'bold'), fg='red', bg='#888888')
                label.place(x=label_x, y=label_y, anchor='center')

            if partida[i][j] == 3000: # 3000 indicates a row and column clue
                square.config(state='disabled')  # Disable the button
                square.configure(bg='#888888')
                
                pista_columna = 0
                pista_fila = 0       
                
                fila = i+1
                col = j+1
                
                while fila < len(partida) and ((partida[fila][j])!=1000 and (partida[fila][j])!=2000 and (partida[fila][j])!=3000):
                    pista_columna += partida[fila][j]
                    fila += 1
                
                while col < len(partida) and ((partida[i][col])!=1000 and (partida[i][col])!=2000 and (partida[i][col])!=3000):
                    pista_fila += partida[i][col]
                    col += 1
                   

                texto = str(pista_columna) + "\\" + str(pista_fila)
                label_x = x + square.winfo_reqwidth() / 2
                label_y = y + square.winfo_reqheight() / 2
                label = tk.Label(cuadricula, text=texto, font=('Arial', 10, 'bold'), fg='blue', bg='#888888')
                label.place(x=label_x, y=label_y, anchor='center')
            
            cuadricula.create_window(x, y, anchor="nw", window=square)  # Agrega el cuadro al canvas
            square.numero = None
            square.config(command=lambda casilla=square: seleccionar_casilla(casilla))
            row.append(square)
        
        squares.append(row)

#Variables cronometro

iniciado = False
cronometro_inicio = 0
temporizador_finalizado = False

#Botones 

#Funciones botones menu jugar

def iniciar_juego():
    timer=[horas_entry.get(),minutos_entry.get(),segundos_entry.get()]
    if nombre.get()=='':
        nombre_entry.config(bg='#ffbba8')
        messagebox.showerror("Error", "Debe ingresar un nombre antes de iniciar el juego.")
    elif configuracion['reloj']==3 and (horas_entry.get()=='' and minutos_entry.get()=='' and segundos_entry.get()==''):
        horas_entry.config(bg='#ffbba8')
        minutos_entry.config(bg='#ffbba8')
        segundos_entry.config(bg='#ffbba8')
        messagebox.showerror("Error", "Debe ingresar un tiempo, este debe ser unicamente en numeros enteros.")
    elif (any(i.isalpha()for i in timer[0])) or (any(i.isalpha()for i in timer[1])) or (any(i.isalpha()for i in timer[2])):
        horas_entry.config(bg='#ffbba8')
        minutos_entry.config(bg='#ffbba8')
        segundos_entry.config(bg='#ffbba8')
        messagebox.showerror("Error", "Debe ingresar un tiempo, este debe ser unicamente en numeros enteros.")
    else:
        nombre_entry.place_forget()
        ingrese_nombre.place_forget()

        boton_iniciar.place_forget()

        horas_entry.place_forget()
        horas_label.place_forget()
        minutos_entry.place_forget()
        minutos_label.place_forget()
        segundos_label.place_forget()
        segundos_entry.place_forget()
        
        iniciar_timer()
        if configuracion['reloj']==3:
            time_label.place(relx=0.85,rely=0.2,anchor='center')
        if configuracion['reloj']==1:
            global iniciado, cronometro_inicio
            iniciado = True
            cronometro_inicio = time.time()
            label_cronometro.place(relx=0.85,rely=0.2,anchor='center')
        
        jugador_label.place(relx=0.85,rely=0.3,anchor='center')
        nombre_label.place(relx=0.85,rely=0.35,anchor='center')



        nivel = nivel_var.get()
        
        #numero_partida = randint(1, 3) 
        numero_partida = 1

        crear_cuadricula(nivel, numero_partida)

        # Crear los botones con números

        for i in range(9):
            numero = i + 1
            boton_numero = tk.Button(win, text=str(numero), command=lambda num=numero: seleccionar_numero(num),bg=gris_oscuro,fg='white',width=4)
            boton_numero.place(relx=0.125,rely=(i/15)+0.1)
            botones_numeros.append(boton_numero)

    print('Iniciar Juego')

def deshacer_jugada():
    if jugadas_realizadas:
        # Obtener la última casilla jugada
        ultima_casilla = jugadas_realizadas.pop()
        # Limpiar la casilla deshaciendo la jugada
        ultima_casilla.config(text="")
        #Añade la jugada antes de borrarle el numero
        jugadas_deshechas.append((ultima_casilla,ultima_casilla.numero))
        #borra el numero
        ultima_casilla.numero = None


    print('Deshacer Jugada')

def rehacer_jugada():
    if jugadas_deshechas:
        # Obtener la última casilla deshecha
        ultima_jugada = jugadas_deshechas.pop()
        ultima_casilla=ultima_jugada[0]
        # Restaurar la jugada rehaciendo la casilla
        ultima_casilla.config(text=str(ultima_jugada[1]))
        ultima_casilla.numero=ultima_jugada[1]
        # Agregar la jugada a la pila de jugadas realizadas
        jugadas_realizadas.append(ultima_casilla)
    print('Rehacer Jugada')

def borrar_casilla():
    print('Borrar Casilla')

def borrar_juego():
    for fila in range(9):
        for columna in range(9):
            casilla = obtener_casilla(fila, columna)
            casilla.config(text="")
            casilla.numero=None
    print('Borrar Juego')

def terminar_juego():
    print('Terminar Juego')

def top_10():
    for r_i, row in enumerate(squares):
        for c_i,casilla in enumerate(row):
            print(f'{r_i},{c_i}',casilla.numero)
    print('Top 10')
    
def guardar_juego():
    print('Guardar Juego')

def cargar_juego():
    print('Cargar Juego')

#Botones de opcion jugar, Checkbuttons y Creditos

if True:
    #Botones de opcion jugar

    boton_iniciar=tk.Button(win, text='INICIAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=iniciar_juego)

    boton_deshacer=tk.Button(win, text='DESHACER JUGADA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=deshacer_jugada)
                
    boton_rehacer=tk.Button(win,text='REHACER JUGADA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=rehacer_jugada)

    boton_borrar_casilla=tk.Button(win,text='BORRAR CASILLA', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=borrar_casilla)

    boton_borrar_juego=tk.Button(win,text='BORRAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=borrar_juego)

    boton_terminar=tk.Button(win,text='TERMINAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=terminar_juego)

    boton_top=tk.Button(win,text='TOP 10', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=top_10)

    boton_guardar=tk.Button(win, text='GUARDAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=guardar_juego)

    boton_cargar=tk.Button(win, text='CARGAR JUEGO', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=cargar_juego)

    #Checkbuttons de configuracion

    
    nivel_var = tk.StringVar()
    nivel = tk.Label(win, text='Nivel',bg=gris_claro,fg='white', font='dubai 15')
    
    
    nivel_ck1 = tk.Checkbutton(win, text='Facil', variable=nivel_var, bg=gris_claro, fg='white', selectcolor=gris_oscuro, onvalue='Facil')
    nivel_ck2 = tk.Checkbutton(win, text='Medio', variable=nivel_var, bg=gris_claro, fg='white', selectcolor=gris_oscuro, onvalue='Medio')
    nivel_ck3 = tk.Checkbutton(win, text='Dificil', variable=nivel_var, bg=gris_claro, fg='white', selectcolor=gris_oscuro, onvalue='Dificil')
    nivel_ck4 = tk.Checkbutton(win, text='Experto', variable=nivel_var, bg=gris_claro, fg='white', selectcolor=gris_oscuro, onvalue='Experto')

    nivel_var.set(configuracion['nivel'])

    reloj_var=tk.IntVar()
    reloj= tk.Label(win, text='Tipo de Reloj',bg=gris_claro,fg='white', font='dubai 15')
    reloj_ck1=tk.Checkbutton(win, text='Reloj Normal', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=1)
    reloj_ck2=tk.Checkbutton(win, text='Sin Reloj', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=2)
    reloj_ck3=tk.Checkbutton(win, text='Timer', variable=reloj_var,bg=gris_claro,fg='white',selectcolor=gris_oscuro,onvalue=3)

    reloj_var.set(configuracion['reloj'])

    #Creditos

    acerca_label = tk.Label(win, text='\nKakuro\nVersion: 1.0\nFecha de Creacion: 24/05/2023\nAutor: Sebastián Guillén Guzmán',bg=gris_claro,fg='white')

#Labels y entry horas, minutos y segundos

if True:
    horas_label = tk.Label(win, text="Horas:")
    horas_entry = tk.Entry(win)

    minutos_label = tk.Label(win, text="Minutos:")
    minutos_entry = tk.Entry(win)   

    segundos_label = tk.Label(win, text="Segundos:")    
    segundos_entry = tk.Entry(win)

    time_label = tk.Label(win, text="00:00:00", font=("Arial", 24),bg=gris_claro,fg='white')

#Funcion para aplicar configuracion

def aplicar_config():
    global configuracion
    configuracion['nivel']=nivel_var.get()
    configuracion['reloj']=reloj_var.get()
    if configuracion['reloj']==3:
        horas_label.place(relx=0.8,rely=0.1,anchor='center')
        horas_entry.place(relx=0.8,rely=0.15,anchor='center')

        minutos_label.place(relx=0.8,rely=0.2,anchor='center')
        minutos_entry.place(relx=0.8,rely=0.25,anchor='center')

        segundos_label.place(relx=0.8,rely=0.3,anchor='center')
        segundos_entry.place(relx=0.8,rely=0.35,anchor='center')
    else:
        horas_entry.place_forget()
        horas_label.place_forget()
        minutos_entry.place_forget()
        minutos_label.place_forget()
        segundos_label.place_forget()
        segundos_entry.place_forget()

    print(configuracion)

#Boton para aplicar configuracion
boton_aplicar=tk.Button(win,text='APLICAR', fg='white',bg = gris_oscuro,font ='Dubai 10 bold',command=aplicar_config)

def ocultar_botones():
    for boton in botones_numeros:
        boton.place_forget()

def borrar_items():
    global botones_numeros, squares
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
    
    nombre_entry.place_forget()
    ingrese_nombre.place_forget()
    nombre_label.place_forget()
    jugador_label.place_forget()

    horas_entry.place_forget()
    horas_label.place_forget()
    minutos_entry.place_forget()
    minutos_label.place_forget()
    segundos_label.place_forget()
    segundos_entry.place_forget()

    if configuracion['reloj']==3:
        time_label.place_forget()
    try:
        time_label.config(win, text="00:00:00", font=("Arial", 24),bg=gris_claro,fg='white')
        win.after_cancel(countdown_id)
    except:
        pass
    try:
        label_cronometro.place_forget()
    except:
        pass
        
    global iniciado
    iniciado = False

    ocultar_botones()

    botones_numeros=[]
    squares=[]
    
#Iniciar Timer

def iniciar_timer():
    global total_segundos
    if segundos_entry.get():
        total_segundos = int(segundos_entry.get())
    else:
        total_segundos = 0
    if minutos_entry.get():
        total_segundos += int(minutos_entry.get()) * 60
    if horas_entry.get():
        total_segundos += int(horas_entry.get()) * 3600  
    countdown(total_segundos)

def countdown(tiempo_restante):
    global countdown_id,temporizador_finalizado
    if tiempo_restante <= 0 and configuracion['reloj']==3: #LLAMAR FUNCION QUE HAGA LO QUE CORRESPONDA
        temporizador_finalizado = True
        time_label.place_forget()
        termina_timer = messagebox.askyesno("Opciones", "¿Desea continuar el juego con reloj (Si selecciona 'No' el juego terminara)?", 
                            detail="Selecciona una opción", 
                            icon="question")
        if termina_timer:
            global iniciado, cronometro_inicio
            iniciado = True
            cronometro_inicio = time.time()
            label_cronometro.place(relx=0.85,rely=0.2,anchor='center')
    else:
        minutos, segundos = divmod(tiempo_restante, 60)
        hours, minutos = divmod(minutos, 60)
        
        time_string = "{:02d}:{:02d}:{:02d}".format(hours, minutos, segundos)
        time_label.config(text=time_string)
        
        tiempo_restante -= 1
        countdown_id = win.after(1000, countdown, tiempo_restante)

#Iniciar Cronometro

def actualizar_cronometro(label):
    if iniciado:
        cronometro_transcurrido = time.time() - cronometro_inicio
        if temporizador_finalizado:
            cronometro_transcurrido += total_segundos
        horas = int(cronometro_transcurrido / 3600)
        minutos = int((cronometro_transcurrido % 3600) / 60)
        segundos = int(cronometro_transcurrido % 60)
        cronometro = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        label.config(text=cronometro)
    label.after(10, lambda: actualizar_cronometro(label))

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
    boton_iniciar.place(relx=0.2, rely=0.75, anchor='center')
    boton_deshacer.place(relx=0.2, rely=0.85, anchor='center')
    boton_rehacer.place(relx=0.2, rely=0.95, anchor='center')
    boton_borrar_casilla.place(relx=0.5, rely=0.75, anchor='center')
    boton_borrar_juego.place(relx=0.5, rely=0.85, anchor='center')
    boton_terminar.place(relx=0.5, rely=0.95, anchor='center')
    boton_top.place(relx=0.8, rely=0.75, anchor='center')
    boton_guardar.place(relx=0.8, rely=0.85, anchor='center')
    boton_cargar.place(relx=0.8, rely=0.95, anchor='center')

    nombre_entry.place(relx=0.5, rely=0.45,anchor=tk.CENTER)  
    ingrese_nombre.place(relx=0.5, rely=0.4,anchor=tk.CENTER) 
    nombre_entry.config(bg='white')
    nombre_entry.delete(0, 'end')

    if configuracion['reloj']==3:
        horas_label.place(relx=0.85,rely=0.1,anchor='center')
        horas_entry.place(relx=0.85,rely=0.15,anchor='center')

        minutos_label.place(relx=0.85,rely=0.2,anchor='center')
        minutos_entry.place(relx=0.85,rely=0.25,anchor='center')

        segundos_label.place(relx=0.85,rely=0.3,anchor='center')
        segundos_entry.place(relx=0.85,rely=0.35,anchor='center')

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

    if configuracion['reloj']==3:
        horas_label.place(relx=0.8,rely=0.1,anchor='center')
        horas_entry.place(relx=0.8,rely=0.15,anchor='center')

        minutos_label.place(relx=0.8,rely=0.2,anchor='center')
        minutos_entry.place(relx=0.8,rely=0.25,anchor='center')

        segundos_label.place(relx=0.8,rely=0.3,anchor='center')
        segundos_entry.place(relx=0.8,rely=0.35,anchor='center')

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

#Inicia cronometro

actualizar_cronometro(label_cronometro)

# Insertarla en la ventana principal.
win.config(menu=barra)

win.mainloop()


