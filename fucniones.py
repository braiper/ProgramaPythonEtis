import re
import os
import sys
from tkinter import messagebox


class Funciones:
    def __init__(self):
        self.zonaP1 = ["SAN FERNANDO", "SAN ISIDRO", "VICENTE LOPEZ", "SAN MARTIN", "TRES DE FEBRERO", "HURLINGHAM", "ITUZAINGÓ", "MORON", "LA MATANZA NORTE", "LOMAS DE ZAMORA", "LANUS", "AVELLANEDA"]
        self.zonaP2 = ["TIGRE", "MALVINAS ARGENTINAS", "JOSE C PAZ", "SAN MIGUEL", "MORENO", "MERLO", "LA MATANZA SUR", "EZEIZA", "ESTEBAN ECHEVERRIA", "ALMIRANTE BROWN", "FLORENCIO VARELA", "QUILMES", "BERAZATEGUI"]

    @staticmethod
    def toma_num(cadena):
        """
        Toma el primer número que encuentra en la cadena dada.
        """
        if not cadena:
            return ""

        p = False
        aux = ""
        for c in cadena:
            if re.match(r"^[0-9]$", c):
                p = True
                aux += c
            elif p:
                break

        return aux

    def carga_cp(self, dir):
        """
        Carga la lista de códigos postales y su respectiva zona desde el archivo dado.
        """
        if not os.path.isfile(dir):
            messagebox.showerror("Error", "Faltan archivos de inicio")
            sys.exit()

        codigos = []
        with open(dir, "r") as f:
            f.readline()  # Saltar primera línea
            for linea in f:
                auxLinea = linea.strip().split(";")
                cp = ""
                zona = ""
                for i, pos in enumerate(auxLinea):
                    if i == 0:
                        cp = pos.replace("\"", "")
                    elif i == 2:
                        zona = pos.replace("\"", "")
                
                codigos.append({"cp": cp, "zona": zona})

        return codigos
def buscar_reemplazar(cadena, palabra):
    position = cadena.find(palabra)
    aux = cadena[:position + len(palabra)]
    cadena = cadena[position + len(palabra):]
    return aux, cadena

def buscar_reemplazar_ref(cadena, palabra):
    aux = ""
    position = cadena.find(palabra)
    if position >= 0:
        aux = cadena[:position + len(palabra)]
        cadena = cadena[position + len(palabra):]
    return aux, cadena

class TCombo:
    def __init__(self, denominacion, productos):
        self.Denominacion = denominacion
        self.Productos = productos
        
    def reset(self):
        self.Denominacion = ""
        self.Productos = []

class ClaseProd:
    def __init__(self, denominacion, cantidad):
        self.Denominacion = denominacion
        self.Cantidad = cantidad

def busca_combo_rep(combos):
    aux = []
    for i in range(len(combos)):
        if combos[i].Denominacion != "":
            aux.append(TCombo(Denominacion=combos[i].Denominacion,
                              Productos=[ClaseProd(Denominacion=combos[i].Productos[0].Denominacion,
                                                   Cantidad=combos[i].Productos[0].Cantidad)]))
            for n in range(len(combos)-1, i, -1):
                if combos[i].Denominacion == combos[n].Denominacion and combos[i].Denominacion != "":
                    aux[i].Productos.append(ClaseProd(Denominacion=combos[n].Productos[0].Denominacion,
                                                      Cantidad=combos[n].Productos[0].Cantidad))
                    combos[n].reset()
    for objeto in combos:
        objeto.reset()
    f = 0
    for objeto in aux:
        if objeto.Denominacion != "":
            combos[f].Denominacion = objeto.Denominacion
            combos[f].Productos = objeto.Productos
            f += 1
def carga_combo(combos):
    if os.path.exists("Combos.csv"):
        combos.clear()
        with open("Combos.csv") as file:
            next(file)  # saltar primera línea
            for line in file:
                parts = line.strip().split(";")
                if len(parts) != 3:
                    continue
                
                combo = TCombo()
                combo.denominacion = parts[0].replace('"', '')
                combo.productos = [ClaseProd(parts[1].replace('"', ''), int(parts[2].replace('"', '')))]
                combos.append(combo)
        
        busca_combo_rep(combos)
    else:
        messagebox.showerror("Alerta", "Archivo de inicio no encontrado C01")


