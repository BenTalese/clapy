<h1 align="center">Clapy</h1>

![banner](clapy-banner.png "banner")

<p align="center">
  <img alt="MIT Licence" src="https://img.shields.io/pypi/l/clapy"/>
  <img alt="Current Release" src="https://img.shields.io/pypi/v/clapy"/>
  <img alt="Repo Size" src="https://img.shields.io/github/repo-size/BenTalese/clapy?color=yellow"/>
</p>

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

## Getting Started
### Installation

To install the Clapy package, simply use pip:
```bash
pip install clapy
```

If you also would like to use the built-in dependency injection solution, use this instead:
```bash
pip install clapy[dependency_injector]
```

### Initial Project Setup
W.I.P.

### Invoking Use Cases
W.I.P.

```python
s = "Python syntax highlighting"
print s
```

## Conventions
W.I.P.

## Limitations
As with any software, there are limitations to consider when using Clapy:

1. **Steep learning curve**: Although Clapy is designed to be easy to use once setup is complete, the implementation of clean architecture and dependency injection in any project has a steep learning curve for developers who are new to these concepts.
2. **Async only**: Clapy is built to only support asynchronous programming at this point in time, which of course increases the complexity of the code.
3. **Lack of flexibility**: Clapy provides a rigid structure for building clean architecture applications. This means you will always have a consistent design structure, but it also means it’s not always straightforward to add functionality to your application. There may be some edge cases that don’t fit neatly into this architecture.
4. **Infrastructure setup**: Using Clapy requires you to choose one of two options:

   1. Use the built-in dependency injection solution that wires up to the dependency_injector Python package.
   2. Write your own dependency injection solution by implementing the IServiceProvider interface from Clapy’s services to wire up to a DI framework of your choosing.

5. **Limited community support**: While clean architecture is not new as a concept, it is not very common to see it applied to Python in the way Clapy is designed and therefore there is not a large community of people who can provide assistance with issues.

## Contributing
Thank you for your interest in contributing to Clapy. At this time, we are not accepting contributions or pull requests from external parties. However, we appreciate your feedback and suggestions and we welcome you to open an issue on our GitHub page.

## Licence
Clapy is released under the MIT Licence. See the LICENCE file for more information.