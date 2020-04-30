## Communication networks project for file storage server and survey on Vehicular Social Networks.



### Task:

Project 1: A survey on Vehicular Social Networks
- [x] Introduction: Existing methodologies - VANET, Pocket Switched Networks, Social Aware Networking and it's importance with examples.
- [x] Next Generation Vehicles- Technology and features, future scope and vision. 
- [x] Vehicular Social Networks - For mobility and social networking
- [x] State of the art safety and entertainment applications based on crowdsourcing.


Project 2: File server
- [x] Connection between client and server.
- [x] Authentication
- [x] View files of designated folder.
- [x] FileHashing
- [x] IndexGet flag shortlist ad longlist
- [x] FileDownload
- [x] Caching
- [x] Bonus

### Overview
A P2P file sharing protocol, with functionalities like download and upload for files and indexed searching. The client has the ability know the files present on the designated shared server folder. File transfer incorporates MD5 checksum.


### Implemented functions:
1. IndexGet flag(args)
  - This allows the client to request the display of shared files on the server.
  - The history of requests is maintained on the client side.
  - flag shortlist
    - This flag allows for the client to query the names of files betweem a specific set of time stamps

    - Outputs the name, size, timestamp, and type of files between the start and end time stamps

    - Apart from this, the client can query only .txt files and .pdf files between specified stamps in the query

    - Usage **(Note the backward slash between date and time)**:

      ```
      IndexGet shortlist 2012-12-17\ 22:06:52 2020-12-19\ 22:06:52
      ```
  - flag longlist
    - This flag allows for the client to view the entire listing of the shared folder present on the server, including the name, size, timestamp, and type of file present.

    - The output is the complete listing.

    - Usage **(Note the backward slash between date and time)**:

      ```
      IndexGet longlist
      ```

      
  - **Bonus**
         - longlist flag that displays file containing user defined string.

       - Usage **(Note the backward slash between date and time)**:

         ```
         IndexGet longlist *.txt <string>
         ```

         - For example if you wish to display text files containing string 'the' the command is: IndexGet longlist *.txt the
         - shortlist flag displaying txt/pdf files between two time stamps

       - Usage **(Note the backward slash between date and time)**:

           ```
           IndexGet shortlist 2012-12-17\ 22:06:52 2020-12-19\ 22:06:52 *.txt
           IndexGet shortlist 2012-12-17\ 22:06:52 2020-12-19\ 22:06:52 *.pdf
           ```

  - Screenshot

    ![Alt text](./src/screenshots/indexget.png?raw=true "Command output")

2. FileHash flag(args)
  - This command allows the client to check if any files on the shared server have been changed. 

  - flag verify
    - This flag allows for the client to check if a particular filename is present
    - If present, the file's checksum and last modified timestamp is returned
    - Usage **(Note the backward slash for file names with spaces)**:

    ```
    FileHash verify test\ (copy).txt
    ```

  - If "test (copy).txt" exists on server, its checksum and last modified timestamp is returned

  - flag checkall

    - This flag allows the client to check if all the status of all files present on the server
    - Returns the filename, checksum, and last modified timestamp of all files present in the shared server folder.
    - Usage:

    ```
    FileHash checkall 
    ```

  - Screenshot

![Alt text](./src/screenshots/fileHash.png?raw=true "Command output")

3. FileDownload flag(args)
  - This command allows the client to download files from the shared server folder.

  - A progress bar is printed showing the status of the download.

  - Outputs the filename, filesize, last modified timestamp and MD5hash of the file requested for download.

       

  - flag tcp/TCP

	- Allows the client to download files to its file storage using the TCP protocol.

  	- A TCP socket is created for this purpose.

  	- Usage **(Note the backward slash for file names with spaces)**:
               
       ```
       FileDownload tcp 000000.png
       FileDownload tcp Lec10.pdf
       FileDownload tcp test\ (copy).txt
       ```
  - flag udp/UDP

	  - Allows the client to download files to its file storage using the UDP protocol.

	  - A UDP datagram socket is created for this purpose.

	  - Usage **(Note the backward slash for file names with spaces)**:
      ```
      FileDownload udp 000000.png	
      FileDownload udp Lec10.pdf
      FileDownload udp test\ (copy).txt
      ```  
	 - Screenshot

	   ![Alt text](./src/screenshots/CN_ss_download.png?raw=true "Command output")

4. Caching flag(args)
  - This command checks if the the requested file is already cached. If true, returns file from the cache without contacting the server.
    - flag show
    	Checks and prints all elements of the cache and their sizes
    	
    - Usage:

      ```
      Cache show
      ```

    - flag verify
	- Checks if file is present in cache. If file is present, the Md5 hash of the file in the cache and the server are verified. If they are the same, no download is done.
	- If file is not present in the cache, the file is downloaded from the shared server using the TCP protocol.
	- Usage **(Note the backward slash for file names with spaces)**:

      ```
      Cache verify 000000.png
      Cache verify test\ (copy).txt
      ```
  - Screenshot

    ![Alt text](./src/screenshots/cache.png?raw=true "Command output")

5. Authentication
	- Method for authenticating a user using a password has been implemented
	- If the password is correct, the prompt for using the aforementioned functions is shown.
	- Password is stored in config file. 

**Note: For filenames with spaces, use escape sequence '\ '**

**A helper function has been written to replace the spaces with "\\ " for ease of use.**  

Contributors
- Rahul Sajnani
- Ajay Shrihari

