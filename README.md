# Graduation Project


# Run FE
This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

Go to the 'frontend' directory, you run:
### `cd frontend`

In the client directory, you run:
### `npm install --force`
Downloads all libraries and dependencies

Create .env file (change your IP address of your computer), you run:
### `echo REACT_APP_BASE_API_URL=http://192.168.0.101 > .env`

Run Frontend application, you run:
### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

# Run BE

## Available Scripts
Install all libraries
### `pip install -r requirements.txt`

Go to the 'server' directory, you run:
### `cd server`

In the 'server' directory, you run:
### `python -m uvicorn main:app --reload` (for local only)
### `python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload` (public for LAN)

# Model
Download models [here](https://drive.google.com/drive/folders/1ejcJtZkA4MkogkID5viuttdpqlsN6fws?usp=sharing)\
/root\
|------checkpoint\
|------server\MMFusion_IML\
|-------------|---------ckpt\
|-------------|---------pretrained