

Well it's that easy!
---

PROLOG:

The people we are looking for should always strive to understand why things work, why things happen.
They must posses (or strive to acquire) essential knowledge about the technologies they work with.
When that's the case - its visible in the work they do.

TEST TASK:

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
<img width="372" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/5ae01bcb-e74a-4000-ad1c-abeeb2c0f373">

3. Server responds with a list of possible opponents (IDs)
<img width="372" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/abe80236-a09a-44cb-af9e-327fd80e833c">

5. Client A requests a match with opponent (ID), specifying a word to guess - command "starting match with {id} {word}"
<img width="700" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/595eb46e-822e-4e61-9ebd-1ed9a8caa3d5">
   
6. Server either confirms this or rejects with an error code
  
8. The target client - client B - is informed of the match, and can begin guesses
<img width="441" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/df35d6c2-fe23-46a8-bf82-fead35794a98">

<img width="441" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/51128088-0328-4b62-a1bb-f29344c698d7">

6. Client A is informed of the progress of Client B (attempts)
<img width="1016" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/e9a9a1de-6526-42e5-bfc3-69753c434b43">


8. Client A can write an arbitrary text (a hint) that is sent to and displayed by Client B
9. Match ends when Client B guesses the word, or gives up
<img width="1598" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/ef1fce70-4ba7-4524-aab8-2f4837a49cd6">

11. Command "get matches"


- Client B receiving invitation
<img width="592" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/382bfc62-5677-4cfb-8739-fc7fa2b9c411">


- GET MATCHES:
<img width="547" alt="image" src="https://github.com/matejbajzelj/matrix_demo/assets/10921665/ff7541ed-a88f-4fa0-a427-48f92e5e6dd9">

| Server specifics:
Must offer both Unix socket and a TCP port for client connection.

Optional/bonus: offer a website that displays the progress of all the matches, for a third party to observe.

| Client specifics:
Must be able to connect to either Unix socket or a TCP port.

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

Header:
- type of a message 2 bytes (after I have changed how small numbers are, this can be changed back to 1 byte)
- data length 2 bytes - integer 0-65536 
- auth token 4 bytes - picked large number to avoid duplicates or manully create one by "attacker"
Data:
- payload: custom X bytes 
