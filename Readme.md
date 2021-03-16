Steps for Installation
- Clone the project using `git clone https://github.com/Akash-Cheerla/Menu-Extraction`
-  setup the environemnt using `python -m venv .env`
- Activate the environment using `source .env/bin/activate`
- Before installing other required libraries, you should first install the OCR. The OCR is taken from [here](https://github.com/myhub/tr)
- After the visiting the above url, you can see that you can install the library using `sudo pip install git+https://github.com/myhub/tr.git@master`. If some problem remove `sudo` and try.
- After that you have install other requirements that is by using `pip install -r requirements.txt`
- Now you can run the API using `python serve.py`. The API will be hosted at `localhost:9000/docs`.
- Two endpoints base64 and image upload are provided. For base64, you have give the base64 of the image to the run the results and for image upload, simple upload the image.
