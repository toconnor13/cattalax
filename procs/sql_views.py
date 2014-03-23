import os, sys
import MySQLdb

# Connect to web database
path='/root/.virtualenvs/cattalax/cattalax' 
if path not in sys.path:
	sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"]="cattalax.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cattalax.settings")

from dashboard.models import *
# Connect to hoover database
HOST="localhost"
USER="root"
PW="the power to do what is right"
DB="cattalax"
con = MySQLdb.connect(HOST,USER,PW,DB)
cursor = con.cursor()


shop_list = [shop for shop in Outlet.objects.all()]

for shop in shop_list:
	view = "capture"+str(shop.sensor_no)
	cursor.execute("CREATE OR REPLACE VIEW "+view+" AS SELECT id, timestamp, count(id) AS obs FROM attendance WHERE sensor_id="+str(shop.sensor_no)+" GROUP BY id")


