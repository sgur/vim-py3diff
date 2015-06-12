vim-py3diff
===========

Description
-----------

A diff plugin using difflib via if\_python3 for vim.

V.S.
----

[vim-diff](https://github.com/ynkdir/vim-diff) (Excellent diff plugin written in pure VimL, non-diff executable!)

For 1466 lines, 4246 words (win7, i7, HDD):

* vim-diff: 0.116763 sec.
* vim-py3diff: 0.014688 sec. (about x8 faster)

Requirement
-----------

* if\_python3

Usage
-----

```vim
set diffexpr=py3diff#diffexpr()
```

License
-------

[MIT License](LICENSE)

Author
------

sgur
