export SOAPUI_HOME=$(cat SOAPUI_HOME)
cd soapui
python soapui_testrunner.py
cd ..

cd program/python
python elastic_data_create.py
python elastic_upload.py ../rest-elastic.json