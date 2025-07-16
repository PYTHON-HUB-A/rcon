import asyncio
import math
import logging

from berconpy import (
    AsyncRCONClient,
    AsyncRCONClientCache,
    AsyncEventDispatcher,
    AsyncClientConnector,
    LoginFailure,
    RCONError,
    ConnectorConfig,
    AsyncCommander
)

from events import (
    on_message,
    on_player_connect,
    on_player_disconnect,
    on_player_guid,
    on_player_kick,
    on_player_verify_guid,
    on_login,
    on_raw_event
)

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Конфигурация подключения с минимальными интервалами
fast_config = ConnectorConfig(
    run_interval=0.2,
    keep_alive_interval=5.0,
    players_interval=10.0,
    initial_connect_attempts=99999,
    connection_timeout=0.8
)

# Кастомный коннектор с агрессивным переподключением
class CustomClientConnector(AsyncClientConnector):
    def __init__(self, *, config=None, commander=None):
        super().__init__(config=config or ConnectorConfig(), commander=commander)

    async def on_connect(self):
        logging.info("🔌 Соединение с сервером установлено.")

    async def on_disconnect(self):
        logging.warning("❌ Соединение с сервером потеряно.")

    async def on_packet_send(self, packet: bytes):
        logging.debug(f"📤 Отправка пакета: {packet.hex()}")

    async def on_packet_receive(self, packet: bytes):
        logging.debug(f"📥 Получен пакет: {packet.hex()}")

    async def _try_connect(self, password: str, *, first_iteration: bool) -> bool:
        """
        Агрессивное переподключение без задержек между попытками.
        """
        logging.info("⚡ Попытка подключения к серверу...")
        self._is_logged_in = asyncio.get_running_loop().create_future()

        attempts = (
            range(self.config.initial_connect_attempts)
            if first_iteration
            else iter(int, 1)  # бесконечный итератор
        )

        for i in attempts:
            if self._close_event.is_set():
                return False

            try:
                timeout = self.config.connection_timeout
                result = await asyncio.wait_for(super().connect(password), timeout=timeout)
                logging.info(f"✅ Успешное подключение (попытка #{i + 1})")
                return result
            except LoginFailure:
                raise
            except (asyncio.TimeoutError, OSError) as e:
                logging.debug(f"⏱ Попытка #{i + 1} неудачна: {e}")
                await self.disconnect()
                continue

        return False


async def main():
    ip = "80.242.59.185"
    port = 2310
    password = "34sDk35khsku345"

    # Командер с быстрыми таймингами
    fast_commander = AsyncCommander(
        command_attempts=1,
        command_interval=0.3
    )

    # Создаём клиента с кастомным протоколом
    client = AsyncRCONClient(
        cache=AsyncRCONClientCache(),
        dispatch=AsyncEventDispatcher(),
        protocol=CustomClientConnector(config=fast_config, commander=fast_commander)
    )

    # Подключение всех обработчиков событий
    client.add_listener("on_player_connect", on_player_connect)
    client.add_listener("on_player_disconnect", on_player_disconnect)
    client.add_listener("on_player_guid", on_player_guid)
    client.add_listener("on_message", on_message)
    client.add_listener("on_player_kick", on_player_kick)
    client.add_listener("on_player_verify_guid", on_player_verify_guid)
    client.add_listener("on_login", on_login)
    client.add_listener("on_raw_event", on_raw_event)

    try:
        async with client.connect(ip, port, password):
            logging.info("🎮 Подключение к RCON установлено, ожидание событий...")
            await asyncio.sleep(math.inf)
    except LoginFailure:
        logging.error("❌ Ошибка: неверный RCON-пароль.")
    except RCONError as e:
        logging.error(f"❌ Ошибка RCON: {e}")
    except Exception as e:
        logging.exception(f"❌ Общая ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())
