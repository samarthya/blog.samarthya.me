---
title: "Tunnel: SSH"
date: "2023-04-28T12:00:00Z"
slug: "tunnel-ssh"
description: "SSH tunneling is a powerful technique that allows you to securely tunnel network traffic between two endpoints."
categories: ["technical"]
tags: ["ssh", "tunnel"]
aliases: ["/wps/2023/04/28/tunnel-ssh/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

SSH tunneling is a powerful technique that allows you to securely tunnel network traffic between two endpoints. `SSH tunneling` can be used for a variety of purposes, including bypassing network security restrictions, accessing resources on a remote network, and encrypting network traffic.

There are three types of SSH tunneling:

- local port forwarding,
- remote port forwarding, and
- dynamic port forwarding.

Each type of tunneling has its own use case and can be used in different scenarios.

## Local Port Forwarding

Local port forwarding allows you to forward traffic from a local port to a remote host and port. This is useful when you need to access a service on a remote host that is not directly accessible from your local machine.

For example, suppose you want to access a web server that is running on a remote host, but the web server is only accessible from the remote host’s local network. To access the web server, you can create a local port forwarding tunnel that forwards traffic from your local machine’s port `8080` to the remote host’s port `80`:

```text
ssh -L 8080:web-server:80 user@remote-host
```

In this example, `web-server` is the hostname or IP address of the remote server that is running the web server.

After creating the tunnel, you can access the web server by opening a web browser and navigating to `http://localhost:8080`.

## Remote Port Forwarding

Remote port forwarding allows you to forward traffic from a remote port to a local host and port. This is useful when you need to access a service on your local machine from a remote host.

For example, suppose you want to give a friend access to a web server that is running on your local machine. To do this, you can create a remote port forwarding tunnel that forwards traffic from the remote host’s port `8080` to your local machine’s port `80`:

```text
ssh -R 8080:localhost:80 user@remote-host
```

In this example, `localhost` is the hostname or IP address of your local machine.

After creating the tunnel, your friend can access the web server by opening a web browser and navigating to `http://remote-host:8080`.

## Dynamic Port Forwarding

Dynamic port forwarding allows you to create a SOCKS proxy server on your local machine that forwards traffic through an SSH tunnel to a remote server. This is useful when you need to access resources on a remote network that is not directly accessible from your local machine.

For example, suppose you are working from a coffee shop and need to access a company network that is behind a firewall. To access the network, you can create a dynamic port forwarding tunnel that forwards traffic from your local machine’s SOCKS proxy server to the remote server:

```text
ssh -D 1080 user@remote-server
```

After creating the tunnel, you can configure your web browser to use the SOCKS proxy server at `localhost:1080`. Any network traffic sent from your web browser will be forwarded through the SSH tunnel to the remote server.

## Conclusion

In conclusion, SSH tunneling is a powerful technique that can be used to securely tunnel network traffic between two endpoints. Local port forwarding, remote port forwarding, and dynamic port forwarding each have their own use case and can be used in different scenarios.

Local port forwarding is useful when you need to access a service on a remote host that is not directly accessible from your local machine. Remote port forwarding is useful when you need to give someone access to a service on your local machine from a remote host. Dynamic port forwarding is useful when you need to access resources on a remote network that is not directly accessible from your local.

---

Image credit to [goteleport.com](https://goteleport.com/blog/ssh-tunneling-explained/)