def busca_combo_rep(combos):
    aux = []
    for i in range(len(combos)):
        combo = combos[i]
        if combo.denominacion == "":
            continue
        
        aux.append(TCombo(denominacion=combo.denominacion, productos=[ClaseProd(combo.productos[0].denominacion, combo.productos[0].cantidad)]))
        
        for j in range(len(combos)-1, i, -1):
            other = combos[j]
            if other.denominacion == combo.denominacion:
                aux[i].productos.append(ClaseProd(other.productos[0].denominacion, other.productos[0].cantidad))
                other.reset()
    
    for combo in combos:
        combo.reset()
    
    i = 0
    j = 0
    for combo in aux:
        j = 0
        if combo.denominacion != "":
            current_combo = combos[i]
            current_combo.denominacion = combo.denominacion
            
            for prod in combo.productos:
                if len(current_combo.productos) <= j:
                    current_combo.productos.append(ClaseProd(prod.denominacion, prod.cantidad))
                else:
                    current_combo.productos[j].denominacion = prod.denominacion
                    current_combo.productos[j].cantidad = prod.cantidad
                j += 1
            
            i += 1
def compara_ped_com(etiquetas, combos):
    for etiqueta in etiquetas:
        for producto_etiqueta in etiqueta.Productos:
            if etiqueta.Id != "" and producto_etiqueta.Denominacion != "":
                for combo in combos:
                    if combo.Denominacion != "" and combo.Denominacion == producto_etiqueta.Denominacion:
                        cantiComb = len(combo.Productos)
                        for i, producto_combo in enumerate(combo.Productos):
                            if producto_combo.Denominacion == "":
                                cantiComb = i
                                break
                        catiprodPed = etiqueta.Productos.index(producto_etiqueta) + 1
                        cantidad = producto_etiqueta.Cantidad
                        producto_etiqueta.Denominacion = combo.Productos[0].Denominacion
                        producto_etiqueta.Cantidad = combo.Productos[0].Cantidad * cantidad
                        if cantiComb > 1:
                            for i in range(1, len(combo.Productos)):
                                producto_nuevo = ClaseProd(
                                    Denominacion=combo.Productos[i].Denominacion,
                                    Cantidad=combo.Productos[i].Cantidad * cantidad
                                )
                                etiqueta.Productos.insert(catiprodPed + i - 1, producto_nuevo)
from datetime import datetime
hoy = datetime.now()
def toma_num(numero):
    return str(numero)

def insertar(etiquetas, vendedor1, vendedor2, vendedor3, vendedor4):
    px = 30
    for etiqueta in etiquetas:
        if etiqueta.vendedor != vendedor1 and etiqueta.vendedor != vendedor2 and etiqueta.vendedor != vendedor3 and etiqueta.vendedor != vendedor4 and etiqueta.vendedor != "999999999":
            messagebox.showerror("Alerta", "Etiqueta Corrupta")
            sys.exit()
        else:
            if etiqueta.id == "":
                break
            else:
                if etiqueta.encontrado:
                    aux_eti = etiqueta.eti
                    aux = buscar_reemplazar("^XA", aux_eti)
                    aux += buscar_reemplazar("Logo Meli^FS", aux_eti)
                    aux += "^FO20, 1210^A0N, 30, 30^FDCant     Producto^FS"
                    for j in range(len(etiqueta.productos)):
                        if j >= 8:
                            aux += "^FO20, " + str(1245 + px * (j)) + "^A0N, 25, 30,^FDMas de 8 Productos^FS"
                            break
                        else:
                            aux += "^FO20, " + str(1245 + px * (j)) + "^A0N, 25, 23,^FD" + str(etiqueta.productos[j].cantidad) + " | " + etiqueta.productos[j].denominacion + "^FS"
                    aux += "^FO30,1520^A0N,40,40^FD" + etiqueta.pedido + "^FS" #PEDIDO
                    if etiqueta.vendedor == vendedor1:
                        nombre = "RC4ASPAS"
                    elif etiqueta.vendedor == vendedor2:
                        nombre = "OMRON ARGENTINA"
                    elif etiqueta.vendedor == vendedor3:
                        nombre = "FEMMTO ARGENTINA"
                    elif etiqueta.vendedor == vendedor4:
                        nombre = "DISBYTE HEALTHCARE"
                    else:
                        nombre= "N/A"
                    hoy = datetime.now()
                    aux += "^FO30,1565^A0N,25,20^FD" + nombre + "^FS" #Venta
                    aux += "^FO250,1565^A0N,25,20^FD" + hoy.strftime('%Y-%m-%d %H:%M:%S') + "^FS"
                    aux += "^BY3,180,50^FO300,1510^BC^FD" + toma_num(etiqueta.envio) + "^FS"
                    if etiqueta.flex:
                        aux += "^FO20,1060^A0N,25,20^FD" + "Observaciones: " + etiqueta.observaciones + "^FS"
                    aux += "^FO20,1165^A0N,25,20^FD" + etiqueta.canal_venta + "^FS"
                    aux += "^FO0,1200^Gb800,398,2,,0^FS^FO0,1500^Gb800,1,1,,0^FS" #recuadro
                    aux += buscar_reemplazar("^XZ", aux_eti)
                    aux += "^XA^MCY^XZ"
                    etiqueta.eti = aux
                    
