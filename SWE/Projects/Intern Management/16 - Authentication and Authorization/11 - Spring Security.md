---
tags: [concept, spring, security, framework]
type: concept
status: complete
related:
  - [[16 - Authentication and Authorization/09 - RBAC (Role-Based Access Control)]]
  - [[16 - Authentication and Authorization/10 - Session Management]]
---

# Spring Security

## What it is

**Spring Security** is the standard security framework for Spring apps. It handles authentication, authorization, session management, CSRF, CORS, password encoding, OAuth2, and more.

## Core components

- **SecurityFilterChain** — servlet filters that intercept requests.
- **AuthenticationManager** — authenticates users.
- **UserDetailsService** — loads user details from DB.
- **PasswordEncoder** — hashes passwords (BCrypt, Argon2).
- **SecurityContext** — holds the current authentication.
- **GrantedAuthority** — a permission/role.

## Basic configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/login").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/dashboard")
            )
            .logout(logout -> logout.logoutUrl("/logout"));
        return http.build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new Argon2PasswordEncoder();
    }
}
```

## Method-level security

```java
@PreAuthorize("hasRole('ADMIN')")
public void deleteUser(long id) { ... }

@PreAuthorize("hasPermission(#internId, 'intern', 'accept')")
public void acceptIntern(long internId) { ... }
```

## Project Connection

For a desktop app, Spring Security is overkill. But if the app evolves to a web app or REST API, Spring Security is the standard.

For now, the project can use:
- `Argon2PasswordEncoder` (from Spring Security) for password hashing.
- A custom `Authz` class for permission checks.

## Further reading

- Spring Security reference documentation.
