import logging
from pathlib import PosixPath

from pytest import mark, raises

from tons.logging_ import (
    SensitiveFormatter,
    tons_logger,
    _escape_separator,
    _ensure_empty_line_at_end_for_multiline,
    TonsFormatter,
    _get_stream_handler,
    UserInterface,
    _get_file_handler,
    _get_formatter,
    _get_log_directory,
    _get_env_log_directory,
    _get_default_log_directory,
    _file_logging_enabled,
    _dont_log_at_all,
    _minimal_qt_stream_level,
    _minimal_qt_file_level,
)
from tons.tonsdk.crypto.bip39 import _english


def test_sensitive_formatter_init():
    # ACTION
    sensitive_formatter = SensitiveFormatter()

    # ASSERT
    assert sensitive_formatter._mnemonic_words == set(_english.words)


@mark.parametrize(
    "msg, expected_formatted_record",
    [
        ("test_sensitive_formatter_format", "test_sensitive_formatter_format"),
        ("", ""),
        (None, "None"),
        (True, "True"),
        (False, "False"),
    ],
)
def test_sensitive_formatter_format(msg, expected_formatted_record):
    # SETUP
    sensitive_formatter = SensitiveFormatter()

    # ACTION
    tons_test_logger = tons_logger()
    record = tons_test_logger.makeRecord(
        tons_test_logger.name, logging.INFO, "some_fn", None, msg=msg, args=None, exc_info=None, func="some_fnName"
    )
    formatted_record = sensitive_formatter.format(record)

    # ASSERT
    assert formatted_record == expected_formatted_record


def test_sensitive_formatter_filter():
    # SETUP
    sensitive_formatter = SensitiveFormatter()

    # ACTION
    tons_test_logger = tons_logger()
    for word in _english.words:
        record = tons_test_logger.makeRecord(
            tons_test_logger.name, logging.INFO, "some_fn", None, msg=word, args=None, exc_info=None, func="some_fnName"
        )
        formatted_record = sensitive_formatter.format(record)
        filtered_record = sensitive_formatter._filter(formatted_record)

        # ASSERT
        assert filtered_record == word


@mark.parametrize(
    "text, expected_filtered_words",
    [
        ("", ""),
        (
            "abandon ability able about above absent absorb abstract absurd abuse access",
            "abandon ability able about above absent absorb abstract absurd abuse access",
        ),
        (
            "abandon ability able about above absent absorb abstract absurd abuse access accident",
            "******* ******* **** ***** ***** ****** ****** ******** ****** ***** ****** ********",
        ),
        (
            "abandon ability able about above absent absorb abstract absurd abuse access accident account",
            "******* ******* **** ***** ***** ****** ****** ******** ****** ***** ****** ******** *******",
        ),
    ],
)
def test_sensitive_formatter_filter_mnemonic_words(text, expected_filtered_words):
    # SETUP
    sensitive_formatter = SensitiveFormatter()

    # ACTION
    filtered_words = sensitive_formatter._filter_mnemonic_words(text)

    # ASSERT
    assert filtered_words == expected_filtered_words


@mark.parametrize(
    "message, expected_formatted_message",
    [
        ("", ""),
        ("some_message", "some_message"),
        ("\t", "\\t"),
        ("\tsome_message", "\\tsome_message"),
        ("some_message\t", "some_message\\t"),
        ("some\tmessage", "some\\tmessage"),
    ],
)
def test_escape_separator(message, expected_formatted_message):
    # ASSERT
    assert _escape_separator(message) == expected_formatted_message


@mark.parametrize(
    "message, expected_formatted_message",
    [
        ("", ""),
        ("some_message", "some_message"),
        ("\n", "\n\n"),
        ("\nsome_message", "\nsome_message\n\n"),
        ("some_message\n", "some_message\n\n"),
        ("some\nmessage", "some\nmessage\n\n"),
    ],
)
def test_ensure_empty_line_at_end_for_multiline(message, expected_formatted_message):
    # ASSERT
    assert _ensure_empty_line_at_end_for_multiline(message) == expected_formatted_message


@mark.parametrize(
    "msg, expected_formatted_record", [("test_tons_formatter_format", "test_tons_formatter_format"), ("", "")]
)
def test_tons_formatter_format(msg, expected_formatted_record):
    # SETUP
    tons_formatter = TonsFormatter()

    # ACTION
    tons_test_logger = tons_logger()
    record = tons_test_logger.makeRecord(
        tons_test_logger.name, logging.INFO, "some_fn", None, msg=msg, args=None, exc_info=None, func="some_fnName"
    )
    formatted_record = tons_formatter.format(record)

    # ASSERT
    assert formatted_record == expected_formatted_record


@mark.parametrize("msg, expected_formatted_record", [(None, "None"), (True, "True"), (False, "False")])
def test_tons_formatter_format_should_raise_AttributeError_when_msg_is_invalid(msg, expected_formatted_record):
    # SETUP
    tons_formatter = TonsFormatter()

    # ACTION
    tons_test_logger = tons_logger()
    record = tons_test_logger.makeRecord(
        tons_test_logger.name, logging.INFO, "some_fn", None, msg=msg, args=None, exc_info=None, func="some_fnName"
    )

    # ASSERT
    with raises(AttributeError):
        tons_formatter.format(record)


