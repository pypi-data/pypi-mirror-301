import abc
import asyncio
from typing import Literal

from email_broadcasting.core._base import BaseMailBroadcaster


class MailBroadcasterAsyncBase(BaseMailBroadcaster, abc.ABC):
    async def send_emails(
        self,
        recipients: list[str],
        subject: str,
        body: str,
        send_from: str,
        body_type: Literal["plain", "html"] = "plain",
    ):
        return await asyncio.to_thread(
            self._send_emails,
            recipients=recipients,
            subject=subject,
            body=body,
            send_from=send_from,
            body_type=body_type,
        )


class MailBroadcasterAsyncSmtpSSL(MailBroadcasterAsyncBase):
    pass
