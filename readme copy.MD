# the enviornment name is deployYolo.
# it was created with
python -m venv deployYolo

# Activate the virtual environment (Windows)
deployYolo\Scripts\activate

# Activate the virtual environment (macOS/Linux)
source deployYolo/bin/activate

# time to install the necessary dependencies. These include FastAPI, Uvicorn (for serving FastAPI apps), YOLO-related libraries, and any additional packages you may need for your project.
pip install -r requirements.txt


# remember to run the scriots in object_detection_api
cd object_detection_api

# run the main.py by using
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# paste the following url in postman and use the get request
http://127.0.0.1:8000

# paste the url with post request with an image in postman to get the response

# if The error message indicates that your FastAPI server does not have the proper CORS (Cross-Origin Resource Sharing) settings to allow requests from your React application running on a different port (3000).

