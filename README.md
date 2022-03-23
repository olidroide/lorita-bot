<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/olidroide/lorita-bot">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Lorita Bot</h3>

  <p align="center">
    Lorita helps you to transcript audio messages of your chat app.
    <br />
    <a href="https://github.com/olidroide/lorita-bot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/olidroide/lorita-bot">View Demo</a>
    ·
    <a href="https://github.com/olidroide/lorita-bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/olidroide/lorita-bot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

How many times you're in a meeting and receives and Audio Message? you can't take your phone and listen it, needs to finish the meeting and then listen.

Lorita-Bot transcribe that Audio Message to text, and you cand read it without listen it.

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [FastAPI](https://fastapi.tiangolo.com/)
* [Python](https://www.python.org/)
* [Docker](https://www.docker.com/)
* [PyCharm](https://www.jetbrains.com/pycharm/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally or in a Server.

### Prerequisites
Depends of how do you want deploy it:
- Local (with Python):
	- Install `Python 3.9`, `pip` and `virtualenv` on your OS.

- Docker:
	- Install `Docker` on your OS (also I recommend install `docker-compose`)

### Installation

- Get a free API Key at [deepgram.com](https://deepgram.com)
- Get a free API Key at [twilio.com](https://twilio.com)
- Clone the repo
   ```sh
   git clone https://github.com/olidroide/lorita-bot.git
   ```
	 

	 
- Create environment file `.env`
   ```js
	 LORITA_BOT_DEBUG=True
	 LORITA_BOT_BASEURL=/
	 LORITA_BOT_LOG_LEVEL=DEBUG
	 LORITA_BOT_TWILIO_ACCOUNT_SID=[Twilio Account SID]
	 LORITA_BOT_TWILIO_AUTH_TOKEN=[Twilio Auth Token]
	 LORITA_BOT_DG_KEY=[Deepgram API KEY]
   ```
	 
- Deploy with Python 🐍
	- Make virtualenv
 		```sh
 		virtualenv venv --python=python3
		```
 	
	- Install dependencies
		```sh
   	pip install -r requirements.txt
   	```
	
	- Launch server
   	```sh
   	python src/main.py 
   	```
	 
- Deploy with Docker 📦
	- Build docker image with docker-compose
   ```sh
   docker-compose up -d --build 
   ```
	 - Or use pre build image from 
	 ```
	 docker pull ghcr.io/olidroide/lorita-bot:main
	 ```
	 
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Dockerized image
- [ ] Multilanguage detection
- [ ] More Chat app integrations
    - [ ] Telegram

See the [open issues](https://github.com/olidroide/lorita-bot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

olidroide - [@olidroide](https://twitter.com/olidroide) - lorita@olidroide.es

Project Link: [https://github.com/olidroide/lorita-bot](https://github.com/olidroide/lorita-bot)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/olidroide/lorita-bot.svg?style=for-the-badge
[contributors-url]: https://github.com/olidroide/lorita-bot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/olidroide/lorita-bot.svg?style=for-the-badge
[forks-url]: https://github.com/olidroide/lorita-bot/network/members
[stars-shield]: https://img.shields.io/github/stars/olidroide/lorita-bot.svg?style=for-the-badge
[stars-url]: https://github.com/olidroide/lorita-bot/stargazers
[issues-shield]: https://img.shields.io/github/issues/olidroide/lorita-bot.svg?style=for-the-badge
[issues-url]: https://github.com/olidroide/lorita-bot/issues
[license-shield]: https://img.shields.io/github/license/olidroide/lorita-bot.svg?style=for-the-badge
[license-url]: https://github.com/olidroide/lorita-bot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/olidroide
[product-screenshot]: images/screenshot.png
