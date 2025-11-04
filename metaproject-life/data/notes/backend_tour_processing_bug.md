Title: Backend bug — tours showing processing above 100%
Created: 2025-10-01
Tags: backend, bug, processing, percentage, tour-processing, keepeyeonball

Category: Project-Specific Technical

Bug description

There's a long-standing bug (present for years) in the backend where tours may display processing percentages above 100% in the tour list view.

Affected systems

- **Tour list view**: https://www.keepeyeonball.com/en/Home/TourList/realestate/1 (requires admin authentication)
- **Example tour showing issue**: https://tour.keepeyeonball.com/Tour/197fec33-85e6-406c-914f-110422a7508b

Bug characteristics

- **Duration**: Present for years
- **Frequency**: Intermittent (happens "sometimes")
- **Visibility**: Shows in admin tour list view
- **Impact**: Cosmetic/UI issue but may indicate underlying processing logic problems

Potential root causes to investigate

**Progress calculation logic:**
- Race conditions in progress updates
- Integer overflow or floating-point precision issues
- Multiple processes updating the same progress counter
- Progress not properly reset between processing runs

**Database/state issues:**
- Stale progress values not being cleared
- Transaction isolation problems during concurrent updates
- Progress field not properly bounded (0-100%)
- Inconsistent progress calculation across different processing stages

**Frontend display issues:**
- Raw progress values displayed without clamping to 100%
- Progress aggregation logic counting steps multiple times
- Caching of outdated progress values

Investigation steps

1. **Reproduce the issue:**
   - Identify specific conditions that trigger >100% display
   - Check if it's consistent across different browsers/sessions
   - Document exact progress values seen (101%? 150%? 200%?)

2. **Backend analysis:**
   - Review progress update code in tour processing pipeline
   - Check database schema for progress field constraints
   - Audit SQL queries that calculate/update progress values
   - Look for race conditions in concurrent processing

3. **Frontend analysis:**
   - Examine progress display component logic
   - Check if percentage is calculated client-side vs server-side
   - Verify progress value validation/clamping

4. **Data analysis:**
   - Query database for tours with progress > 100%
   - Analyze processing logs for tours showing the issue
   - Check for correlation with specific tour types/sizes

Immediate fixes to consider

- **Client-side clamping**: `Math.min(100, progressValue)` in display logic
- **Server-side validation**: Ensure progress values are bounded 0-100% before storage
- **Database constraints**: Add CHECK constraint to progress field
- **Progress reset**: Ensure progress is reset to 0 at start of new processing

Long-term solutions

- **Atomic progress updates**: Use database transactions for progress modifications
- **Progress audit trail**: Log all progress updates for debugging
- **Processing state machine**: Formalize tour processing states and transitions
- **Monitoring**: Add alerts for tours with anomalous progress values

Next actions

- Reproduce the bug and document exact conditions
- Review tour processing code for progress calculation logic
- Add client-side progress clamping as quick fix
- Implement proper progress bounds validation

Done: saved as `data/notes/backend_tour_processing_bug.md`