## Screenshots, Input & Output
This page contains screenshots, input and output of each screen.\
Each grouped by its modules.

## This page contains screenshots, input & output of:

Account Module

* Login
* Registration

[Tutorial Editor Module](https://github.com/maxosen/codinglab-1/blob/main/documentation/input-output.md#tutorial-editor-module)

* [Lesson Editor](https://github.com/maxosen/codinglab-1/blob/main/documentation/input-output.md#lesson-editor)
* Exercise Editor

Tutorial and Exercise Module

* Lesson
* Exercise

Feedback, Behaviour and Analytics Module

* Feedback Form
* Analytics

## Tutorial Editor Module
### Lesson Editor
![](markdown-images/lesson-editor-screenshot.png)\
Form / Editor for creating a lesson

![](markdown-images/lesson-editor-sample.png)\
Sample Inputs for creating a lesson

**Expected Input**

1. Title `String`
2. Order `Integer`
3. Content `String`
4. Question `String`
5. Answer `String`

**Invalid Input**

* Order must be an `Integer`
    * This rule is enforced by HTML input field validation.

**Expected Output**

A new row in PostgreSQL that consists of following columns with following data types:

1. ID `PRIMARY KEY`
2. Title `VARCHAR`
3. Order `INTEGER`
4. Markdown `TEXT`
5. Exercise Question `TEXT`
6. Exercise Answer `TEXT`
7. Date Created `DATE`


