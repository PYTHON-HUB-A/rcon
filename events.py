import berconpy as rcon

async def on_message(message: str):
    """
    Срабатывает при любом сообщении от сервера.
    """
    print(f'[SERVER] {message}')


async def on_player_connect(player: rcon.Player):
    """
    Срабатывает при подключении игрока к серверу.
    """
    try:
        print(f'[on_player_connect] ID: {player.id}, Name: {player.name}, IP: {player.ip}, Addr: {player.addr}, In lobby: {player.in_lobby}')
    except Exception as e:
        print(f'[on_player_connect][ERROR] {e}')


async def on_player_disconnect(player: rcon.Player):
    """
    Срабатывает при отключении игрока от сервера.
    """
    try:
        print(f'[on_player_disconnect] ID: {player.id}, Name: {player.name}, IP: {player.ip}')
    except Exception as e:
        print(f'[on_player_disconnect][ERROR] {e}')


async def on_player_guid(player: rcon.Player):
    """
    Срабатывает, когда сервер получает GUID игрока.
    """
    try:
        print(f'[on_player_guid] ID: {player.id}, Name: {player.name}, GUID: {player.guid}, Valid: {player.is_guid_valid}')
    except Exception as e:
        print(f'[on_player_guid][ERROR] {e}')


async def on_player_kick(player: rcon.Player, reason: str):
    """
    Срабатывает при кике игрока с сервера.
    """
    try:
        print(f'[on_player_kick] Name: {player.name}, Reason: {reason}')
    except Exception as e:
        print(f'[on_player_kick][ERROR] {e}')


async def on_player_verify_guid(player: rcon.Player):
    """
    Срабатывает при проверке GUID игрока сервером.
    """
    try:
        print(f'[on_player_verify_guid] ID: {player.id}, GUID: {player.guid}, Valid: {player.is_guid_valid}')
    except Exception as e:
        print(f'[on_player_verify_guid][ERROR] {e}')


async def on_raw_event(packet):
    """
    Срабатывает для каждого необработанного пакета от сервера.
    """
    try:
        print(f'[on_raw_event] {packet}')
    except Exception as e:
        print(f'[on_raw_event][ERROR] {e}')


async def on_login():
    """
    Срабатывает при успешном подключении к RCON.
    """
    print("🔐 Успешное подключение к RCON.")
