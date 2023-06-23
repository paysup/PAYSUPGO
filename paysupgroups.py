import tkinter as tk
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Crear la ventana principal
root = tk.Tk()
root.title("Extractor de Miembros")

# Crear un cuadro de entrada para la URL del grupo
url_label = tk.Label(root, text="URL del Grupo:")
url_label.pack()
url_entry = tk.Entry(root)
url_entry.pack()

# Crear un cuadro de entrada para las palabras clave
keyword_label = tk.Label(root, text="Palabras Clave:")
keyword_label.pack()
keyword_entry = tk.Entry(root)
keyword_entry.pack()

# Crear un botón para extraer la lista de miembros
extract_button = tk.Button(root, text="Extraer Miembros")
extract_button.pack()

# Crear un botón para descargar la lista de miembros
download_button = tk.Button(root, text="Descargar Miembros")
download_button.pack()

# Crear una lista para almacenar los miembros extraídos
members_list = []

def extract_members():
    # Obtener la URL y las palabras clave
    url = url_entry.get()
    keywords = keyword_entry.get().split(",")
    
    # Inicializar el driver de Selenium
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Esperar hasta que se cargue la página
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='grid']")))
    
    # Buscar los miembros que contengan las palabras clave
    members = []
    for keyword in keywords:
        search_box = driver.find_element(By.XPATH, "//input[@aria-label='Buscar miembros']")
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@role='grid']")))
        
        member_list = driver.find_elements(By.XPATH, "//div[@role='grid']/div")
        for member in member_list:
            if keyword.lower() in member.text.lower():
                members.append(member.text)
    
    # Cerrar el driver de Selenium
    driver.quit()
    
    # Añadir los miembros a la lista
    members_list.append(members)
    
    # Mostrar los miembros en la pantalla
    members_text = "\n".join(members)
    members_label = tk.Label(root, text=members_text)
    members_label.pack()

def download_members():
    # Guardar los miembros en un archivo Excel
    members_df = pd.DataFrame(members_list)
    members_df.to_excel("members.xlsx", index=False)
    
    # Descargar la lista de miembros del archivo Excel
    members_text = "\n".join(members_df.stack().tolist())
    
    # Mostrar la lista de miembros en la pantalla
    members_label = tk.Label(root, text=members_text)
    members_label.pack()

# Configurar los botones para llamar a las funciones correspondientes
extract_button.config(command=extract_members)
download_button.config(command=download_members)

# Mostrar la ventana
root.mainloop()
