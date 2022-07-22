python setup.py sdist bdist_wheel
echo finished. now please upload your project
pause
python -m twine upload  dist/*
echo finished. press any key to exit
pause