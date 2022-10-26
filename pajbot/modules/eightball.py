import logging
import random

from pajbot.models.command import Command, CommandExample
from pajbot.modules import BaseModule, ModuleSetting

log = logging.getLogger(__name__)


class EightBallModule(BaseModule):
    ID = __name__.split(".")[-1]
    NAME = "8-ball"
    DESCRIPTION = "Permite a los usuarios acceder al comando !8ball"
    CATEGORY = "Game"
    SETTINGS = [
        ModuleSetting(
            key="online_global_cd",
            label="Cooldown Global (segundos)",
            type="number",
            required=True,
            placeholder="",
            default=4,
            constraints={"min_value": 0, "max_value": 120},
        ),
        ModuleSetting(
            key="online_user_cd",
            label="Cooldown por-usuario (segundos)",
            type="number",
            required=True,
            placeholder="",
            default=10,
            constraints={"min_value": 0, "max_value": 240},
        ),
    ]

    def __init__(self, bot):
        super().__init__(bot)
        self.phrases = [
            "Seguro",
            "¡¿Estás bromeando?!",
            "Sí",
            "No",
            "Creo que sí",
            "No apuestes por ello",
            "Já",
            "Dudoso",
            "Seguro",
            "Olvídate de ello",
            "Nein",
            "Tal vez",
            "Kappa Keepo PogChamp",
            "Seguro",
            "No lo creo",
            "Es así",
            "Me inclino hacia el no",
            "Mira en el fondo de tu corazón y verás la respuesta",
            "Definitivamente",
            "Lo más probable",
            "Mis fuentes dicen que sí",
            "Nunca",
            "Nah m8",
            "Podría ser que sí",
            "No",
            "Perspectiva buena",
            "Perspectiva no tan buena",
            "Quizás",
            "Tal vez",
            "Eso es difícil",
            "No sé, Kev",
            "No preguntes eso",
            "La respuesta a eso no es bonita",
            "Los cielos apuntan al sí",
            "¿Quién sabe?",
            "Sin duda",
            "Ayer hubiera sido un sí, pero hoy es un sis",
            "Tendrás que esperar",
        ]

        self.emotes = [
            "Kappa",
            "Keepo",
            "xD",
            "KKona",
            "4Head",
            "EleGiggle",
            "DansGame",
            "KappaCool",
            "BrokeBack",
            "OpieOP",
            "KappaRoss",
            "KappaPride",
            "FeelsBadMan",
            "FeelsGoodMan",
            "PogChamp",
            "VisLaud",
            "OhMyDog",
            "FrankerZ",
            "DatSheffy",
            "BabyRage",
            "VoHiYo",
            "haHAA",
            "FeelsBirthdayMan",
            "LUL",
        ]

    def eightball_command(self, bot, source, message, **rest):
        if not message or len(message) <= 0:
            return False

        phrase = random.choice(self.phrases)
        emote = random.choice(self.emotes)
        bot.me(f"{source}, la bola-8 dice... {phrase} {emote}")

    def load_commands(self, **options):
        self.commands["8ball"] = Command.raw_command(
            self.eightball_command,
            delay_all=self.settings["online_global_cd"],
            delay_user=self.settings["online_user_cd"],
            description="¿Necesitas ayuda para tomar una decisión? Utiliza el comando !8ball",
            examples=[
                CommandExample(
                    None,
                    "!8ball",
                    chat="user:!8ball ¿Debería escuchar gachimuchi?\n"
                    "bot:pajlada, la bola-8 dice... ¡Por supuesto que sí!",
                    description="Hazle una pregunta importante a la bola 8",
                ).parse()
            ],
        )
