# EasySMTP: A simple SMTP client

EasySMTP is a simple and lightweight SMTP client written in pure Python.It is distributed as a single file module and has no dependencies other than the Python Standard Library.

## Features

- Send plain text email
- Send HTML email
- Send email with attachments
- Guess MIME type of attachments
- Send email with embedded images
- Built-in well-known SMTP servers configuration

## Installation

Install the latest stable release with `pip install easysmtp` or download easysmtp.py into your project.

## Usage

To use it, you need to enable SMTP for your email. You can find instructions on how to enable SMTP for your email service provider on the internet.

```python
import easysmtp


from_addr = 'user@gmail.com'
smtp_username = from_addr # SMTP login username. It's usually your email address.
smtp_password = 'password'

smtp = easysmtp.EasySMTP()
smtp.config(from_addr,
            username=smtp_username, 
            password=smtp_password,)

to_addr = 'to@gmail.com'
subject = 'Hello'

# Send a plain text email
smtp.send_mail(from_addr, to_addr, subject, body='Hello world!')

# Send an HTML email
smtp.send_mail(from_addr, to_addr, subject, html_body='<h1>Hello world!</h1>')

# Send an email with attachments
smtp.send_mail(from_addr, to_addr, subject, body='Hello world!', attachments=['README.md'])

# Send an email with embedded images
html_body = '<p>Hello world!</p><img src="cid:test.png">'
smtp.send_mail(from_addr, to_addr, subject, html_body=html_body, attachments=['test.png'])

# or more control with attachment cid
attachments = [Attachment("tests/测试.png", cid="test.png")]
smtp.send_mail(from_addr, to_addr, subject, html_body=html_body, attachments=attachments)
```

## Built-in SMTP servers

- 126.com
- 163.com
- gmail.com
- outlook.com
- qq.com
- sina.com
- yahoo.com