# ForceFetchBot

## A program to interact with Genscape's Manual Force Fetcher PHP webpage to re-run jobs in a date range

*By Dominic Eggerman*

### Installation

In order to run the program, you will need `selenium`, which can be installed from the command line with `pip install selenium`.  Selenium is a module that can automate browsers and test web applications.

You will also need the ChromeDriver WebDriver for Chrome (https://sites.google.com/a/chromium.org/chromedriver/downloads).  I have included the file in the /drivers/ folder in this program.  The program accesses this file so it is important not to move things around (or change the paths).

### How To - `forceFetchBot`

Launch `forceFetchBot` from the command line with `python forceFetchBot.py`.  The input instructions are straightforward from then on out.  Note that the chrome webpage that the program creates acts as a interactable webpage, and can be manipulated by the user like an internet browser.  Therefore it is important to remember not to click around the driver page as it will throw off the program, which does not anticipate any user input after launching.

To stop the driver running, you can close the driver window or press CTRL + C while focusing on the command line to cause a keyboard interrupt.

### Known bugs

- At times the web driver can hang up when selecting a source id and the job table does not load and is not caught by the backup while loop. This bug is seen when the driver clicks the button to force fetch and the web message appears saying "Please select a dataset".
    - You can manually fix this bug as the program is running.  When the terminal starts printing "Waiting for fetcher to initialize...", you can select another pipeline, re-select the desired pipeline, check the desired job box, and click the "Force Fetch" button.  The loop will catch the popup window and the program will continue.