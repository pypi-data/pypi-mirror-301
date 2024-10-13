# -*- coding: UTF-8 -*-
"""
:filename: whintpy.config.settings.py
:author: Brigitte Bigi
:contact: contact@sppas.org
:summary: Settings for managing documents in a deposit and their accesses

.. _This file is part of WhintPy: https://whintpy.sourceforge.io
..
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


class WhintPySettings:
    """Manage the configuration settings for the WhintPy library.

    This class defines default naming conventions and rules for folders and
    files, including separators, minimum name lengths, and invalid characters.
    Once initialized, the settings become immutable, enforcing consistency
    throughout the application. The class also supports context management,
    allowing temporary changes using the 'with' statement.

    Attributes:

    - FOLDER_NAME_SEPARATOR (str): Character used to separate parts of a folder name.
    - FIELDS_NAME_SEPARATOR (str): Character used to separate fields within a folder name.
    - MIN_FILE_NAME_LENGTH (int): Minimum length required for a valid file name.
    - INVALID_CHARS_FOR_FOLDERS (str): String of characters that are disallowed in folder names.
    - INVALID_CHARS_FOR_FIELDS (str): String of characters that are disallowed in file names.
    - DOWNLOADS_FILENAME (str): Default name for the downloads file.
    - DESCRIPTION_FILENAME (str): Default name for the description file.

    """

    def __init__(self):
        """Initialize the default settings for WhintPy library.

        Sets default values for folder and file name separators, as well as
        restrictions on file name lengths and characters. After initialization,
        the settings are frozen to prevent modifications unless explicitly
        unfrozen.

        """
        self.__dict__ = dict(
            # Separator used to separate the parts of a document folder name
            # and the one for the fields of a folder
            FOLDER_NAME_SEPARATOR='.',
            FIELDS_NAME_SEPARATOR='_',

            # Minimum length of a file name
            MIN_FILE_NAME_LENGTH=4,

            # Invalid characters for folder names
            INVALID_CHARS_FOR_FOLDERS="/\\.$@#%&*()[]{}<>:;,?\"'`!^+=|~",

            # Invalid characters for file names
            INVALID_CHARS_FOR_FIELDS="/$@#%&*()[]{}<>:;,?\"'`!^+=|~",

            # Default filenames
            DOWNLOADS_FILENAME="downloads.txt",
            DESCRIPTION_FILENAME="description.txt"

        )
        self._is_frozen = True

    # -----------------------------------------------------------------------

    def freeze(self):
        """Freeze the settings to make them immutable.

        Once frozen, any attempt to modify or delete attributes will raise
        an AttributeError.

        """
        super().__setattr__('_is_frozen', True)

    # -----------------------------------------------------------------------

    def unfreeze(self):
        """Unfreeze the settings, allowing temporary modifications.

        This allows attributes to be modified, but should be used with care.

        """
        super().__setattr__('_is_frozen', False)

    # -----------------------------------------------------------------------

    def __setattr__(self, key, value):
        """Override the default behavior to prevent attribute modification when frozen.

        :param key: The attribute name.
        :param value: The new value to set for the attribute.
        :raises: AttributeError: If the class is frozen and an attempt is made to set an attribute.

        """
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"{self.__class__.__name__} object is immutable")
        super().__setattr__(key, value)

    # -----------------------------------------------------------------------

    def __delattr__(self, key):
        """Override the default behavior to prevent deletion of attributes.

        :param key: The attribute name.
        :raises: AttributeError: Always raised since attribute deletion is not allowed.

        """
        raise AttributeError(f"{self.__class__.__name__} object does not allow attribute deletion")

    # -----------------------------------------------------------------------

    def __enter__(self):
        """Override to allow the support the 'with' statement.

        To be used for temporary settings changes.
        :return: the object itself for use in 'with' blocks.

        """
        return self

    # -----------------------------------------------------------------------

    def __exit__(self, exc_type, exc_value, traceback):
        """Context manager exit method, no specific handling required.

        This ensures that when exiting a 'with' block, the settings remain unchanged.

        :param exc_type: The exception type.
        :param exc_value: The exception value.
        :param traceback: The traceback.

        """
        pass

    # -----------------------------------------------------------------------

    def __iter__(self):
        """Iterate over the settings attributes.

        This allows iterating through all configuration settings, providing access to each key.

        :return: An iterator over the dictionary keys.

        """
        for item in self.__dict__.keys():
            yield item
