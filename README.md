# Fatmug Assessment - Website for Search in Subtitles

## Overview

This project is a Django-based web application that allows users to upload videos and automatically extracts subtitles in the background. Users can search the subtitles and jump to specific timestamps in the video based on the search results. 

## Features

- **Video Upload**: Users can upload video files having subtitles (.mp4,.mkv).
- **Subtitle Extraction**: Subtitles are automatically extracted in the background after video uploads, subtitles are extracted using ffmpeg.
- **Search Subtitles**: Users can search for words, phrases within subtitles and jump to the timestamp in the video.
- **Django Backend**: Django framework are used in this assessment.
- **PostgreSQL Support** (optional): You can configure the application to use PostgreSQL for storing subtitle data.

## Getting Started

### Prerequisites

- Python 3.x
- Django
- PostgreSQL (optional for advanced database setup)

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Huzaifa-Antule/Fatmug-Assessment.git
   cd Fatmug-Assessment
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required Python dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup (Optional)**

   By default, the project uses SQLite, but you can configure it to use PostgreSQL if needed. To configure PostgreSQL, update your `DATABASES` setting in `settings.py`:
   PostgreSQL
   ```bash
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'Fatmug',
           'USER': 'postgres',
           'PASSWORD': '123',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```
   Django's Default
   ```bash
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
      }
    }
   ```
   Ensure PostgreSQL is running and accessible with the provided credentials.

5. **Run Migrations (Optional)**

   If you have updated the database to PostgreSQL or made changes to the models, you can run migrations:

   ```bash
   python manage.py makemigrations
   ```
   
   ```bash
   python manage.py migrate
   ```

   For SQLite (default setup), migrations will already be included.

7. **Create a Superuser**

   To manage the application through Django’s admin interface, create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server**

   Finally, start the development server:

   ```bash
   python manage.py runserver
   ```

   Open your browser and navigate to `http://127.0.0.1:8000` or `http://localhost:8000` to access the application.

### Optional: Docker Setup

If you prefer to use Docker for containerizing the application, follow these steps.

1. **Build and Run Containers**

   ```bash
   docker-compose up --build
   ```

2. **Access the Application**

   - **Django Application**: `http://localhost:8000`
   - **PostgreSQL**: Accessible at `localhost:5432` with the credentials in `docker-compose.yml`.


## Usage

1. **Uploading Videos**: you can upload videos via the web interface. The application will extract subtitles from the video automatically.
2. **Search Subtitles**: You can search within the subtitles and navigate to the specific timestamp in the video by clicking on the search result.

## Screenshots
![ScreenShots](https://github.com/Huzaifa-Antule/Fatmug-Assessment/blob/6d52392e3dce42a28e3ee8e7eb8561a5a0b01118/Screenshots/commands.JPG)
![ScreenShots](https://github.com/Huzaifa-Antule/Fatmug-Assessment/blob/6d52392e3dce42a28e3ee8e7eb8561a5a0b01118/Screenshots/Details%20Page.JPG)
![ScreenShots](https://github.com/Huzaifa-Antule/Fatmug-Assessment/blob/6d52392e3dce42a28e3ee8e7eb8561a5a0b01118/Screenshots/Searching.JPG)


## License

This project is licensed under the MIT License - see the [MIT](https://github.com/Huzaifa-Antule/Fatmug-Assessment?tab=MIT-1-ov-file) file for details.

## Contributing

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -am 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Submit a pull request.

## Limitations

- Large videos can decrease the performance of the application.
- some .mkv or other files create issue for jumping on timestamps and skipping issue.
- Subtitles are stored in media folder, hard to retrieve from PostgreSQLdatabase.

