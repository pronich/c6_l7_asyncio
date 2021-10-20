import sqlite3
import asyncio
import smtplib
from settings import EMAIL, PASSWORD

sender = EMAIL
password = PASSWORD


async def send_email(receiver, first_name):
    subject = f'Рады, что вы с нами!'
    content = f'Уважаемый, {first_name}!\nСпасибо, что пользуетесь нашим сервисом объявлений.'

    mail_lib = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mail_lib.login(sender, password)

    msg = 'From: %s\r\nTo: %s\r\nContent-Type: text/plain; charset="utf-8"\r\nSubject: %s\r\n\r\n' % (
        sender, receiver, subject)
    msg += content

    result = await mail_lib.sendmail(sender, receiver, msg.encode('utf8'))

    await mail_lib.quit()

    return result


async def main():
    conn = sqlite3.connect('contacts.db')
    curs = conn.cursor()
    contacts = curs.execute("SELECT * FROM contacts limit 2;").fetchall()

    mail = await asyncio.gather(*[send_email(contact[3], contact[1]) for contact in contacts])
    print('and now')
    return mail


if __name__ == "__main__":
    asyncio.run(main())
