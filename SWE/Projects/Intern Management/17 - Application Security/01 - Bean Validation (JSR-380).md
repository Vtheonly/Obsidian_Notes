---
tags: [concept, validation, bean-validation, jsr-380]
type: concept
status: complete
related:
  - [[17 - Application Security/05 - Input Validation]]
---

# Bean Validation (JSR-380)

## What it is

**Bean Validation** (Jakarta Validation, formerly JSR-380) is a Java standard for declarative validation. You annotate fields; a validator checks them.

## Annotations

| Annotation | Checks |
|---|---|
| `@NotNull` | Not null |
| `@NotEmpty` | Not null and not empty (strings, collections) |
| `@NotBlank` | Not null and contains non-whitespace |
| `@Size(min, max)` | Length/size within range |
| `@Min`, `@Max` | Numeric range |
| `@Email` | Valid email format |
| `@Pattern(regexp)` | Matches regex |
| `@Past`, `@Future` | Date in past/future |
| `@AssertTrue`, `@AssertFalse` | Boolean assertion |
| `@DecimalMin`, `@DecimalMax` | BigDecimal range |
| `@Positive`, `@Negative` | Sign |

## Usage

```java
public record CreateInternCommand(
    @NotBlank(message = "Name is required") @Size(max = 100) String name,
    @NotNull @Min(16) @Max(100) Integer age,
    @NotBlank @Email String email,
    @Size(max = 150) String university,
    @Pattern(regexp = "^\+?[0-9 ]{8,20}$") String phoneNumber
) {}
```

```java
Validator validator = Validation.buildDefaultValidatorFactory().getValidator();
Set<ConstraintViolation<CreateInternCommand>> violations = validator.validate(cmd);
if (!violations.isEmpty()) {
    throw new ValidationException(violations);
}
```

## Spring integration

Spring auto-validates `@Valid` parameters:
```java
@RestController
public class InternController {
    @PostMapping("/interns")
    public Intern create(@Valid @RequestBody CreateInternCommand cmd) {
        // cmd is validated before this method is called
        return internService.create(cmd);
    }
}
```

## Custom validators

```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Constraint(validatedBy = PhoneNumberValidator.class)
public @interface PhoneNumber {
    String message() default "Invalid phone number";
    Class<?>[] groups() default {};
    Class<? extends Payload>[] payload() default {};
}

public class PhoneNumberValidator implements ConstraintValidator<PhoneNumber, String> {
    public boolean isValid(String value, ConstraintValidatorContext ctx) {
        return value != null && value.matches("^\+?[0-9 ]{8,20}$");
    }
}
```

## Project Connection

The project has no validation framework. The fix: Bean Validation on command objects, validated in the service layer.

## Further reading

- Jakarta Validation specification.
- Hibernate Validator (reference implementation).
