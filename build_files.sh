echo "build start"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
python manage.py makemigrations
python manage.py migrate
echo "build end"