# PLT Connectivity and PLTcloud Status

What a PLT needs from the network to reach PLTcloud, and where to check PLTcloud service status.

## PLT Connectivity

Source: `pltcloud/plt-connectivity/`

PLTs rely on secured connectivity with the PLTcloud cloud backend, used for:

- Receiving firmware, test plans from PLTcloud
- Executing webhooks during tests execution
- Sending test reports to PLTcloud

All communication between the PLT and AWS endpoints is encrypted with TLS, with authentication based on a private key securely managed by a hardware-based cryptographic element that prevents key extraction.

**References**

- Introducing mutual TLS authentication for Amazon API Gateway | AWS Compute Blog (https://aws.amazon.com/blogs/compute/introducing-mutual-tls-authentication-for-amazon-api-gateway/)

**Network Requirements**

The Ethernet port of the PLT should be connected to a network with (outbound) Internet access.

**DHCP**

The PLT automatically obtains its IP address, subnet mask, default gateway, and optionally DNS and NTP server addresses via DHCP from the connected Ethernet network.

To assign a static IP address, configure the local DHCP server to reserve an IP for the PLT’s MAC address. The MAC address of the PLT can be found under under Menu → About this PLT.

Manual configuration of IP network settings (e.g., via the front-panel UI) is not supported.

> **NOTE:** If MAC or IP spoofing is a concern, deploy PLTs on a dedicated LAN or VLAN with no user-accessible devices. Consider using switch-level security features such as port security or MAC address filtering to ensure only authorized devices can communicate on the network.

**DNS**

The DNS server specified by the DHCP server should be able to resolve:

- *.pltcloud.com
- *.amazonaws.com
- *.ntp.org

| Service | Protocol | Ports |
|---|---|---|
| DNS | UDP, TCP (used for larger responses) | 53 |

**Firewall Settings**

TCP (outbound) and UDP traffic should be allowed to these AWS API endpoints:

| Service | Endpoint | Ports |
|---|---|---|
| PLTcloud | *.pltcloud.com | 443 |
| AWS IoT | a347l7e88enrtv-ats.iot.us-west-2.amazonaws.com | 80, 443, 8883 |
| AWS S3 | s3.us-west-2.amazonaws.com | 80, 443 |
| AWS S3 | plt-asset-production.s3.us-west-2.amazonaws.com | 80, 443 |

> **NOTE:** Ports 80 and 8883 are not actively used, but may be accessed in error handling of failed AWS IoT or S3 interactions.

**NTP**

UDP NTP traffic (port 123) should be allowed for these NTP Time servers:

| Service | Protocol | NTP Time server | Port |
|---|---|---|---|
| NTP | UDP | 0.pool.ntp.org | 123 |
| NTP | UDP | 1.pool.ntp.org | 123 |
| NTP | UDP | 2.pool.ntp.org | 123 |
| NTP | UDP | 3.pool.ntp.org | 123 |
| NTP | UDP | 0.cn.pool.ntp.org | 123 |
| NTP | UDP | 1.cn.pool.ntp.org | 123 |
| NTP | UDP | 2.cn.pool.ntp.org | 123 |
| NTP | UDP | 3.cn.pool.ntp.org | 123 |

**DHCP NTP Config**

In enterprise environments with restricted outbound access, access to the default NTP servers may be blocked by perimeter firewalls or proxies.

Use DHCP option 42 to deliver internal NTP server IPs to PLT devices. This is supported by all major DHCP servers (Cisco IOS DHCP, Windows Server, ISC DHCP, dnsmasq, etc.).

**References**

- RFC 2132 - DHCP Options and BOOTP Vendor Extensions (https://datatracker.ietf.org/doc/html/rfc2132)

Not bundled; see Cisco IOS DHCP Server (`pltcloud/plt-connectivity/#cisco-ios-dhcp-server`), Windows Server DHCP (`pltcloud/plt-connectivity/#windows-server-dhcp`), ISC DHCP (Linux) (`pltcloud/plt-connectivity/#isc-dhcp-linux`), dnsmasq (`pltcloud/plt-connectivity/#dnsmasq`).

**Optional: Deploy a Local NTP Relay**

If a dedicated NTP server is not available, consider deploying one internally (e.g., chronyd or ntpd on Linux) and sync it to a trusted corporate time source or GPS device.

**Security**

The PLT runs pltOS, a hardened Linux distribution that minimizes the system’s attack surface and reduces potential vectors for exploitation.

To protect both test asset deployment and secure reporting, the PLT includes a Secure Element (aka “crypto chip”) responsible for critical cryptographic operations. This hardware component implements the following security standards:

- FIPS 186-3 ECDSA
- FIPS SP800-56A ECDH
- NIST Standard P256 Elliptic Curve

**Secure Report Encryption and Transmission**

Before being stored or transmitted, each report is cryptographically signed and encrypted:

- The compressed report is hashed with SHA-256 and signed using the PLT’s Secure Element, ensuring authenticity and integrity.
- A random AES-GCM key and IV are generated to encrypt the report. The AES key is then encrypted using a public key from a validated trust bundle specific to the organization.
- Encrypted reports and their metadata are transmitted to PLTcloud over mutually authenticated TLS 1.2. If primary credentials are unavailable, the system can fall back to device-based credentials for reliable delivery.

## PLTcloud Status

Source: `pltcloud/status/`

PLTcloud system status is available here:

- https://status.pltcloud.com/

Identity management for PLTcloud is provided by Auth0. Auth0 service status can be monitored at:

- https://status.auth0.com/
