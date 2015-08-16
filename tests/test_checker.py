import mock

import flake8_quotes


@mock.patch('flake8_quotes.errors')
def test_dq_being_used(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, '"a"')  # "a"
    assert len(errors.method_calls) == 1
    assert errors.Q100.called


@mock.patch('flake8_quotes.errors')
def test_sq_being_used(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "'a'")  # 'a'
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_dq_with_sq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, '"aa\'aa"')  # "aa'aa"
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_sq_with_dq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "'aa\"aa'")  # 'aa"aa'
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_sq_with_sq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "'asd\\'asd'")  # 'asd\'asd'
    assert len(errors.method_calls) == 1
    assert errors.Q101.called


@mock.patch('flake8_quotes.errors')
def test_dq_with_dq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, '"asd\\"asd"')  # "asd\"asd"
    assert len(errors.method_calls) == 1
    assert errors.Q100.called


@mock.patch('flake8_quotes.errors')
def test_raw_dq_being_used(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, 'r"a"')  # r"a"
    assert len(errors.method_calls) == 1
    assert errors.Q100.called


@mock.patch('flake8_quotes.errors')
def test_raw_sq_being_used(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "r'a'")  # r'a'
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_raw_dq_with_sq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, 'r"aa\'aa"')  # r"aa'aa"
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_raw_sq_with_dq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "r'aa\"aa'")  # r'aa"aa'
    assert not errors.method_calls


@mock.patch('flake8_quotes.errors')
def test_raw_sq_with_sq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, "r'asd\\'asd'")  # r'asd\'asd'
    assert len(errors.method_calls) == 1
    assert errors.Q101.called


@mock.patch('flake8_quotes.errors')
def test_raw_dq_with_dq_inside(errors):
    qc = flake8_quotes.QuotesChecker(None, None)
    qc.check_quote(0, 0, 'r"asd\\"asd"')  # r"asd\"asd"
    assert len(errors.method_calls) == 1
    assert errors.Q100.called
