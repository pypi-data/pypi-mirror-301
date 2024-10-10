=============================
duplicate-url-discarder-rules
=============================

.. image:: https://img.shields.io/pypi/v/duplicate-url-discarder-rules.svg
   :target: https://pypi.python.org/pypi/duplicate-url-discarder-rules
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/duplicate-url-discarder-rules.svg
   :target: https://pypi.python.org/pypi/duplicate-url-discarder-rules
   :alt: Supported Python Versions

.. image:: https://github.com/zytedata/duplicate-url-discarder-rules/workflows/tox/badge.svg
   :target: https://github.com/zytedata/duplicate-url-discarder-rules/actions
   :alt: Build Status:

This contains rules for https://github.com/zytedata/duplicate-url-discarder.

Quick Start
***********

Installation
============

.. code-block::

    pip install duplicate-url-discarder-rules

Using
=====

The rules can be imported via:

.. code-block:: python

    from duplicate_url_discarder_rules import RULE_PATHS

It can then be used to configure the ``DUD_LOAD_RULE_PATHS`` setting of
``duplicate-url-discarder``.
