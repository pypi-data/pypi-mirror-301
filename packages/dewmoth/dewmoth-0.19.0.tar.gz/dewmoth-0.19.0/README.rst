Dewmoth - Sphinx Autodoc with Partial Doxygen Support
=====================================================

Dewmoth forks Hawkmoth to add support for ``//!<`` comments trailing after field
declarations.

Full list of changes from Hawkmoth:

- Support for trailing field comments with ``//!<``.
- Multiple trailing comments supported (concatenated).
- Using ``@file`` in a toplevel comment properly positions it as a toplevel comment (skip binding it to the next declaration).

See Hawkmoth_ `Hawkmoth` for further details.

.. _Hawkmoth: https://github.com/jnikula/hawkmoth
