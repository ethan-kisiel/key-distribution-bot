client_secret=$1
file_name="src/environment_vars.py"

# remove existing environment vars file
if test -f "$file_name"; then
    rm $file_name
fi

# create environment vars file
if test -f ""; then
    rm "claim_chats.txt"
fi

touch $file_name

touch "claim_chats.txt"

echo "from os import environ" >> $file_name
echo "" >> $file_name
echo "environ['CLIENT_SECRET'] = '$client_secret'" >> $file_name


# install python version

# create virtual environment
python3 -m venv env
source env/bin/activate

# install requirements.txt
pip install -r requirements.txt

sh startup.sh
# remove this script after running
# rm $0