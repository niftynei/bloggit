python3 script.py

if [ $? -eq 0 ]; then 
  cd site; python3 -m http.server 8080; cd -
fi
