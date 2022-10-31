import logging

from pajbot import utils
from pajbot.managers.db import DBManager
from pajbot.models.command import Command, CommandExample
from pajbot.models.user import User
from pajbot.modules import BaseModule, ModuleSetting
from pajbot.modules.basic import BasicCommandsModule
from pajbot.utils import time_since

log = logging.getLogger("pajbot")


class FollowAgeModule(BaseModule):
    ID = __name__.split(".")[-1]
    NAME = "Followage"
    DESCRIPTION = "Activa el uso de los comandos !followage y !followsince"
    CATEGORY = "Feature"
    PARENT_MODULE = BasicCommandsModule
    SETTINGS = [
        ModuleSetting(
            key="action_followage",
            label="MessageAction para !followage",
            type="options",
            required=True,
            default="reply",
            options=["say", "whisper", "reply"],
        ),
        ModuleSetting(
            key="action_followsince",
            label="MessageAction para !followsince",
            type="options",
            required=True,
            default="reply",
            options=["say", "whisper", "reply"],
        ),
        ModuleSetting(
            key="global_cd",
            label="Cooldown Global (Segundos)",
            type="number",
            required=True,
            placeholder="",
            default=4,
            constraints={"min_value": 0, "max_value": 120},
        ),
        ModuleSetting(
            key="user_cd",
            label="Cooldown Por-Usuario (Segundos)",
            type="number",
            required=True,
            placeholder="",
            default=8,
            constraints={"min_value": 0, "max_value": 240},
        ),
    ]

    def load_commands(self, **options):
        self.commands["followage"] = Command.raw_command(
            self.follow_age,
            delay_all=self.settings["global_cd"],
            delay_user=self.settings["user_cd"],
            description="Comprueba tu tiempo de seguimiento o el de otra persona en este u otro canal",
            can_execute_with_whisper=True,
            examples=[
                CommandExample(
                    None,
                    "Comprueba tu propio tiempo de seguimiento",
                    chat="user:!followage\n" "bot:pajlada, Tú has estado siguiendo a Karl_Kons durante 4 meses y 24 días",
                    description="Comprueba el tiempo que llevas siguiendo al streamer actual (Karl_Kons en este caso)",
                ).parse(),
                CommandExample(
                    None,
                    "Comprobar el tiempo de seguimiento de otro",
                    chat="user:!followage NightNacht\n"
                    "bot:pajlada, NightNachtha estado siguiendo a Karl_Kons durante 5 meses y 4 días",
                    description="Comprueba cuánto tiempo lleva cualquier usuario siguiendo al streamer actual (Karl_Kons en este caso)",
                ).parse(),
                CommandExample(
                    None,
                    "Comprobar el tiempo de seguimiento de un streamer determinado",
                    chat="user:!followage NightNacht forsen\n"
                    "bot:pajlada, NightNacht ha estado siguiendo a forsen durante 1 año y 4 meses",
                    description="Comprueba el tiempo que NightNacht lleva siguiendo a forsen",
                ).parse(),
                CommandExample(
                    None,
                    "Comprueba tu propio tiempo de seguimiento de un determinado streamer",
                    chat="user:!followage pajlada forsen\n"
                    "bot:pajlada, Tú has estado siguiendo a forsen durante 1 año y 3 meses",
                    description="Comprueba el tiempo que llevas siguiendo a forsen",
                ).parse(),
            ],
        )

        self.commands["followsince"] = Command.raw_command(
            self.follow_since,
            delay_all=self.settings["global_cd"],
            delay_user=self.settings["user_cd"],
            description="Compruebe desde cuándo usted u otra persona siguió por primera vez un canal",
            can_execute_with_whisper=True,
            examples=[
                CommandExample(
                    None,
                    "Compruebe su propio seguimiento",
                    chat="user:!followsince\n"
                    "bot:pajlada, Tú has estado siguiendo a Karl_Kons desde el 04 March 2015, 07:02:01 UTC",
                    description="Comprueba cuándo seguiste por primera vez al streamer actual (Karl_Kons en este caso)",
                ).parse(),
                CommandExample(
                    None,
                    "Comprueba el seguimiento de otros",
                    chat="user:!followsince NightNacht\n"
                    "bot:pajlada, NightNacht ha estado siguiendo a Karl_Kons desde el 03 July 2014, 04:12:42 UTC",
                    description="Comprueba cuándo NightNacht siguió por primera vez al streamer actual (Karl_Kons en este caso)",
                ).parse(),
                CommandExample(
                    None,
                    "Comprueba el seguimiento de alguien más desde a otro streamer",
                    chat="user:!followsince NightNacht forsen\n"
                    "bot:pajlada, NightNacht ha estado siguiendo a forsen desde el 13 June 2013, 13:10:51 UTC",
                    description="Comprueba cuándo NightNacht siguió por primera vez al streamer dado (forsen)",
                ).parse(),
                CommandExample(
                    None,
                    "Comprueba tu seguimiento a otro streamer",
                    chat="user:!followsince pajlada forsen\n"
                    "bot:pajlada, Tú has estado siguiendo a forsen desde el 16 December 1990, 03:06:51 UTC",
                    description="Comprueba cuándo has seguido por primera vez el streamer dado (forsen)",
                ).parse(),
            ],
        )

    @staticmethod
    def _format_for_follow_age(follow_since):
        human_age = time_since(utils.now().timestamp() - follow_since.timestamp(), 0)
        return f"durante {human_age}"

    @staticmethod
    def _format_for_follow_since(follow_since):
        human_age = follow_since.strftime("%d-%m-%Y, %X %Z")
        return f"desde el {human_age}"

    @staticmethod
    def _parse_message(message):
        from_input = None
        to_input = None
        if message is not None and len(message) > 0:
            message_split = message.split(" ")
            if len(message_split) >= 1:
                from_input = message_split[0]
            if len(message_split) >= 2:
                to_input = message_split[1]

        return from_input, to_input

    def _handle_command(self, bot, source, message, event, format_cb, message_method):
        from_input, to_input = self._parse_message(message)

        with DBManager.create_session_scope(expire_on_commit=False) as db_session:
            if from_input is not None:
                from_user = User.find_or_create_from_user_input(db_session, bot.twitch_helix_api, from_input)

                if from_user is None:
                    bot.execute_now(
                        bot.send_message_to_user,
                        source,
                        f'El usuario "{from_input}" no ha sido encontrado',
                        event,
                        method=self.settings["action_followage"],
                    )
                    return
            else:
                from_user = source

            if to_input is None:
                to_input = bot.streamer.login

            to_user = User.find_or_create_from_user_input(db_session, bot.twitch_helix_api, to_input)
            if to_user is None:
                bot.execute_now(
                    bot.send_message_to_user,
                    source,
                    f'El usuario "{to_input}" no ha sido encontrado',
                    event,
                    method=message_method,
                )
                return

        follow_since = bot.twitch_helix_api.get_follow_since(from_user.id, to_user.id)
        is_self = source == from_user

        if follow_since is not None:
            # Following
            suffix = f"estado siguiendo a {to_user} {format_cb(follow_since)}"
            if is_self:
                message = f"Has {suffix}"
            else:
                message = f"{from_user.name} ha {suffix}"
        else:
            # Not following
            suffix = f"a {to_user}"
            if is_self:
                message = f"No sigues {suffix}"
            else:
                message = f"{from_user.name} no sigue {suffix}"

        bot.execute_now(bot.send_message_to_user, source, message, event, method=message_method)

    def follow_age(self, bot, source, message, event, **rest):
        self.bot.action_queue.submit(
            self._handle_command,
            bot,
            source,
            message,
            event,
            self._format_for_follow_age,
            self.settings["action_followage"],
        )

    def follow_since(self, bot, source, message, event, **rest):
        self.bot.action_queue.submit(
            self._handle_command,
            bot,
            source,
            message,
            event,
            self._format_for_follow_since,
            self.settings["action_followsince"],
        )
