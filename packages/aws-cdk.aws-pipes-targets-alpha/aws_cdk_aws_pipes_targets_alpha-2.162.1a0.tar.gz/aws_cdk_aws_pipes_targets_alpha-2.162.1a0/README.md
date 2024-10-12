# Amazon EventBridge Pipes Targets Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

EventBridge Pipes Targets let you create a target for a EventBridge Pipe.

For more details see the service documentation:

[Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html)

## Targets

Pipe targets are the end point of a EventBridge Pipe.

The following targets are supported:

1. `targets.SqsTarget`: [Send event source to an SQS queue](#amazon-sqs)
2. `targets.SfnStateMachine`: [Invoke a State Machine from an event source](#aws-step-functions-state-machine)
3. `targets.LambdaFunction`: [Send event source to a Lambda function](#aws-lambda-function)
4. `targets.ApiDestinationTarget`: [Send event source to an EventBridge API destination](#amazon-eventbridge-api-destination)
5. `targets.KinesisTarget`: [Send event source to a Kinesis data stream](#amazon-kinesis-data-stream)
6. `targets.EventBridgeTarget`: [Send event source to an EventBridge event bus](#amazon-eventbridge-event-bus)

### Amazon SQS

A SQS message queue can be used as a target for a pipe. Messages will be pushed to the queue.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The target input can be transformed:

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue,
    input_transformation=pipes.InputTransformation.from_object({
        "SomeKey": pipes.DynamicInput.from_event_path("$.body")
    })
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### AWS Step Functions State Machine

A State Machine can be used as a target for a pipe. The State Machine will be invoked with the (enriched) source payload.

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

Specifying the Invocation Type when the target State Machine is invoked:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The input to the target State Machine can be transformed:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    input_transformation=pipes.InputTransformation.from_object({"body": "<$.body>"}),
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### AWS Lambda Function

A Lambda Function can be used as a target for a pipe. The Lambda Function will be invoked with the (enriched) source payload.

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The target Lambda Function is invoked synchronously by default. You can also choose to invoke the Lambda Function asynchronously by setting `invocationType` property to `FIRE_AND_FORGET`.

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function,
    invocation_type=targets.LambdaFunctionInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The input to the target Lambda Function can be transformed:

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### Amazon EventBridge API Destination

An EventBridge API destination can be used as a target for a pipe.
The API destination will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# dest: events.ApiDestination


api_target = targets.ApiDestinationTarget(dest)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

The input to the target API destination can be transformed:

```python
# source_queue: sqs.Queue
# dest: events.ApiDestination


api_target = targets.ApiDestinationTarget(dest,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

### Amazon Kinesis Data Stream

A data stream can be used as a target for a pipe. The data stream will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_stream: kinesis.Stream


stream_target = targets.KinesisTarget(target_stream,
    partition_key="pk"
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=stream_target
)
```

The input to the target data stream can be transformed:

```python
# source_queue: sqs.Queue
# target_stream: kinesis.Stream


stream_target = targets.KinesisTarget(target_stream,
    partition_key="pk",
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=stream_target
)
```

### Amazon EventBridge Event Bus

An event bus can be used as a target for a pipe. The event bus will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_event_bus: events.EventBus


event_bus_target = targets.EventBridgeTarget(target_event_bus)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=event_bus_target
)
```

The input to the target event bus can be transformed:

```python
# source_queue: sqs.Queue
# target_event_bus: events.EventBus


event_bus_target = targets.EventBridgeTarget(target_event_bus,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=event_bus_target
)
```
