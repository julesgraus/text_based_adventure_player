export PYTHONPATH="$(pwd)/tests:$(pwd)/src"
echo $PYTHONPATH

echo "Using $PYTHONPATH for PYTHONPATH environment variable that will be added to sys.path"
python -m unittest discover -v -s ./tests -p "*_test.py"
