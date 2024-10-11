import typing
import collections.abc
import typing_extensions

def keyconfig_export(wm, kc, filepath): ...
def keyconfig_merge(kc1, kc2):
    """note: kc1 takes priority over kc2"""

def keyconfig_test(kc): ...
def km_exists_in(km, export_keymaps): ...
