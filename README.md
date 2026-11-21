# Simple Web App - CI/CD to AWS EC2 with Docker

Files:
- `app.py` - the web app (3 pages: `/`, `/health`, `/api/info`)
- `test_app.py` - 3 automated tests
- `requirements.txt` - Python packages
- `Dockerfile` - how to build the container image
- `.github/workflows/ci-cd.yml` - the pipeline: test -> build & push to Docker Hub -> deploy to EC2
- `postman_collection.json` - Postman tests (set `base_url` to `http://<your-elastic-ip>`)

Run locally:  `docker build -t simple-webapp .`  then  `docker run -p 8080:8080 simple-webapp`  and open http://localhost:8080

GitHub settings (Settings -> Secrets and variables -> Actions):
- Secrets: `DOCKERHUB_TOKEN`, `EC2_SSH_KEY` (whole .pem file)
- Variables: `DOCKERHUB_USERNAME`, `EC2_HOST` (your Elastic IP)

EC2: Amazon Linux 2023, ports 22 + 80 open, Elastic IP attached, Docker installed:
`sudo dnf install -y docker && sudo systemctl enable --now docker && sudo usermod -aG docker ec2-user`
