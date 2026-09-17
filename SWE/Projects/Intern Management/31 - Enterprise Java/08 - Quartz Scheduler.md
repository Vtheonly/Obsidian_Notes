---
tags: [concept, enterprise, scheduler, quartz]
type: concept
status: complete
related:
  - [[31 - Enterprise Java/03 - Jakarta Mail]]
---

# Quartz Scheduler

## What it is

**Quartz** is a job scheduling library for Java. Schedule jobs to run at specific times, intervals, or cron expressions.

## Maven

```xml
<dependency>
    <groupId>org.quartz-scheduler</groupId>
    <artifactId>quartz</artifactId>
    <version>2.3.2</version>
</dependency>
```

## Usage

### Define a job
```java
public class PendingInternReminderJob implements Job {
    public void execute(JobExecutionContext context) {
        List<Intern> pending = internRepository.findPendingOlderThan(Duration.ofDays(7));
        for (Intern intern : pending) {
            emailService.sendReminderEmail(intern);
        }
    }
}
```

### Schedule
```java
Scheduler scheduler = StdSchedulerFactory.getDefaultScheduler();
scheduler.start();

JobDetail job = JobBuilder.newJob(PendingInternReminderJob.class)
    .withIdentity("reminderJob", "group1")
    .build();

Trigger trigger = TriggerBuilder.newTrigger()
    .withIdentity("reminderTrigger", "group1")
    .withSchedule(CronScheduleBuilder.cronSchedule("0 0 9 ? * MON"))  // every Monday 9 AM
    .build();

scheduler.scheduleJob(job, trigger);
```

## Spring @Scheduled (simpler)

For Spring Boot apps, `@Scheduled` is simpler than Quartz:
```java
@Service
public class ReminderService {
    @Scheduled(cron = "0 0 9 ? * MON")
    public void sendReminders() {
        // ...
    }
}
```

Use Quartz when:
- You need persistent jobs (survive restart).
- You need clustering (multiple instances, no duplicate execution).
- You need complex triggers.

## Use cases

- **Nightly reminders** — "You have 5 pending interns."
- **Weekly reports** — email a summary every Monday.
- **Password expiry** — notify users 7 days before password expiry.
- **Cleanup** — delete old audit logs every night.

## Project Connection

The project has no scheduled jobs. The fix: Quartz (or Spring `@Scheduled` if using Spring) for:
- Nightly "pending intern" reminder to chiefs.
- Weekly stats digest.
- Daily password expiry notification.
- Daily audit log archival.

## Further reading

- Quartz documentation.