def buscar_reemplazar(buscar, cadena):
    reemplazo = ''
    if buscar in cadena:
        reemplazo = cadena.replace(buscar, '')
    return reemplazo

def insertar_nuevo_al_reves(etiquetas, vendedor1, vendedor2, vendedor3, vendedor4):
    px = 30
    aux = ""
    nombre = ""
    auxEti = ""
    for etiqueta in etiquetas:
        if (etiqueta.Vendedor != vendedor1 and etiqueta.Vendedor != vendedor2 and etiqueta.Vendedor != vendedor3 and etiqueta.Vendedor != vendedor4 and etiqueta.Vendedor != "999999999"):
            messagebox.showerror("Alerta", "Etiqueta Corrupta")
            # HACER MENCIÓN DE CIERRE
        else:
            if etiqueta.Id == "":
                break
            else:
                if etiqueta.Encontrado:
                    auxEti = etiqueta.Eti
                    aux = buscar_reemplazar(auxEti, "^XA")
                    aux += buscar_reemplazar(auxEti, "^LH5,15")
                    aux += "^FO20, 15^A0N, 30, 30^FDCant     Producto^FS"
                    aux = aux.replace("^LH5,15", "^LH5,45")
                    for j in range(len(etiqueta.Productos)):
                        if j >= 8:
                            aux += "^FO20, " + str(50 + px * j) + "^A0N, 25, 30,^FDMas de 8 Productos^FS"
                            break
                        elif etiqueta.Productos[j].Cantidad > 0:
                            aux += "^FO20, " + str(50 + px * j) + "^A0N, 25, 23,^FD" + str(etiqueta.Productos[j].Cantidad) + " | " + etiqueta.Productos[j].Denominacion + "^FS"
                    aux += "^FO30,230^A0N,40,40^FD" + etiqueta.Pedido + "^FS" #PEDIDO
                    if etiqueta.Vendedor == vendedor1:
                        nombre = "DILUCE"
                    else:
                        if etiqueta.Vendedor == vendedor2:
                            nombre = "SAJO"
                        elif etiqueta.Vendedor == vendedor3 or etiqueta.Vendedor == vendedor4:
                            nombre = "SAJO"
                        else:
                            nombre = "N/A"
                    if etiqueta.Flex:
                        try:
                            carga_zonas()
                            finalPosition = etiqueta.Eti.find("Nickname")
                            part_of_eti = etiqueta.Eti[:finalPosition]
                            zona_encontrada = False
                            if "CABA" in part_of_eti:
                                etiqueta.ZonaFlex = "CABA"
                                zona_encontrada = True
                            else:
                                for p1 in zonaP1:
                                    if p1 in part_of_eti:
                                        zona_encontrada = True
                                        etiqueta.ZonaFlex = "P1"
                                        break
                                if not zona_encontrada:
                                    for p2 in zonaP2:
                                        if p2 in part_of_eti:
                                            zona_encontrada = True
                                            etiqueta.ZonaFlex = "P2"
                                            break
                            if not zona_encontrada:
                                etiqueta.ZonaFlex = "S/Z"
                        except:
                            etiqueta.ZonaFlex = "Error"
                        hoy = datetime.now()
            aux = f"^FO30,275^A0N,25,20^FD{etiqueta.ZonaFlex}^FS"  # Venta
            aux += f"^FO250,275^A0N,25,20^FD{hoy}^FS"
            aux += f"^BY3,180,50^FO450,220^BC^FD{toma_num(etiqueta.Er)}^FS"
            aux += f"^FO500,15^A0N,25,20^FD{etiqueta.Id}^FS"
            aux += "^FO0,0^Gb800,315,2,,0^FS^FO0,210^Gb800,1,1,,0^FS"  # recuadro
            aux += "^LH5,360"
            
            aux = buscar_reemplazar(aux, "^XZ")
            etiqueta.Eti = aux
            
    etiquetas.sort(key=lambda x: x.Pedido)
    return etiquetas
