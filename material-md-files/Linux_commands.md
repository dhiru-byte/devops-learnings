### Linux Commands


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