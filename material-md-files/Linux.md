### Linux 
--------------------------------------------------------------------------------------

<details>
<summary>Prompt Customization.</code></summary><br><b>

Ubuntu
`sudo vi .bashrc` : `PS1="\[\033[01;32m\]\d \T \[\033[00m\]\$"`

Mac bash_profile file 
`export PS1="Dhirendra @\d \T $" ` & ` export PS1=”\u@\d \T $” `
</b></details>

<details>
<summary>Functions of OS ?.</code></summary><br><b>

 OS functions may include managing memory, files, processes, I/O system & devices, security, etc.

<p align="center">
<img src="./images/OS_functions.jpg" width="800" height="300" /> 
</p>

In an operating system software performs each of the function:

- `Process management`: It helps OS to create and delete processes. It also provides mechanisms for synchronization and communication among processes.
- `Memory management`: It performs the task of allocation and de-allocation of memory space to programs in need of this resources.
- `File management`: It manages all the file-related activities such as organization storage, retrieval, naming, sharing, and protection of files.
- `Device Management`: It keeps tracks of all devices. This module also responsible for this task is known as the I/O controller. It also performs the task of allocation and de-allocation of the devices.
- `I/O System Management`: One of the main objects of any OS is to hide the peculiarities of that hardware devices from the user.
- `Secondary-Storage Management`: Systems have several levels of storage which includes primary storage, secondary storage, and cache storage. Instructions and data must be stored in primary storage or cache so that a running program can reference it.
- `Security`: it protects the data and information of a computer system against malware threat and authorized access.
- `Command interpretation`: it interprets the commands given by the and acting system resources to process that commands.
- `Networking`: A distributed system is a group of processors which do not share memory, hardware devices, or a clock. The processors communicate with one another through the network.

- `Job accounting`: Keeping track of time & resource used by various job and users.

- `Communication management`: Coordination and assignment of compilers, interpreters, and another software resource of the various users of the computer systems.

</b></details>

<details>
<summary>Features of OS ?.</code></summary><br><b>

- Protected and supervisor mode.
- Allows disk access and file systems Device drivers Networking Security.
- Program Execution.
- Memory management Virtual Memory Multitasking.
- Handling I/O operations.
- Manipulation of the file system.
- Error Detection and handling.
- Resource allocation.
- Information and Resource Protection.

</b></details>

<details>
<summary>What Happens When You Type google.com Or Any Other URL In Your Browser And Press Enter ? .</code></summary><br><b>

A webpage is basically a text file formatted a certain way so that your browser (ie. Chrome, Firefox, Safari, etc) can understand it; this format is called HyperText Markup Language (HTML). These files are located in computers that provide the service of storing said files and wait for someone to need them to deliver them. They are called servers because they serve the content that they hold to whoever needs it.

These servers can vary in classes, the most common and the one that we'll be talking about in the main portion of this article is a web server, the one that serves web pages. We can also find application servers, which are the ones that hold an application base code that will then be used to interact with a web browser or other applications. Database servers are also out there, which are the ones that hold a database that can be updated and consulted when needed.

These servers in order to deliver their content, much like in physical courier services, need to have an address so that the person needing said content can make a "letter" requesting the delivery; the person requesting the content in turn also has an address where the server can deliver the content to. These addresses are called IP (Internet Protocol) Address, a set of 4 numbers that range from 0 to 255 (one byte) separated by periods (ie. 127.0.0.1).

Another concept that is important to know is that the courier service traffic for the delivery can be one of two: Transmission Control Protocol (TCP) and User Datagram Protocol (UDP). Each one determines the way the content of a server is served, or delivered.

TCP is usually used to deliver static websites such as Wikipedia or Google and also email services and to download files to your computer because TCP makes sure that all the content that is needed gets delivered. It accomplishes this by sending the file in small packets of data and along with each packet a confirmation to know that the packet was delivered; that's why if you are ever downloading something and your internet connection suddenly drops when it comes back up you don't have to start over because the server would know exactly how many packets you have and how many you still need to receive. The downside to TCP is that because it has to confirm whether you got the packet or not before sending the next, it tends to be slower.

