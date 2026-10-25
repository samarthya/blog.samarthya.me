---
title: "Personal Access Token"
date: "2021-09-23T16:45:26Z"
slug: "personal-access-token"
categories: ["technical"]
tags: ["github", "pat"]
aliases: ["/wps/2021/09/23/personal-access-token/"]
wp_id: 1754
---

In case you are still using the basic/auth it is time to move to personal access token.

{{< lead >}}
[Official documentation](https://docs.github.com/en/enterprise-server@3.1/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) is the best guide.
{{< /lead >}}

Personal access tokens (PATs) are an alternative to using `passwords` for authentication to GitHub Enterprise Server when using the [GitHub API](https://docs.github.com/en/enterprise-server@3.1/rest/overview/other-authentication-methods#via-oauth-and-personal-access-tokens) or the [command line](https://docs.github.com/en/enterprise-server@3.1/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token#using-a-token-on-the-command-line).

## Step 1:

Go to the settings from the

![top right](screenshot-2021-09-23-at-10.07.40-pm.png "top right")

![](screenshot-2021-09-23-at-10.07.00-pm.png)

Once you navigate into settings, you have to select

![](screenshot-2021-09-23-at-10.08.46-pm.png)

![](screenshot-2021-09-23-at-10.09.31-pm.png)

Select Personal access tokens, and then click `Generate new token` in the next scren

![](screenshot-2021-09-23-at-10.10.47-pm.png)

Select the appropriate name and scope for the token.

![](screenshot-2021-09-23-at-10.12.02-pm.png)

Once you are done click `Generate`

![](screenshot-2021-09-23-at-10.12.46-pm.png)

Once added you can use that as part of the `scm` plugin in the main pom, or use it in the `settings.xml`. In my case I am using it in `server.xml` but need to add the property `project.scm.id` so that you refer the credentials.

```text
<project.scm.id>github.com</project.scm.id>
```
