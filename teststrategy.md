# FIT2107 Assignment 2 Test strategy
Group members:
1) Morad Abou Shadi (29799260)
2) Teo Wei Sheng (29800668)

### Introduction / Overview
This document serves to record the test strategies that we have utilized in order to come out with the best testing methods for the Calendar Application in Assignment 2. The test strategies used are all in accordance with the black box and white box testing methods that we have learned and effort was made to ensure that our test file could achieve a test coverage as close to 100% as possible.

### Test strategies

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

With that, all scenarios should be tested as any input that is less than 2 should yield the same result and any input that is 2 or more should also produce the same result.

##
#### User story 3
> As a user, I can navigate through different days, months, and years in the calendar so that I can view the details of events. For example, if the year 2019 is selected, all events and reminders(and any other information associated to the event) will be shown. This means on selecting the specific event or reminder I can see the detailed information.

For this user story, we made 2 separate functions, `get_specific_time_events()` that makes calls to the google calendar API to retrieve events based on the provided year/month/day, and also `navigate_calendar()`, which prints out the menu and collects user input to allow the user to simulate the process of navigating the calendar. To test this user story, we again utilized **equivalence partitioning** to separate the test inputs into different categories that might occur, which is:

 1. Input with only the year provided
 2. Input with the year and month provided
 3. Input with the year, month, and day provided

The value for year, month, and day is chosen arbitrarily as it does not matter as long as testing is done appropriately. Other than that, we also have to take into consideration erroneous inputs that might get passed into the function, for example, entering a value of year, month, and day that is less than 0, entering a month value larger than 12, entering a day value of larger than 31, and so on. For those cases, since there is no fairly straightforward way of doing the tests, we simply used **random testing** to pick out a few cases that might cause an error to be raised, and tested them.

On the other hand, for the menu, since it utilizes the `get_specific_time_events()` function, which has already been tested, we only tested the menu by providing it with random values, again, using **random testing**, to see if everything prints out as expected. Since there are various scenarios and inputs to consider for the menu, we simply used a basic **statement coverage** to ensure that each statement in the function (which includes the error handling) is covered by a part of the test code.

##
#### User story 4
> As a user, I can search events and reminders using different key words.

The search function for our Calendar Application is called `search_event()`, which searches the calendar to find events that has the provided keyword in their names and returns them. The testing function for this is also fairly straightforward, and we can only really partition the inputs into two different categories using **equivalence partitioning**, which is:

 1. Searching for an event that exists in the calendar
 2. Searching for an event that does not exist in the calendar

With that, we should be able to cover all cases for the search function.

##
#### User story 5
> As a user, I can delete events and reminders.

The function for deleting events in our Calendar Application is called `delete_event_by_name()`, which searches the calendar to find events that has the provided keyword in their names and removes them from the calendar. Just like the previous user story, the testing function for this is also fairly straightforward, and we can only really partition the inputs into two different categories using **equivalence partitioning**, which is:

 1. Deleting an event that exists in the calendar
 2. Deleting an event that does not exist in the calendar

With that, we should be able to cover all cases for the event delete function.

On the other hand, for deleting reminders, we have a function called `delete_event_reminder()`, which searches a given event for a reminder with the specified amount of minutes and deletes it. Since there are a plethora of conditions to account for in the function, such as if the given reminder exists, or if the given event name exists in the calendar, we utilized a **condition + branch coverage** to ensure each condition and its respective branches are tested accordingly by a test case. With that, we can ensure that the function will behave appropriately in any given scenario.

<br></br>
### Other test strategies conducted

#### Mocking
Other than testing out the actual Google Calendar API, mocking is also performed as the API is a web service and may be too slow to test out for some instances. Mocking is also conducted to simulate exceptions that may be hard to trigger in the actual system.

#### Coverage testing
To find out the coverage of our testing file, we utilized the coverage.py tool to measure and see which lines of code in the Calendar Application we covered, and which lines we did not. After running the coverage tool initially, we realized that our coverage of the code was only at around 60%, which means that our test file is missing a lot of the code. With that information, we added more tests to cover the lines of code that we did not tested previously before running the coverage file again, as we ideally want the coverage of our test file to be as close to 100% as possible. Ultimately, since some of the code such as the `get_calendar_api()` function and the `main()` function do not need to be tested, we resorted to just testing everything that we can and end up with with a coverage of around 80+% for our test code.

