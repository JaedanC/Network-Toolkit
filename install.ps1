python -m venv venv
./venv/Scripts/activate
pip install -q -r requirements.txt
python compile.py -d

pip install -q -r requirements_gen.txt
git submodule update --recursive

cd tools

cd LoudPing
python -m venv venv
./venv/Scripts/activate
pip install -q -r requirements.txt
python setup.py
cd ..

cd Meraki-App
python -m venv venv
./venv/Scripts/activate
pip install -q -r requirements.txt
python setup.py
cd ..

cd MultiPing
python -m venv venv
./venv/Scripts/activate
pip install -q -r requirements.txt
python setup.py
cd ..

cd Ping-App
python -m venv venv
./venv/Scripts/activate
pip install -q -r requirements.txt
python setup.py
cd ..

cd ..

./venv/Scripts/activate
