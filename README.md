# PyNexus

This repository contains the Python codes that represent a HTTP communication between a client and a server.

## Usage

This project has no requirements besides Python native libraries.

### Start the Client

```
python3 http_client.py <port> <webhost>
```

### Start the Server

```
python3 http_server.py <port> <ip>
```

## Disclaimer

This project is still under development and its requirements may change in the future. Feel free to report any issues or open an pull request with desired enhancements.

This branch is made to accomodate testing when connected to an IPv4 only network. This does not comply with most recent networking best practices nor with 'Happy Eyeballs' principles.