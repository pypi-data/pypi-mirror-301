# Capote AI Documentation

This document details how to setup the AI component on your PC.

## Building the environment
1. Create an `.env` file and add the following:
```.env
OPENAI_API_KEY = **input_here**
organization = **input_here**
project = **input_here**
```
2. Setup a virtual environment using the following command:
```powershell
py -3.12 -m venv venv_name
```
- Make sure to update `.gitignore` if you set the `venv_name` to anything other than `venv`.

3. Activate the virtual environment:
```powershell
.\venv_name\Scripts\activate
```
4. Install all requirements using `pip`:
```powershell
pip install -r .\requirements.txt
```
- Make sure to `cd AI/src` before running this.

## Calling the AI Package
Make sure you have activated your virtual environment. A sample implementation has been shown in `main_test.py`.