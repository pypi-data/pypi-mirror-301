import inspect
import json
from typing import Callable, get_type_hints, TypedDict, Optional, Any, Dict, NewType, Union

from nanoid import generate

from ipc_sdk import get_instance_id, IpcSdk
from log_config import setup_logger

logger = setup_logger('AgentFramework')


class AgentInfoData(TypedDict):
    instance_id: str
    description: str
    weight: int


class AgentInfo(TypedDict):
    type: str
    name: str
    data: Optional[AgentInfoData]


AgentName = NewType("AgentName", str)


class AgentFramework:
    def __init__(self, agent_name, **kwargs):
        self.agent_name = agent_name
        self.agent_map: Dict[AgentName, Union[Callable, tuple]] = {}
        self.play_output = True 
        logger.info("AgentFramework has started")
        self.ipc = IpcSdk(**kwargs)
        try:
            from global_sdk import set_framework
            set_framework(self)
        except ImportError:
            pass
        try:
            from carasdk.global_sdk import set_framework
            set_framework(self)
        except ImportError:
            pass

    async def start(self):
        from global_sdk import get_ipc
        ipc = get_ipc()
        # Register the request handler for action "MAIN" and category "Agent"
        await ipc.register_service(self.agent_name, "MAIN", "Agent")
        await ipc.on("MAIN", self.request_handler, category="Agent")

    async def end(self):
        from global_sdk import get_ipc
        await get_ipc().end()

    async def register_service(self, action: str, category: str):
        from global_sdk import get_ipc
        await get_ipc().register_service(self.agent_name, action, category)

    async def register_agent(
            self,
            handler: Union[Callable, object],
            prompt: str = "",
            method_name: Optional[str] = None,
            weight=1
    ) -> None:
        """
        Register a new Agent.

        :param weight:
        :param handler: Agent's handling function or object containing the method
        :param description: Description of the Agent
        :param method_name: Method name if handler is an object
        """
        if inspect.ismethod(handler) or inspect.isfunction(handler):
            function = handler
            function_name = handler.__name__
            self.agent_map[function_name] = handler
        elif isinstance(handler, object) and method_name:
            function = getattr(handler, method_name)
            function_name = method_name
            self.agent_map[function_name] = (handler, method_name)
        else:
            raise ValueError("Invalid handler type or missing method_name for object handler")

        # input_spec = self._get_input_spec(function)
        # output_spec = self._get_output_spec(function)

        agent_info: AgentInfo = {
            "type": "register_agent",
            "name": function_name,
            "data": {
                "instance_id": get_instance_id(),
                "description": prompt,
                "weight": weight,
            }
        }
        await self._change_data(agent_info)

    async def _change_data(self, agent_info: AgentInfo) -> None:
        """
        Update Agent data.

        :param agent_info: Agent information
        """
        from global_sdk import get_ipc
        ipc = get_ipc()
        try:
            await ipc.send_request(
                instance_id="org.humanify.agents-manager",
                action="MAIN",
                category="Agent",
                data=json.dumps(agent_info).encode()
            )
            logger.info(f"Tool {agent_info['name']} has been updated")
        except Exception as e:
            logger.error(f"Error occurred while updating tool {agent_info['name']}: {str(e)}")

    async def remove_agent(self, name: str) -> None:
        """
        Remove an Agent.

        :param name: Name of the Agent to be removed
        """
        agent_info: AgentInfo = {
            "type": "remove_agent",
            "name": name,
            "data": None
        }
        self.agent_map.pop(name, None)
        await self._change_data(agent_info)

    def get_play_output(self):
        return self.play_output

    async def request_handler(self, data: bytes) -> Any:
        """
        Handle received requests.

        :param data: Received request data
        :return: Processing result
        """
        try:
            res = json.loads(data.decode('utf-8'))
            _type = res.get("type")
            function_name = res.get("name")
            input_data = res.get("data")
            self.play_output = res.get("play_output", True)
            logger.info(f"Request type: {_type}: {function_name}: {input_data}")

            if _type == "register_agent":
                handler = self.agent_map.get("register_agent")
                response = handler(name=function_name, **input_data)
                logger.info(f"{function_name} Agent registered: {response}")
                return response
            else:
                logger.info(f"{function_name} Agent received request: {res}")
                logger.info(f"{function_name} Agent received input: {input_data}")
                handler = self.agent_map.get(function_name)
                if not handler:
                    raise ValueError(f"Unknown Agent: {function_name}")

                logger.info(f"{handler}")
                if isinstance(handler, tuple):
                    obj, method_name = handler
                    response = await getattr(obj, method_name)()
                else:
                    response = await handler()

                logger.info(f"{function_name} Agent returned: {response}")
                return json.dumps(response).encode()
        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.error(f"Error occurred while processing request: {str(e)}")
            return "Agent error, please try again later".encode()

    async def output_str_chunk(self, message_id: str, chunk: str, print_output=False, play_output=True):
        """
        Output voice string to output service.
        """
        if print_output:
            logger.info(chunk)
        await self.add_ai_message(message_id, chunk)
        if play_output:
            from global_sdk import get_ipc
            await get_ipc().send_request(
                instance_id="org.humanify.output-service",
                action="MAIN",
                category="OutputAudioDataChunk",
                data=chunk.encode()
            )

    async def request_agent(self, instance_id, agent_name: str, play_output: bool):
        from global_sdk import get_ipc
        res = await get_ipc().send_request(
            instance_id=instance_id,
            action="MAIN",
            category="Agent",
            data=json.dumps({
                "type": "request",
                "name": agent_name,
                "play_output": play_output
            }).encode(),
        )
        if res and res.is_ok:
            return res.result
        else:
            logger.error(f"Error occurred while requesting tool {agent_name}: {res.error if res else 'No response'}")
            return None

    @staticmethod
    def _get_input_spec(func: Callable) -> dict:
        hints = get_type_hints(func)
        params = inspect.signature(func).parameters
        properties = {}
        required = []

        for name, param in params.items():
            if name != 'return' and name != 'self':
                type_hint = hints.get(name, Any)
                properties[name] = {"type": getattr(type_hint, '__name__', str(type_hint))}
                if param.default == inspect.Parameter.empty:
                    required.append(name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    @staticmethod
    def _get_output_spec(func: Callable) -> dict:
        hints = get_type_hints(func)
        return_type = hints.get('return', Any)
        return {
            "type": "object",
            "properties": {
                "result": {"type": getattr(return_type, '__name__', str(return_type))}
            }
        }

    async def get_history(self, count: int = 1, response_timeout=10) -> Optional[list]:
        from global_sdk import get_ipc
        res = await get_ipc().send_request(
            instance_id="org.humanify.store",
            action="MAIN",
            category="Store",
            data=json.dumps({
                "type": "get_activate_history",
                "count": count
            }).encode(),
            response_timeout=response_timeout
        )
        logger.info(f"History: {res}")
        if res and res.is_ok:
            data = json.loads(res.result.decode('utf-8'))
            return [(item[0], item[1]) for item in data]
        else:
            logger.error(f"Error occurred while requesting history: {res.error if res else 'No response'}")
            return None

    async def add_ai_message(self, message_id, chunk: str):
        from global_sdk import get_ipc
        await get_ipc().send_request(
            instance_id="org.humanify.store",
            action="MAIN",
            category="Store",
            data=json.dumps({
                "type": "add_ai_message",
                "message_id": message_id,
                "agent_name": self.agent_name,
                "chunk": chunk,
            }).encode(),
        )

    def create_new_message_id(self):
        return generate()

    async def get_agent_list(self) -> list:
        from global_sdk import get_ipc
        res = await get_ipc().send_request(
            instance_id="org.humanify.agents-manager",
            action="MAIN",
            category="Agent",
            data=json.dumps({
                "name": "get_list",
                "data": {}
            }).encode(),
            response_timeout=10
        )
        if res and res.is_ok:
            return json.loads(res.result)
        else:
            logger.error(f"Error occurred while getting Agent list: {res.error if res else 'No response'}")
            return []