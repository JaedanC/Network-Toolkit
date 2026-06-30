git submodule update --recursive

python -m venv venv 2>$null
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
python compile.py -exe

pip install -q -r requirements_gen.txt
pip install py2exe

cd tools

cd Catalyst-Switch-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
pip install py2exe
python setup.py
cd ..

cd LoudPing
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
pip install py2exe
python setup.py
cd ..

cd Meraki-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
pip install py2exe
python setup.py
cd ..

cd MultiPing
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
pip install py2exe
python setup.py
cd ..

cd Ping-App
python -m venv venv
./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -q -r requirements.txt
pip install py2exe
python setup.py
cd ..

cd ..

./venv/Scripts/activate
