# ForceFetchBot

## A program to interact with Genscape's Manual Force Fetcher PHP webpage to re-run jobs in a date range.
*By Dominic Eggerman*

### How To - `forceFetchBot`:
Launch `forceFetchBot` from the command line with `python forceFetchBot.py`.  The input instructions are straightforward from then on out.  Note that the chrome driver webpage that the program creates acts as a interactable webpage, and can be manipulated by the user like an internet browser.  Therefore it is important to remember not to click around the driver page as it will throw off the program, which does not anticipate any user input after launching its jobs.

### Known bugs:
- At times the web driver can hang up when selecting a source id and the job table does not load and is not caught by the backup while loop. This bug is seen when the driver clicks the button to force fetch and the web message appears saying "Please select a dataset".