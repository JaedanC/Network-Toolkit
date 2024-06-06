python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt

python compile.py -d
pip install -r requirements_gen.txt
git submodule update --recursive

cd tools

cd LoudPing
python setup.py
cd ..

cd Meraki-App
python setup.py
cd ..

cd MultiPing
python setup.py
cd ..

cd Ping-App
python setup.py
cd ..

cd ..