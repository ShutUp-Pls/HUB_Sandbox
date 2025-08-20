import requests

# URL y encabezados
url = "http://prod-gen.rjcfactura17.com/producto/agregar_gra.aspx"
headers = {
    "Host": "prod-gen.rjcfactura17.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Origin": "http://prod-gen.rjcfactura17.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": "http://prod-gen.rjcfactura17.com/producto/agregar.aspx",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "ASP.NET_SessionId=ysasnkexgnlc5juyu5l0p2w5; login_rut=; idmaquina=4y5boyu5ttmzqp14a4oykhs0; idcliente=prod_f1578; empresa_nombre=; idsession=4y5boyu5ttmzqp14a4oykhs0; empresa=1; usuario=3; usuario_nombre=admin; perfil=1"
}

# Datos del cuerpo de la solicitud
data = {
    "txtporcentaje_iva": "19",
    "txtcodigo": "codigo_prueba3",
    "txtcod_interno": "interno_prueba3",
    "txtnombre": "nombre_prueba3",
    "txtfamilia_producto": "1",
    "txtsubfamilia_producto": "1",
    "txtunidad": "KG",
    "txtiva": "S",
    "txtid_impuestos1": "25",
    "txtprecio_venta": "2512,61",
    "txtprecio_venta_boleta": "2990",
    "txtstock_critico": "6",
    "txtdias_reposion": "9",
    "txtvigente": "S",
    "txtfactor_compra": "0",
    "txtid_producto": ""
}

# Enviar el request POST
response = requests.post(url, headers=headers, data=data)

# Imprimir el resultado
print("Código de estado:", response.status_code)
print("Respuesta del servidor:", response.text)