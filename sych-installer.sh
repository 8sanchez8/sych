#!/bin/bash

# Функции ==============================================

# Проверяет наличие в системе установленного пакета, и в случае его отсутствия, устанавливает его
# Пример использования:
# echo "node: $(seek_and_install node)"
function seek_and_install {
  if dpkg -s "$1" 2>/dev/null 1>/dev/null; 
  	then 
  	echo "Package $1 is already installed." 
  else 
  	echo "Package $1 isn't installed."
  	echo "Installing..."
  	sudo apt-get -qq -o=Dpkg::Use-Pty=0 -y install $1 > /dev/null
  fi  
}
# ============================================== Функции


# Тело сценария ========================================

# Проверка на наличие прав администратора
if test "`id -u`" -ne 0
	then 
	echo "You need to run this script as root!" 
	exit -1
fi

# Проверка дистрибутива
if [[ $(lsb_release -si) != *"Ubuntu"* ]]
then
	echo "It's not Ubuntu, sorry"
	exit -1
fi

# Проверка и установка зависимостей
 requirements=(
	"apache2"
	"git"
	"libapache2-mod-wsgi"
	"libpq-dev" 		
 	"postgresql" 
 	"python"
 	"python2.7" 
 	"python-pip"
	"python-psycopg2"
 	"python-django"
	"unzip"
	"wget"
 	)
 for package in "${requirements[@]}"
 do
 	seek_and_install $package
 done

# Создание базы данных
echo "CREATE ROLE django LOGIN ENCRYPTED PASSWORD 'django';" | sudo -u postgres psql
su postgres -c "createdb django --owner django"
service postgresql reload

# Создание установочной директории
read -p "Enter installation path [/opt]: " INSTALLATION_PATH
INSTALLATION_PATH=${INSTALLATION_PATH:-/opt}
echo "Installation path: $INSTALLATION_PATH..."

# # Скачивание и распаковка актуальной версии проекта
echo "Downloading files..."
sudo wget --quiet --show-progress --no-clobber --directory-prefix=$INSTALLATION_PATH https://github.com/8sanchez8/sych/archive/master.zip
echo "Unpacking files..."
sudo unzip -q -u $INSTALLATION_PATH/master.zip -d $INSTALLATION_PATH
sudo mv $INSTALLATION_PATH/sych-master $INSTALLATION_PATH/sych
sudo rm $INSTALLATION_PATH/master.zip
sudo chown -R $USER $INSTALLATION_PATH/sych

# # Установка виртуального окружения Python
echo "Installing virtualenv..."
pip -q install virtualenv 2>/dev/null 1>/dev/null
virtualenv --system-site-packages -q $INSTALLATION_PATH/sych -p python2.7

source $INSTALLATION_PATH/sych/bin/activate
echo "Installing Django..."
pip -q install django
echo "Installing Django additions..."
pip -q install django-bootstrap3-datetimepicker
pip -q install django-bootstrap-pagination
pip -q install django-jfu
pip -q install psycopg2

echo "Making migrations..."
python $INSTALLATION_PATH/sych/manage.py makemigrations
python $INSTALLATION_PATH/sych/manage.py migrate
python $INSTALLATION_PATH/sych/manage.py collectstatic

echo "Creating superuser..."
python $INSTALLATION_PATH/sych/manage.py createsuperuser

echo "Installation succeeded!"

# Тестирование сервера
echo "Starting server..."
python $INSTALLATION_PATH/sych/manage.py runserver 0.0.0.0:8080 & firefox http://127.0.0.1:8080
deactivate

# ======================================== Тело сценария
