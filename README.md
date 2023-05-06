<h1 align="center">Clapy</h1>

<img alt="Banner" src="img/clapy-banner.png"/>
<br/>
<br/>

<p align="center">
  <img alt="MIT Licence" src="https://img.shields.io/pypi/l/clapy"/>
  <img alt="Current Release" src="https://img.shields.io/pypi/v/clapy"/>
  <img alt="Current Release" src="https://img.shields.io/github/actions/workflow/status/BenTalese/clapy/build-and-test.yml?branch=ReleaseCandidate"/>
  <img alt="Repo Size" src="https://img.shields.io/github/repo-size/BenTalese/clapy?color=red"/>
  <img alt="Awesomeness" src="https://img.shields.io/badge/Awesomeness-100%25-brightgreen" />
</p>

Standing for **Cl**ean **A**rchitecture **Py**thon, Clapy is a powerful, generic tool designed to provide the perfect solution for constructing and invoking clean architecture use cases in Python. Featuring all the essential building blocks for creating simple to complex use cases, Clapy is adaptable to the needs of any project or business.

See Clapy in action: <W.I.P.>

## Features
  * Predefined use case output ports and pipes for typical usage, which can be easily added to.
  * A use case invoker to orchestrate your use cases and help manage your inputs and outputs.
  * A dependency injection container solution that works out of the box.
  * Automatic scanning of use case pipes within your project.
  * Super fast speed by leveraging the power of asynchronous programming with AsyncIO.
  * Highly extensible and customisable design, suitable for a project of any size, or even a suite of projects.

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

To install the Clapy package, simply use pip:
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

    def __init__(self, message: str):
        self.message = message

class IExampleOutputPort(ABC):
    
    @abstractmethod
    async def present_message_async(self, message: str) -> None:
        pass
```

#### Generic Outputs
A use case will always have its specific outputs, but it can be good to define generic outputs across use cases. This comes in handy when you want categories of outputs to be consistent across use cases so you can deal with them easily in your presenters. You can of course define as many of your own as you want, but Clapy does provide some output ports for you to use by default:

  * `IAuthenticationOutputPort`
  * `IAuthorisationOutputPort`
  * `IValidationOutputPort`

We can inherit these generic output ports on our use case's output port so that the presenter knows to deal with that type of output. This would be done like so:

```python
class IExampleOutputPort(IValidationOutputPort, ABC):
    
    @abstractmethod
    async def present_message_async(self, message: str) -> None:
        pass
```

#### Introduction to Pipes
Every use case is going to have varying requirements, meaning they can be vastly different. But what if we could group certain behaviour/requirements together and identify commonalities between the use cases? Let's call these "pipes", where a "pipe" may be something generic to represent a common step in a use case such as authorisation. All of these pipes of a use case come together to create the "pipeline" to be invoked, and this pipeline can contain as few or as many pipes as required by the use case.

To represent this, Clapy defines the `IPipe` interface which defines at its root, a "pipe" must have a "priority" and a way to "execute" its behaviour. Clapy also defines a set of default pipes which implement the `IPipe` interface to represent common types of pipes you may have in your use cases. This is useful for defining the priority of pipes in a generic way. These provided pipes are:

  * `AuthenticationVerifier`
  * `AuthorisationEnforcer`
  * `BusinessRuleValidator`
  * `EntityExistenceChecker`
  * `InputPortValidator`
  * `Interactor`

#### Creating a Use Case Pipe
Using these classes as our "pipe types/categories", we can then construct specific pipes for our use cases. It's worth mentioning that Clapy's `UseCaseInvoker` is going to expect a result from each pipe after its execution method is called. This result must be either a `Coroutine` (a method of the use case's output port), or `None`. Once the `UseCaseInvoker` has received a `Coroutine` result from a pipe, it stops the execution of the pipeline and executes the resulting action it received from the use case. Here is an example input port validator pipe:

```python
class ExampleInputPortValidator(InputPortValidator[ExampleInputPort, IExampleOutputPort]):

    def execute_async(self, input_port: ExampleInputPort, output_port: IExampleOutputPort) -> Coroutine | None:
        _Failures = []

        if input_port.message != "Hello world!":
            _Failures.append("Message was not 'Hello world!'.")
            return output_port.present_validation_failure_async(_Failures)
```

Some important points to be aware of with Clapy:

  * You do not need to use any of the pre-defined pipe category classes. You could instead create as many of your own as you require, and they do not need to be applied to every use case. The default categories are just there for convenience/as suggestions.
  * Clapy does not strictly require a use case's pipe to inherit a pipe category, the pipe category is just a convenient means of setting a reliable ordering and structure for use cases to follow.
  * Clapy does require every use case pipe to implement the `IPipe` interface, either directly or through a pipe category class the pipe inherits from, otherwise Clapy will not recognise the use case pipe.
  * A pipe **must** either return a `Coroutine`, or `None` as a result of its execution.

### Dependency Injection Setup
#### Implementing IServiceProvider
After creating a use case, it's time to configure Clapy within your application. The first step is to create an instance of your chosen implementation of Clapy's `IServiceProvider` interface. This is what allows Clapy to talk to any dependency injection framework. You can do this via two options:

  * Option 1: Use the built-in `DependencyInjectorServiceProvider` class which hooks up to the `dependency_injector` package. Note this does require you to install `dependency_injector` separately or install `clapy[dependency_injector]`.
  * Option 2: Create your own implementation of `IServiceProvider` that hooks up to a dependency injection framework of your choosing.

#### Registering Services
With your service provider, you then need to register your services to the DI container. Note, from here on it is assumed you are using `DependencyInjectorServiceProvider` from Clapy. This class contains methods to register your services.

```python
_ServiceProvider = DependencyInjectorServiceProvider()

