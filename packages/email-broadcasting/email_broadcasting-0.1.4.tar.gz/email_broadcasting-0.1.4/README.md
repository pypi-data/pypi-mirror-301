### Stack:

- [x] <a href="https://www.python.org/"><img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-plain.svg" alt="python" width="15" height="15"/>
  Python 3.11+ <br/></a>

### Installation

    pip install email-broadcasting

### Usage

### Asyncio with SSL

    import asyncio

    from email_broadcasting import MailBroadcasterAsyncSmtpSSL


    async def main():
        config = dict(
            login=EMAIL_SERVER_LOGIN,
            password=EMAIL_SERVER_PASSWORD,
            host=EMAIL_SERVER_HOSTNAME,
            port=EMAIL_SERVER_PORT,
        )
        mailer = MailBroadcasterAsyncSmtpSSL(**config)
        await mailer.send_emails(
            recipients=[LIST_OF_RECIPIENTS],
            subject=EMAIL_SUBJECT,
            body=EMAIL_BODY,
            send_from=EMAIL_SENT_FROM,
        )


    if __name__ == '__main__':
        asyncio.run(main())

#### Sync with SSL

    from email_broadcasting import MailBroadcasterSyncSmtpSSL


    def main():
        config = dict(
            login=EMAIL_SERVER_LOGIN,
            password=EMAIL_SERVER_PASSWORD,
            host=EMAIL_SERVER_HOSTNAME,
            port=EMAIL_SERVER_PORT,
        )
        mailer = MailBroadcasterSyncSmtpSSL(**config)
        mailer.send_emails(
            recipients=[LIST_OF_RECIPIENTS],
            subject=EMAIL_SUBJECT,
            body=EMAIL_BODY,
            send_from=EMAIL_SENT_FROM,
        )


    if __name__ == '__main__':
        main()
