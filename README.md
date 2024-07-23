# Network-Toolkit

To install the network toolkit on windows you only need two things installed:

- [python](https://www.python.org/downloads/) (Note: Python 12 is not supported yet)
- [git](https://git-scm.com/download/win)

You may be able to install git with:

```cmd
winget install --id Git.Git -e --source winget
```

Download this repository with:

```bash
git clone git@github.com:JaedanC/Network-Toolkit.git --recursive
```

Open powershell to the root folder of the project and run:

```bash
./install.ps1
```

## Extra notes

- GUI apps require you to position the windows for the first time.
- For the Meraki-App you can supply a `meraki_api_key.txt` which will make running the app easier.
- For the Catalyst-Switch-App you can supply a `password.txt` which will make running the app easier.
