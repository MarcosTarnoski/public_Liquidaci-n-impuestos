#Standard library imports
import smtplib
from email.message import EmailMessage
import traceback

#Third party imports

#Proyect imports


def send_email(pathFiles, receiver, subject):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'robycoop912@yahoo.com'
    msg['To'] = receiver
    msg.set_content('Adjunto registros a revisar')

    for file in pathFiles:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name[f.name.rfind('\\')+1:] # 'f.name' tira el path del archivo

        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

    # Ingreso a email y envio el objeto msg, que ya tiene todos los atributos configurados
    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
            smtp.login('robycoop912@yahoo.com','nnhqhwgqvospbqqe')
            smtp.send_message(msg)
        print(f"\n## MAIL ENVIADO ## {subject}")
    except smtplib.SMTPAuthenticationError:
        print(traceback.format_exc())
        input("Por favor, enviar EMAIL manualmente. Presione ENTER para continuar...")

# send_email(["IVA Compras - WENTEK SA 202102 - A CARGAR TACTICA.xlsx"], 'marcos98tarnoski@hotmail.com', "IVA Compras")
