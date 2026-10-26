---
title: "Creating your app with VUEJS"
date: "2019-02-28T12:00:00Z"
slug: "creating-your-app-with-vuejs"
description: "This is my attempt at learning a new framework and using it to create my own webapp uing vueJS."
categories: ["others"]
tags: ["vue"]
aliases: ["/wps/2019/02/28/creating-your-app-with-vuejs/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

This is my attempt at learning a new framework and using it to create my own webapp uing vueJS.

> Vue is a progressive and reactive framework for building user interfaces.

The things I need is first

## VUE-CLI

> npm install -g @vue/cli

You can test the installation was successful or not by issuing *vue –version command.* In my case it is returning *3.4.1.* Vue CLI uses a plugin based architecture

## Creating a new application

I am going to create a single landing page for my application as the first step and keep adding to it as I go along so first step what all options do I have

### vue –help

It returns a standard help output identifying the common commands you can use.

```text
Commands:
create [options] <app-name> create a new project powered by vue-cli-service
add [options] <plugin> [pluginOptions] install a plugin and invoke its generator in an already created project
invoke [options] <plugin> [pluginOptions] invoke the generator of a plugin in an already created project
inspect [options] [paths...] inspect the webpack config in a project with vue-cli-service
serve [options] [entry] serve a .js or .vue file in development mode with zero config
build [options] [entry] build a .js or .vue file in production mode with zero config
ui [options] start and open the vue-cli ui
init [options] <template> <app-name> generate a project from a remote template (legacy API, requires @vue/cli-init)
config [options] [value] inspect and modify the config
upgrade [semverLevel] upgrade vue cli service / plugins (default semverLevel: minor)
info print debugging information about your environment

Run vue <command> --help for detailed usage of given command.
```

### vue create –help

```text
Usage: create [options] <app-name>

create a new project powered by vue-cli-service

Options:
-p, --preset <presetName> Skip prompts and use saved or remote preset
-d, --default Skip prompts and use default preset
-i, --inlinePreset <json> Skip prompts and use inline JSON string as preset
-m, --packageManager <command> Use specified npm client when installing dependencies
-r, --registry <url> Use specified npm registry when installing dependencies (only for npm)
-g, --git [message] Force git initialization with initial commit message
-n, --no-git Skip git initialization
-f, --force Overwrite target directory if it exists
-c, --clone Use git clone when fetching remote preset
-x, --proxy Use specified proxy when creating project
-b, --bare Scaffold project without beginner instructions
-h, --help output usage information
```

I will create my application by the name samarthya just to see how it works.

### vue create samarthya

The moment you issue this command in the terminal you will be prompted to select some options choose the default and press enter

### npm run serve

The last step to execute and see the application is to run this command npm run serve as open the localhost:8080 in browser and you can see your boiler plate application running.
