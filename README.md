Python-Shared-Hosting-Scanner
=============================

Uses Bing search engine to identify (and validate) websites hosted on the same web server.

Messy code but works. For each found domain, it will verify its IP address to eliminate false positives. This is why this script is too damn slow. If you need quicker but less accurate results, find and comment the following line and remove a tab from the next two lines.

```
if resolve(sharedHost) == resolve(domain):
```

Syntax
=============================

This script is OS agnostic. Takes one param, HOSTNAME or IP of the target. For example...

```
python neighbs.py www.green-apple.gr
```
or
```
python neighbs.py 176.9.145.29
```

For any libs that are missing, use pip to install.

Example output
=============================

```
C:\tools\Projects\PYTHON>python neighbs.py www.green-apple.gr

[*] Scanning for shared hosts. Please wait...
------------------------------------------------
[+] www.restozorba.be
[+] www.hotelmelissa.gr
[+] www.epiplotexan.gr
[+] www.n-everalone.com
[+] www.proedriki-froura.gr
[+] www.zpalace.gr
[+] www.green-apple.gr
[+] www.ktelxanthis.gr
[+] www.foititisweb.gr
[+] www.hotelnessos.gr
[+] www.tosteki.gr
[+] www.gashome.gr
[+] www.raptopoulos-stores.gr
[+] www.ksxanthi.gr
[+] www.olang.gr
[+] www.promoaction.gr
[+] www.kokkalas.co.gr
[+] www.inside.com.gr
[+] www.makka.gr
[+] www.christospoulios.gr
[+] www.outsis.gr
[+] www.velkopoulosgas.gr
[+] www.carnivalxanthi.gr
[+] www.serrespress.gr
[+] www.mpatsakis.gr
[+] www.moumtzaki.gr
[+] www.kopsidas.com.gr
[+] pse.co.gr
[+] www.krista.gr
[+] www.findgas.gr
[+] www.ippokratiskamaridis.gr
[+] www.vion.gr
------------------------------------------------
[*] 32 unique domains found and verified to be on the same server.

C:\tools\Projects\PYTHON>
```

Penetrating in to target machines by using shared hosts' vulnerabilities is not always legal even if you have a signed contract with the target. Make sure the shared hosts you're attacking belong to the same person/company before doing anything stupid.
