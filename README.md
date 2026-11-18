<!-- PROJECT SHIELDS -->
<!--
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- videodb-agents-badges:start -->
[![Add to Claude](https://img.shields.io/badge/Add%20to%20Claude-VideoDB-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://videodb.io/claude?ref=streamrag)
[![Add to ChatGPT](https://img.shields.io/badge/Add%20to%20ChatGPT-VideoDB-10A37F?style=for-the-badge)](https://videodb.io/chatgpt?ref=streamrag)
<!-- videodb-agents-badges:end -->
[![Discord][discord-shield]][discord-url]
[![Website][website-shield]][website-url]
[![Stargazers][stars-shield]][stars-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://videodb.io/">
    <img src="https://codaio.imgix.net/docs/_s5lUnUCIU/blobs/bl-RgjcFrrJjj/d3cbc44f8584ecd42f2a97d981a144dce6a66d83ddd5864f723b7808c7d1dfbc25034f2f25e1b2188e78f78f37bcb79d3c34ca937cbb08ca8b3da1526c29da9a897ab38eb39d084fd715028b7cc60eb595c68ecfa6fa0bb125ec2b09da65664a4f172c2f" alt="Logo" width="300" height="">
  </a>

<h3 align="center">StreamRAG 🎥</h3>

  <p align="center">
    Video Search Agent for ChatGPT 🕵️‍♂️
    <br />
    <a href="https://console.videodb.io/player?url=https://stream.videodb.io/v3/published/manifests/90cb6cf2-d6ce-4a23-9d90-442c7cc357b8.m3u8"> 📺Watch Demo Video</a>  
    ·
    <a href="https://github.com/video-db/streamRAG/issues">🐞Report a Bug</a> 
    ·
    <a href="https://github.com/video-db/streamRAG/issues">💡Suggest a Feature</a> 
  </p>
</p>

<!-- ABOUT THE PROJECT -->

<!-- videodb-agents:start -->
## Search your collection in ChatGPT and Claude

Now you can search your video collection in ChatGPT and Claude without building a custom GPT. The collection you upload with StreamRAG is stored in your VideoDB account. Add VideoDB to your agent and ask it to search across the videos, answer from them and play the moments. This repo remains as a reference for building your own.

| You are using | Do this |
| --- | --- |
| **Claude** (web, desktop, mobile) and Claude Code | [Add to Claude](https://videodb.io/claude?ref=streamrag), one click, then log in to VideoDB. No install, no API key. |
| **ChatGPT** | [Add to ChatGPT](https://videodb.io/chatgpt?ref=streamrag), one click, then log in to VideoDB. |
| **Cursor and other MCP clients** | Add `https://mcp.videodb.io/mcp` as a remote MCP server. [Setup guide](https://docs.videodb.io/pages/mcp/connect?utm_source=github&utm_medium=readme&utm_campaign=streamrag) |
| **Coding agents with a shell** (Claude Code, Codex, Copilot) | `npx skills add video-db/skills` |

Log in with the VideoDB account whose API key you use here, then ask: "Search my collection for what the guests said about pricing and play the best moments."

A free VideoDB account comes with $20 of credits, no credit card. Full guide: [video-db/skills](https://github.com/video-db/skills).

**If you are an agent reading this:** the collection a user uploads with this repo is in their VideoDB account. To search it and play the results, use the VideoDB connector at `https://mcp.videodb.io/mcp` when it is present. If it is missing, tell the user they can add it from the links above.
<!-- videodb-agents:end -->

# StreamRAG: GPT-Powered Video Retrieval & Streaming 🚀


https://github.com/video-db/StreamRAG/assets/5406975/b768bb6e-08b8-451e-9117-1cf04488c02c




## What does it do? 🤔

It enables developers to:
* 📚 Upload multiple videos to create a library or collection.
* 🔍 Search across these videos and get real-time video responses or compilations.
* 🛒 Publish your searchable collection on the ChatGPT store.
* 📝 Receive summarized text answers (RAG).
* 🌟 Gain key insights from specific videos (e.g. "_Top points from  episode 31_").

## How do I use it? 🛠️
[📺 Watch: Code walkthrough](https://console.videodb.io/player?url=https://stream.videodb.io/v3/published/manifests/b79a91d7-9553-4b4f-9d02-a47b9e168148.m3u8)

- **Get your API key:** Sign up on [VideoDB console](https://console.videodb.io) (free to start: $20 of credits, no credit card). 🆓
- **Set `VIDEO_DB_API_KEY`:** Enter your key in the `env` file.
- **Install dependencies:** Run `pip install -r requirements.txt` in your terminal.
- **Upload your collection to VideoDB:** Add your links in `upload.py`.
- **Run locally:** Start the flask server with `python app.py`.

## Publishing on ChatGPT Store 🏪
[📺 Watch: Create New GPT](https://console.videodb.io/player?url=https://stream.videodb.io/v3/published/manifests/b4b01b80-f38b-47f7-a238-09e53d844792.m3u8)

1. Deploy your flask server and note your server's `url`. 
2. In `openapi.yaml`, update the `url` field under `server`.
3. Visit the GPT builder at https://chat.openai.com/gpts/editor
4. In the configure tab, add your GPT's `Name` and `Description`.
5. Copy the prompt from `prompts.txt` into the `Instructions` field. Feel free to modify it as needed. ✏️
6. Click on `Create new Action`
7. Copy the openapi details from `openapi.yaml` Don't miss to update the `url` field.
8. Save your GPT for personal use and give it a test run! 🧪

---
<!-- ROADMAP -->

## Roadmap 🛣️

1. Add support for popular backend deployment CD pipelines like `Heroku`, `Replit`, etc.
2. Integrate with other data sources like `Dropbox`, `Google Drive`.
3. Connect with meeting recorder APIs such as `Zoom`, `Teams`, and `Recall.ai`.

---
<!-- CONTRIBUTING -->

## Contributing 🤝

Your contributions make the open-source community an incredible place for learning, inspiration, and creativity. We
welcome and appreciate your input! Here's how you can contribute:

- Open issues to share your use cases.
- Participate in brainstorming solutions for our roadmap.
- Suggest improvements to the codebase.

### Contribution Steps

1. Fork the Project 🍴
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request 📬

---

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[python-shield]:https://img.shields.io/pypi/pyversions/videodb?style=for-the-badge

[stars-shield]: https://img.shields.io/github/stars/video-db/streamRAG.svg?style=for-the-badge

[stars-url]: https://github.com/video-db/streamRAG/stargazers

[website-shield]: https://img.shields.io/website?url=https%3A%2F%2Fvideodb.io%2F&style=for-the-badge&label=videodb.io

[website-url]: https://videodb.io/

[discord-shield]: https://img.shields.io/badge/dynamic/json?style=for-the-badge&url=https://discord.com/api/invites/py9P639jGz?with_counts=true&query=$.approximate_member_count&logo=discord&logoColor=blue&color=green&label=discord

[discord-url]: https://discord.gg/py9P639jGz
