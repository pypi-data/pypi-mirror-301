import asyncio
import inspect
import os
import struct
import threading
from queue import Queue, Empty
from typing import Awaitable, Optional, Dict, List, Callable, Tuple, Union, Set

import zmq.asyncio
from nanoid import generate

from carasdk.utils import parse_yaml
from carasdk.ipc_pb2 import IPCCommand, IPCMessage, RegisterHandlerRequest, RegisterServiceRequest, Request, Response, Event
from carasdk.log_config import setup_logger

HUMANIFY_INSTANCE_ID_ENV_VAR = "HUMANIFY_INSTANCE_ID"

logger = setup_logger('IpcSdk')


def get_instance_id():
    if HUMANIFY_INSTANCE_ID_ENV_VAR in os.environ:
        return os.environ[HUMANIFY_INSTANCE_ID_ENV_VAR]
    else:
        logger.error("No instance ID found in environment variables")
        raise Exception("No instance ID found")


def set_instance_id(instance_id):
    os.environ[HUMANIFY_INSTANCE_ID_ENV_VAR] = instance_id


# Type of handlers (event_name, handler[])
HandlerType = Union[Callable[[bytes], bytes],
                    Callable[[bytes], Awaitable[bytes]]]

EventHandlerType = Union[Callable[[bytes], None],
                         Callable[[bytes], Awaitable[None]]]


