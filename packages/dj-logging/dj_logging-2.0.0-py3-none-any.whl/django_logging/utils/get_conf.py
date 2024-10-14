import os
from typing import Dict

from django.conf import settings

from django_logging.constants import DefaultConsoleSettings, DefaultLoggingSettings


# pylint: disable=too-many-locals
def get_config(extra_info: bool = False) -> Dict:
    """Retrieve logging configuration from Django settings.

    Returns:
        A Dict containing all necessary configurations for logging.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    logging_defaults = DefaultLoggingSettings()
    console_defaults = DefaultConsoleSettings()

    if not isinstance(log_settings, dict):
        raise ValueError("DJANGO_LOGGING must be a dictionary with configs as keys")

    log_levels = log_settings.get("LOG_FILE_LEVELS", logging_defaults.log_levels)
    log_dir = log_settings.get(
        "LOG_DIR", os.path.join(os.getcwd(), logging_defaults.log_dir)
    )
    log_file_formats = log_settings.get(
        "LOG_FILE_FORMATS", logging_defaults.log_file_formats
    )
    log_file_format_types = log_settings.get(
        "LOG_FILE_FORMAT_TYPES", logging_defaults.log_file_format_types
    )
    extra_log_files = log_settings.get(
        "EXTRA_LOG_FILES", logging_defaults.extra_log_files
    )
    console_level = log_settings.get(
        "LOG_CONSOLE_LEVEL", console_defaults.log_console_level
    )
    console_format = log_settings.get(
        "LOG_CONSOLE_FORMAT", console_defaults.log_console_format
    )
    colorize_console = log_settings.get(
        "LOG_CONSOLE_COLORIZE", console_defaults.log_console_colorize
    )
    log_date_format = log_settings.get(
        "LOG_DATE_FORMAT", logging_defaults.log_date_format
    )

    log_email_notifier = log_settings.get(
        "LOG_EMAIL_NOTIFIER", logging_defaults.log_email_notifier
    )
    log_email_notifier_enable = log_email_notifier.get("ENABLE")
    log_email_notifier_log_levels = [
        "ERROR" if log_email_notifier.get("NOTIFY_ERROR", False) else None,
        "CRITICAL" if log_email_notifier.get("NOTIFY_CRITICAL", False) else None,
    ]
    log_email_notifier_log_format = log_email_notifier.get("LOG_FORMAT")

    config = {
        "log_levels": log_levels,
        "log_dir": log_dir,
        "log_file_formats": log_file_formats,
        "log_file_format_types": log_file_format_types,
        "extra_log_files": extra_log_files,
        "console_level": console_level,
        "console_format": console_format,
        "colorize_console": colorize_console,
        "log_date_format": log_date_format,
        "log_email_notifier_enable": log_email_notifier_enable,
        "log_email_notifier_log_levels": log_email_notifier_log_levels,
        "log_email_notifier_log_format": log_email_notifier_log_format,
    }
    if extra_info:
        config.update(
            {"log_email_notifier": log_email_notifier, "log_settings": log_settings}
        )

    return config


def use_email_notifier_template() -> bool:
    """Check whether the email notifier should use a template based on Django
    settings.

    Returns:
        bool: True if the email notifier should use a template, False otherwise.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    log_email_notifier = log_settings.get(
        "LOG_EMAIL_NOTIFIER", defaults.log_email_notifier
    )
    return log_email_notifier.get("USE_TEMPLATE", True)


def is_auto_initialization_enabled() -> bool:
    """Check if the AUTO_INITIALIZATION_ENABLE for the logging system is set to
    True in Django settings.

    Returns:
        bool: True if AUTO_INITIALIZATION_ENABLE, False otherwise.
         Defaults to True if not specified.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    return log_settings.get(
        "AUTO_INITIALIZATION_ENABLE", defaults.auto_initialization_enable
    )


def is_initialization_message_enabled() -> bool:
    """Check if the INITIALIZATION_MESSAGE_ENABLE is set to True in Django
    settings.

    Returns:
        bool: True if INITIALIZATION_MESSAGE_ENABLE is True, False otherwise.
         Defaults to True if not specified.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    return log_settings.get(
        "INITIALIZATION_MESSAGE_ENABLE", defaults.initialization_message_enable
    )


def is_log_sql_queries_enabled() -> bool:
    """Check if the LOG_SQL_QUERIES_ENABLE for the logging system is set to
    True in Django settings.

    Returns:
        bool: True if LOG_SQL_QUERIES_ENABLE, False otherwise.
         Defaults to False if not specified.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    return log_settings.get("LOG_SQL_QUERIES_ENABLE", defaults.log_sql_queries_enable)


def get_log_dir_size_limit() -> int:
    """Check for the LOG_DIR_SIZE_LIMIT for managing the log dir size.

    Returns:
        int: the limit of log directory size.
         Defaults to 1024 MB if not specified.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    return log_settings.get("LOG_DIR_SIZE_LIMIT", defaults.log_dir_size_limit)


def include_log_iboard() -> bool:
    """Check if the INCLUDE_LOG_iBOARD for the logging system is set to True in
    Django settings.

    Returns:
        bool: True if INCLUDE_LOG_iBOARD, False otherwise.
         Defaults to False if not specified.

    """
    log_settings = getattr(settings, "DJANGO_LOGGING", {})
    defaults = DefaultLoggingSettings()

    return log_settings.get("INCLUDE_LOG_iBOARD", defaults.include_log_iboard)
