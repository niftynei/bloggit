poetry run python script.py

if [ $? -eq 0 ]; then 
  cd site; poetry run python -m http.server 8080; cd -
fi
