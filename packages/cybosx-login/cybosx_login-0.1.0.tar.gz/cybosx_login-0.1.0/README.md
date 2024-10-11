# cybosx\_login
Dhashin Cybosplus 로그인 자동화 라이브러리. This library automates the login process for Dhashin Cybosplus, simplifying authentication and enhancing usability.

## Installation

```powershell
PS > pip install cybosx_login
```

### How to Build 32-bit Python Environment
This section explains how to create a virtual environment using 32-bit Python on Windows, using [pyenv-win](https://github.com/pyenv-win/pyenv-win) and [Poetry](https://python-poetry.org/).

1. **Install 32-bit Python**: Install the desired version of 32-bit Python using pyenv.
```powershell
PS > pyenv install 3.9-win32
```
2. **Set the Local Python Version**: Navigate to your project directory and set the local Python version to the installed 32-bit version.
```powershell
PS C:\...\project_dir > pyenv local 3.9.XX-win32
```
3. **Create a Virtual Environment with Poetry**: Configure Poetry to use the installed 32-bit Python by running the following command.
```powershell
PS C:\...\project_dir > poetry env use (where.exe python | Select-Object -First 1)
```

## Usage
To see how to use the package, check the example script located at `example/example.py`. This script demonstrates the following functionalities:

1. **Retrieve Credentials**: It uses the `create_provider` function to retrieve credentials from a `.env` file and from KeePassXC.

2. **Run as a Task**: The script demonstrates how to use the `run_as_task` function, which allows scripts to escalate their privileges to Administrator (Local Service) without requiring UAC approval.

3. **Login to Cybosplus**: It shows how to log in to Cybosplus using credentials fetched from KeePassXC.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For any questions or support, please reach out to me via [GitHub Issues](https://github.com/th-yoo/cybosx_login/issues).
