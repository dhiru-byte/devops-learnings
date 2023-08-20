### Docker
--------------------------------------------------------------------------------------
<details>
<summary>Create image out of running container.</code></summary><br><b>

docker commit [OPTIONS] CONTAINER [REPOSITORY[:TAG]]

```shell
docker commit my-container my-image:my-tag
```

`my-container` is the name or ID of the running container.
`my-image` is the name of the new image.
`my-tag` is the optional tag for the new image.

</b></details>

<details>
<summary>Create a Docker image from a file or URL.</code></summary><br><b>

docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]

```shell
docker import my_archive.tar my-image:tag

```
`my_archive.tar`  is a tarball archive file, and `my-image:tag` is the name and tag you want to assign to the imported Docker image.
</b></details>

<details>
<summary>What is Docker & it's feature ?.</code></summary><br><b>

Docker is an open-source containerization platform. It is used to automate the deployment of any application, using lightweight, portable containers.

Docker’s most essential features include:

* Application agility
* Developer productivity
* Easy modeling
* Operational efficiencies
* Placement and affinity
* Version control
</b></details>

<details>
<summary> Different type of Networking in Docker.</code></summary><br><b>

• bridge:  The default network driver. If you don’t specify a driver, this is the type of network you are creating. Bridge networks are usually used when your applications run in standalone containers that need to communicate, are best when you need multiple containers to communicate on the same Docker host.

• host: For standalone containers, remove network isolation between the container and the Docker host, and use the host’s networking directly, are best when the network stack should not be isolated from the Docker host, but you want other aspects of the container to be isolated. 

• overlay: Overlay networks connect multiple Docker daemons together and enable swarm services to communicate with each other. You can also use overlay networks to facilitate communication between a swarm service and a standalone container, or between two standalone containers on different Docker daemons. This strategy removes the need to do OS-level routing between these containers. are best when you need containers running on different Docker hosts to communicate, or when multiple applications work together using swarm services.

• macvlan: Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. The Docker daemon routes traffic to containers by their MAC addresses. Using the macvlan driver is sometimes the best choice when dealing with legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host’s network stack, are best when you are migrating from a VM setup or need your containers to look like physical hosts on your network, each with a unique MAC address.

• none: For this container, disable all networking. Usually used in conjunction with a custom network driver. none is not available for swarm services. 
</b></details>

<details>
<summary> Does Docker have any downsides?.</code></summary><br><b>

Docker isn’t perfect. It comes with its share of drawbacks, including:

* Lacks a storage option.
* Monitoring options are less than ideal.
* You can’t automatically reschedule inactive nodes.
* Automatic horizontal scaling set up is complicated.
</b></details>

<details>
<summary> Explain the various Docker components.</code></summary><br><b>

* `Docker Client`: Performs Docker build pull and run operations to open up communication with the Docker Host. The Docker command then employs Docker API to call any queries to run.

* `Docker Host`: Contains Docker daemon, containers, and associated images. The Docker daemon establishes a connection with the Registry. The stored images are the type of metadata dedicated to containerized applications.

* `Registry`: This is where Docker images are stored. There are two of them, 

public registry and  private one. 
Docker Hub and Docker Cloud are two public registries available for use by anyone.
</b></details>


<details>
<summary> What is a container?.</code></summary><br><b>

Containers are deployed applications bundled with all necessary dependencies and configuration files. All of the elements share the same OS kernel  and run as isolated systems in the host operating system.. Since the container isn’t tied to any one IT infrastructure, it can run on a different system or the cloud.
</b></details>

<details>
<summary> Explain virtualization.</code></summary><br><b>

A hypervisor is a software that makes virtualization happen because of which is sometimes referred to as the Virtual Machine Monitor. This divides the resources of the host system and allocates them to each guest environment installed such as a server, data storage, or application.
Virtualization lets you divide a system into a series of separate sections, each one acting as a distinct individual system. The virtual environment is called a virtual machine.

* Native Hypervisor: This type is also called a Bare-metal Hypervisor and runs directly on the underlying host system which also ensures direct access to the host hardware which is why it does not require base OS.

* Hosted Hypervisor: This type makes use of the underlying host operating system which has the existing OS installed.


</b></details>

<details>
<summary> What’s the difference between virtualization and containerization?.</code></summary><br><b>

Virtualization is an abstract version of a physical machine, while containerization is the abstract version of an application.
</b></details>