UDP, on the other hand, is usually used to serve live videos or online games. This is because UDP is a lot faster than TCP since UDP does not check if the information was received or not; it is not important. The only thing UDP cares about is sending the information. That is the reason why if you've ever watched a live video and if either your internet connection or the host's drops, you would just stop seeing the content; and when the connection comes back up you will only see the current stream of the broadcast and what was missed is forever lost. This is also true for online videogames (if you've played them you know exactly what this means)

What actually happens...

So back to the main question of what happens when you type www.google.com or any other URL (Uniform Resource Locator) in your web browser and press Enter. So the first thing that happens is that your browser looks up in its cache to see if that website was visited before and the IP address is known. If it can't find the IP address for the URL requested then it asks your operating system to locate the web site. The first place your operating system is going to check for the address of the URL you specified is in the hosts file (/etc/hosts in Linux and Mac, c:\windows\system32\drivers\etc\hosts in Windows). If the URL is not found inside this file, then the OS will make a DNS request to find the IP Address of the web page. The first step is to ask the Resolver (or Internet Service Provider) server to look up in its cache to see if it knows the IP Address, if the Resolver does not know then it asks the root server to ask the .COM TLD (Top Level Domain) server - if your URL ends in .net then the TLD server would be .NET and so on - the TLD server will again check in its cache to see if the requested IP Address is there. If not, then it will have at least one of the authoritative name servers associated with that URL, and after going to the Name Server, it will return the IP Address associated with your URL. All this was done in a matter of milliseconds WOW!

After the OS has the IP Address and gives it to the browser, it then makes a GET (a type of HTTP Method) to said IP Address. When the request is made the browser again makes the request to the OS which then, in turn, packs the request in the TCP traffic protocol we discussed earlier, and it is sent to the IP Address. On its way, it is checked by both the OS' and the server's firewall to make sure that there are no security violations. And upon receiving the request the server (usually a load balancer that directs traffic to all available server for that website) sends a response with the IP Address of the chosen server along with the SSL (Secure Sockets Layer) certificate to initiate a secure session (HTTPS). Finally, the chosen server then sends the HTML, CSS, and Javascript files (If any) back to the OS who in turn gives it to the browser to interpret it. And then you get your website as you know it.

</b></details>

<details>
<summary>Resident & Virtual Memory in Linux .</code></summary><br><b>

`Resident memory` is the part of the process memory that corresponds to the physical memory actually in operational use by this process. Over time, the operating system may swap out some of a process's resident memory according to a least-recently-used algorithm to make room for other code or data.

`Resident memory`, labelled RES: How much physical memory, how much RAM, your process is using. RES is the important number. 

`Virtual memory`, labelled VIRT: How much memory your process thinks it's using. Usually much bigger than RES, thanks to the Linux kernel's clever memory management.Virtual memory is Hard Disk space reserved for the O/S to act as RAM. The O/S “swaps” data in and out of the virtual memory to place it in RAM, or to take it out of RAM.
</b></details>

<details>
<summary>Top Command Different column info.</code></summary><br><b>

The column headings in the process list are as follows:

* PID: Process ID.

* USER: The owner of the process.

* PR: Process priority.

* NI: The nice value of the process.

* VIRT: Amount of virtual memory used by the process.

* RES: Amount of resident memory used by the process.

* SHR: Amount of shared memory used by the process.

* S: Status of the process. (See the list below for the values this field can take).

* %CPU: The share of CPU time used by the process since the last update.

* %MEM: The share of physical memory used.

* TIME+: Total CPU time used by the task in hundredths of a second.

* COMMAND: The command name or command line (name + options).

[Detail](https://www.howtogeek.com/668986/how-to-use-the-linux-top-command-and-understand-its-output/)
</b></details>


<details>
<summary>What is Operating System ?.</code></summary><br><b>

Operating system is an interface between user and the computer hardware. The hardware of the computer cannot understand the human readable language as it works on binaries i.e. 0's and 1's. Also it is very tough for humans to understand the binary language, in such case we need an interface which can translate human language to hardware and vice-versa for effective communication. 

* <b> Types of Operating System:</b>  
  * Single User - Single Tasking Operating System  
  * Single User - Multitasking Operating System  
  * Multi User - Multitasking Operating System  
</b></details>

<details>
<summary>What is OSI model & it's Layers?.</code></summary><br><b>

The Open Systems Interconnection (OSI) model describes seven layers that computer systems use to communicate over a network. It was the first standard model for network communications, adopted by all major computer and telecommunication companies in the early 1980s.

The modern Internet is not based on OSI, but on the simpler TCP/IP model. However, the OSI 7-layer model is still widely used, as it helps visualize and communicate how networks operate, and helps isolate and troubleshoot networking problems.

  * All --> People --> Seem --> To --> Need--> Data --> Processing "Application to physical"
<p align="center">
<img src="./images/OSI_Model3.jpg" width="500" height="450" /> 
</p>

<p align="center">
<img src="./images/OSI_Model2.jpg" width="500" height="450" /> 
</p>

</b></details>
<details>
<summary>Linux File System Hierarchy.</code></summary><br><b>

|Path     | Description        |
|:-----: |:---      |
| / |It is parent directory for all other directories.(root directory)|
| /root | It is home directory for root user and it provides working environment for root user|
| /home | It is home directory for other users and it provide working environment for other users|
| /boot |It contains bootable files for Linux. Like `GRUB (GRand Unified Boot loader)  boot.ini, ntldr` |
| /etc | It contains all configuration files. Like `User info /etc/passwd` |
| /usr | By default softwares are installed in /usr directory|
| /opt | It is optional directory for /usr and it contains third party softwares. |
| /bin | It contains commands used by all users(Binary files)|   
| /sbin | It contains commands used by only Super User (root) |
| /dev | It contains device file like `hard disk /dev/hda` |
| /proc |  It contain process files and data are not permanent, they keep changing like `information of CPU /proc/cpuinfo` |
| /var |It is containing variable data like `mails, log files` |   
| /mnt |It is default mount point for any partition. It is empty by default |
| /media |It contains all of removable media like `CD-ROM, pen drive` |
| /lib | It contains library files which are used by OS. Library files in Linux are shared object files|

</b></details>


<details>
<summary>Linux Architecture.</code></summary><br><b>

* The architecture of UNIX can be divided into Four levels of functionality, as shown in Figure .  
<p align="center">
<img src="./images/LinuxArchitecture.jpg" width="500" height="450" /> 
</p>

* <b> Hardware </b>   
Hardware consists of all physical devices attached to the System.   
<b>Example:-</b> Hard disk drive, RAM, Motherboard, CPU etc.

* <b> Kernel </b>  
kernel is the core component for any (Linux) operating system which directly interacts with the hardware. it schedules tasks, manages resources, and controls security.  
  * Different types of the kernel are:  
    * Monolithic Kernel  
    * Hybrid kernels  
    * Exo kernels  
    * Micro kernels  

* <b> Shell </b>  
Shell is the interface which takes input from users and sends instructions to the Kernel, Also takes the output from Kernel and send the result back to output user and starting applications.  
  * Types of shells are classified into four:
    * Korn shell
    * Bourne shell
    * C shell

* <b> Utilities </b>  
Utilities provides the functionalities of an operating system to the users. 

</b></details>

<details>
<summary>What is Linux?.</code></summary><br><b>

Linux is an operating system based on UNIX and was first introduced by Linus Torvalds. It is based on the Linux Kernel and can run on different hardware platforms manufactured by Intel, MIPS, HP, IBM, SPARC, and Motorola. Another popular element in Linux is its mascot, a penguin figure named Tux.
</b></details>

<details>
<summary>What is the difference between UNIX and LINUX?.</code></summary><br><b>

Unix originally began as a propriety operating system from Bell Laboratories, which later on spawned into different commercial versions. On the other hand, Linux is free, open source and intended as a non-propriety operating system for the masses.
</b></details>

<details>
<summary>What is BASH?.</code></summary><br><b>

BASH is short for Bourne Again SHell, was written by Steve Bourne as a replacement to the original Bourne Shell(represented by /bin/sh). It combines all the features from the original version of Bourne Shell, plus additional functions to make it easier and more convenient to use. It has since been adapted as the default shell for most systems running Linux.
</b></details>

<details>
<summary>What is Linux Kernel?.</code></summary><br><b>

The Linux Kernel is a low-level systems software whose main role is to manage hardware resources for the user. It is also used to provide an interface for user-level interaction.
</b></details>

<details>
<summary> What is LILO?.</code></summary><br><b>

LILO is a boot loader for Linux. It is used mainly to load the Linux operating system into main memory so that it can begin its operations.
</b></details>

<details>
<summary> What is a swap space?.</code></summary><br><b>

Swap space is a certain amount of space used by Linux to temporarily hold some programs that are running concurrently. This happens when RAM does not have enough memory to hold all programs that are executing.
</b></details>

<details>
<summary> What is the advantage of open source?.</code></summary><br><b>

Open source allows you to distribute your software, including source codes freely to anyone who is interested. People would then be able to add features and even debug and correct errors that are in the source code. They can even make it run better and then redistribute these enhanced source code freely again. This eventually benefits everyone in the community.
</b></details>

<details>
<summary> What are the basic components of Linux?.</code></summary><br><b>

Just like any other typical operating system, Linux has all of these components: kernel, shells and GUIs, system utilities, and an application program. What makes Linux advantageous over other operating system is that every aspect comes with additional features and all codes for these are downloadable for free.
</b></details>

<details>
<summary> Does it help for a Linux system to have multiple desktop environments installed?.</code></summary><br><b>

In general, one desktop environment, like KDE or Gnome, is good enough to operate without issues. It’s all a matter of preference for the user, although the system allows switching from one environment to another. Some programs will work in one environment and not work on the other, so it could also be considered a factor in selecting which environment to use.
</b></details>

<details>
<summary> What is the basic difference between BASH and DOS?.</code></summary><br><b>

The key differences between the BASH and DOS console lie in 3 areas:

* BASH commands are case sensitive while DOS commands are not;

* Under BASH, / character is a directory separator and \ acts as an escape character. Under DOS, / serves as a command argument delimiter and \ is the directory separator

* DOS follows a convention in naming files, which is 8 character file name followed by a dot and 3 characters for the extension. BASH follows no such convention.
</b></details>

<details>
<summary> What is the importance of the GNU project?.</code></summary><br><b>

This so-called Free software movement allows several advantages, such as the freedom to run programs for any purpose and freedom to study and modify a program to your needs. It also allows you to redistribute copies of software to other people, as well as the freedom to improve software and have it released for the public.
</b></details>

<details>
<summary> Describe the root account.</code></summary><br><b>

The root account is like a systems administrator account and allows you full control of the system.
Here you can create and maintain user accounts, assigning different permissions for each account.
It is the default account every time you install Linux.
</b></details>


<details>
<summary> What is CLI?.</code></summary><br><b>

CLI is short for Command Line Interface. This interface allows the user to type declarative commands to instruct the computer to perform operations. CLI offers greater flexibility. However, other users who are already accustomed to using GUI find it difficult to remember commands including attributes that come with it.

</b></details>

<details>
<summary> What are the different modes when using vi editor?.</code></summary><br><b>

There are 3 modes under vi:
* ` Command mode ` – this is the mode where you start in
* ` Edit mode `  – this is the mode that allows you to do text editing
* ` Ex mode `    – this is the mode wherein you interact with vi with instructions to process a file.

</b></details>


<details>
<summary> How can you find out how much memory Linux is using?.</code></summary><br><b>

` cat /proc/meminfo ` : total memory Linux has available to use.

` free -b `: gives the size in bytes.

` free -k `: gives the size in kilobytes.

` free -m `: gives the size in megabytes.

` free -g `: gives the size in gigabytes.

` top `    : lists the physical memory information in a clear way.

` vmstat ` : vmstat (virtual memory stats) with -s switch lists the memory in detail.

 ` htop`

</b></details>

<details>
<summary>  find out  CPU Info Linux is using?.</code></summary><br><b>

` cat /proc/cpuinfo `
</b></details>


<details>
<summary> What is a typical size for a swap partition under a Linux system?.</code></summary><br><b>

The preferred size for a swap partition is twice the amount of physical memory available on the system. 

If this is not possible, then the minimum size should be the same as the amount of memory installed. 
</b></details>

<details>
<summary> Difference Between Process vs Thread.</code></summary><br><b>

A process is the execution of a program that allows you to perform the appropriate actions specified in a program. It can be defined as an execution unit where a program runs. The OS helps you to create, schedule, and terminates the processes which is used by CPU. The other processes created by the main process are called child process.

A process operations can be easily controlled with the help of PCB(Process Control Block). You can consider it as the brain of the process, which contains all the crucial information related to processing like process id, priority, state, and contents CPU register, etc.

Thread is an execution unit that is part of a process. A process can have multiple threads, all executing at the same time. It is a unit of execution in concurrent programming. A thread is lightweight and can be managed independently by a scheduler. It helps you to improve the application performance using parallelism.

Multiple threads share information like data, code, files, etc. We can implement threads in three different ways:
* Kernel-level threads

* User-level threads

* Hybrid threads

KEY DIFFERENCE

* Process means a program is in execution, whereas thread means a segment of a process.

* A Process is not Lightweight, whereas Threads are Lightweight.

* A Process takes more time to terminate, and the thread takes less time to terminate.

* Process takes more time for creation, whereas Thread takes less time for creation.

* Process likely takes more time for context switching whereas as Threads takes less time for context switching.

* A Process is mostly isolated, whereas Threads share memory.

* Process does not share data, and Threads share data with each other.

Properties of Process

* Creation of each process requires separate system calls for each process.

* It is an isolated execution entity and does not share data and information.

* Processes use the IPC(Inter-Process Communication) mechanism for communication that significantly increases the number of system calls.

* Process management takes more system calls.

* A process has its stack, heap memory with memory, and data map.

Properties of Thread

* Single system call can create more than one thread

* Threads share data and information.

* Threads shares instruction, global, and heap regions. However, it has its register and stack.

* Thread management consumes very few, or no system calls because of communication between threads that can be achieved using shared memory.
</b></details>


<details>
<summary> Differences Among A, CNAME, ALIAS, and URL records.</code></summary><br><b>

These are the main differences:

* The A record points a name to one or more IP addresses when the IP are known and stable.

i.e.  
     
     blog.dnsimple.com.     A        185.31.17.133

* A CNAME record can point a name to another CNAME or to an A record.. It should only be used when there are no other records on that name.

i.e. 
     
     blog.dnsimple.com.      CNAME   aetrion.github.io.

     aetrion.github.io.      CNAME   github.map.fastly.net.

     github.map.fastly.net.  A       185.31.17.133

* The ALIAS record maps a name to another name, but can coexist with other records on that name.

* The URL record redirects the name to the target name using the HTTP 301 status code.

Important rules:

* The A, CNAME, and ALIAS records cause a name to resolve to an IP. Conversely, the URL record redirects the name to a destination. 

* The URL record is a simple and effective way to apply a redirect for one name to another name, for example redirecting www.example.com to example.com.

* The A name must resolve to an IP. The CNAME and ALIAS records must point to a name.

</b></details>

<details>
<summary> How do you make your database work for a high number of requests at peak hours?.</code></summary><br><b>

To make the database perform higher.

* ` CPU ` : Increase no. of cores of CPU to keep host responsive. 

* ` Memory ` : Look at the page faults per second in the memory and keep it low. 

* ` Disk space ` : Make sure that you have a high amount of disk space.

* ` Database connections` : Make sure that you have enough database connections.

</b></details>


<details>
<summary> How do you optimize database?.</code></summary><br><b>

For better performance & optimizing the database following steps,

* `Use Indexing `: Index is a data structure that increases the speed of the data retrieval operations.

* `Execution plans `: Execution plan tool in the SQL server is useful in creating indexes.

* `Avoid coding loops `: When possible avoid the loops in your code to increase the performance of the database.

* `Avoid correlated SQL subqueries `: A correlated subquery gets values from the parent query. It decreases the performance of the database operations. So try to avoid it. Finally, Use or avoid temporary tables according to your specific requirements.

</b></details>

<details>
<summary> If there are no cookies how do you make your application work?.</code></summary><br><b>

The application can make use of the session ID tag to be used for creating sessions in the applications without the need for the cookies. Using the session ID, the application can create individual sessions for users without using cookies.
</b></details>

<details>
<summary> Tell me about garbage collection programming.</code></summary><br><b>

Garbage collection is the collection or gaining the memory back from the objects. 

The memory collected are not in use at the moment in any part of the program where the object is used. This process frees up the memory space that is no longer used by the objects and such. This process is implemented differently in different languages.

Most of the high-level programming languages have garbage collection process built into it. Low- level programming languages add garbage collection processes through external libraries. 

For eg: In C programming language, the garbage collection is taken care of by the user by using the malloc() and dealloc() functions. 

In C# programming language, the garbage collection is taken care of automatically. Users don’t need to do anything.
</b></details>


<details>
<summary> How do you measure network packet?.</code></summary><br><b>

Network performance of a packet is measured using various factors,

* ` Latency `: Amount of time that takes for the data to travel from one location to another.

* ` Packet Loss `: No. of packets transmitted from one location to another that fails to transmit.

* ` Throughput `: No. of items passing through a particular system.

* ` Bandwidth `: Amount of data that can be transferred over a given period of time.

* ` Jitter `: It is defined as the variation in time delay for the data packets that are sent over a network.

</b></details>

<details>
<summary> What are symbolic links?.</code></summary><br><b>

Symbolic links act similarly to shortcuts in Windows. Such links point to programs, files or directories. It also allows you instant access to it without having to go directly to the entire pathname.
</b></details>


<details>
<summary>  What are hard links?.</code></summary><br><b>

Hard links point directly to the physical file on disk, and not on the pathname. This means that if you rename or move the original file, the link will not break since the link is for the file itself, not the path where the file is located.
</b></details>

<details>
<summary>  What is iNode on Linux and more details on that?.</code></summary><br><b>

The iNode in Linux is an entry table containing information about the regular file and directory. It can be viewed as a data structure that contains the metadata about the files. 

The following are the contents of the iNode.

* ` User ID `     - Owner of the file.

* ` Group ID `    - Owner of the group.

* ` Size of File `- a major or minor number in some files.

* ` Timestamp `   - access time, and modification time.

* ` Attributes `  - some properties of the file.

* ` Access control list `- permission for users.

* ` Link count `  - The number of hard links relative to the inode.

* ` File type `   - Type of the file i.e. regular, directory, or pipe.

   Link to the location of the file and other metadata.
</b></details>

<details>
<summary>  What are Daemons?.</code></summary><br><b>

Daemons are services that provide several functions that may not be available under the base operating system. Its main task is to listen for service request and at the same time to act on these requests. After the service is done, it is then disconnected and waits for further requests.
</b></details>

<details>
<summary>  How do you switch from one desktop environment to another, such as switching from KDE to Gnome?.</code></summary><br><b>

Assuming you have these two environments installed, just log out from the graphical interface. Then at the login screen, type your login ID and password and choose which session type you wish to load. This choice will remain your default until you change it to something else.
</b></details>


<details>
<summary> HTTP Rest Api status codes.</code></summary><br><b>

HTTP defines these standard status codes that can be used to convey the results of a client’s request. The status codes are divided into five categories.

* 1xx: Informational – Communicates transfer protocol-level information.

* 2xx: Success – Indicates that the client’s request was accepted successfully.

* 3xx: Redirection – Indicates that the client must take some additional action in order to complete their request.

* 4xx: Client Error – This category of error status codes points the finger at clients.

* 5xx: Server Error – The server takes responsibility for these error status codes.

[Detail Read](https://restfulapi.net/http-status-codes/)
</b></details>

<details>
<summary>  What are the kinds of permissions under Linux?.</code></summary><br><b>

* ` Read (r) ` : users may read the files or list the directory

* ` Write (w)` : users may write to the file or new files to the directory
      
* ` Execute (x)`: users may run the file or lookup a specific file within a directory

Numeric representation :

| Read (r)| Write (w) | Execute (x) |
|---------|-----------|-------------|
|   4     |    2      |      1      |

`chmod 650 test.txt` : The user's permissions are: rw- or 4+2=6
                       The group's permissions are: r-x or 4+1=5
                        The others's permissions are: --- or 0

Symbolic Representation :

* Who - represents identities: u,g,o,a (user, group, other, all)

* What - represents actions: +, -, = (add, remove, set exact)

* Which - represents access levels: r, w, x (read, write, execute)

`chmod ug+rw test.txt` : to add the read and write permissions to a file named test.txt for user and group.

[In Detail](https://www.redhat.com/sysadmin/suid-sgid-sticky-bit)
</b></details>


<details>
<summary> What is Zombie Process in Linux?.</code></summary><br><b>

A zombie process is a process in its terminated state. This usually happens in a program that has parent-child functions. After a child function has finished execution, it sends an exit status to its parent function. Until the parent function receives and acknowledges the message, the child function remains in a “zombie” state, meaning it has executed but not exited.

A zombie process is also known as a defunct process. A zombie process or defunct process is a process that has completed execution (via the exit system call) but still has an entry in the process table: it is a process in the "Terminated state".

</b></details>

<details>
<summary> How to Setup SSH without password ?</code></summary><br><b>

* Generate A New SSH Key Pair on Local Machine `ssh-keygen -t rsa` .

* Copy Public Key to Remote Machine `ssh-copy-id remote_user@remote_IP` .
  
   copy the public key to the remote system that you want to access from your local system without passwords. We will use the ssh-copy-id command that is by default available in most Linux distributions. This command will copy the public key id_rsa.pub to the .ssh/authorized_keys file in the remote system.

* Add Private Key to SSH Authentication Agent on Local Server `ssh-add` .
  
  In our local machine, we will add the private key to the SSH authentication agent. This will allow us to log into the remote server without having to enter a password every time.
</b></details>


<details>
<summary> What is CIDR?.</code></summary><br><b>

Classless inter-domain routing (CIDR), which stands for Classless Inter-Domain Routing, is an IP addressing scheme that improves the allocation of IP addresses. It replaces the old system based on classes A, B, and C. This scheme also helped greatly extend the life of IPv4 as well as slow the growth of routing tables.

[Reference Video](https://www.youtube.com/watch?v=z07HTSzzp3o)

[Javatpoint](https://www.javatpoint.com/binary-numbers-list)
</b></details>

<details>
<summary> What is CPU load in Linux?.</code></summary><br><b>

 CPU load is the number of processes which are being executed by CPU or waiting to be executed by CPU. So CPU load average is the average number of processes being or waiting executed over past 1, 5 and 15 minutes. So the number shown above means:

* load average over the last 1 minute is 3.84

* load average over the last 5 minute is 3.72

* load average over the last 15 minute is 2.41

High load average sometimes implies CPU is overloaded with too many processes. However, this can be a different case depending on how many CPU cores are installed. One single CPU core can only handle one task at a time. The more cores system has, the more tasks system can handle in parallel. Below is an example to understand the relationship between load average and CPU cores:

On single core system this would mean:grep -o -i page test.txt | wc -l

* The CPU was fully (100%) utilized on average; 1 process was running on the CPU (1.00) over the last 1 minute.

* The CPU was idle by 60% on average; no processes were waiting for CPU time (0.40) over the last 5 minutes.

* The CPU was overloaded by 235% on average; 2.35 processes were waiting for CPU time (3.35) over the last 15 minutes.

On a dual-core system this would mean:

* The one CPU was 100% idle on average, one CPU was being used; no processes were waiting for CPU time(1.00) over the last 1 minute.

* The CPUs were idle by 160% on average; no processes were waiting for CPU time. (0.40) over the last 5 minutes.

* The CPUs were overloaded by 135% on average; 1.35 processes were waiting for CPU time. (3.35) over the last 15 minutes.
</b></details>


<details>
<summary> Command to calculate the size of a folder?.</code></summary><br><b>

` du –sh folder1 `
</b></details>

<details>
<summary> How can you append one file to another in Linux?.</code></summary><br><b>

To append one file to another in Linux.

` cat file2 >> file 1 ` : operator ` >> ` appends the output of the named file or creates the file if it is not created.

` cat file 1 file 2 > file 3 ` : appends two or more files to one.
</b></details>


<details>
<summary> How you can find a file using Terminal?.</code></summary><br><b>

` find . –name “process.txt” ` :  It will look for the current directory for a file called process.txt.

` find / -type d -name techno ` : all dir whose name is techno in / directory.

` find / -type f -name index.html`:all files whose name is index.html.

` find  . -type f -name “*.php” ` : all php files in a dir.

</b></details>

<details>
<summary> How you can count no. of lines, words & characters?.</code></summary><br><b>

` wc -l Linux.md ` :  to count no. of lines in a file.

` wc -w Linux.md ` : to count no. of words in file.

` wc -c Linux.md ` : to count no. of characters.

` grep -o -i page test.txt | wc -l` : To Print the no. of times a word occured in a file.

</b></details>


<details>
<summary> How do you change the priority of a running process ?.</code></summary><br><b>

You can change the process priority using nice and renice utility.

* Nice command will launch a process with an user defined scheduling priority. Instead of launching the program with the default priority, you can use nice command to launch the process with a specific priority.

`nice -10 perl test.pl `: test.pl is launched with a nice value of 10.

Launch a Program with High Priority

* Negative nice value will increase the priority a the process. So, the value has to be specified with a — (two hyphens) in front of the nice command  `nice --10 perl test.pl` 

Change the Priority with option -n

` nice -n -5 perl test.pl `: Increase the priority.
` nice -n 5 perl test.pl ` : Decrease the priority.

* Renice command will modify the scheduling priority of a running process.

` renice -n -19 -p 3534 ` : We can change the nice value of the above program to -19 as shown below. Pass the process id of the above program to -p option.

Verify that the nice value got changed to -19.

` ps -fl -C "perl test.pl" `

[Reference URL](https://www.thegeekstuff.com/2013/08/nice-renice-command-examples/)
</b></details>

<details>
<summary> To know which directory you are in.</code></summary><br><b>

`pwd`: print working directory.
</b></details>

<details>
<summary> TO shows the manual pages of the command.</code></summary><br><b>

`man pwd`
</b></details>

<details>
<summary>To clear terminal &  have a clean window to work.</code></summary><br><b>

`clear / ctrl+l`
</b></details>

<details>
<summary>To display a line of text/string on standard output or a file.</code></summary><br><b>

`echo testing`
</b></details>

<details>
<summary>To displays the username of the current user.</code></summary><br><b>

`whoami`
</b></details>

<details>
<summary>To displays the hostname.</code></summary><br><b>

`hostname`

`hostnamectl set-hostname` : to change hostname.
</b></details>

<details>
<summary>To Check how long the system has been running + load.</code></summary><br><b>

`uptime`
</b></details>

<details>
<summary>To Check date & time.</code></summary><br><b>

`date`
</b></details>


<details>
<summary>To see current month's calendar.</code></summary><br><b>

`cal`
</b></details>

<details>
<summary>To Display the user and group ids of your current user.</code></summary><br><b>

`id`
</b></details>

<details>
<summary>To Display last user who have logged onto the system.</code></summary><br><b>

`last`
</b></details>

<details>
<summary> To Create  file .</code></summary><br><b>

`touch filename1 filename2 filename3`
</b></details>

<details>
<summary> To Create  file, display & modify the contents of a file.</code></summary><br><b>

`cat > filename` : to create a file.

`cat filename`   : to display the content of the file.

`cat >> <filename>` : to append data in already existing file.

</b></details>

<details>
<summary> To list file & directory.</code></summary><br><b>

`ls` : To list the file and directories.   

`ls -al`: To view hidden file starting with ‘.‘.  

`ls -r` : To List Files in Reverse Order. 

`ls -R` : Recursively list Sub-Directories.

` lsof ` : to list all open file.

</b></details>

<details>
<summary> To Copy files into directory.</code></summary><br><b>

`cp image.jpg Downloads` 

`cp –rvfp ./Technology /home/Technology` : Copying directories from one location to other.
</b></details>

<details>
<summary> To move files from one location to other(cut and Paste).</code></summary><br><b>

`mv file2 Technology` 

`mv ./Technology /home/Technology` : Moving a Directory from one location to other.

`mv sample.txt kernelfile` : Renaming a File.

` mv ktdir kerneldir ` : Renaming a Directory.
</b></details>

<details>
<summary> To delete a directory.</code></summary><br><b>

`rmdir testdirectory` : to delete an empty directory.

`rm -rf deletedirectory` : to delete files and directory ((where r stands for recursive and f stands for forcefully ).
</b></details>

<details>
<summary> To change the directory.</code></summary><br><b>

`cd $HOME`
</b></details>

<details>
<summary> To show all the commands that you have used in the past for the current terminal session.</code></summary><br><b>

`history`
</b></details>

<details>
<summary> To search for pattern in file.</code></summary><br><b>

`grep hello sample`
</b></details>


<details>
<summary> To verify that a computer can communicate over the network with another computer or network device.</code></summary><br><b>

`ping google.com`
</b></details>

<details>
<summary> To display the amount of disk space available on the file system containing each file name argument.</code></summary><br><b>

`df -TH`  &  `df -h`
</b></details>

<details>
<summary> To track the files and directories which are consuming excessive amount of space on hard disk drive.</code></summary><br><b>

`du -h`
</b></details>

<details>
<summary> To kill a process with processID.</code></summary><br><b>

`kill pid`
</b></details>

<details>
<summary> To display process.</code></summary><br><b>

`ps ` : to display your currently running processes.

`ps -ef ` : to show all the currently running processes on the system.

`ps -ef | grep processname` : to get process information for processname
</b></details>


<details>
<summary> To create a group.</code></summary><br><b>

`groupadd test `
</b></details>

<details>
<summary> To create a user.</code></summary><br><b>

`useradd -c "Admin" -m dhiru ` : Create an account named dhiru, with a comment of "Admin" and create the user's home directory.
</b></details>

<details>
<summary> To delete a user.</code></summary><br><b>

`userdel dhiru `
</b></details>


<details>
<summary> To add a user to group.</code></summary><br><b>

`usermod -aG devops dhiru`
</b></details>

<details>
<summary> To downloads files served with HTTP/HTTPS/FTP over a network.</code></summary><br><b>

`wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key`
</b></details>

<details>
<summary> To display current network configuration information, setting up an ip address, netmask or broadcast address to an network interface, creating an alias for network interface, setting up hardware address and enable or disable network interfaces.</code></summary><br><b>

`ifconfig`
</b></details>

<details>
<summary> To Create  file, display & modify the contents of a file.</code></summary><br><b>

`$ mkdir mydir `

* Making multiple directories inside a directory  
`$ mkdir -p Technology/{Devops/{docker,ansible,kubernetes},Cloud/{AWS,Azure,GCP}}   

* Check it by using tree command or ls –R command   
$ `tree Technology/`
```
Technology/
├── Cloud
│   ├── AWS
│   ├── Azure
│   └── GCP
└── Devops
    ├── ansible
    ├── docker
    └── kubernetes

8 directories, 0 files
```

</b></details>


<details>
<summary> Filter Commands.</code></summary><br><b>

Filter commands are used to filter the output so that the required things can easily be picked up. The commands which are used to filter the output are 

* `less` : to see the output line wise or page wise. 
    Ex: $ `less /etc/passwd`
    Note: -press Enter key to scroll down line by line (or)  
    Use d to go to next page  
    Use b to go to previous page  
    Use / to search for a word in the file 
    Use v to go vi mode where you can edit the file and once you save it you will back to less command.

* `more` : exactly same like less.
            
   Ex: $ `more /etc/passwd` 
   Note: -press Enter key to scroll down line by line (or)  
   Use d to go to next page  
   Use / to search for a word in the file 
   Use v to go vi mode where you can edit the file and once you save it you will back to more command 

* `head` : to display the top 10 lines of the file.

  Ex: $ `head /etc/passwd` 

* To display the custom lines #head -n /etc/passwd (where n can be any number).  
  Ex: $ `head -3 /etc/passwd` 

* `tail` : to display the last 10 lines of the file.
   Ex: $ `tail /etc/passwd` 

* To display the custom lines   
Ex: $ `tail -3 /etc/passwd`    


* `sort` : to sort the output in numeric or alphabetic order.

* sort by alphabetic order   
   $ `sort sample.txt`
```
    Hello world
    Hello world
    Linux basic commands
    scripts
    testing
    welcome to CLI
```
* To sort the file according to numbers 
Ex: $ `sort –d sample.txt`
```
    1. Linux basic commands
    2. scripts
    3. Hello world
    4. welcome to CLI
    5. Hello world
    6. testing
``` 

* To remove the duplicate entries from the output.  
Ex: $ `sort –u sample.txt`
```
    Hello world
    Linux basic commands
    scripts
    testing
    welcome to CLI
``` 
* `cut` : to pick the given expression (in columns) and display the output.

$ `cut  -d  -f   filename` (where d stands for delimiter ex. : , “  “ etc and f stands for field)  

To delimit colon(:) and print the field 
Ex: $ `cut -d: -f1  /etc/passwd`

To delimit spaces and print the field  
Ex: $ `cut –d “ “ –f1 sample.txt`  
```
    welcome
    Linux
    Hello
    testing
    scripts
    Hello
``` 

* `sed` : to search a word in the file and replace it with the word required to be in the output. sed stands for stream editor.

$ `sed  ‘s/searchfor/replacewith/g’  filename`   
Note: it will only modify the output, but there will be no change in the original file.

Ex: $ `sed 's/Hello/hai/g' sample.txt`

```
    welcome to CLI
    Linux basic commands
    hai world
    testing
    scripts
    hai world
```
</b></details>


[Reference](https://krishnaprasadkv.github.io/Linux-Commands/)