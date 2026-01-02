# Django Docker Multistage Builds

A Django recipe management application demonstrating Docker image optimization techniques using single-stage, multistage, and distroless builds.

## Project Goal

Learn and demonstrate Docker image optimization by comparing three different build approaches for the same Django application.

## Technologies Used

- **Application**: Python/Django
- **Database**: PostgreSQL
- **Web Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Containerization**: Docker

## Project Setup

1. **Clone the Repository**

```bash
git clone https://github.com/nihmaltk/django-docker-multistage.git
cd django-docker-multistage
```

2.  **Configure Environment**
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your values
```

3. **Build images**

- Choose one or all of the following commands to build the images. The project goal is to compare them!

**Single-stage Build** 
```bash
docker build -t recipe-app:single .
```
**Multistage Build**
```bash
docker build -f Dockerfile.multistage -t recipe-app:multi .
```
**Distroless Build**
```bash
docker build -f Dockerfile.distroless -t recipe-app:distroless .
```

4. **Running the Application**

- Create a dedicated network for secure, internal container communication
```bash
docker network create recipe-network
```
- **Start Database**
```bash
docker run -d \
  --name recipedb \
  --network recipe-network \
  --env-file .env \
  postgres:15-alpine
```
- **Run Application**
```bash
# Using distroless (smallest)
docker run -d \
  --name recipeweb \
  --network recipe-network \
  -p 8000:8000 \
  --env-file .env \
  recipe-app:distroless
```
- **Run Database Migrations**
```bash
docker exec recipeweb /usr/bin/python3 manage.py migrate
```
- **Create Superuser**
```bash
docker exec -it recipeweb /usr/bin/python3 manage.py createsuperuser
```

5. **Access Application**
- **Application:** http://localhost:8000
- **Admin Panel:** http://localhost:8000/admin

## Image Size Comparison

| Build Type   | Dockerfile              | Image Size | Description                 |
|------------  |-----------------------  |----------- |---------------------------  |
| Single-stage | `Dockerfile`            | 193 MB     | Simple, one-stage build     |
| Multistage   | `Dockerfile.multistage` | 185 MB     | Separates build and runtime |
| Distroless   | `Dockerfile.distroless` | 121 MB     | Minimal runtime, no shell   |

## Commands Reference

### View Images
```bash
docker images
```
### View Logs
```bash
docker logs recipeweb
docker logs recipedb
```
### Cleanup
```bash
docker stop recipeweb recipedb
docker rm recipeweb recipedb
docker network rm recipe-network
docker rmi recipe-app:single  recipe-app:multi recipe-app:distroless 
```

## Key Learnings

### Single-stage Builds
- Simple and straightforward
- Contains everything in one stage
- Larger final image size
- Includes build tools in runtime

### Multistage Builds
- Separates build stage from runtime stage
- Builder stage installs dependencies
- Runtime stage copies only necessary files
- Reduces image size by eliminating build tools

### Distroless Images
- Minimal runtime environment
- No shell, package managers, or unnecessary tools
- Significantly smaller image size
- Enhanced security (smaller attack surface)
- Trade-off: Harder to debug (no shell access)

## Key Concepts Applied

- **Layer caching:** Copying `requirements.txt` before code for faster rebuilds
- **`--user` flag:** Installing packages in user directory for easier copying between stages
- **Full paths in distroless:** Using absolute paths in the distroless environment due to the absence of a shell.
- **Security:** Minimal images reduce potential vulnerabilities by eliminating unnecessary binaries, shells, and package managers.

