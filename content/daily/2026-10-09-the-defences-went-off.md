---
title: "The defences went off"
date: 2026-10-09T20:00:00-04:00
slug: "the-defences-went-off"
description: "A fake administrator, 20 plugins switched off in one second, and a hidden loader planted to stay."
milestone: "incident"     # shows in the Milestones timeline on /daily/
categories: ["daily"]
tags: ["security", "wordpress", "incident"]
---

*Written on 26 October from the old site's own records. At the time, I didn't know any of this.*

Just after midnight (UTC), an administrator account "registered in 1970" logged in. A minute later, **20 plugins
were switched off in the same second**, including the one that blocks password guessing.

In the afternoon, a code-snippets plugin appeared, and with it a snippet called `content-cache-support`. I only
decoded it today, 26 October. It plants a hidden must-use plugin that WordPress loads on every request, even
though it never shows up in the plugin list. That plugin covered every page, even the login page, with a
white loading screen, and fetched its next instructions from a blockchain, where they're hard to take down. It
re-installed itself every six hours and deleted rival malware it found on the site.

Not a smash-and-grab. They meant to stay.
