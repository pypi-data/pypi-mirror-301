#  tgcalls - a Python binding for C++ library by Telegram
#  velar - a library connecting the Python binding with MTProto
#  Copyright (C) 2020-2021 Il`ya (Marshal) <https://github.com/MarshalX>
#
#  This file is part of tgcalls and velar.
#
#  tgcalls and velar is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  tgcalls and velar is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License v3
#  along with tgcalls. If not, see <http://www.gnu.org/licenses/>.


class VelarBaseException(Exception):
    ...


class VelarError(VelarBaseException):
    def __init__(self, caption):
        super().__init__(caption)

class KeyTooLong(VelarBaseException):
    def __init__(self, lengthKey: int):
        super().__init__(f"Keyword Is Too Long, Max Length Is 35 characters But Provided: {lengthKey}")
