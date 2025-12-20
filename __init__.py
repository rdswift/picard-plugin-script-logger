# -*- coding: utf-8 -*-
#
# Copyright (C) 2023, 2025 Bob Swift (rdswift)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

# pylint: disable=missing-module-docstring, line-too-long


from picard.plugin3.api import PluginApi


class LogLine:
    """Logs text to the Picard log."""

    api: PluginApi = None
    LEVELS = {}

    @classmethod
    def initialize(cls, api: PluginApi):
        cls.api = api
        cls.LEVELS = {
            'E': cls.api.logger.error,
            'W': cls.api.logger.warning,
            'I': cls.api.logger.info,
            'D': cls.api.logger.debug,
        }


def func_logline(_parser, text: str, level=None):
    """Logs text to the Picard log.

    Args:
        _parser (parser): Script parser
        text (str): Text message to log
        level (str, optional): Level to use for logging ('E', 'W', 'I' or 'D'). Defaults to 'I'.
    """
    if level:
        _level = (str(level).strip().upper() + 'I')[0]
    else:
        _level = 'I'
    if _level not in LogLine.LEVELS:
        _level = 'I'
    LogLine.LEVELS[_level](text.strip())
    return ''


def enable(api: PluginApi):
    """Called when plugin is enabled."""
    LogLine.initialize(api)

    api.register_script_function(
        func_logline,
        name="logline",
        documentation=api.tr(
            'help.logline',
            (
                "`$logline(text[,level])`\n\n"
                "Logs the text to the Picard log. "
                "The entry will be written at log level `Info` by default, but this can be changed by "
                "specifying a different level as an optional second parameter. Allowable log levels are:\n\n"
                "- E (Error)\n"
                "- W (Warning)\n"
                "- I (Info)\n"
                "- D (Debug)\n\n"
                "If an unknown level is entered, the function will use the default `Info` level."
            )
        )
    )
