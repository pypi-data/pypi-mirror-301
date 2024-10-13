"""
:filename: whintpy.connection.__init__.py
:author: Brigitte Bigi
:contributor: Chiheb Bradai
:contact: contact@sppas.org

.. _This file is part of WhintPy: https://whintpy.sourceforge.io
..
    -------------------------------------------------------------------------

    ██╗    ██╗ ██╗  ██╗ ██╗ ███╗   ██╗ ████████╗ ██████╗  ██╗   ██╗
    ██║    ██║ ██║  ██║ ██║ ████╗  ██║ ╚══██╔══╝ ██╔══██╗ ╚██╗ ██╔╝
    ██║ █╗ ██║ ███████║ ██║ ██╔██╗ ██║    ██║    ██████╔╝  ╚████╔╝
    ██║███╗██║ ██╔══██║ ██║ ██║╚██╗██║    ██║    ██╔═══╝    ╚██╔╝
    ╚███╔███╔╝ ██║  ██║ ██║ ██║ ╚████║    ██║    ██║         ██║
     ╚══╝╚══╝  ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═══╝    ╚═╝    ╚═╝         ╚═╝

            a Python library for managing shared files

    -------------------------------------------------------------------------

    Copyright (C) 2024 Brigitte Bigi, CNRS
    Laboratoire Parole et Langage, Aix-en-Provence, France

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    This banner notice must not be removed.

    -------------------------------------------------------------------------

"""

from .base_authentication import BaseAuthentication
from .ldap_authentication import LdapAuthentication
from .jwt_authetication import JwtAuthentication
from .authentication import Authentication
from .connection import Connection

__all__ = (
    'BaseAuthentication',
    'LdapAuthentication',
    'JwtAuthentication',
    'Authentication',
    'Connection'
)
