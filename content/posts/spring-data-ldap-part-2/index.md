---
title: "Spring Data-Ldap: Part 2"
date: "2019-04-24T12:00:00Z"
slug: "spring-data-ldap-part-2"
description: "Now since we have plugged in the LDAP information it is time now to stitch it with Spring Security and the easiest thing to do is"
categories: ["others"]
tags: ["ldap", "spring"]
aliases: ["/wps/2019/04/24/spring-data-ldap-part-2/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

Now since we have plugged in the LDAP information it is time now to stitch it with Spring Security and the easiest thing to do is

> ```text
@Configuration
@EnableWebSecurity(debug = true)
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    private static final Logger logger = LoggerFactory.getLogger(WebSecurityConfig.class);

    @Autowired
    private LdapContextSource ldapContextSource;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.httpBasic().and().authorizeRequests().antMatchers("/users","/").permitAll()
                .anyRequest().authenticated().and().csrf().disable();
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
        auth.ldapAuthentication().contextSource(ldapContextSource)
                .userSearchBase("ou=users")
                .groupSearchBase("ou=groups")
                .groupSearchFilter("member={0}")
                .userDnPatterns("ou=users,dc=example,dc=com")
                .userSearchFilter("uid={0}");
    }
}
```

I have already added the ldapContextInformation in the ApacheDSConfiguration class.

```text
@Bean
LdapTemplate ldapTemplate(ContextSource contextSource) {
    return new LdapTemplate(contextSource);
}
```

After weaving this together I exposed a new method in controller

```text
@ResponseBody
@PostMapping("/protected")
public String protectedMethod(HttpServletRequest request) {
    logger.debug(" Requested: " + request.getRequestURI() + " : " + request.getUserPrincipal().getName() + " : " + context.getApplicationName());
    return "Method Protected";
}
```

and am ready to fire my application with a post method that has been protected by the backed Ldap (Apache DS).

> POST /events/protected HTTP/1.1  
> > Host: localhost:8082  
> > Authorization: Basic c3NoYXJtYTpmaXJld2FsbA==  
> > User-Agent: insomnia/6.3.2  
> > Cookie: JSESSIONID=A049DCE901E82092A38867FA67A773A9  
> > Accept: \*/\*  
> > Content-Length: 0  
> < HTTP/1.1 200  
> \* Replaced cookie JSESSIONID=”635AE0B0C5C3F7C6BF28FA7776D2FBA0″ for domain localhost, path /events, expire 0  
> < Set-Cookie: JSESSIONID=635AE0B0C5C3F7C6BF28FA7776D2FBA0; Path=/events; HttpOnly  
> < X-Content-Type-Options: nosniff  
> < X-XSS-Protection: 1; mode=block  
> < Cache-Control: no-cache, no-store, max-age=0, must-revalidate  
> < Pragma: no-cache  
> < Expires: 0  
> < X-Frame-Options: DENY  
> < Content-Type: text/plain;charset=UTF-8  
> < Content-Length: 16  
> < Date: Wed, 24 Apr 2019 14:12:30 GMT

![](screenshot-2019-04-24-at-7.42.36-pm.png)
