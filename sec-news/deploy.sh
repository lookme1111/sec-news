#!/bin/bash
# deploy.sh

set -e

echo "开始部署网安资讯平台..."

mkdir -p data backend/spiders backend/models backend/templates backend/static/{css,js,images}

docker-compose down
docker-compose up -d

echo "部署完成！"
echo "访问地址: http://localhost"
echo "查看日志: docker-compose logs -f web"