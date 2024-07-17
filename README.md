# Reports
A script to generate formated reports from different file sources. 

## Installation
1. [Download][1] and install Python
2. Search in Windowns Start Menu `Powershell` and open it. Run the next steps in the command line prompt
3. Confirm if python is installed by running `python --version`
4. Run `py -m ensurepip --upgrade` to install the package manager pip
5. Follow the step in [this post](https://stackoverflow.com/questions/49943410/pip-ssl-error-on-windows) to add pip.ini (Self signed certificate error)
6. Install the datafeeds report script by running `pip install -U git+https://github.com/salahfh/datafeeds_reports`
7. After installation completed. Run `reports` first time to create the folders structure.

## How to use the script
1. Copy the exported CSV file in the input folder.
2. Run the command `reports` in a Powershell window.
3. The report will be saved in your output folder. 

**Note**: the `input` and `output` folders are created in the user's home directory under `C:\Users\[USERNAME]\Datafeed_reports`.


[1]:https://www.python.org/downloads/
