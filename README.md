# Notes

The patch files and tools in this repository were created to solve the specific problem of [using `g++` with the Nordic SDKs](https://devzone.nordicsemi.com/question/7830/please-fix-the-enum-in-ble_gattsh/). Although that question linked to a [putative answer on StackOverflow](http://stackoverflow.com/questions/15712894/using-c-headers-in-c-code-in-gnu-error-including-inline-assembly-impossible), it was noted that the "casting" solution presented did not work with `g++`, and furthermore might be dependent on optimization level (due to constant folding, implicit conversions, code movement, and so on).

Therefore, I wrote a simple C-header parser to change the `enum` statements used by Nordic into `#define` constants. These work fine for all versions (4.7, 4.8, and 4.9) of the [GNU Tools for ARM Embedded Processors](https://launchpad.net/gcc-arm-embedded) for both the `gcc` and `g++` compilers.

Note that on the Cortex-M0, `SVC` call operands must be in the range of 0-255, and hence fit in an `unsigned char` which is what we pick for our `typedef`. This choice follows the Keil ARMCC 5.05 default [convention for enums](http://infocenter.arm.com/help/index.jsp?topic=/com.arm.doc.dui0491i/Babjddhe.html). If you want to change this `typedef`, be aware that ISO-C and ISO-C++ have _substantially_ different rules for inferring the type of an `enum`, and as of `g++-4.9` using the `enum : unsigned char { ... }` syntax of `C++11` doe **not** work with the inline assembler for the `SVC` call.

These are the **only** changes I've made to the SDKs as distributed by Nordic.

* A `.gitignore` file was added to ignore OS-specific files.

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
