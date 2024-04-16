# AOX Reverse Shell

<img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" alt="Python"><img src="https://img.shields.io/badge/Sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="sqlite"><img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux"><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows">


The AOX Reverse Shell is a simple multiclient Python reverse shell with extra functionalities designed to provide remote control and management capabilities over multiple client machines. This tool allows you to establish reverse connections with client machines, enabling remote execution of commands and additional features.



## Features 


```
AOX Shell Commands 

    'list':['lists all active connections'] 
    'select (target Client_ID)':['selects a target and creates a session between the server and the client machine ']
    'guide': Display Corona's user commands

Client Commands 

    'quit':['takes you back to the Corona shell interface'] 
    'wifi_passwords':['gets all known wifi password that the client node has ever connected to']
    'screenshot':['takes a screen shot of the client machine']
    'camshot':['captures an image from the client's webcam']
    'encrypt (password) (directory)':['encrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be encrypted']
    'decrypt (password) (directory)':['decrypts all files in the directory specified'] [if directory is not specified all files in the current directory will be decrypted']
    'get (filename or path)':['gets file from the victim's machine and sends it over to the server']
    'send (filename or path)':['send file from server and stores it on the victim's machine'] 

```


## Installation

AOX Reverse Shell requires Python 3 and certain dependencies. Use pip to install the required packages:

```
pip install -r requirements.txt

```




## Disclaimer

This code is intended for educational and informational purposes only. Use it responsibly and ensure compliance with applicable laws and regulations. Respect the privacy and security of others.  
The author of this code assume no liability and is not responsible for misuses or damages caused by any code contained in this repository in any event that, accidentally or otherwise, it comes to be utilized by a threat agent or unauthorized entity as a means to compromise the security, privacy, confidentiality, integrity, and/or availability of systems and their associated resources. In this context the term "compromise" is henceforth understood as the leverage of exploitation of known or unknown vulnerabilities present in said systems, including, but not limited to, the implementation of security controls, human or electronically-enabled.



