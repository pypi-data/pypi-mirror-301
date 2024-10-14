import abc
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class BaseMailBroadcaster(abc.ABC):
    def __init__(
        self,
        login: str,
        password: str,
        host: str,
        port: int,
        timeout: int = 60,
    ):
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.timeout = timeout

    @classmethod
    def _create_message(
        cls,
        send_from: str,
        subject: str,
        body: str,
        body_type: str = "plain",
    ) -> str:
        msg = MIMEMultipart()
        msg["From"] = send_from
        msg["Subject"] = subject

        msg.attach(MIMEText(body, body_type))

        return msg.as_string()

    def _send_emails(
        self,
        recipients: list[str],
        subject: str,
        body: str,
        send_from: str,
        body_type: str = "plain",
    ):
        with smtplib.SMTP_SSL(
            host=self.host,
            port=self.port,
            timeout=self.timeout,
        ) as server:
            server.login(self.login, self.password)
            email_message: str = self._create_message(
                send_from=send_from,
                subject=subject,
                body=body,
                body_type=body_type,
            )
            server.sendmail(
                from_addr=send_from,
                to_addrs=recipients,
                msg=email_message,
            )
