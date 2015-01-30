# Notes

These are the **only** changes to the SDKs as distributed by Nordic.

* A `.gitignore` file was added to ignore Mac-specific files.

* The `enum2define.py` script was used (see usage in its embedded comments)
  to convert softdevice `SVC` calls from `enum` to `define` statements. This
  is because `enum` has slightly different semantics between `C` and `C++`,
  and this change is needed for `C++`. Again, see the embedded comments in
  the script for more details.

* The `gcc_startup_nrf51.s` files were **not** been modified. They were only
  renamed to `gcc_startup_nrf51.sx` since `.sx` the recommended extension for
  assembler code that must be preprocessed, as per the GCC documentation.
  (Double-check the individual patch files to check on this renaming as
  sometimes the rename operations aren't noted in the patch files.)
