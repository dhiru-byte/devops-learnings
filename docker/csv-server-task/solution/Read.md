docker run infracloudio/csvserver:latest 
docker logs <containerID>
docker ps 
docker ps -a
docker cp inputFile <containerID>:/csvserver/inputdata
docker start <containerID>

docker stop <containerID>
docker run -d -p 9393:9300 --env CSVSERVER_BORDER=Orange infracloudio/csvserver:latest 
docker logs <containerID>
docker ps 
docker ps -a
docker cp inputFile <containerID>:/csvserver/inputdata
docker start <containerID>
