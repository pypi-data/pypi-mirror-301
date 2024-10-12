import os

os.system('pip install --upgrade pip')
os.system('pip install twine')
os.system('python billionaires-bot/setup.py sdist bdist_wheel')
os.system('twine upload dist/*')