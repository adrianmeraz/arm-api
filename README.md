# Dependencies

## Rust & Cargo

### Windows
https://win.rustup.rs/

## VS Build Tools with C++ options
### Windows
https://visualstudio.microsoft.com/downloads/?q=build+tools#build-tools-for-visual-studio-2022

## Install Astral UV
https://docs.astral.sh/uv/getting-started/installation/

## Starting App
From app root directory, run:
```
uv run fastapi dev src\main.py --port 8086 --reload
```
Via Uvicorn
```
uvicorn src.main:app --port 8086 --reload --log-level trace
```

## Building / Pushing Images (WSL) Windows

### Open WSL
Open Powershell 7, and run this command:
```
wsl --install
```

### Change to project directory

Example:
```
cd /mnt/c/Users/adria/PycharmProjects/arm-api
```

## Docker

### Login to Docker
```
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 687272729792.dkr.ecr.us-west-2.amazonaws.com
```
### Build image
```
docker build -t arm-api-dev-ecr .
```
### Tag image
```
docker tag arm-api-dev-ecr:latest 687272729792.dkr.ecr.us-west-2.amazonaws.com/arm-api-dev-ecr:latest
```
### Push image to ECR
```
docker push 687272729792.dkr.ecr.us-west-2.amazonaws.com/arm-api-dev-ecr:latest
```

## uv commands

### Install Dependency
```
uv add ${dependency}
```
#### Example:
```
uv add httpx
```

## Repository Secrets
AWS_ACCESS_KEY_ID
AWS_REGION
AWS_SECRET_ACCESS_KEY
GH_PAT