<details>
<summary> Describe a Docker container’s lifecycle.</code></summary><br><b>

* Create container
* Run container
* Pause container
* Unpause container
* Start container
* Stop container
* Restart container
* Kill container
* Destroy container
</b></details>

<details>
<summary> What are docker images?.</code></summary><br><b>

They are executable packages(bundled with application code & dependencies, software packages, etc.) for the purpose of creating containers. 
Docker images can be deployed to any docker environment and the containers can be spun up there to run the application.
</b></details>

<details>
<summary> What is a DockerFile?.</code></summary><br><b>

It is a  file that has all Instructions which need to build a docker image. filename should be `Dockerfile`
</b></details>

<details>
<summary> What can you tell about Docker Compose?.</code></summary><br><b>

It is a YAML file consisting of all the details regarding various services, networks, and volumes that are needed for setting up the Docker-based application. So, docker-compose is used for creating multiple containers, host them and establish communication between them. For the purpose of communication amongst the containers, ports are exposed by each and every container.
</b></details>

<details>
<summary> Can you tell something about docker namespace?.</code></summary><br><b>

A namespace is basically a Linux feature that ensures OS resources partition in a mutually exclusive manner. This forms the core concept behind containerization as namespaces introduce a layer of isolation amongst the containers. In docker, the namespaces ensure that the containers are portable and they don't affect the underlying host. Examples for namespace types that are currently being supported by Docker – PID, Mount, User, Network, IPC.
</b></details>

<details>
<summary> Difference between COPY & ADD Instruction in Dockerfile?.</code></summary><br><b>

Both the commands have similar functionality, but COPY is more preferred because of its higher transparency level than that of ADD.

* COPY provides just the basic support of copying local files into the container whereas

* ADD provides additional features like remote URL and tar extraction support.
</b></details>


<details>
<summary> Can you tell the differences between a docker Image and Layer?.</code></summary><br><b>

Image: This is built up from a series of read-only layers of instructions. An image corresponds to the docker container and is used for speedy operation due to the caching mechanism of each step.

Layer: Each layer corresponds to an instruction of the image’s Dockerfile. In simple words, the layer is also an image but it is the image of the instructions run.

The result of building a dockerfile is an image. Whereas the instructions present in this file add the layers to the image. The layers can be thought of as intermediate images. 
</b></details>

<details>
<summary>  Where are docker volumes stored in docker?.</code></summary><br><b>

Volumes are created and managed by Docker and cannot be accessed by non-docker entities. They are stored in Docker host filesystem at 
/var/lib/docker/volumes/
</b></details>

<details>
<summary> Can you differentiate between Daemon Logging and Container Logging?.</code></summary><br><b>

In docker, logging is supported at 2 levels and they are logging at the Daemon level or logging at the Container level.
Daemon Level has kind of logging has four levels- Debug, Info, Error, and Fatal.
- Debug has all the data that happened during the execution of the daemon process.
- Info carries all the information along with the error information during the execution of the daemon process.
- Errors have those errors that occurred during the execution of the daemon process.
- Fatal has the fatal errors that occurred during the execution.

Container Level:
- Container level logging can be done using the command: sudo docker run –it <container_name> /bin/bash
- In order to check for the container level logs, we can run the command: sudo docker logs <container_id>

</b></details>

<details>
<summary> Difference between CMD and ENTRYPOINT?.</code></summary><br><b>

* `CMD` command provides executable defaults for an executing container. In case the executable has to be omitted then the usage of ENTRYPOINT instruction along with the JSON array format has to be incorporated.

* `ENTRYPOINT` specifies that the instruction within it will always be run when the container starts. 
This command provides an option to configure the parameters and the executables. If the DockerFile does not have this command, then it would still get inherited from the base image mentioned in the FROM instruction.

* Most commonly used ENTRYPOINT is /bin/sh or /bin/bash for most of the base images.As part of good practices, every DockerFile should have at least one of these two commands.
</b></details>

<details>
<summary> What is the default IP address of the Docker host?.</code></summary><br><b>

` 172.17. 0.0/16`
</b></details>

<details>
<summary> Pull, create, and run 'hello-world'.</code></summary><br><b>

` docker run hello-world`
</b></details>

<details>
<summary> Get the Docker version.</code></summary><br><b>

` docker version `
</b></details>

