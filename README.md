# CurrentAI Application
![image](https://github.com/user-attachments/assets/f7a2e23b-4006-454d-b8b7-3c1ba6b96ca3)

## Overview

CurrentAI is an AI-based chat application that allows users to interact with an AI model with real-time information. It includes functionality for user sign-up, login, password recovery, and conversation history management. Users can save and export their chat history once logged in.

Live page link: [CurrentAI Live Page](https://currentai.onrender.com/)

## Features

- **Sign Up**: Register a new account.
- **Log In**: Access your account.
- **Forgot Password**: Reset your password.
- **Chat**: Interact with the AI.
- **Save Conversation**: Save chat history.
- **Export Conversation**: Download conversation history as a CSV file.

## Setup Instructions

Follow these steps to set up and run the application:

1. **Clone the Repository**
    ```bash
    git clone https://github.com/rkstu/CurrentAI.git
    cd CurrentAI
    ```

2. **Create Conda Environment**
    ```bash
    conda create --prefix ./venv python==3.10 -y
    ```

3. **Activate the Environment**
    ```bash
    conda activate venv/
    ```

4. **Install Required Libraries**
    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up Environment Variables, Particularly for [TiDB](https://tidbcloud.com/free-trial/) and [Google Gemini](https://ai.google.dev/)**
    Create a `.env` file in the root directory of the project with the following content:

    ```
    DB_HOST=something.aws.tidbcloud.com
    DB_USER=something.root
    DB_PASSWORD=something
    DB_PORT=4000
    DB_NAME=test
    GOOGLE_API_KEY=something
    ```

6. **Run the Application**
    ```bash
    streamlit run app.py
    ```

## Additional Notes

- Make sure to replace the placeholder values in the `.env` file with your actual database and API credentials.
- For more details on how to use the application, refer to the in-app help and documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
