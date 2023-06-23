import tkinter as tk
from tkinter import filedialog
from selenium import webdriver
import time
import openpyxl

class FacebookGroupScraper:
    def __init__(self, root):
        self.root = root
        self.group_url = tk.StringVar()
        self.navegador = tk.StringVar()
        self.miembros = []
        
        # Configuración de la interfaz gráfica
        self.group_url_label = tk.Label(self.root, text="URL del grupo de Facebook:")
        self.group_url_label.pack()
        self.group_url_entry = tk.Entry(self.root, textvariable=self.group_url)
        self.group_url_entry.pack()

        self.navegador_label = tk.Label(self.root, text="Selecciona el navegador a utilizar:")
        self.navegador_label.pack()
        self.navegador_radio1 = tk.Radiobutton(self.root, text="Chrome", variable=self.navegador, value="Chrome")
        self.navegador_radio2 = tk.Radiobutton(self.root, text="Firefox", variable=self.navegador, value="Firefox")
        self.navegador_radio1.pack()
        self.navegador_radio2.pack()

        self.scrape_button = tk.Button(self.root, text="Extraer miembros", command=self.scrape_members)
        self.scrape_button.pack()

        self.export_button = tk.Button(self.root, text="Exportar a Excel", command=self.export_to_excel)
        self.export_button.pack()
        
    def scrape_members(self):
        # Configuración del navegador
        if self.navegador.get() == "Chrome":
            driver = webdriver.Chrome()
        elif self.navegador.get() == "Firefox":
            driver = webdriver.Firefox()
        
        # Navegación a la página del grupo
        driver.get(self.group_url.get())
        time.sleep(5)
        
        # Hacer clic en la pestaña "Miembros"
        members_tab = driver.find_element_by_css_selector("a[href*='view=members']")
        members_tab.click()
        time.sleep(5)
        
        # Desplazarse por la lista de miembros y extraer información
        members_list = driver.find_element_by_css_selector("div[role='tablist']")
        members = members_list.find_elements_by_css_selector("div[role='option']")
        for member in members:
            self.miembros.append({
                "Nombre": member.text,
                "URL": member.find_element_by_css_selector("a").get_attribute("href")
            })
        
        driver.quit()

    def export_to_excel(self):
        # Abrir cuadro de diálogo para guardar archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        
        # Escribir información en archivo Excel
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Miembros"
        worksheet.append(["Nombre", "URL"])
        for member in self.miembros:
            worksheet.append([member["Nombre"], member["URL"]])
        workbook.save(file_path)
        workbook.close()

if __name__ == "__main__":
    # Configuración de la ventana principal
    root = tk.Tk()
    root.title("Extractor de miembros de Facebook")
    root.geometry("400x300")

    # Iniciar aplicación
    app = FacebookGroupScraper(root)
    root.mainloop()
