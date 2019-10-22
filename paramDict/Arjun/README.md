
<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Arjun"><img src="https://image.ibb.co/c618nq/arjun.png" alt="Arjun"></a>
  <br>
  Arjun
  <br>
</h1>

<h4 align="center">HTTP Parameter Discovery Suite</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Arjun/releases">
    <img src="https://img.shields.io/github/release/s0md3v/Arjun.svg">
  </a>
  <a href="https://github.com/s0md3v/Arjun/issues?q=is%3Aissue+is%3Aclosed">
      <img src="https://img.shields.io/github/issues-closed-raw/s0md3v/Arjun.svg">
  </a>
  <img src="https://img.shields.io/badge/god%20level-shit-green.svg">
</p>

![demo](https://i.ibb.co/0V6ymPy/Screenshot-2019-04-12-18-17-49.png)

### Introduction
Web applications use parameters (or queries) to accept user input, take the following example into consideration

`http://api.example.com/v1/userinfo?id=751634589`

This URL seems to load user information for a specific user id, but what if there exists a parameter named `admin` which when set to `True` makes the endpoint provide more information about the user?\
This is what Arjun does, it finds valid HTTP parameters with a huge default dictionary of 25,980 parameter names.

The best part? It takes less than 30 seconds to go through this huge list while making just 30-35 requests to the target.\
Want to know how Arjun does that? [Here's how](https://github.com/s0md3v/Arjun/wiki/How-Arjun-works%3F).

### Features
- Multi-threading
- Thorough detection
- `GET/POST/JSON` methods supported
- A typical scan takes 30 seconds
- Regex powered heuristic scanning
- Huge list of 25,980 parameter names
- Makes just 30-35 requests to the target

> **Note:** Arjun doesn't work with python < 3.4

#### How to use Arjun?

A detailed usage guide is available on [Usage](https://github.com/s0md3v/Arjun/wiki/Usage) section of the Wiki.\
An index of options is given below:

- [Scanning a single URL](https://github.com/s0md3v/Arjun/wiki/Usage#scanning-a-single-url)
- [Scanning multiple URLs](https://github.com/s0md3v/Arjun/wiki/Usage#scanning-multiple-urls)
- [Choosing number of threads](https://github.com/s0md3v/Arjun/wiki/Usage#multi-threading)
- [Delay between requests](https://github.com/s0md3v/Arjun/wiki/Usage#delay-between-requests)
- [Including presistent data](https://github.com/s0md3v/Arjun/wiki/Usage#including-persistent-data)
- [Saving output to a file](https://github.com/s0md3v/Arjun/wiki/Usage#saving-output-to-a-file)
- [Adding custom HTTP headers](https://github.com/s0md3v/Arjun/wiki/Usage#adding-http-headers)

##### Credits
The parameter names are taken from [@SecLists](https://github.com/danielmiessler/SecLists).
