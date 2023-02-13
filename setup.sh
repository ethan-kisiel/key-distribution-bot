client_secret=$1
file_name="src/environment_vars.py"

# remove existing environment vars file
if test -f "$file_name"; then
    rm $file_name
fi

# create environment vars file
touch $file_name

echo "from os import environ" >> $file_name
echo "" >> $file_name
echo "environ['CLIENT_SECRET'] = '$client_secret'" >> $file_name


# install python version

# create virtual environment
python3.9 -m venv env
source env/bin/activate

# install requirements.txt
pip install -r requirements.txt


# remove this script after running
# rm $0