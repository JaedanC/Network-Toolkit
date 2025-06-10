git submodule update --recursive

python -m venv venv 2>$null
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
python compile.py -d

pip install -q -r requirements_gen.txt

cd tools

cd Catalyst-Switch-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
cd ..

cd LoudPing
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
cd ..

cd Meraki-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
cd ..

cd MultiPing
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
cd ..

cd Ping-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
cd ..

cd ..

./venv/Scripts/activate
