import os
import uvloop
import asyncio
import threading
import mimetypes

from .core import HttpServer, HttpRequestFactory, HttpResponse

# Constants
DEFAULT_PORT = 8080
DEFAULT_HOST = "localhost"
AREION_LOGO = """
           >>\\.
          /_  )`.
         /  _)`^)`.   _.---._  
        (_,' \\  `^-)""      `.\\
              |           | \\ \\-...
             /   /  /-----| | | |
            /   /  /      | | | |
         __/___/__/_______|_|__\\_\\___
        //         v1.1.10          \\
       //       A R E I O N          \\
      //      joshcap20/areion        \\
     //________________________________\\
"""


class AreionServer:
    """
    AreionServer is a class that represents a server for the Areion application. It provides methods to start, run, and stop the server, as well as manage its components such as the orchestrator, router, and HTTP server.

    Attributes:
        orchestrator (any | None): The orchestrator instance responsible for managing tasks.
        router (any | None): The router instance for handling HTTP routes.
        static_dir (str | None): Directory for serving static files.
        logger (any | None): Logger instance for logging server activities.
        engine (any | None): Engine instance for executing tasks.
        host (str): Host address for the server.
        port (int): Port number for the server.
        loop (asyncio.AbstractEventLoop): Event loop for asynchronous operations.
        _shutdown_event (asyncio.Event): Event to signal server shutdown.
        http_server (HttpServer | None): Instance of the HTTP server.
        request_factory: Factory for creating HTTP requests.
        global_middlewares: List of global middlewares to be applied to requests.

    Methods:
        __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, router=None, orchestrator=None, logger=None, engine=None, static_dir=None, request_factory=None, global_middlewares=None):
            Initializes the AreionServer with the given parameters.

        run(self) -> None:
            Starts the server synchronously. This is a simplified entry point for users to start the server without dealing with asyncio directly.

        async start(self) -> None:
            Starts the Areion server asynchronously.

        async shutdown(self, server_task):
            Gracefully shuts down the server.

        stop(self):
            Initiates server shutdown.
    """

    def __init__(
        self,
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        router=None,
        orchestrator=None,
        logger=None,
        engine=None,
        static_dir=None,
        request_factory=None,
        global_middlewares=None,
    ):
        self.orchestrator: any | None = orchestrator
        self.router: any | None = router
        self.static_dir: str | None = static_dir
        self.logger: any | None = logger
        self.engine: any | None = engine
        self.host: str = host
        self.port: int = port
        self.http_server: HttpServer | None = None
        self.request_factory = request_factory
        self.global_middlewares = global_middlewares or []
        
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        # TODO: Implement _loop handling below
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._shutdown_event: asyncio.Event = asyncio.Event()

        

    def run(self) -> None:
        """
        Start the server synchronously.

        This is a simplified entry point for users to start the server without
        dealing with asyncio directly.

        This method attempts to run the `start` coroutine using `asyncio.run()`.
        If a `KeyboardInterrupt` or `SystemExit` exception is raised, it will
        call the `stop` method to perform any necessary cleanup.

        Raises:
            KeyboardInterrupt: If the user interrupts the program execution.
            SystemExit: If a system exit is triggered.
        """
        try:
            asyncio.run(self.start())
        except (KeyboardInterrupt, SystemExit):
            self.stop()

    async def start(self) -> None:
        """
        Start the Areion server asynchronously
        """
        if self.static_dir:
            self.router.add_route(
                "/static/:filename", self._static_file_handler, methods=["GET"]
            )

        print(AREION_LOGO)

        self.log("info", f"Starting server on {self.host}:{self.port}")

        self._start_orchestrator_in_thread()

        # TODO: Allow setting of max_conns, buffer_size, and keep_alive_timeout in builder and pass through here
        # Add the HTTP Server
        self.http_server = HttpServer(
            router=self.router,
            host=self.host,
            port=self.port,
            request_factory=self.request_factory,
            logger=self.logger,
        )

        # Start the HTTP server
        server_task = asyncio.create_task(self.http_server.run())

        # Wait for shutdown signal
        await self._shutdown_event.wait()

        # Shutdown the HTTP server
        await self.http_server.stop()
        await server_task

    async def shutdown(self, server_task):
        """
        Gracefully shutdown the server.
        """
        # Trigger the HTTP server to stop
        if self.http_server:
            await self.http_server.stop()

        # Wait for the HTTP server to finish
        await server_task
        self.stop()

        # Shutdown orchestrator
        if self.orchestrator:
            try:
                await asyncio.get_event_loop().run_in_executor(
                    None, self.orchestrator.shutdown
                )
                self.log("info", "Orchestrator shutdown complete.")
            except Exception as e:
                self.log("error", f"Orchestrator shutdown error: {e}")

    def stop(self):
        """
        Initiate server shutdown.
        """
        self.logger.info("Shutdown initiated.")
        self._loop.call_soon_threadsafe(self._shutdown_event.set)


    def _start_orchestrator_in_thread(self):
        """
        Start orchestrator tasks in a separate thread.
        """
        if self.orchestrator:
            orchestrator_thread = threading.Thread(
                target=self._start_orchestrator, daemon=True
            )
            orchestrator_thread.start()

    def _start_orchestrator(self):
        if self.orchestrator:
            try:
                self.orchestrator.start()
            except Exception as e:
                self.log("error", f"Orchestrator start error: {e}")

    async def _static_file_handler(self, request, filename):
        """
        Handles serving static files from the static directory.
        """
        file_path = os.path.join(self.static_dir, filename)

        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return HttpResponse(status_code=404, body="File Not Found")

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        with open(file_path, "rb") as file:
            content = file.read()

        return HttpResponse(
            status_code=200, body=content, headers={"Content-Type": mime_type}
        )

    def log(self, level: str, message: str) -> None:
        """
        Log a message using the server's logger.
        """
        if self.logger:
            log_method = getattr(self.logger, level, None)
            if log_method:
                log_method(message)
        else:
            print(f"[{level.upper()}] {message}")


