<h1 align="center">Clapy</h1>

<img alt="Banner" src="img/clapy-banner.png"/>
<br/>
<br/>

<p align="center">
  <img alt="MIT Licence" src="https://img.shields.io/pypi/l/clapy"/>
  <img alt="Python Versions" src="https://img.shields.io/pypi/pyversions/clapy"/>
  <img alt="Wheel" src="https://img.shields.io/pypi/wheel/clapy"/>
  <img alt="Current Release" src="https://img.shields.io/pypi/v/clapy"/>
  <img alt="Build and Test" src="https://img.shields.io/github/actions/workflow/status/BenTalese/clapy/build-and-test.yml?branch=ReleaseCandidate"/>
  <img alt="Repo Size" src="https://img.shields.io/github/repo-size/BenTalese/clapy?color=red"/>
  <img alt="Awesomeness" src="https://img.shields.io/badge/Awesomeness-100%25-brightgreen" />
</p>

Standing for **Cl**ean **A**rchitecture **Py**thon, Clapy is a powerful, generic tool designed to provide the perfect solution for constructing and invoking clean architecture use cases in Python. Featuring all the essential building blocks for creating simple to complex use cases, Clapy is adaptable to the needs of any project or business.

**See Clapy in action ➡️ [Discount Dora](https://github.com/BenTalese/DiscountDora) ⬅️**

<br/>

## Features
  * Predefined use case output ports and pipes for typical usage, which can be easily added to.
  * A use case invoker to orchestrate your use cases and help manage your inputs and outputs.
  * A dependency injection solution that works out of the box.
  * Super fast speed by leveraging the power of asynchronous programming with AsyncIO.
  * Highly extensible and customisable design, suitable for a project of any size.

## Why Clapy?
### Introducing the problem
Imagine you are working on a large-scale suite of applications. Maybe there’s a web API, a desktop application and a mobile app. Over time, you add new features and functionality to the codebase to meet the demands of the business. As a result, the codebase grows larger and more complex, with different components tightly coupled and entangled with each other. Eventually, it becomes too difficult to make changes without causing unintended side effects in other areas of the codebase, resulting in bugs and slowdowns in development and overcomplicated testing.

### Clean architecture to the rescue
<img alt="clean architecture diagram" src="https://blog.cleancoder.com/uncle-bob/images/2012-08-13-the-clean-architecture/CleanArchitecture.jpg" height="450px"/>
<br/>
<br/>

Clean architecture, as depicted by the popular diagram above, is a software design pattern that promotes separation of concerns, making it cheaper and more efficient to maintain and extend complex software systems. By clearly defining the responsibilities and boundaries of each component, it becomes easier to make changes and test them in isolation without impacting other areas of the application.

But how do you go about creating applications following the principles of clean architecture? How would you do it in Python?

### This is where Clapy comes in
The goal of Clapy is to provide a modern, modular solution for handling the entire flow of control from the controller to the presenter as shown in the bottom right of the above diagram. With Clapy, you can easily write and invoke use cases, freeing up time and effort to focus on more complex aspects of your project. Whether you're starting a new project or looking to refactor an existing one, Clapy provides an effective way to implement clean architecture in your Python projects.

## Getting Started
### Installation

To install the Clapy package, simply use pip. Note, Clapy requires Python 3.7 or above.
```bash
pip install clapy
```

If you would also like to use the built-in dependency injection solution, use this instead:
```bash
pip install clapy[dependency_injector]
```

### Use Case Construction
#### Input and Output Ports
Before we can use anything from Clapy, we need a use case to invoke. Firstly, a use case is going to need its inputs and potential outputs. In Clapy, the inputs of a use case are defined on the use case's "input port", which will inherit the `InputPort` class. The outputs are defined on an interface called the "output port". This is done deliberately so that the consumer of the use case can decide what to do depending on the use case behaviour. It's also clear to the consumer exactly what could happen upon invoking a use case, rather than having to deal with exceptions. All together, it might look something like this:

```python
class ExampleInputPort(InputPort):
    message: str


class IExampleOutputPort(IOutputPort, ABC):

    @abstractmethod
    async def present_message_async(self, message: str) -> None:
        pass
```

#### Input Validation
Clapy supports Pydantic-like validation of inputs via type hints and default value assignment with the `InputTypeValidator` and `RequiredInputValidator`. This allows you to restrict and validate inputs provided to a use case without an exception being thrown like you would get with Pydantic or a constructor.

  * Specifying a type hint enforces the value assigned to that input to be the same type as (or a subclass of) the type hint.
  * Specifying no type hint means type validation is skipped for that input.
  * Not assigning a default value means the input is required and must be provided a value.
  * Assigning a default value means the input is optional.
  * Type validation and required inputs can be turned on by including the `InputTypeValidator` and/or the `RequiredInputValidator` pipes in your configuration. You must also have `IValidationOutputPort` inherited on your output port.

#### Generic Outputs
A use case will always have its specific outputs, but it can be good to define generic outputs across use cases. This comes in handy when you want categories of outputs to be consistent across use cases so you can deal with them easily in your presenters. You can of course define as many of your own as you want, but Clapy does provide some output ports for you to use by default:

  * `IAuthenticationOutputPort`
  * `IAuthorisationOutputPort`
  * `IValidationOutputPort`

We can inherit these generic output ports on our use case's output port so that the presenter knows to deal with that type of output. This would be done like so:

```python
class IExampleOutputPort(IOutputPort, IValidationOutputPort, ABC):

    @abstractmethod
    async def present_message_async(self, message: str) -> None:
        pass
```

#### Introduction to Pipes
Every use case is going to have varying requirements, meaning they can be vastly different. But what if we could group certain behaviour/requirements together and identify commonalities between the use cases? Let's call these "pipes", where a "pipe" may be something generic to represent a common step in a use case such as authorisation. All of these pipes of a use case come together to create the "pipeline" to be invoked, and this pipeline can contain as few or as many pipes as required by the use case.

To represent this, Clapy defines the `IPipe` interface which defines at its root, a "pipe" must have a way to "execute" its behaviour, and a way to report "failures". Clapy also defines a set of default pipes which implement the `IPipe` interface to represent common types of pipes you may have in your use cases. This is useful for defining and configuring your pipes in a generic way so that your configuration will apply across many use cases. These provided pipes are:

  * `AuthenticationVerifier`
  * `AuthorisationEnforcer`
  * `EntityExistenceChecker`
  * `InputPortValidator`
  * `InputTypeValidator`
  * `Interactor`
  * `PersistenceRuleValidator`
  * `RequiredInputValidator`

Note, the only pipes with a default implementation here are the `InputTypeValidator` and `RequiredInputValidator`. They are special pipes that can either be set up as a blank pipe in your use case (the inherited pipe type will handle the work), or you can configure them to be inserted into the pipeline upon pipeline construction.

#### Creating a Use Case Pipe
Using these classes as our "pipe types/categories", we can then construct specific pipes for our use cases. The `UseCaseInvoker` will invoke the `execute_async` method of each pipe in the defined order until it reaches the last pipe, or if one of the pipes reports it has errors. This is overridable for cases such as wanting to get the errors of a set of pipes before stopping the pipeline. Here is an example input port validator pipe:

```python
class ExampleInputPortValidator(InputPortValidator):

    async def execute_async(self, input_port: ExampleInputPort, output_port: IExampleOutputPort) -> None:
        if input_port.message != "Hello world!":
            _Failure = ValidationResult.from_error(input_port, 'message', "Message was not 'Hello world!' 😔")
            self.has_failures = True
            await output_port.present_validation_failure_async(_Failure)
```

Some important points to be aware of with Clapy:

  * You do not need to use any of the pre-defined pipe category classes. You could instead create as many of your own as you require, and they do not need to be applied to every use case. The default categories are just there for convenience/as suggestions.
  * Clapy does not strictly require a use case's pipe to inherit a pipe category, the pipe category is just a convenient means of setting a reliable ordering and structure for use cases to follow. It also allows you to set default behaviour if you wish to do so.
  * Clapy does require every use case pipe to implement the `IPipe` interface, either directly or through a pipe category class the pipe inherits from, otherwise Clapy will not recognise the use case pipe.
  * If a failure occurs such as a resource was not found, or a business rule was violated, you should always let the `UseCaseInvoker` know this by setting the `has_failures` flag on the pipe.

### Dependency Injection Setup
#### Implementing IServiceProvider
After creating a use case, it's time to configure Clapy within your application. The first step is to create an instance of your chosen implementation of Clapy's `IServiceProvider` interface. This is what allows Clapy to talk to any dependency injection framework. You can do this via two options:

  * Option 1: Use the built-in `DependencyInjectorServiceProvider` class which hooks up to the `dependency_injector` package. Note this does require you to install `dependency_injector` separately or install `clapy[dependency_injector]`.
  * Option 2: Create your own implementation of `IServiceProvider` that hooks up to a dependency injection framework of your choosing.

#### Registering Services
With your service provider, you then need to register your services to the DI container. Note, from here on it is assumed you are using `DependencyInjectorServiceProvider` from Clapy. This class contains methods to help register your services.

```python
_ServiceProvider = DependencyInjectorServiceProvider()

_ServiceProvider.register_service(providers.Factory, ExampleImplementation, IExampleInterface)

_ServiceProvider.register_service(providers.Factory, AnotherExample)
```

#### Registering the UseCaseInvoker and its Dependencies
Once you have finished registering your services, you need to also:
  * Create the use case registry
  * Register the pipes of your use cases
  * Register the `PipelineFactory`
  * Register the `UseCaseInvoker`

Clapy's `DependencyInjectorServiceProvider` contains methods to help automate this task:

```python
# You can have as many or as few locations as needed...
_UsecaseScanLocations = ["application/use_cases", "some/other/location"]

_ServiceProvider.configure_clapy_services(_UsecaseScanLocations)
```

### Configuring a Pipeline
In [Introduction to Pipes](#introduction-to-pipes), we introduced the concept of a "pipe", and together these pipes make a "pipeline". Clapy allows you to configure the pipeline by providing the `UseCaseInvoker` with a list of `PipeConfiguration` when invoking a use case. This allows you to define:
  * Which pipes should be included in the pipeline
  * How the pipes will be included in the pipeline
  * The order the pipes should be in
  * Whether or not failures from a pipe should be ignored
  * Any pre/post actions to be performed for each pipe (note: these must be asynchronous functions)

With this flexibility, we are able to create specific pipelines for specific usages of our use cases. For example, we can have a default pipeline that invokes all pipes found in the use case, and another pipeline that only includes validation to check whether or not we can invoke a use case without actually performing the action. Here's an example of how we might organise this:

```python
class PipelineConfiguration(Enum):

    DefaultConfiguration = [
        PipeConfiguration(AuthenticationVerifier),
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT),
        PipeConfiguration(AuthorisationEnforcer, should_ignore_failures=True),
        PipeConfiguration(EntityExistenceChecker),
        PipeConfiguration(InputPortValidator),
        PipeConfiguration(Interactor, post_action=report_time("Finish time is: "))
    ]

    ValidationOnlyConfiguration = [
        PipeConfiguration(RequiredInputValidator, PipeConfigurationOption.INSERT, True),
        PipeConfiguration(AuthorisationEnforcer, should_ignore_failures=True),
        PipeConfiguration(EntityExistenceChecker, should_ignore_failures=True),
        PipeConfiguration(InputPortValidator)
    ]
```

### Invoking Use Cases
Now that we've created our use case and we've wired up Clapy, it's time to finally invoke our use case! We do this by getting the `IUseCaseInvoker` service from the DI container, creating an "input port" and a "presenter" that implements our use case's output port, then we call the `invoke_usecase_async` method.

```python
# An example presenter that implements our use case's output port...
class ExamplePresenter(IExampleOutputPort, IValidationOutputPort):

  async def present_message_async(self, message: str) -> None:
    print(f"Wow it worked, see!!  :  {message}")

  async def present_validation_failure_async(self, validation_failure: ValidationFailure) -> None:
    print(validation_failure)


async def main():

  # Other code...

  _UseCaseInvoker = _ServiceProvider.get_service(IUseCaseInvoker)

  await _UseCaseInvoker.invoke_usecase_async(ExampleInputPort("Hello world!"), ExamplePresenter())

  # Other code...

asyncio.run(main())
```

Assuming we have a pipe to return the `present_message_async` coroutine, we could expect a result like so:

```console
Wow it worked, see!!  :  Hello world!
```

Now let's say we intentionally passed in an invalid input:

```python
await _UseCaseInvoker.invoke_usecase_async(ExampleInputPort("Do as I say, not as I do!"), ExamplePresenter())
```

We could then expect from this the result from the `ExampleInputPortValidator`:

```console
{'errors': {'message': ["Message was not 'Hello world!'."]}, 'summary': None}
```

Which concludes the basics of using Clapy. This is simply a snippet of what you could do with Clapy and clean architecture use cases. Go forth and be clean!

## Limitations & Considerations
As with any software, there are limitations to consider when using Clapy:

  1. **Steep learning curve**: Although Clapy is designed to be easy to use once setup is complete, the implementation of clean architecture and dependency injection in any project has a steep learning curve for developers who are new to these concepts.
  2. **Async only**: Clapy is built to only support asynchronous programming currently, which increases the complexity of the code.
  3. **Reliance on type hints**: Both the engine of Clapy and the built-in DI solution rely on type hints being provided for all parameters so their types can be checked.
  4. **Complex design considerations**: While crafting your use cases, you must be careful to consider what your framework is going to do with them. For example, an MVC web API will have completely different requirements to a bulk synchronisation processor, and again to an MVVM desktop application. While the use case may not be affected much, the onflow affect of how it is utilised in the framework will need considerable thought put into it.
  5. **Limited community support**: While clean architecture is not new as a concept, it is not very common to see it applied to Python in the way Clapy is designed and therefore there is not a large community of people who can provide assistance with issues.


## Licence
Clapy is released under the MIT Licence. See the LICENCE file for more information.
