#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import hasnain_kk
from hasnain_kk import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~hasnain_kk.types.InlineQueryResultCachedAudio`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedDocument`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedAnimation`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedPhoto`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedSticker`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedVideo`
    - :obj:`~hasnain_kk.types.InlineQueryResultCachedVoice`
    - :obj:`~hasnain_kk.types.InlineQueryResultArticle`
    - :obj:`~hasnain_kk.types.InlineQueryResultAudio`
    - :obj:`~hasnain_kk.types.InlineQueryResultContact`
    - :obj:`~hasnain_kk.types.InlineQueryResultDocument`
    - :obj:`~hasnain_kk.types.InlineQueryResultAnimation`
    - :obj:`~hasnain_kk.types.InlineQueryResultLocation`
    - :obj:`~hasnain_kk.types.InlineQueryResultPhoto`
    - :obj:`~hasnain_kk.types.InlineQueryResultVenue`
    - :obj:`~hasnain_kk.types.InlineQueryResultVideo`
    - :obj:`~hasnain_kk.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "hasnain_kk.Client"):
        pass