class AreionServerBuilder:
    """
    AreionServerBuilder is a builder class for constructing an AreionServer instance with various configurable components.
    It also creates a default logger if none is provided and injects this into other components.
    Methods:
        __init__():
            Initializes the builder with default values for host, port, and other components.
        with_host(host: str):
            Sets the host for the server. Raises ValueError if the host is not a string.
        with_port(port: int):
            Sets the port for the server. Raises ValueError if the port is not an integer.
        with_router(router):
            Sets the router for the server. Validates that the router has the required methods. Raises ValueError if validation fails.
        with_orchestrator(orchestrator):
            Sets the orchestrator for the server. Validates that the orchestrator has the required methods. Raises ValueError if validation fails.
        with_logger(logger):
            Sets the logger for the server. Validates that the logger has the required methods. Raises ValueError if validation fails.
        with_engine(engine):
            Sets the template engine for the server. Validates that the engine has the required methods. Raises ValueError if validation fails.
        with_static_dir(static_dir: str):
            Sets the static directory for the server. Raises ValueError if the static directory is not a string or does not exist.
        _validate_component(component, required_methods, component_name):
            Validates that the component has the required methods. Raises ValueError if validation fails.
        _initialize_logger():
            Initializes the logger to a default logger if none is provided.
        build():
            Constructs and returns an AreionServer instance with the configured components. Raises ValueError if required components are missing.
    """

    def __init__(self):
        self.host = DEFAULT_HOST
        self.port = DEFAULT_PORT
        self.router = None
        self.orchestrator = None
        self.logger = None
        self.engine = None
        self.static_dir = None
        # Development Only
        self.development_mode = False
        self.swagger_handler = None

    def with_host(self, host: str):
        if not isinstance(host, str):
            raise ValueError("Host must be a string.")
        self.host = host
        return self

    def with_port(self, port: int):
        if not isinstance(port, int):
            raise ValueError("Port must be an integer.")
        self.port = port
        return self

    def with_router(self, router):
        self._validate_component(router, ["add_route", "get_handler"], "Router")
        self.router = router
        return self

    def with_orchestrator(self, orchestrator):
        self._validate_component(
            orchestrator,
            ["start", "submit_task", "run_tasks", "shutdown"],
            "Orchestrator",
        )
        self.orchestrator = orchestrator
        return self

    def with_logger(self, logger):
        self._validate_component(
            logger, ["info", "error", "debug", "warning", "critical"], "Logger"
        )
        self.logger = logger
        return self

    def with_engine(self, engine):
        self._validate_component(engine, ["render"], "Template engine")
        self.engine = engine
        return self

    def with_static_dir(self, static_dir: str):
        if not isinstance(static_dir, str):
            raise ValueError("Static directory must be a string.")
        if not os.path.isdir(static_dir):
            raise ValueError(f"Static directory {static_dir} does not exist.")
        self.static_dir = static_dir
        return self

    def with_development_mode(self, development_mode: bool = False):
        if not isinstance(development_mode, bool):
            raise ValueError("Development mode flag must be a boolean.")
        self.development_mode = development_mode
        return self

    def _validate_component(self, component, required_methods, component_name):
        if not all(hasattr(component, method) for method in required_methods):
            raise ValueError(
                f"{component_name} must implement {', '.join(required_methods)}"
            )

    def _initialize_logger(self) -> None:
        if not self.logger:
            from .default import Logger as DefaultLogger

            self.logger = DefaultLogger()
            self.logger.info("Logger missing, defaulting to console logging.")

    def build(self):
        """
        Builds and returns an AreionServer instance.
        This method initializes the logger, sets the logger for the orchestrator if it exists,
        and creates an HttpRequestFactory instance. It then uses these components to build
        and return an AreionServer instance.
        Raises:
            ValueError: If the router is not set.
        Returns:
            AreionServer: The configured AreionServer instance.
        """
        if not self.router:
            raise ValueError("Router is required.")

        self._initialize_logger()

        if self.orchestrator:
            self.orchestrator.set_logger(self.logger)

        request_factory = HttpRequestFactory(
            logger=self.logger, engine=self.engine, orchestrator=self.orchestrator
        )

        if self.development_mode:
            from .dev.swagger import SwaggerHandler

            self.swagger_handler = SwaggerHandler(self.router)

        return AreionServer(
            host=self.host,
            port=self.port,
            router=self.router,
            orchestrator=self.orchestrator,
            logger=self.logger,
            engine=self.engine,
            static_dir=self.static_dir,
            request_factory=request_factory,
        )
