# Docker Setup for YouTube AI Downloader

This document explains how to use Docker to set up and run the YouTube AI Downloader application.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your system
- [Docker Compose](https://docs.docker.com/compose/install/) installed on your system

## Quick Start

1. **Set up environment variables**

   Create a `.env` file in the root directory based on the `.env-sample`:

   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

2. **Build and start the Docker containers**

   ```bash
   docker-compose up -d
   ```

3. **Access the application**

   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Using Docker Commands

### Build the Docker image
```bash
docker build -t youtube-ai .
```

### Start the container
```bash
docker-compose up
```

### Start in detached mode (background)
```bash
docker-compose up -d
```

### Stop the container
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f
```

### Create a superuser for Django admin
```bash
docker-compose exec web python manage.py createsuperuser
```

## Data Persistence

- The `media` directory is mapped to the container for storing downloaded videos and audio files
- The SQLite database is also persisted through volume mapping
- Static files are mapped to the local system

## Customization

You can modify the `docker-compose.yml` file to change:
- Port mapping (default is 8000)
- Environment variables
- Volume mappings

## Troubleshooting

1. **Permission issues with media directory**

   If you encounter permission issues:
   ```bash
   sudo chmod -R 777 ./media
   ```

2. **Container fails to start**

   Check logs:
   ```bash
   docker-compose logs
   ```

3. **FFmpeg issues**

   The Dockerfile includes FFmpeg installation. If there are issues, you can check:
   ```bash
   docker-compose exec web ffmpeg -version
   ```
