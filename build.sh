git pull
cd webserver
docker build -t tlgcode .
docker-compose down
docker-compose up -d