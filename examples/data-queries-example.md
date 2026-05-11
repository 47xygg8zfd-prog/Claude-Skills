# Example Output: Data Queries Skill

**Prompt used:** "Write a Snowflake SQL query for weekly active users by plan tier over the last 90 days, and a Splunk search for digest email delivery errors"

---

## Snowflake SQL: Weekly Active Users by Plan Tier (Last 90 Days)

```sql
WITH weekly_activity AS (
    SELECT
        DATE_TRUNC('week', event_timestamp)      AS week_start,
        u.user_id,
        a.plan_tier
    FROM events e
    JOIN users u
        ON e.user_id = u.user_id
    JOIN accounts a
        ON u.account_id = a.account_id
    WHERE
        e.event_timestamp >= DATEADD(day, -90, CURRENT_DATE)
        AND e.event_type IN ('page_view', 'dashboard_load', 'filter_applied', 'export')
        AND u.is_internal = FALSE
)

SELECT
    week_start,
    plan_tier,
    COUNT(DISTINCT user_id)                         AS weekly_active_users,
    LAG(COUNT(DISTINCT user_id)) OVER (
        PARTITION BY plan_tier
        ORDER BY week_start
    )                                               AS prior_week_wau,
    ROUND(
        (COUNT(DISTINCT user_id) - LAG(COUNT(DISTINCT user_id)) OVER (
            PARTITION BY plan_tier ORDER BY week_start
        )) / NULLIF(LAG(COUNT(DISTINCT user_id)) OVER (
            PARTITION BY plan_tier ORDER BY week_start
        ), 0) * 100, 1
    )                                               AS wow_change_pct
FROM weekly_activity
GROUP BY 1, 2
ORDER BY week_start DESC, plan_tier
;
```

**Notes**:
- Replace `events`, `users`, `accounts` with your actual table names
- `event_type` filter captures meaningful engagement — adjust to match your event taxonomy
- `is_internal = FALSE` excludes Pulse employees from WAU counts
- `NULLIF(..., 0)` prevents division-by-zero in the WoW % calculation for new plan tiers

---

## Splunk SPL: Digest Email Delivery Errors

```
index=pulse_app sourcetype=sendgrid_events
    (event="bounce" OR event="dropped" OR event="deferred" OR event="spamreport")
    tag="weekly_digest"
| eval error_type = case(
    event="bounce",     "Hard Bounce",
    event="dropped",    "Dropped (invalid/unsubscribed)",
    event="deferred",   "Deferred (temp failure)",
    event="spamreport", "Spam Report",
    true(),             "Other"
  )
| stats
    count             AS total_errors,
    dc(email)         AS unique_recipients_affected
    BY error_type, date_hour
| sort - date_hour, - total_errors
| rename date_hour AS "Hour", error_type AS "Error Type",
         total_errors AS "Error Count", unique_recipients_affected AS "Recipients Affected"
```

**What this shows:**
- Breakdown of delivery failures by error type and hour
- Distinguishes hard bounces (permanent — remove from list) from deferrals (temporary — will retry)
- `tag="weekly_digest"` assumes you're passing `utm_campaign=weekly_digest` or a custom tag in your SendGrid send

**Alert recommendation**: Set a Splunk alert if `total_errors > 50` in any 1-hour window on Monday mornings (digest send window). Route to `#pulse-oncall` Slack channel.
