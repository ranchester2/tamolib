# Classes

## Tamo `class tamo.Tamo`

### **Description**

Tamo is the main object used, it is your session with Tamo. Everything is done through.

#### **`Tamo(username, password)`**

Create a TAMO session.

#### **Arguments**

##### **`username`**

Your TAMO account's username.

###### **Type**

`str`

##### **`password`**

Your TAMO account's password.

###### **Type**

`str`

### **Properties**

### `username`

Your TAMO account's username

##### **Type**

`str`

### `password`

Your TAMO account's password

##### **Type**

`str`

### **Methods**

### **`close()`**

Close your connection with TAMO, most TAMO functions will become unusable, unrecommended to use your
session after closing.

## Schedule `class tamo.models.Schedule`

### **Description**

Your account's schedule in TAMO, know what lessons happen when.

### **Iterate**.

Iterate through the `days` property.

### **Properties**

### **`days`**

A `list` of `tamo.models.SchoolDay`.

##### **Type**

`list`

## SchoolDay `class tamo.models.SchoolDay`

### **Description**

A School Day in TAMO.

### **Iterate**

Will iterate through the `lessons` property

### **Properties**

### **`empty`**

Wether the scool day is empty and has no lessons

##### **Type**

`bool`

### **`lessons`**

List of `tamo.models.Lesson` in the day, does not exist if the property `emtpy` is `True`.

##### **Type**

`list`

### **Methods**

### **`append_lesson(lesson)`**

Append a lesson to the day's list of lessons. Designed mostly for developers.  
**NOTE**: you do not need to worry about the order, as they are automatically sorted by their `num_in_day` property

#### **Arguments**:

#### **`lesson`**

The lesson you want to add.s

##### **Type**

`tamo.models.Lesson`

## Lesson `class tamo.models.Lesson`

### **Description**

A school lesson in TAMO,

### **Properties**

### **`num_in_day`**

Which lesson in the day is the lesson  
**NOTE**: uses IRL counting

##### **Type**

`int`

### **`start`**

At what time does the lesson start in the day.

##### **Type**

`datetime.datetime`

### **`end`**

At what time does the lesson end in the day

##### **Type**

`datetime.datetime`

### **`name`**

Full name of the lesson

##### **Type**

`str`

### **`teacher`**

The Teacher of the lesson

##### **Type**

`tamo.models.Teacher`

## Teacher `class tamo.models.Teacher`

A teacher represented in TAMO

### **Properties**

### **`name`**

Full name of the teacher.

##### **Type**

`str`
