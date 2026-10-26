---
title: "PAT: Personal Access Token"
date: "2023-02-24T12:00:00Z"
slug: "pat-personal-access-token"
description: "Using Git Personal Access Tokens (PATs) is a secure and convenient way to authenticate with Git service providers."
categories: ["technical"]
tags: ["configure", "pat", "tokens"]
aliases: ["/wps/2023/02/24/pat-personal-access-token/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

*[image unavailable: an-lint.png]*

Using Git Personal Access Tokens (PATs) is a secure and convenient way to authenticate with Git service providers. In this blog post, we will discuss how to use Git PATs on both Mac and CentOS 7 systems.

## Generation a PAT

{{< lead >}}
You can refer to the previous [blog]({{< relref "/posts/personal-access-token" >}})
{{< /lead >}}

Before we begin, we need to generate a Personal Access Token from our Git service provider. The exact steps to generate a PAT may differ depending on the service provider, but usually, you can find the option to generate a PAT under your account settings.

Once you have generated your PAT, keep it safe as it will be used to authenticate with Git service providers.

## Using on OSX

To configure Git to use a PAT on a Mac, follow these steps:

1. Open Terminal on your Mac.
2. Set your Git username and email address using the following commands:
   - `git config --global user.name "Your Name"`
   - `git config --global user.email "youremail@example.com"`
3. Configure Git to use the PAT for authentication by running the following command:
   - `git config --global credential.helper osxkeychain`
4. When you run any Git command that requires authentication, Git will prompt you for your username and PAT. Enter your Git username and PAT and select the “Always allow” option to store the credentials in the macOS Keychain.

Now, Git will automatically use the stored credentials when you run any Git command that requires authentication.

### Using Git PAT on CentOS 7

To configure Git to use a PAT on CentOS 7, follow these steps:

1. Open the terminal on your CentOS 7 machine.
2. Set your Git username and email address using the following commands:
   - `git config --global user.name "Your Name"`
   - `git config --global user.email "youremail@example.com"`
3. Configure Git to use the PAT for authentication by running the following command:
   - `git config --global credential.helper store`
4. Create a new file named `.git-credentials` in your home directory using the following command:
   - `touch ~/.git-credentials`
5. Open the `.git-credentials` file using a text editor and add the following lines:
   - `https://<git-service-provider>/username:personal-access-token`
   - Replace `<git-service-provider>` with the URL of your Git service provider (e.g. github.com, gitlab.com, bitbucket.org, etc.).
   - Replace `username` with your Git username.
   - Replace `personal-access-token` with the PAT that you generated earlier.
6. Save and close the `.git-credentials` file.

Now, when you run any Git command that requires authentication, Git will automatically use the PAT that you specified in the `.git-credentials` file.

### Conclusion

In this blog post, we discussed how to use Git Personal Access Tokens (PATs) on both Mac and CentOS 7 systems. By configuring Git to use PATs, we can authenticate securely with Git service providers and avoid the need to enter our username and password every time we use Git.
