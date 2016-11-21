### Output Folder

#### Usage
Files are added to the `output/` directory w/ an incrementing nonce value appended to their filename.  This allows for simple recursive calls to the dmdx.py file without needing to have any pre-determined organizational schema.

If one wishes to return the nonce to zero, simply delete the `src/nonce.txt` file.

***Note:*** This is a temporary feature while a more long-term method of interface is developed.  No features should be added which rely upon the output files or the nonce.

#### Bye.
