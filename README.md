TrafficManegment

لطفا برای وارد کردن اطلاعات از فایل json دستور زیر را اجرا کنید و به جای عبارت path/to/your مسیر فایل های خود را جایگذاری کنید 

python manage.py load_json --owners="/path/to/your/owners.json" --roads="/path/to/your/roads.json" --tolls="/path/to/your/tollStations.json" --movements="/path/to/your/all_nodes.json"


پروژه داکرایز شده و با دستورات build و up در localhost شما اجرا میشود

دیتابیس این پلتفرم postgersql بوده و با افزونه postgis امکان دسترسی به داده های gis را فراهم کردن است 
