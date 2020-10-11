# FIT2107 Assignment 2 Test strategy
Group members:
1) Morad Abou Shadi (29799260)
2) Teo Wei Sheng (29800668)

### Introduction / Overview
This document serves to record the test strategies that we have utilized in order to come out with the best testing methods for the Calendar Application in Assignment 2. The test strategies used are all in accordance with the black box and white box testing methods that we have learned and effort was made to ensure that our test file could achieve a test coverage as close to 100% as possible.

### Test Strategies

#### User story 1
> As a user, I can see events and reminders for at least 5 years in past from the today’s date.

For this user story, we created a function `get_year_past_events()` that allows the user to choose how many years in the past they want to see events from. Since the user should see events and reminders for at least 5 years in the past, any input that is less than 5 should not be allowed. With that, we utilized **equivalence partitioning** to separate our test inputs to 2 different categories:

 1. Input of less than 5 years
 2. Input of 5 or more years

With that, all scenarios should be tested as any input that is less than 5 should yield the same result and any input that is 5 or more should also produce the same result.

##
#### User story 2
> As a user, I can see events and reminders for at least next two years (in future).

This user story is similar to the first one, with the only difference being that it is for events in the future rather than the past. For this user story, we created a function `get_year_future_events()` that allows the user to choose how many years in the future they want to see events from. Since the user should see events and reminders for at least 2 years in the future, any input that is less than 2 should not be allowed. With that, we utilized **equivalence partitioning** to separate our test inputs to 2 different categories:

 1. Input of less than 2 years
 2. Input of 2 or more years

With that, all scenarios should be tested as any input that is less than2 should yield the same result and any input that is 2 or more should also produce the same result.

##
#### User story 3
> As a user, I can navigate through different days, months, and years in the calendar so that I can view the details of events. For example, if the year 2019 is selected, all events and reminders(and any other information associated to the event) will be shown. This means on selecting the specific event or reminder I can see the detailed information.

For this user story, we wrote a function `get_specific_time_events()` that allows users to input 
