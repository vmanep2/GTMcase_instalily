#!/bin/bash

echo "Starting Script"

if [ -f .env ]; then
  echo "Loading environment variables from .env"
  export $(grep -v '^#' .env | xargs)
else
  echo "No .env file found. You must create one in your root folder with the following API keys."
  echo "  OPENAI_KEY=sk-..."
  echo "  SERPAPI_KEY=..."
  echo "  APOLLO_API_KEY=..."
  exit 1
fi

echo "Activating python virtual environment"
source backend/venv/bin/activate || { echo "Failed to activate venv. Try running 'python3 -m venv backend/venv' "; exit 1; }

echo "Installing Python dependencies"
pip install -r backend/requirements.txt

echo "Installing frontend dependencies"
cd frontend
npm install

cd ../backend
echo "Starting Flask app"
FLASK_APP=app.py FLASK_ENV=development flask run --port=5001 &
BACKEND_PID=$!
cd ..

cd frontend
echo "Starting React frontend"
npm run dev &
FRONTEND_PID=$!
cd ..

sleep 3
if command -v open &> /dev/null; then
  open http://localhost:5173
elif command -v xdg-open &> /dev/null; then
  xdg-open http://localhost:5173
fi

trap "echo 'Shutting down app'; kill $BACKEND_PID $FRONTEND_PID; exit 0" INT
wait