class IpcSdk:
    def __init__(self, host='localhost', port=5555, package_path='package.yaml'):
        # Read package.yaml file in the current directory
        self.services = {}
        if package_path and os.path.exists(package_path):
            package = parse_yaml(package_path)
            self.services = package['service']
            set_instance_id(package['id'])
            logger.info(package)
        self.port = port
        context = zmq.asyncio.Context()
        self.socket = context.socket(zmq.DEALER)
        # setsockopt
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RECONNECT_IVL, 1000)
        self.socket.setsockopt(zmq.RECONNECT_IVL_MAX, 5000)
        self.socket.monitor("inproc://monitor", zmq.EVENT_ALL)

        self.monitor_socket = context.socket(zmq.PAIR)
        self.monitor_socket.connect("inproc://monitor")

        self.socket.connect(f"tcp://{host}:{port}")
        logger.info(f"Connected to ZMQ socket on port {port}")
        self.response_queues = {}
        self.handlers: Dict[Tuple[str, str], List[HandlerType]] = {}
        self.event_handlers: Dict[Tuple[str, str],
                                  List[Tuple[EventHandlerType, bool]]] = {}
        self.registered_services: Set[Tuple[str, str, str]] = set()
        self.registered_handlers: Set[Tuple[str, str]] = set()

        threading.Thread(target=self.run_async_function_in_thread).start()
        asyncio.create_task(self.monitor())

        try:
            from global_sdk import set_ipc
            set_ipc(self)
        except ImportError:
            pass
        try:
            from carasdk.global_sdk import set_ipc
            set_ipc(self)
        except ImportError:
            pass
        logger.info("IpcSdk initialized, started message loop")
        asyncio.create_task(self.register_services())

    async def handle_monitor_event(self, event_id, event_value, address):
        if event_id == zmq.EVENT_CONNECT_RETRIED:
            logger.info(f"Reconnecting to {address}")
            # Reconnect to the socket
        elif event_id == zmq.EVENT_CONNECTED:
            logger.info(f"Connected to {address}, re-registering services and handlers")
            await self.reregister_services_and_handlers()
        else:
            logger.info(f"Event {event_id} from {address}")

    async def monitor(self):
        def parse_zmq_event(event: bytes):
            # Parse the event
            event_id, event_value = struct.unpack('=HI', event[:6])
            return event_id, event_value

        while True:
            event = await self.monitor_socket.recv_multipart()
            event_id, event_value = parse_zmq_event(event[0])
            address = event[1].decode()
            await self.handle_monitor_event(event_id, event_value, address)

    async def reregister_services_and_handlers(self):
        logger.info("Re-registering services")
        for service_name, action, category in self.registered_services:
            await self.register_service(service_name, action, category, store=False)

        logger.info("Re-registering handlers")
        for event_name, category in self.registered_handlers:
            await self.register_handler(event_name, category, store=False)

    async def end(self):
        await self.loop_task.cancel()

    def run_async_function_in_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.loop())
        loop.close()

    async def register_services(self):
        # Iterate through each service in self.services
        if not self.services:
            return
        for service_name, service_info in self.services.items():
            # Get the entry and action list
            actions = service_info['action']

            # Iterate through each action, calling register_conn separately
            for action in actions:
                # Split action into action and category
                action_part, category_part = action.split(',')

                # Call register_conn
                await self.register_service(service_name, action_part, category_part)

    async def register_service(self, service_name: str, action: str, category: str = "DEFAULT", store=True):
        instance_id = get_instance_id()
        if not instance_id:
            raise ValueError("Instance ID not found")

        register_request = RegisterServiceRequest()
        register_request.instance_id = instance_id
        register_request.service_name = service_name
        register_request.action = action
        register_request.category = category

        ipc_message = IPCMessage()
        ipc_message.command = IPCCommand.IPC_COMMAND_REGISTER_SERVICE
        ipc_message.content = register_request.SerializeToString()

        message = ipc_message.SerializeToString()

        logger.debug(f"Registering service: service_name={service_name}, action={action}, category={category}")
        await self.socket.send(message)

        if store:
            self.registered_services.add((service_name, action, category))

    async def register_handler(self, event_name: str, category: str = "DEFAULT", store=True):
        instance_id = get_instance_id()
        if not instance_id:
            raise ValueError("Instance ID not found")

        register_request = RegisterHandlerRequest()
        register_request.instance_id = instance_id
        register_request.event = event_name
        register_request.category = category

        ipc_message = IPCMessage()
        ipc_message.command = IPCCommand.IPC_COMMAND_REGISTER_HANDLER
        ipc_message.content = register_request.SerializeToString()

        message = ipc_message.SerializeToString()

        logger.debug(f"Registering handler: event={event_name}, category={category}")
        await self.socket.send(message)

        if store:
            self.registered_handlers.add((event_name, category))

    async def on(self, action: str, handler: HandlerType, category: str = "DEFAULT"):
        key = (action, category)
        if key not in self.handlers:
            self.handlers[key] = []
        self.handlers[key].append(handler)

    async def off(self, action: str, handler: HandlerType, category: str = "DEFAULT"):
        key = (action, category)
        if key in self.handlers:
            del self.handlers[key]

    async def on_event(self, event_name: str, handler: EventHandlerType, category: str = "DEFAULT", once: bool = False):
        key = (event_name, category)
        if key not in self.event_handlers:
            self.event_handlers[key] = []
        self.event_handlers[key].append((handler, once))

    async def off_event(self, event_name: str, handler: HandlerType, category: str = "DEFAULT"):
        key = (event_name, category)
        if key in self.event_handlers:
            self.event_handlers[key] = [
                (h, o) for h, o in self.event_handlers[key] if h != handler]
            if not self.event_handlers[key]:
                del self.event_handlers[key]

    async def send_request(self, instance_id, action, category, data=None, args=None, response_timeout=30) -> Optional[Response]:
        request = Request()
        request.request_id = str(generate())
        request.instance_id = instance_id
        request.action = action
        request.category = category

        if data:
            if isinstance(data, str):
                data = data.encode('utf-8')
            request.data = data

        if args:
            request.args = args

        ipc_message = IPCMessage()
        ipc_message.command = IPCCommand.IPC_COMMAND_REQUEST
        ipc_message.content = request.SerializeToString()

        message = ipc_message.SerializeToString()

        logger.debug(
            f"Sending request to instance_id={instance_id}, action={action}, category={category}, request_id={request.request_id}"
        )

        await self.socket.send(message)

        if response_timeout:
            queue = Queue()
            self.response_queues[request.request_id] = queue
            logger.debug(
                f"Created response queue for request {request.request_id}"
            )

            def wait_for_response():
                try:
                    response = queue.get(timeout=response_timeout)
                    logger.debug(
                        f"Received response for request {request.request_id} within timeout"
                    )
                    return response
                except Empty:
                    logger.warning(
                        f"Timeout waiting for response to request {request.request_id}. Request info: instance_id={instance_id}, action={action}, category={category}, data={data}, args={args}"
                    )
                    # Raise error
                    raise TimeoutError(
                        f"Timeout waiting for response to request {request.request_id}"
                    )

            logger.debug(
                f"Waiting for response to request {request.request_id}, timeout is {response_timeout} seconds"
            )
            response = await asyncio.get_event_loop().run_in_executor(None, wait_for_response)
            del self.response_queues[request.request_id]
            logger.debug(
                f"Removed response queue for request {request.request_id}"
            )
            return response

    async def emit_event(self, event_name: str, category: str = "DEFAULT", data=None, args=None):
        event = Event()
        event.event = event_name
        event.category = category
        event.data = data
        if args:
            event.args = args

        ipc_message = IPCMessage()
        ipc_message.command = IPCCommand.IPC_COMMAND_EVENT
        ipc_message.content = event.SerializeToString()

        message = ipc_message.SerializeToString()

        await self.socket.send(message)

    async def loop(self):
        logger.info("Starting main message loop")
        while True:
            message = await self.socket.recv()
            asyncio.create_task(self.handle_message(message))

    async def handle_message(self, message):
        ipc_message = IPCMessage()
        ipc_message.ParseFromString(message)
        if len(ipc_message.content) < 100:
            logger.debug(f"Received message: {ipc_message}")

        if ipc_message.command == IPCCommand.IPC_COMMAND_REQUEST:
            request = Request()
            request.ParseFromString(ipc_message.content)
            logger.debug(
                f"Handling REQUEST: ID={request.request_id}, Action={request.action}, Category={request.category}")

            key = (request.action, request.category)
            if key in self.handlers:
                for handler in self.handlers[key]:
                    await self.handle_process_request(handler, request.request_id, request.data)

        if ipc_message.command == IPCCommand.IPC_COMMAND_RESPONSE:
            response = Response()
            response.ParseFromString(ipc_message.content)
            logger.debug(
                f"Received RESPONSE for request {response.request_id}")

            if response.request_id in self.response_queues:
                logger.debug(
                    f"Putting response for request {response.request_id} into queue")
                self.response_queues[response.request_id].put(response)
            else:
                logger.debug(
                    f"Received response for unknown request: {response.request_id}")

        if ipc_message.command == IPCCommand.IPC_COMMAND_EVENT:
            event = Event()
            event.ParseFromString(ipc_message.content)
            logger.debug(
                f"Received EVENT: Name={event.event}, Category={event.category}")

            key = (event.event, event.category)
            if key in self.event_handlers:
                handlers_to_remove = []
                tasks = []
                for handler, once in self.event_handlers[key]:
                    task = asyncio.create_task(
                        self.handle_process_event(handler, event.data))
                    tasks.append(task)
                    if once:
                        handlers_to_remove.append(handler)

                # Execute all handlers concurrently
                await asyncio.gather(*tasks)

                # Remove one-time handlers
                for handler in handlers_to_remove:
                    await self.off_event(event.event, handler, event.category)

    async def handle_process_request(self, handler, request_id, data):
        if handler is None:
            logger.warning("No request handler provided")
            return

        result = None
        if asyncio.iscoroutinefunction(handler):
            result = await handler(data)
        elif inspect.isfunction(handler):
            result = handler(data)
        else:
            try:
                result = handler(data)
            except Exception as e:
                logger.error(f"Error calling request handler: {e}")
            logger.error(f"Invalid handler type: {type(handler)}")

        logger.debug(f"Result: {result}")

        response = Response()
        response.request_id = request_id
        if result:
            response.result = result
        response.is_ok = True

        ipc_message = IPCMessage()
        ipc_message.command = IPCCommand.IPC_COMMAND_RESPONSE
        ipc_message.content = response.SerializeToString()

        message = ipc_message.SerializeToString()

        logger.debug(f"Sending response for request {request_id}")
        await self.socket.send(message)

    async def handle_process_event(self, handler: EventHandlerType, data):
        if handler is None:
            logger.warning("No event handler provided")
            return

        result = None
        if asyncio.iscoroutinefunction(handler):
            await handler(data)
        elif inspect.isfunction(handler):
            handler(data)
        else:
            try:
                handler(data)
            except Exception as e:
                logger.error(f"Error calling event handler: {e}")
            logger.error(f"Invalid handler type: {type(handler)}")