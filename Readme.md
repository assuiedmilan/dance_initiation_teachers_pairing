# Dance Pairing Scheduler

This Python program provides a simple and efficient way to schedule dancers for a series of dance events. It handles pairings of dancers based on their availabilities, levels of experience, and roles (lead or follow), ensuring that everyone has a fair chance to perform while maintaining balanced pairings.

## About

In the world of social dance, it's common to have a group of dancers where some act as leads and others act as follows. Each dancer has their own availability, and they may differ in their level of dance experience. It's desirable that all dancers get an equal chance to perform and beginners should always be paired with expert dancers for better guidance.

This program takes these factors into consideration to generate optimal dance pairings for a list of dates.

## Features

The algorithm has several important features:

- Takes into account the availability of each dancer on the given dates
- Ensures that a lead is always paired with a follow
- Considers the level of experience of each dancer (beginner, medium, expert)
- Beginners are always paired with experts for better learning experience
- All dancers should perform a similar number of times for fairness
- If no match exists for a date, the program highlights it 

## Usage

To use this program, you'll need to:

1. Create instances of the `Dancer` class for each dancer, providing their name, level of experience and role (lead or follow).
2. Add the dates when each dancer is available using the `add_availability()` method.
3. Call the `assign_dates()` function with the list of leads, follows, and dates.

## Testing

Unit tests have been written to ensure the correctness of the code. These tests check various aspects of the algorithm like generating possible matches, filtering valid matches, ensuring balanced performances, and overall assignment of dates.

You can run the tests using the pytest framework. 

This program is a powerful tool for event organizers and can be further expanded or modified to fit specific requirements. Happy dancing!


## Initial Generation of the program

This program first draft was generated using ChatGPT before being fixed and reworked, the program did not perform as expected initially and some tests were failed due to incompletely implemented requirements.

The initial set of requirements stands as follow:

### Requirements:

Write a python 11 program that will pair dancers based on the following requirements:

- We have a set of dancers, that we will name leads, and follow
- Each lead, and each follow, has an assigned level, from begginer to expert
- Each lead, and each follow, also has a name
- Dancers information must be stored in a class and not in a dict
- A lead must always be paired with a follow
- All properties (name and level) must be accessible from a property
- Level comparison with another dancer shall be accessible as a member static method of the dancer class

For the algorithm:

- Eacher dancer will select availabilities from a list of dates
- Start by matching all dancers that have availabilities compatibilities. You could do that by generating tuples of potentials dancers for each date. This will be a first process
- Once you have all the tuples for a potential date, make sure each tuple is valid, a tuple will be valid based on the following criteria: Expert and Medium dancers can be matched with anyone. Begginers dancers can be matched only with expert dancers. Also, dancers should both be available for the date their tuple is associated with. Even if this should be intrinsequely the case, the verification needs to be performed. This will be a second process.
- Once we have all the valid tuples only, select the dancers for this date, to do this, make sure that there's no imbalance in dates attributions: available dancers should all perform a similar number of times. This will be a third process.
- If a date has no match, generate a tuple for this date that shows it


### Tests:

Generate the following unit tests using pytest:

- Verify that generate_tuples will match only based on availabilities
- Verify that generate_tuples will not match two dancers that do not have common availabilities
- Verify that generate_tuples will not match a lead and a follow together whatever their availabilites are

- Verify that filter_valid_tuples will allow begginers dancers with expert dancers, medium dancers with expert dancers, and expert dancers with expert dancers. Perform this test with a set of lead and follow then invert their roles, keeping the same level. Use pytest parametrize
- Verify that filter_valid_tuples will not allow begginers dancers with medium dancers.  Perform this test with a set of lead and follow then invert their roles, keeping the same level. Use pytest parametrize
- Verify that filter_valid_tuples will reject valid pairing when the dancers have no common availabilities

- Verify that balance_performances will not create imbalances. You can use a set of several dancers and have some available for all dates, while some others have only one availability

- Verify that assign_dates function properly by using a set of 6 leads and 4 follows, that should be available for 1 to 4 dates among 6 possible

## Updates to the requirements following trials:

### Balance function is not working properly

Initially the balance function was favoring experienced dancers only, it was rewritten using the following set of requirements:

- When in a valid tuple, a lead have less assigned dates than the other lead, it should be favored
- When in a valid tuple, a follow have less assigned dates than the other follow, it should be favored
- When making an arbitration between an begginer and a more advanced dancer, favor the tuple with the less experienced dancer
- When the lead and follow of both tuples have 0 dates, assign the date randomly, this is to avoid having all begginers getting the first dates, and all experienced dancers having the last
- The balance_performances function shall have the same signature as the first version of it