_ServiceProvider.register_service(providers.Factory, ExampleImplementation, IExampleInterface)

_ServiceProvider.register_service(providers.Factory, AnotherExample)
```

#### Registering The UseCaseInvoker and its Dependencies
Once you have finished registering your services, you need to also:
  * Create the use case registry
  * Register the pipes of your use cases
  * Register the `PipelineFactory`
  * Register the `UseCaseInvoker`

Clapy's `DependencyInjectorServiceProvider` contains methods to help automate this task:

```python
# You can have as many or as few locations as needed...
_UsecaseScanLocations = ["application/usecases", "some/other/location"]

_UsecaseRegistry = construct_usecase_registry(_UsecaseScanLocations)
_ServiceProvider.register_usecase_services(_UsecaseScanLocations)
_ServiceProvider.register_service(providers.Singleton, PipelineFactory, IPipelineFactory, _ServiceProvider, _UsecaseRegistry)
_ServiceProvider.register_service(providers.Factory, UseCaseInvoker, IUseCaseInvoker)
```

### Setting the Priority of Your Use Case Pipes
In [Introduction to Pipes](#introduction-to-pipes), we introduced the concept of a "pipe" where it must have a "priority". The way this works in practice is we define the priority property of the pipe using the `PipePriority` class. We don't directly assign the priority here, but we reference the attribute name to access the pipe's priority by.

```python
class Interactor(IPipe, Generic[TInputPort, TOutputPort]):
    '''Marks a class as an interactor pipe.'''
    @property
    def priority(self) -> PipePriority:
        return PipePriority.Interactor
```

Notice how Clapy is defining the priority on the interactor pipe type rather than specific interactors? By doing this we can control the ordering of our pipes efficiently, and therefore only leaving the execution behaviour to be defined in the specific use case pipe.

Once our pipes have a priority defined (or inherit a pipe type which has its priority defined) as an attribute on the `PipePriority` class, we can finally set the actual ordering of the pipes. This is done by assigning a value to the attributes via the `set_pipe_priority` method provided by Clapy.

```python
  set_pipe_priority({
          f'{AuthenticationVerifier.__name__}': 1,
          f'{EntityExistenceChecker.__name__}': 2,
          f'{AuthorisationEnforcer.__name__}': 3,
          f'{BusinessRuleValidator.__name__}': 4,
          f'{InputPortValidator.__name__}': 5,
          f'{Interactor.__name__}': 6
      })
```

For this example we are defining the order of Clapy's default pipe categories. Points to learn how this works in practice:

  * These attributes are created and added to the class at runtime through this method.
  * You cannot have two different pipes assigned the same priority within the PipePriority class.
  * The priority forms a queue, where smaller numbers are earlier in the pipeline and larger numbers are later.
  * You only have to assign a priority for the pipes you are using within your use cases.
  * You can define your own pipes and assign their order here instead of Clapy's default pipes.

### Invoking Use Cases
Now that we've created our use case and we've wired up Clapy, it's time to finally invoke our use case! We do this by getting the `IUseCaseInvoker` service from the DI container, creating an "input port" and a "presenter" that implements our use case's output port, then calling `invoke_usecase_async` within our main asynchronous event loop.


```python
# An example presenter that implements our use case's output port...
class ExamplePresenter(IExampleOutputPort, IValidationOutputPort):

  async def present_message_async(self, message: str) -> None:
    print(f"Wow it worked, see!!  :  {message}")
  
  async def present_validation_failure_async(self, validation_failure: TValidationFailure) -> None:
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
["Message was not 'Hello world!'."]
```

Which concludes the basics of using Clapy. This is simply a snippet of what you could do with Clapy and clean architecture use cases. Go forth and be clean!

## Conventions, Rules & Restrictions
<W.I.P.>

Clapy was built with a general project structure in mind... some may or may not work outside of these assumptions that were made

* One DI class per file (scanning)
* One pipe per file? Might be separate issue to above for registry
* Same naming of class/module
* Use case in its own folder (for registry name) #TODO: should it be the input port? if input port found in folder?... might be dumb
* Services are registered in the correct order (dependency graph...whatever the name for it is...look at uni materials)
* Some of these may only apply if using the `DependencyInjectorServiceProvider` class
* Dependencies of a service (especially pipes) can only be resolved via type hints with the current design

## Limitations & Considerations
As with any software, there are limitations to consider when using Clapy:

  1. **Steep learning curve**: Although Clapy is designed to be easy to use once setup is complete, the implementation of clean architecture and dependency injection in any project has a steep learning curve for developers who are new to these concepts.
  2. **Async only**: Clapy is built to only support asynchronous programming currently, which increases the complexity of the code.
  3. **Lack of flexibility**: Clapy provides a rigid structure for building clean architecture applications. This means you will always have a consistent design structure, but it also means it’s not always straightforward to add functionality to your application. There may be some edge cases that don’t fit neatly into this architecture.
  4. **Complex design considerations**: While crafting your use cases, you must be careful to consider what your framework is going to do with them. For example, an MVC web API will have completely different requirements to a bulk synchronisation processor, and again to an MVVM desktop application. While the use case may not be affected much, the onflow affect of how it is utilised in the framework will need considerable thought put into it.
  5. **Limited community support**: While clean architecture is not new as a concept, it is not very common to see it applied to Python in the way Clapy is designed and therefore there is not a large community of people who can provide assistance with issues.

## Contributing
Thank you for your interest in contributing to Clapy. At this time, we are not accepting contributions or pull requests from external parties. However, we appreciate your feedback and we welcome you to open an issue on our GitHub page.

## Licence
Clapy is released under the MIT Licence. See the LICENCE file for more information.
