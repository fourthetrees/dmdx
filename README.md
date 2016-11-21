## dmdx

### Quick Start:

Navigate to the `dmdx/` folder, and run the `dmdx.py` file with `$ ./dmdx.py`.  This will generate a DMDX file in in the `output/` folder.  The `dmdx.py` file may be recursively called to generate a number of DMDX files; filenames include a nonce and will not overwrite one another.

** Troubleshooting: ** If you are unable to launch the `dmdx.py` file from the terminal, run the command `$ chmod +x dmdx.py` or launch it explicitly as a python file with `$ python3 dmdx.py`.  If the program fails to generate output files, or gives a permissions related error, ensure that your user account has read/write/execute permission for `dmdx/` and all sub-directories.

### Purpose:

This is a utility for generating randomized DMDX files for serial presentations of stimuli.  This is essentially a small script wrapping the `order_generator.py` file, which is an in-progress attempt to make a highly versatile randomization program for psychological stimuli.  The goal of the *order generator* project is to create a simple and versatile program which can create randomized trial conditions for complex multi-modal tests.

### Future Work:

Future work will focus on three main areas:

  **Expanded Randomization Options:**  Additional config options (modified via `src/config.json` will be added in order to expand the range of test procedures for which the program is appropriate.

  **Dynamic DMDX Support:**  Currently, the script does no direct customization of DMDX-specific options, supplying only the raw ordering for a pre-made template.  In the future it may be desireable to have the randomization script be able to control various more advanced options.

  **Non-DMDX Presentation:**  For long-term devlopment, completely circumventing DMDX, and implementing custom stimulus presentation software is desireable.  This would allow for full-stack control over presentation options, as well as interfaces with some parallel hardware projects.