<details>
<summary> Container Lifecycle</code></summary><br><b>

* [`docker create`](https://docs.docker.com/engine/reference/commandline/create) creates a container but does not start it.
* [`docker rename`](https://docs.docker.com/engine/reference/commandline/rename/) allows the container to be renamed.
* [`docker run`](https://docs.docker.com/engine/reference/commandline/run) creates and starts a container in one operation.
* [`docker rm`](https://docs.docker.com/engine/reference/commandline/rm) deletes a container.
* [`docker update`](https://docs.docker.com/engine/reference/commandline/update/) updates a container's resource limits.

If you want a transient container, 

`docker run --rm` : will remove the container after it stops.

`docker run -v $HOSTDIR:$DOCKERDIR` : To map a directory on the host to a docker container.

If you want to remove also the volumes associated with the container, the deletion of the container must include the `-v` switch like in `docker rm -v`.
</b></details>


<details>
<summary> Starting and Stopping.</code></summary><br><b>

* [`docker start`](https://docs.docker.com/engine/reference/commandline/start) starts a container so it is running.
* [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop) stops a running container.
* [`docker restart`](https://docs.docker.com/engine/reference/commandline/restart) stops and starts a container.
* [`docker pause`](https://docs.docker.com/engine/reference/commandline/pause/) pauses a running container, "freezing" it in place.
* [`docker unpause`](https://docs.docker.com/engine/reference/commandline/unpause/) will unpause a running container.
* [`docker wait`](https://docs.docker.com/engine/reference/commandline/wait) blocks until running container stops.
* [`docker kill`](https://docs.docker.com/engine/reference/commandline/kill) sends a SIGKILL to a running container.
* [`docker attach`](https://docs.docker.com/engine/reference/commandline/attach) will connect to a running container.

If you want to detach from a running container, use `Ctrl + p, Ctrl + q`.
If you want to integrate a container with a [host process manager](https://docs.docker.com/engine/admin/host_integration/), start the daemon with `-r=false` then use `docker start -a`.

If you want to expose container ports through the host, see the [exposing ports](#exposing-ports) section.

Restart policies on crashed docker instances are [covered here](http://container42.com/2014/09/30/docker-restart-policies/).
</b></details>

<details>
<summary> CPU Constraints.</code></summary><br><b>


You can limit CPU, either using a percentage of all CPUs, or by using specific cores.  

For example, you can tell the [`cpu-shares`](https://docs.docker.com/engine/reference/run/#/cpu-share-constraint) setting.  The setting is a bit strange -- 1024 means 100% of the CPU, so if you want the container to take 50% of all CPU cores, you should specify 512.  See <https://goldmann.pl/blog/2014/09/11/resource-management-in-docker/#_cpu> for more:

```sh
docker run -it -c 512 agileek/cpuset-test
```

You can also only use some CPU cores using [`cpuset-cpus`](https://docs.docker.com/engine/reference/run/#/cpuset-constraint).  See <https://agileek.github.io/docker/2014/08/06/docker-cpuset/> for details and some nice videos:

```sh
docker run -it --cpuset-cpus=0,4,6 agileek/cpuset-test
```

Note that Docker can still **see** all of the CPUs inside the container -- it just isn't using all of them.  See <https://github.com/docker/docker/issues/20770> for more details.
</b></details>

<details>
<summary> Memory Constraint.</code></summary><br><b>

You can also set [memory constraints](https://docs.docker.com/engine/reference/run/#/user-memory-constraints) on Docker:

```sh
docker run -it -m 300M ubuntu:14.04 /bin/bash
```
</b></details>

<details>
<summary> Different objects Info.</code></summary><br><b>

* [`docker ps`](https://docs.docker.com/engine/reference/commandline/ps) shows running containers.
* [`docker logs`](https://docs.docker.com/engine/reference/commandline/logs) gets logs from container.  (You can use a custom log driver, but logs is only available for `json-file` and `journald` in 1.10).
* [`docker inspect`](https://docs.docker.com/engine/reference/commandline/inspect) looks at all the info on a container (including IP address).
* [`docker events`](https://docs.docker.com/engine/reference/commandline/events) gets events from container.
* [`docker port`](https://docs.docker.com/engine/reference/commandline/port) shows public facing port of container.
* [`docker top`](https://docs.docker.com/engine/reference/commandline/top) shows running processes in container.
* [`docker stats`](https://docs.docker.com/engine/reference/commandline/stats) shows containers' resource usage statistics.
* [`docker diff`](https://docs.docker.com/engine/reference/commandline/diff) shows changed files in the container's FS.

`docker ps -a` shows running and stopped containers.

`docker stats --all` shows a list of all containers, default shows just running.
</b></details>

<details>
<summary> Image Lifecycle.</code></summary><br><b>

* [`docker images`](https://docs.docker.com/engine/reference/commandline/images) shows all images.
* [`docker import`](https://docs.docker.com/engine/reference/commandline/import) creates an image from a tarball.
* [`docker build`](https://docs.docker.com/engine/reference/commandline/build) creates image from Dockerfile.
* [`docker commit`](https://docs.docker.com/engine/reference/commandline/commit) creates image from a container, pausing it temporarily if it is running.
* [`docker rmi`](https://docs.docker.com/engine/reference/commandline/rmi) removes an image.
* [`docker load`](https://docs.docker.com/engine/reference/commandline/load) loads an image from a tar archive as STDIN, including images and tags (as of 0.7).
* [`docker save`](https://docs.docker.com/engine/reference/commandline/save) saves an image to a tar archive stream to STDOUT with all parent layers, tags & versions (as of 0.7).
* [`docker history`](https://docs.docker.com/engine/reference/commandline/history) shows history of image.
* [`docker tag`](https://docs.docker.com/engine/reference/commandline/tag) tags an image to a name (local or registry).

</b></details>

<details>
<summary> What command is used for remove all stopped containers, unused networks, build caches, and dangling images?.</code></summary><br><b>

` docker system prune -f`

* `docker system prune`
* `docker volume prune`
* `docker network prune`
* `docker container prune`
* `docker image prune`
</b></details>

<details>
<summary> Copying Files From/To  docker containers.</code></summary><br><b>

` docker cp myfile.txt ccae4670f030:/usr/share`

Syntax to Copy from Container to Docker Host  
` docker cp {options} CONTAINER:SRC_PATH DEST_PATH `
</b></details>

<details>
<summary> Clean your docker host using the commands (in bash).</code></summary><br><b>
 
` docker stop  $(docker ps -aq) `
` docker rm -f $(docker ps -a -q) `
` docker volume rm $(docker volume ls -q) `
</b></details>

<details>
<summary> Network Lifecycle.</code></summary><br><b>


* [`docker network connect`](https://docs.docker.com/engine/reference/commandline/network_connect/) NETWORK CONTAINER Connect a container to a network
* [`docker network disconnect`](https://docs.docker.com/engine/reference/commandline/network_disconnect/) NETWORK CONTAINER Disconnect a container from a network

You can specify a [specific IP address for a container](https://blog.jessfraz.com/post/ips-for-all-the-things/):

```sh
# create a new bridge network with your subnet and gateway for your ip block
docker network create --subnet 203.0.113.0/24 --gateway 203.0.113.254 iptastic

# run a nginx container with a specific ip in that block
$ docker run --rm -it --net iptastic --ip 203.0.113.2 nginx

# curl the ip from any other place (assuming this is a public ip block duh)
$ curl 203.0.113.2
```
</b></details>

<details>
<summary> List Docker Images.</code></summary><br><b>

`docker images` : to list Docker Images.

`docker images -a` : Show all images(default hides intermediate images).

`docker images alpine:3.7` : List images by name and tag.

`docker images --no-trunc` : List the full length image IDs.

`docker images --filter=reference='alpine'` : List images with filter.

</b></details>

<details>
<summary> Saving Images & Containers as Tar Files for Sharing.</code></summary><br><b>

save and load work with Docker images.

save works with Docker images. It saves everything needed to build a container from scratch. Use this command if you want to share an image with others.

load works with Docker images. Use this command if you want to run an image exported with save. Unlike pull, which requires connecting to a Docker registry, load can import from anywhere (e.g. a file system, URLs).

export works with Docker containers, and it exports a snapshot of the container’s file system. Use this command if you want to share or back up the result of building an image.

import works with the file system of an exported container, and it imports it as a Docker image. Use this command if you have an exported file system you want to explore or use as a layer for a new image.

Load an image from file:

```sh
docker load < my_image.tar.gz
```

Save an existing image:

```sh
docker save my_image:my_tag | gzip > my_image.tar.gz
```

Import a container as an image from file:

```sh
cat my_container.tar.gz | docker import - my_image:my_tag
```

Export an existing container:

```sh
docker export my_container | gzip > my_container.tar.gz
```

Difference between loading a saved image and importing an exported container as an image.

Loading an image using the `load` command creates a new image including its history.  
Importing a container as an image using the `import` command creates a new image excluding the history which results in a smaller image size compared to loading an image.
</b></details>

<details>
<summary> Registry & Repository.</code></summary><br><b>

A repository is a *hosted* collection of tagged images that together create the file system for a container.

A registry is a *host* -- a server that stores repositories and provides an HTTP API for [managing the uploading and downloading of repositories](https://docs.docker.com/engine/tutorials/dockerrepos/).

Docker.com hosts its own [index](https://hub.docker.com/) to a central registry which contains a large number of repositories.  Having said that, the central docker registry [does not do a good job of verifying images](https://titanous.com/posts/docker-insecurity) and should be avoided if you're worried about security.

* [`docker login`](https://docs.docker.com/engine/reference/commandline/login) to login to a registry.
* [`docker logout`](https://docs.docker.com/engine/reference/commandline/logout) to logout from a registry.
* [`docker search`](https://docs.docker.com/engine/reference/commandline/search) searches registry for image.
* [`docker pull`](https://docs.docker.com/engine/reference/commandline/pull) pulls an image from registry to local machine.
* [`docker push`](https://docs.docker.com/engine/reference/commandline/push) pushes an image to the registry from local machine.
</b></details>

<details>
<summary> Dockerfile Instruction.</code></summary><br><b>


* [.dockerignore](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
* [FROM](https://docs.docker.com/engine/reference/builder/#from) Sets the Base Image for subsequent instructions.
* [MAINTAINER (deprecated - use LABEL instead)](https://docs.docker.com/engine/reference/builder/#maintainer-deprecated) Set the Author field of the generated images.
* [RUN](https://docs.docker.com/engine/reference/builder/#run) execute any commands in a new layer on top of the current image and commit the results.
* [CMD](https://docs.docker.com/engine/reference/builder/#cmd) provide defaults for an executing container.
* [EXPOSE](https://docs.docker.com/engine/reference/builder/#expose) informs Docker that the container listens on the specified network ports at runtime.  NOTE: does not actually make ports accessible.
* [ENV](https://docs.docker.com/engine/reference/builder/#env) sets environment variable.
* [ADD](https://docs.docker.com/engine/reference/builder/#add) copies new files, directories or remote file to container.  Invalidates caches. Avoid `ADD` and use `COPY` instead.
* [COPY](https://docs.docker.com/engine/reference/builder/#copy) copies new files or directories to container.  By default this copies as root regardless of the USER/WORKDIR settings.  Use `--chown=<user>:<group>` to give ownership to another user/group.  (Same for `ADD`.)
* [ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint) configures a container that will run as an executable.
* [VOLUME](https://docs.docker.com/engine/reference/builder/#volume) creates a mount point for externally mounted volumes or other containers.
* [USER](https://docs.docker.com/engine/reference/builder/#user) sets the user name for following RUN / CMD / ENTRYPOINT commands.
* [WORKDIR](https://docs.docker.com/engine/reference/builder/#workdir) sets the working directory.
* [ARG](https://docs.docker.com/engine/reference/builder/#arg) defines a build-time variable.
* [ONBUILD](https://docs.docker.com/engine/reference/builder/#onbuild) adds a trigger instruction when the image is used as the base for another build.
* [STOPSIGNAL](https://docs.docker.com/engine/reference/builder/#stopsignal) sets the system call signal that will be sent to the container to exit.
* [LABEL](https://docs.docker.com/config/labels-custom-metadata/) apply key/value metadata to your images, containers, or daemons.
* [SHELL](https://docs.docker.com/engine/reference/builder/#shell) override default shell is used by docker to run commands.
* [HEALTHCHECK](https://docs.docker.com/engine/reference/builder/#healthcheck) tells docker how to test a container to check that it is still working.
</b></details>

<details>
<summary> Docker Volumes.</code></summary><br><b>

* [`docker volume create`](https://docs.docker.com/engine/reference/commandline/volume_create/)
* [`docker volume rm`](https://docs.docker.com/engine/reference/commandline/volume_rm/)
* [`docker volume ls`](https://docs.docker.com/engine/reference/commandline/volume_ls/)
* [`docker volume inspect`](https://docs.docker.com/engine/reference/commandline/volume_inspect/)

Volumes are useful in situations where you can't use links (which are TCP/IP only). For instance, if you need to have two docker instances communicate by leaving stuff on the filesystem.

You can mount them in several docker containers at once, using `docker run --volumes-from`.

Because volumes are isolated filesystems, they are often used to store state from computations between transient containers. That is, you can have a stateless and transient container run from a recipe, blow it away, and then have a second instance of the transient container pick up from where the last one left off.

See [advanced volumes](http://crosbymichael.com/advanced-docker-volumes.html) for more details. [Container42](http://container42.com/2014/11/03/docker-indepth-volumes/) is also helpful.
</b></details>

<details>
<summary> Difference between docker attach and docker exec
.</code></summary><br><b>

* `docker attach` command allows you to attach to a running container using the container’s ID or name, either to view its ongoing output or to control it interactively. You can attach to the same contained process multiple times simultaneously, screen sharing style, or quickly view the progress of your detached process.

command docker attach is for attaching to the existing process. So when you exit, you exit the existing process.

If we use docker attach, we can use only one instance of shell. So if we want open new terminal with new instance of container’s shell, we just need run docker exec

If the docker container was started using /bin/bash command, you can access it using attach, if not then you need to execute the command to create a bash instance inside the container using exec. Attach isn’t for running an extra thing in a container, it’s for attaching to the running process.

To stop a container, use CTRL-c. This key sequence sends SIGKILL to the container. If –sig-proxy is true (the default),CTRL-c sends a SIGINT to the container. You can detach from a container and leave it running using the CTRL-p CTRL-q key sequence.

* `docker exec` is specifically for running new things in a already started container, be it a shell or some other process. The docker exec command runs a new command in a running container.

The command started using docker exec only runs while the container’s primary process (PID 1) is running, and it is not restarted if the container is restarted.

exec command works only on already running container. If the container is currently stopped, you need to first run it. So now you can run any command in running container just knowing its ID (or name)

</b></details>

<details>
<summary> What does docker run --network=none nginx do ?.</code></summary><br><b>

Disables all incoming and outgoing networking.
</b></details>

<details>
<summary> What is continuous Integration, Continuous Delivery & Continuous Deployment?.</code></summary><br><b>

`Continuous Integration (CI)` is a DevOps software development practice that enables the developers to merge their code changes in the central repository. That way, automated builds and tests can be run. The amendments by the developers are validated by creating a built and running an automated test against them.
In the case of Continuous Integration, a tremendous amount of emphasis is placed on testing automation to check on the application. This is to know if it is broken whenever new commits are integrated into the main branch.

`Continuous Delivery (CD)` is a DevOps practice that refers to the building, testing, and delivering improvements to the software code. The phase is referred to as the extension of the Continuous Integration phase to make sure that new changes can be released to the customers quickly in a substantial manner. This can be simplified as, though you have automated testing, the release process is also automated, and any deployment can occur at any time with just one click of a button.
Continuous Delivery gives you the power to decide whether to make the releases daily, weekly, or whenever the business requires it. The maximum benefits of Continuous Delivery can only be yielded if they release small batches, which are easy to troubleshoot if any glitch occurs.

`Continuous Deployment (CD)` is the final stage in the pipeline that refers to the automatic releasing of any developer changes from the repository to the production.
Continuous Deployment ensures that any change that passes through the stages of production is released to the end-users. There is absolutely no way other than any failure in the test that may stop the deployment of new changes to the output. This step is a great way to speed up the feedback loop with customers and is free from human intervention

</b></details>

<details>
<summary> Can a paused container be removed from Docker?.</code></summary><br><b>

No, it is not possible! A container MUST be in the stopped state before we can remove it.
</b></details>

<details>
<summary> Deploy Minio.</code></summary><br><b>

`docker run -d -p  9000:9000   -e "MINIO_ROOT_USER=admin"   -e "MINIO_ROOT_PASSWORD=123Dhiru!"   -v /mnt/data:/data   minio/minio server /data `

`mc config host add local http://172.17.0.2:9000 admin 123Dhiru! --api S3v4 --lookup auto `

`mc find local/test --newer-than 2d0h0m --ignore '*.html'`
</b></details>
