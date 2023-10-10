import random
import string
import smtplib
import datetime
from email.mime.text import MIMEText

from config.config import email_remetente, senha_remetente

class SendEmail():
    def __init__(self, destinatario) -> None:
        self.destinatario = destinatario
        self.tempo_inicial = None
        self.codigo = self.gerar_codigo_aleatorio()
        self.enviar_email()

    def gerar_codigo_aleatorio(self):
        caracteres = string.ascii_letters + string.digits
        codigo = ''.join(random.choice(caracteres) for i in range(6))
        return codigo


    def enviar_email(self):
        remetente = email_remetente
        senha = senha_remetente

        corpo = f'Seu código de verificação é {self.codigo}'
        assunto = 'Código de verificação'

        msg = MIMEText(corpo)
        msg['Subject'] = assunto
        msg['From'] = remetente
        msg['To'] = self.destinatario

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, self.destinatario, msg.as_string())
            server.quit()
            self.tempo_inicial = datetime.datetime.now()
            print("Email enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar email: {e}")