"""Manages dashboards WebSocket connections, queues and distributes telemetry messages, handles incoming commands, and cleans up disconnected clients. """
import asyncio
import logging
from collections.abc import Awaitable, Callable
import src.telemetry_server.config as config
from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class _Client:
    """One connected dashboard. Has an information about WebSocket(konkretne ustawione połaczenie z DASHBOARD_PORT),
    every object of this class has its own queue (buffer) of messages, so every object is independent from others in case of slowing down or crashing. """

    def __init__(self, websocket: WebSocket, queue_size: int):
        self.websocket = websocket
        self.queue = asyncio.Queue(maxsize=queue_size)# Buffer, FIFO queue
        self.dropped = 0 #Counts how many messages have been rejected

    def queue_package(self, message: dict) -> None:
        """Put a message in the queue without waiting.

        If the dashboard is too slow and its queue is full, the OLDEST message is
        dropped: for live telemetry the newest value is the one that matters.
        """
        if self.queue.full():
            self.queue.get_nowait() #Removes the oldest message, without waiting
            if self.dropped == 0:
                logger.warning("A dashboard is too slow: dropping its oldest message")
            self.dropped += 1
        self.queue.put_nowait(message)#Adds message to the end of the queue without waiting


class DashboardHub:
    """Class for managing dashboards. Keeps track of connected dashboards(Clients) and delivers already formatted messages to all of them (dashboardw broadcast manager)."""

    def __init__(self, queue_size: int = config.DEFAULT_QUEUE_SIZE):
        self._queue_size = queue_size
        self._clients: set[_Client] = set()

    def count_dashboards(self) -> int:
        """Number of connected dashboards."""
        return len(self._clients)

    def broadcast(self, message: dict) -> None:
        """Send formatted data package to all dashboards (add message to Client's queue)"""
        for client in self._clients:  
            client.queue_package(message)

    async def handle(self, websocket: WebSocket, initial_message: dict | None = None, dashboard_command: Callable[[str], Awaitable[None]] | None = None) -> None:
        """Serve one dashboard from connect to disconnect.

        websocket: connection with individual dashboard (Client object)
        initial_message: sent first (e.g. the last known data, so widgets on newly opened dashboards are not empty).
        dashboard_command: #TODO: called with every text the dashboard sends (for commands later), messages are ignored when it is None.
        """
        await websocket.accept() #request DASHBOARD_PORT to connect this dashboard to port, wait for the operation to complete

        #Adding new dashboard
        client = _Client(websocket, self._queue_size)
        self._clients.add(client)
        logger.info("Dashboard connected (%d total)", len(self._clients))
        if initial_message != None:
            client.queue_package(initial_message)

        #Launch two dashboard tasks: listening for data, sending commands (concurrently)
        receiver = asyncio.create_task(self._receive_loop(websocket, dashboard_command))
        sender = asyncio.create_task(self._send_loop(client))
        try:
            # Whichever ends first (dashboard left, or sending failed) ends this dashboard.
            done, _ = await asyncio.wait({receiver, sender}, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                if task.exception() is not None:
                    logger.warning("Dashboard connection ended with an error: %r", task.exception())
        finally: 
            #closing connection with this dashboard
            receiver.cancel()
            sender.cancel()
            await asyncio.gather(receiver, sender, return_exceptions=True)#wait for closing all tasks
            
            self._clients.discard(client) 
            logger.info("Dashboard disconnected (%d total)", len(self._clients))

    @staticmethod
    async def _receive_loop(websocket: WebSocket, on_message) -> None:
        """Read what the dashboard sends. Ends only when the dashboard disconnects."""
        try:
            while True:
                text = await websocket.receive_text()
                if on_message is None:
                    continue
                try:
                    await on_message(text)
                except Exception:
                    # A bad command must not drop the dashboard: log it and keep listening.
                    logger.exception("Error while handling a dashboard message: %s", text)
        except WebSocketDisconnect:
            pass # the dashboard left normally (closed tab, refresh), nothing to report

    @staticmethod
    async def _send_loop(client: _Client) -> None:
        """Send queued messages to one dashboard, one at a time. Ends when sending fails."""
        try:
            while True:
                message = await client.queue.get()
                await client.websocket.send_json(message)
        except WebSocketDisconnect:
            pass  # the dashboard left normally (closed tab, refresh), nothing to report
        except Exception as error:
            logger.warning("Cannot send to a dashboard (%r), closing its connection", error)