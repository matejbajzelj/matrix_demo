

Matrix Demo - Word Game
### Tasks to do

- [x] Server, Client App
- [x] TCP & Unix socket
- [x] Custom Binary protocol (7bit header - 1b message type, 2b message length, 4b auth token size) + data
- [x] Client A requests a list of possible opponents: command `get users`
- [x] Server responds with a list of possible opponents (IDs)
- [x] Client A requests a match with opponent (ID), specifying a word to guess: command `start match with {id} {word to guess]`
- [x] Server either confirms this or rejects with an error code. NOTE: I made client to either accept or declined.
- [x] The target client - client B - is informed of the match, and can begin guesses
- [x] Client A is informed of the progress of Client B (attempts)
- [x] Client A can write an arbitrary text (a hint) that is sent to and displayed by Client B. Command `hint: {growing in the forest.]`
- [x] Match ends when Client B guesses the word, or gives up. command `give up` during active match
- [x] Command "get matches" - to display text based list of matches
- [x] Command "help" - to display command and usage
- [x] Command "show my id" - to display to client his id, so he could exclude him self from match list and do a match with other IDs
- [x] Website to show matches (used flask lib)
- [x] Live update with socketIO (used flask-socketio)

### Install
- Clone / download zip for repository
- `sudo apt install python3-pip` - if pip is not installed
- `pip install -r requirements.txt` - to install libraries (they are needed for website part of the task, which was build with Flask, Flask-socketIO

### Run the app TCP)
- python3 server.py {tcpMode = true / false} {tcp port / unix socket patch} {tcp host}
  
* #### TCP mode:
    - `python3 server.py` (with default params, which is predefined TCP_mode = true, port and host)
    - `python3 client.py` (with default params, which is predefined TCP_mode = true, port and host)

* #### UNIX Socket mode:
    - `python3 server.py false`
    - `python3 client.py false`
  

#### How I tested it
- Since I don't have access to real ubuntu, I made virtual machine to install ubuntu 22.04 LTS Desktop.

  <img width="1879" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/fc186508-7635-42df-9ca3-46c5a610b83a">

## TEST TASK:

Using a language of choice from the following:

- Rust
- Typescript
- Python
- C/C++

Without using external libraries (unless neccessary), write two applications. These applications will be a client and a server app.
They will communicate over a TCP socket and the exact "protocol" on top of that is up to you. 
Note: using just utf8 strings will have a negative impact on the judgement (hint - custom binary protocol is expected).

Upon connection - the server must send a message to the client - initiating the communication.
Client upon receiving it - answers to the server with a password.
This initial exchange then ends with server either disconnecting the client (wrong password) or assigning the client an ID and sending the ID back to the client.

At this moment, the server answers to any requests the client sends to the server. For unknown requests, the server must respond as well, such that client can identify it as an error.

The main function of the server at this moment - is to facilitate game of "Guess a word" between two clients.
The game flow is as follows:

1. Client A requests a list of possible opponents (IDs) - command "get users"
2. Server responds with a list of possible opponents (IDs)
<img width="410" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/5582df4f-20d8-4d58-a53d-e12f7edd6fa5">

3. Client A requests a match with opponent (ID), specifying a word to guess - command "starting match with {id} {word}"
<img width="222" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/cac7fa73-0762-4409-93a9-7e83517252f8">
   
4. Server either confirms this or rejects with an error code. I made that clientB gets invitation, so he can declined or accept.
  <img width="462" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/b46e9019-b43a-43ef-969e-2764f150c545">

5. The target client - client B - is informed of the match, and can begin guesses
<img width="417" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/16962d26-4399-411c-b7c8-58bb72ff89f6">

6. Client A is informed of the progress of Client B (attempts)
<img width="406" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/30b85e0c-c94d-45ac-97cc-e00eb65a2abd">

7. Client A can write an arbitrary text (a hint) that is sent to and displayed by Client B
<img width="1347" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/3aa27630-4122-4995-a7f2-72bbbbf14048">

8. Match ends when Client B guesses the word, or gives up
<img width="1347" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/ec192ffa-e15b-4255-937e-c19b12ab2a1b">

9. Command "get matches"
<img width="547" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/ff7541ed-a88f-4fa0-a427-48f92e5e6dd9">

10. Client B receiving invitation
<img width="592" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/382bfc62-5677-4cfb-8739-fc7fa2b9c411">

11. Client can list help with command `help`
<img width="586" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/9f50f51d-0540-445b-aa49-eb2d20225d04">


| Server specifics:
Implemented. You can specify TCP (with host, port) or Unix (path) or leave empty with default. 

<img width="424" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/812fa508-e23d-4a2d-a6c1-86333073540d">

<img width="396" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/b98eebf3-d4a4-44f0-b95f-63e6ede94915">

Optional/bonus: offer a website that displays the progress of all the matches, for a third party to observe.

| Client specifics:
Must be able to connect to either Unix socket or a TCP port.
Implemented. You can specify TCP (with host, port) or Unix (path) or leave empty with default. 

Example of terminas, website.
<img width="3565" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/6b794c9d-4050-4867-b653-0ca63f9cbecd">


RUNTIME:

Both the client and the server must run on Linux, specifically Ubuntu 22.04, without any containers or virtualization. It will be tested on x86 64bit architecture system.

JUDGEMENT:

The following things play role for passing to the interview stage:

- Understanding of both the technologies used and the language chosen.
- Complexity of the chosen solution.
- Efficiency of the custom communication protocol.
- Instructions to run the test task provided -> we will evaluate it on freshly installed Ubuntu 22.04.
--------------------------------------

1. Message format

Header (7 bytes):
- message type = 1 bytes
- data length  = 2 bytes - integer 0-65536 
- auth token   = 4 bytes - picked large number to avoid duplicates or manully create one by "attacker"

Data:
- payload: custom X bytes 
