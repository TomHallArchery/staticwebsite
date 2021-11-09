trap 'kill 0' SIGINT;

mongod --config database/db.conf &
python -m scripts.run &
sleep 2
./node_modules/.bin/browser-sync start --proxy localhost:5000 --files website --port 5001 --reload-delay 300
