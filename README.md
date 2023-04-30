# Clapy
Standing for **Cl**ean **A**rchitecture **Py**thon, Clapy is a powerful, generic tool designed to provide the perfect solution for constructing and invoking clean architecture use cases in Python. Featuring all the essential building blocks for creating simple to complex use cases, Clapy is adaptable to the needs of any project or business.

## Features
  * Predefined use case output ports and pipes for typical usage, which can be easily added to.
  * A use case invoker to orchestrate your use cases and help manage your inputs and outputs.
  * A dependency injection container solution that works out of the box.
  * Automatic scanning of use case pipes within your project.
  * Super fast speed by leveraging the power of asynchronous programming with AsyncIO
  * Highly extensible and customisable design, suitable for a project of any size, or even a suite of projects.

## Why Clapy?
### Introducing the problem
Imagine you are working on a large-scale suite of applications. Maybe there’s a web API, a desktop application and a mobile app. Over time, you add new features and functionality to the codebase to meet the demands of the business. As a result, the codebase grows larger and more complex, with different components tightly coupled and entangled with each other. Eventually, it becomes too difficult to make changes without causing unintended side effects in other areas of the codebase, resulting in bugs and slowdowns in development and overcomplicated testing.

### Clean architecture to the rescue
![clean architecture diagram](https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg "clean architecture diagram")

Clean architecture, as defined by the popular diagram above, is a software design pattern that promotes separation of concerns, making it cheaper and more efficient to maintain and extend complex software systems. By clearly defining the responsibilities and boundaries of each component, it becomes easier to make changes and test them in isolation without impacting other areas of the application. 

But how do you go about creating applications following the principles of clean architecture? How would you do it in Python?

### This is where Clapy comes in
The goal of Clapy is to provide a modern, modular solution for handling the entire flow of control between the controller and the presenter as shown in the above diagram. With Clapy, you can easily write and invoke use cases, freeing up time and effort to focus on more complex aspects of your project. Whether you're starting a new project or looking to refactor an existing one, Clapy provides an effective way to implement clean architecture in your Python projects.

```python
s = "Python syntax highlighting"
print s
```


CONVENTIONS