@mark.parametrize("user_interface", [UserInterface.direct, UserInterface.interactive, UserInterface.tests])
@mark.parametrize("level", range(logging.CRITICAL + 10))
@mark.parametrize("expected_final_level", [_dont_log_at_all])
def test_get_stream_handler_non_qt(user_interface: UserInterface, level: int, expected_final_level: int):
    # SETUP
    handler = _get_stream_handler(user_interface, level)

    # ASSERT
    assert handler.level == expected_final_level


@mark.parametrize("user_interface", [UserInterface.qt])
@mark.parametrize("level", range(_minimal_qt_stream_level + 1))
def test_get_stream_handler_qt_lower_than_minimal(user_interface: UserInterface, level: int):
    # SETUP
    handler = _get_stream_handler(user_interface, level)

    # ASSERT
    assert handler.level == level


@mark.parametrize("user_interface", [UserInterface.qt])
@mark.parametrize("level", range(_minimal_qt_stream_level, logging.CRITICAL + 10))
@mark.parametrize("expected_final_level", [_minimal_qt_stream_level])
def test_get_stream_handler_qt_higher_than_minimal(
    user_interface: UserInterface, level: int, expected_final_level: int
):
    # SETUP
    handler = _get_stream_handler(user_interface, level)

    # ASSERT
    assert handler.level == expected_final_level


@mark.parametrize("user_interface", [UserInterface.direct, UserInterface.interactive, UserInterface.tests])
@mark.parametrize("level", range(logging.CRITICAL + 10))
def test_get_file_handler_non_qt(user_interface: UserInterface, level: int):
    # SETUP
    handler = _get_file_handler(user_interface, level)

    # ASSERT
    assert handler.level == level


@mark.parametrize("user_interface", [UserInterface.qt])
@mark.parametrize("level", range(_minimal_qt_file_level + 1))
def test_get_file_handler_qt_lower_than_minimal(user_interface: UserInterface, level: int):
    # SETUP
    handler = _get_file_handler(user_interface, level)

    # ASSERT
    assert handler.level == level


@mark.parametrize("user_interface", [UserInterface.qt])
@mark.parametrize("level", range(_minimal_qt_file_level, logging.CRITICAL + 10))
@mark.parametrize("expected_final_level", [_minimal_qt_file_level])
def test_get_file_handler_qt_higher_than_minimal(user_interface: UserInterface, level: int, expected_final_level: int):
    # SETUP
    handler = _get_file_handler(user_interface, level)

    # ASSERT
    assert handler.level == expected_final_level


@mark.parametrize(
    "user_interface", (UserInterface.direct, UserInterface.interactive, UserInterface.qt, UserInterface.tests)
)
def test_get_formatter(user_interface):
    # SETUP
    formatter = _get_formatter(user_interface)

    # ASSERT
    assert formatter._mnemonic_words == set(_english.words)


@mark.parametrize("expected_directory", (PosixPath("/Users/Library/Logs/tons/log"),))
def test_get_log_directory(monkeypatch, expected_directory):
    # SETUP
    import tons

    monkeypatch.setattr(tons.logging_, "_get_default_log_directory", lambda: expected_directory)

    # ASSERT
    assert _get_log_directory() == expected_directory


@mark.parametrize("expected_directory", (None,))
def test_get_env_log_directory(expected_directory):
    # ASSERT
    assert _get_env_log_directory() == expected_directory


@mark.parametrize("mock_directory", (PosixPath("/Users/Library/Logs/tons"),))
@mark.parametrize("expected_directory", (PosixPath("/Users/Library/Logs/tons/log"),))
@mark.parametrize('platform_name', ('darwin',))
def test_get_default_log_directory(monkeypatch, mock_directory, expected_directory, platform_name):
    # SETUP
    import os
    import platform

    def system():
        return platform_name

    monkeypatch.setattr(os.path, "expanduser", lambda path: mock_directory)
    monkeypatch.setattr(platform, "system", system)

    # ASSERT
    assert _get_default_log_directory() == expected_directory


@mark.parametrize("expected_file_logging_enabled", (False,))
def test_file_logging_enabled(expected_file_logging_enabled):
    # SETUP
    tons_test_logger = tons_logger()

    # ASSERT
    assert _file_logging_enabled(tons_test_logger) == expected_file_logging_enabled


@mark.parametrize("expected_tons_logger_name", ("tons",))
@mark.parametrize("expected_tons_logger_level", (10,))
def test_tons_logger(expected_tons_logger_name, expected_tons_logger_level):
    # SETUP
    tons_test_logger = tons_logger()

    # ASSERT
    assert tons_test_logger.name == expected_tons_logger_name
    assert tons_test_logger.level == expected_tons_logger_level
