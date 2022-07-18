<h1 align="center">
    coursehero downloader (broken)
</p>

<p align="center">
    <a href="https://github.com/ryan5453/coursehero-api/stargazers">
        <img src="https://img.shields.io/github/stars/ryan5453/coursehero-api?style=social">
    </a>
    <a href="https://github.com/ryan5453/coursehero-api/blob/main/LICENSE">
        <img src="https://img.shields.io/github/license/ryan5453/coursehero-api">
    </a>
    <a href="https://python.org/">
        <img src="https://img.shields.io/badge/python-3.9-blue">
    </a>
    <a href="https://github.com/ambv/black">
        <img src="https://img.shields.io/badge/code%20style-black-black.svg">
    </a>
    <a href="https://github.com/PyCQA/isort">
        <img src="https://img.shields.io/badge/imports-isort-black.svg">
    </a>
</p>

## What is this?
This is a backend api that used to allow you to download coursehero documents (up to 9 pages) for free. It downloaded the previews and patched all the unblured images together to create one pdf. Coursehero has since changed their preview method and this no longer works. I spent a lot of time on this and I think the code quality is pretty good, so I thought I'd share it.

## Credits
This project was inspired by [daijro's](https://github.com/daijro) [CourseHeroUnblur](https://github.com/daijro/CourseHeroUnblur) project. It shares a lot of similarities with that project, however this project was written from scratch with the exception of a tiny bit of processing logic.