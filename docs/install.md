# Steps for setting up the repository and running the web app

## Step 1: Git Clone the Repository
  
    git clone https://github.com/CSC-510-Group-5/BingeSuggest.git
    
  (OR) Download the .zip file on your local machine from the following link
  
    https://github.com/CSC-510-Group-5/BingeSuggest

### Step 2: Setup up environment variables

    Copy the .example-env file located at `src/recommenderapp/.example-env` into a new `.env` file located in the same directory.

    Replace `<your_omdb_api_key>` with your own API key from [OMDb API](http://www.omdbapi.com/).

## Step 3: Install docker and docker-compose

    You will need to install docker for your system which can be found [here](https://www.docker.com/products/docker-desktop/).

    The install for docker desktop should come with docker-compose built in by default. This can be confirmed by running the command:

    ```
    docker-compose --version
    ```

## Step 4: Starting the application

    The application can be started by running `docker-compose up --build` from the root of the project directory.

## Step 5: Open the URL in your browser 

      http://127.0.0.1:5001/


**NOTE: For the email notifier feature - create a new gmail account, replace the sender_email variable with the new email and sender_password variable with its password (2 factor authentication) in the utils.py file (function: send_email_to_user(recipient_email, categorized_data)).**
