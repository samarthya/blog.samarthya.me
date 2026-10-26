---
title: "Spring Data-LDAP"
date: "2019-04-24T12:00:00Z"
slug: "spring-data-ldap"
description: "I have a small problem at hand which girdles around learning Angular, with a Spring enabled Rest endpoints which uses a DB to store data and have security layer in between that should interact with a…"
categories: ["others"]
tags: ["security", "spring"]
aliases: ["/wps/2019/04/24/spring-data-ldap/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

I have a small problem at hand which girdles around learning Angular, with a Spring enabled Rest endpoints which uses a DB to store data and have security layer in between that should interact with a LDAP for authentication and authorization and finally the application should run as one smooth unit. It will be too much to cover in single blog so I will be writing multiple blogs in continuation to this one.

There were multiple start points that I could have started but in retrospect as I blog about it, the best starting point is to think about the services alone at first, what you want to develop and create them independently and test them as a unit before you can proceed to any other component.

The other way could have been, that I define the functional signature and agree on expectation, especially if it was more than one team member project and it would have been much easier to develop parallely.

Anyway, I am just using my spare time to develop it, so I thought of crunching some sample code to try out the service that I wanted before jumping on the actual application.

Starting point as  always is sprint initializer and it helped me chose what I want and get the guideline project to start with.

> <dependencies>  
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-data-ldap</artifactId>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-data-rest</artifactId>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-security</artifactId>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-web</artifactId>  
> </dependency>
>
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-tomcat</artifactId>  
> <scope>provided</scope>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.boot</groupId>  
> <artifactId>spring-boot-starter-test</artifactId>  
> <scope>test</scope>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.security</groupId>  
> <artifactId>spring-security-test</artifactId>  
> <scope>test</scope>  
> </dependency>  
> </dependencies>

Since I have added these dependencies now, and am using IntelliJ to develop, life becomes a little easier.

The current code looks minimal with the two classes

> @SpringBootApplication  
> public class EventsServicesApplication {
>
> public static void main(String[] args) {  
> SpringApplication.run(EventsServicesApplication.class, args);  
> }
>
> }

and

> public class ServletInitializer extends SpringBootServletInitializer {
>
> @Override  
> protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {  
> return application.sources(EventsServicesApplication.class);  
> }
>
> }

So scaffolding is ready, and it is time to add some dummy capabilities to try out.

You can configure few properties in the *application.properties* file

> spring.profiles.active=default  
> server.port=8082  
> server.servlet.context-path=/events  
> logging.level.org.springframework=DEBUG

If you now execute you can watch out for the information in the console that can help you understand what is getting initialized and how the spring framework is helping to stitch the capability that we are trying to achieve.

> 2019-04-23 23:15:10.932 INFO 62835 — [ main] o.s.b.w.embedded.tomcat.TomcatWebServer : Tomcat started on port(s): 8082 (http) with context path ‘/events’  
> 2019-04-23 23:15:10.938 INFO 62835 — [ main] m.s.E.EventsServicesApplication : Started EventsServicesApplication in 3.486 seconds (JVM running for 4.881)

I added my first controller a [RestController](https://docs.spring.io/spring/docs/current/javadoc-api/org/springframework/web/bind/annotation/RestController.html)

> @RestController  
> public class ControllerOne {
>
> @GetMapping(“/”)  
> @ResponseBody  
> public String bonsoir(@RequestParam(name = “id”, required = false) String id, HttpServletRequest request) {  
> if(id != null )  
> return “Bonsoir ” + id + ” !”;  
> else  
> return “Bonsoir!”;  
> }
>
> @ResponseBody  
> @GetMapping(“/error”)  
> public String errorMessage(HttpServletRequest request) {  
> return “Error occurred, please see the server logs.”;  
> }  
> }

At this moment if you try to call the endpint using any of the rest clients (your preference, but I use insomnia)  in this application you may see something like below

> > GET /events HTTP/1.1  
> > Host: localhost:8082  
> > User-Agent: insomnia/6.3.2  
> > Cookie: JSESSIONID=67570EB8C6F2A822F908C4A9F1CBA2E7  
> > Accept: \*/\*

Response would be

> < HTTP/1.1 401  
> < Set-Cookie: JSESSIONID=DBC2F7DF3DBE01D6E3B45E9B311ABB66; Path=/events; HttpOnly  
> < WWW-Authenticate: Basic realm=”Realm”  
> < X-Content-Type-Options: nosniff  
> < X-XSS-Protection: 1; mode=block  
> < Cache-Control: no-cache, no-store, max-age=0, must-revalidate  
> < Pragma: no-cache  
> < Expires: 0  
> < X-Frame-Options: DENY  
> < Content-Type: application/json;charset=UTF-8  
> < Transfer-Encoding: chunked  
> < Date: Tue, 23 Apr 2019 17:47:07 GMT

It is simply because we have enabled the security which enforces all the request that is being sent to this server are being scrutnized and by default the value that it uses for the [WebSecurityConfigurerAdapter](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/web/configuration/WebSecurityConfigurerAdapter.html) is below

> http.authorizeRequests().anyRequest().authenticated().and().formLogin().and().httpBasic();

All request that reach the server are all evaluated for the right Access.

> org.springframework.security.access.AccessDeniedException: Access is denied  
> at org.springframework.security.access.vote.AffirmativeBased.decide(AffirmativeBased.java:84) ~[spring-security-core-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.access.intercept.AbstractSecurityInterceptor.beforeInvocation(AbstractSecurityInterceptor.java:233) ~[spring-security-core-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.invoke(FilterSecurityInterceptor.java:124) ~[spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.access.intercept.FilterSecurityInterceptor.doFilter(FilterSecurityInterceptor.java:91) ~[spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.access.ExceptionTranslationFilter.doFilter(ExceptionTranslationFilter.java:119) ~[spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.session.SessionManagementFilter.doFilter(SessionManagementFilter.java:137) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.AnonymousAuthenticationFilter.doFilter(AnonymousAuthenticationFilter.java:111) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.servletapi.SecurityContextHolderAwareRequestFilter.doFilter(SecurityContextHolderAwareRequestFilter.java:170) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.savedrequest.RequestCacheAwareFilter.doFilter(RequestCacheAwareFilter.java:63) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.www.BasicAuthenticationFilter.doFilterInternal(BasicAuthenticationFilter.java:158) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.ui.DefaultLogoutPageGeneratingFilter.doFilterInternal(DefaultLogoutPageGeneratingFilter.java:52) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.ui.DefaultLoginPageGeneratingFilter.doFilter(DefaultLoginPageGeneratingFilter.java:206) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.AbstractAuthenticationProcessingFilter.doFilter(AbstractAuthenticationProcessingFilter.java:200) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.authentication.logout.LogoutFilter.doFilter(LogoutFilter.java:116) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.csrf.CsrfFilter.doFilterInternal(CsrfFilter.java:100) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.header.HeaderWriterFilter.doFilterInternal(HeaderWriterFilter.java:74) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.context.SecurityContextPersistenceFilter.doFilter(SecurityContextPersistenceFilter.java:105) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.context.request.async.WebAsyncManagerIntegrationFilter.doFilterInternal(WebAsyncManagerIntegrationFilter.java:56) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.security.web.FilterChainProxy$VirtualFilterChain.doFilter(FilterChainProxy.java:334) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy.doFilterInternal(FilterChainProxy.java:215) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.security.web.FilterChainProxy.doFilter(FilterChainProxy.java:178) [spring-security-web-5.1.5.RELEASE.jar:5.1.5.RELEASE]  
> at org.springframework.web.filter.DelegatingFilterProxy.invokeDelegate(DelegatingFilterProxy.java:357) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.web.filter.DelegatingFilterProxy.doFilter(DelegatingFilterProxy.java:270) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.springframework.web.filter.RequestContextFilter.doFilterInternal(RequestContextFilter.java:99) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.springframework.web.filter.FormContentFilter.doFilterInternal(FormContentFilter.java:92) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.springframework.web.filter.HiddenHttpMethodFilter.doFilterInternal(HiddenHttpMethodFilter.java:93) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.springframework.web.filter.CharacterEncodingFilter.doFilterInternal(CharacterEncodingFilter.java:200) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.springframework.web.filter.OncePerRequestFilter.doFilter(OncePerRequestFilter.java:107) [spring-web-5.1.6.RELEASE.jar:5.1.6.RELEASE]  
> at org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:193) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.ApplicationFilterChain.doFilter(ApplicationFilterChain.java:166) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.StandardWrapperValve.invoke(StandardWrapperValve.java:200) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.StandardContextValve.invoke(StandardContextValve.java:96) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.authenticator.AuthenticatorBase.invoke(AuthenticatorBase.java:490) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.StandardHostValve.invoke(StandardHostValve.java:139) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.valves.ErrorReportValve.invoke(ErrorReportValve.java:92) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.core.StandardEngineValve.invoke(StandardEngineValve.java:74) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.catalina.connector.CoyoteAdapter.service(CoyoteAdapter.java:343) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.coyote.http11.Http11Processor.service(Http11Processor.java:408) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.coyote.AbstractProcessorLight.process(AbstractProcessorLight.java:66) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.coyote.AbstractProtocol$ConnectionHandler.process(AbstractProtocol.java:834) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.tomcat.util.net.NioEndpoint$SocketProcessor.doRun(NioEndpoint.java:1415) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at org.apache.tomcat.util.net.SocketProcessorBase.run(SocketProcessorBase.java:49) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1167) [na:na]  
> at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:641) [na:na]  
> at org.apache.tomcat.util.threads.TaskThread$WrappingRunnable.run(TaskThread.java:61) [tomcat-embed-core-9.0.17.jar:9.0.17]  
> at java.base/java.lang.Thread.run(Thread.java:844) [na:na]

Time to customize [security](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/web/configuration/WebSecurityConfigurerAdapter.html)

I started by adding extending the [WebSecurityConfigurerAdapter](https://docs.spring.io/spring-security/site/docs/current/api/org/springframework/security/config/annotation/web/configuration/WebSecurityConfigurerAdapter.html)

> @Configuration  
> @EnableWebSecurity(debug = true)  
> public class WebSecurityConfig extends WebSecurityConfigurerAdapter {  
> @Override  
> protected void configure(HttpSecurity http) throws Exception {  
> http.authorizeRequests().anyRequest().permitAll();  
> }  
> }

What I have done in the configure method is bypassed all the security explicitly by stating that permits all the requests with the overridden configure method.

## Spring Data Ldap

Now time to start with the Ldap structuring. From the introduction available at [spring.io](https://spring.io/projects/spring-data-ldap)

> The Spring Data LDAP project provides repository abstractions for Spring LDAP  
> on top of Spring LDAP’s LdapTemplate and Object-Directory Mapping.

Object-relational mapping frameworks like Hibernate and JPA offers developers the ability to use annotations to map relational database tables to Java objects.Spring LDAP project offers a similar ability with respect to LDAP directories through a number of methods: in `LdapOperations`

Also, note

> Spring LDAP repositories can be enabled by using a <data-ldap:repositories>  
> tag in your XML configuration or by using an @EnableLdapRepositories annotation  
> on a configuration class.

For Ldap source I am using apacheDS which is fairly easy to use and manage.

![Image title](https://dzone.com/storage/temp/11718636-screenshot-2019-04-24-at-122059-pm.png)

With a typical user attributes as under

![Image title](https://dzone.com/storage/temp/11718641-screenshot-2019-04-24-at-122213-pm.png)

Points to remember straight from the documentation

1. All Spring LDAP repositories must work with entities annotated with the ODM annotations, as described in [Object-Directory Mapping](https://docs.spring.io/spring-ldap/docs/2.3.2.RELEASE/reference/#odm).
2. Since all ODM managed classes must have a Distinguished Name as the ID, all Spring LDAP repositories must have the ID type parameter set to `javax.naming.Name`. Indeed, the built-in `LdapRepository` only takes one type parameter: the managed entity class, which defaults the ID to `javax.naming.Name`.
3. Due to specifics of the LDAP protocol, paging and sorting are not supported for Spring LDAP repositories.

- I wanted to try out user listing first, so first thing I need to define is the ODM for the user.
- 1. Added the maven dependency

> <dependency>  
> <groupId>org.springframework.ldap</groupId>  
> <artifactId>spring-ldap-core</artifactId>  
> </dependency>  
> <dependency>  
> <groupId>org.springframework.data</groupId>  
> <artifactId>spring-data-ldap</artifactId>  
> </dependency>

Added the Entity class with the right annotation

> @Entry(base=”ou=users”, objectClasses = {  
> “top”,  
> “inetOrgPerson”, “person”, “organizationalPerson”,  
> “simpleSecurityObject”})  
> public class UserModel {
>
> @JsonIgnore  
> @Id  
> private Name id;
>
> @JsonProperty(“userName”)  
> private @Attribute(name = “uid”) String uid;
>
> @JsonProperty(“firstName”)  
> private @Attribute(name = “cn”) String firstName;
>
> @JsonIgnore  
> private @Attribute(name = “displayname”) String displayName;
>
> @JsonProperty(“lastName”)  
> private @Attribute(name = “sn”) String lastName;
>
> public UserModel(String uid, String firstName, String displayName, String lastName) {  
> this.uid = uid;  
> this.firstName = firstName;  
> this.displayName = displayName;  
> this.lastName = lastName;  
> }
>
> public UserModel(String userName, String firstName, String lastName) {  
> this.uid = userName;  
> this.firstName = firstName;  
> this.lastName = lastName;  
> }
>
> public UserModel() {
>
> }
>
> public String getFirstName() {  
> return firstName;  
> }
>
> public void setFirstName(String firstName) {  
> this.firstName = firstName;  
> }
>
> public String getLastName() {  
> return lastName;  
> }
>
> public void setLastName(String lastName) {  
> this.lastName = lastName;  
> }
>
> public String getUid() {  
> return uid;  
> }
>
> public void setUid(String uid) {  
> this.uid = uid;  
> }
>
> public String getDisplayName() {  
> return displayName;  
> }
>
> public void setDisplayName(String displayName) {  
> this.displayName = displayName;  
> }
>
> @Override  
> public String toString() {  
> return “UserModel{” +  
> “uid='” + uid + ‘\” +  
> “, firstName='” + firstName + ‘\” +  
> “, displayName='” + displayName + ‘\” +  
> “, lastName='” + lastName + ‘\” +  
> ‘}’;  
> }  
> }

Added configuration

> @Configuration  
> @EnableLdapRepositories(basePackages = “me.samarthya.EventsServices.ldap”)  
> public class ApacheDSConfiguration {  
> @Bean  
> LdapTemplate ldapTemplate(ContextSource contextSource) {  
> return new LdapTemplate(contextSource);  
> }  
> }

Added properties

> spring.ldap.base=dc=example,dc=com  
> spring.ldap.password=secret  
> spring.ldap.username=uid=admin,ou=system  
> spring.ldap.urls=ldap://localhost:10389

Created repository

> @Repository  
> public interface ApacheDSRepository extends LdapRepository<UserModel> {
>
> }

Added a method in the controller to get the user list.

> @ResponseBody  
> @GetMapping(“/users”)  
> public Iterable<UserModel> getAllUsers() {  
> return apacheDSRepository.findAll();  
> }

Firewaway any request to find the information

> > GET /events/users HTTP/1.1  
> > Host: localhost:8082  
> > User-Agent: insomnia/6.3.2  
> > Cookie: JSESSIONID=438BF9E64596D6A1F96F49E7302BB8A9; JSESSIONID=67570EB8C6F2A822F908C4A9F1CBA2E7  
> > Accept: \*/\*
>
> < HTTP/1.1 200  
> < X-Content-Type-Options: nosniff  
> < X-XSS-Protection: 1; mode=block  
> < Cache-Control: no-cache, no-store, max-age=0, must-revalidate  
> < Pragma: no-cache  
> < Expires: 0  
> < X-Frame-Options: DENY  
> < Content-Type: application/json;charset=UTF-8  
> < Transfer-Encoding: chunked  
> < Date: Wed, 24 Apr 2019 09:02:06 GMT

![Response received](https://dzone.com/storage/temp/11719231-screenshot-2019-04-24-at-35124-pm.png)

If you wish to see the code it is available in [github.com](https://github.com/samarthya/EventsService)
