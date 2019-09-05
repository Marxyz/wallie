import argparse
import internals.configuration
import internals.recognizers
import internals.core


parser = argparse.ArgumentParser("Wallie - changes your wallpaper how adn when uou want it.")
parser.add_argument(
    "-n",
    "--now",
    required=False,
    default=False,
    action="store_true",
    help="Reloads the options and changes wallpaper as soon as it is possible.",
)
parser.add_argument(
    "-t",
    "--tags",
    required=False,
    help="Changes the tags which define allow wallpapers. If set without -now flag, the change occurs after previously defined or default interval.",
    nargs="+",
)
parser.add_argument(
    "-i",
    "--interval",
    required=False,
    help="Sets the time interval in which the change ocurres.",
    type=int,
)
parser.add_argument(
    "-r",
    "--repeat",
    default=True,
    action="store_true",
    required=False,
    help="Used in conjuction with --interval argument, tells program to repeat execution with same configuration. Default value is set to True.",
)
parser.add_argument(
    "-f",
    "--fetcher",
    required=False,
    type=str,
    default="rWallpapers",
    help='Changes the fetcher to provided. If supported. The default one is named "rWallpapers"',
)

parser.add_argument(
    "-r",
    "--recognizer",
    required=False,
    type=str,
    default="IntelImages",
    help='Changeas the recognizer to provided. If supported. The default one is named "IntelImages"',
)
parser.add_argument(
    "-s",
    "--set",
    required=False,
    type=str,
    help="Sets the wallpaper from provided path. If not specified, resets the repeat flag to false so the wallpaper change does not occur anymore.",
)

args = parser.parse_args()


commands = internals.configuration.ArgsInterceptor(args)

recognizer = internals.recognizers.GetRecognizer(commands.Recognizer)
fetcher = internals.fetchers.GetFetcher(commands.Fetcher)

config = internals.configuration.AppConfiguration(commands.Config)

if commands.App:
    application = internals.core.Application(config, fetcher, recognizer)
    application.Invoke(commands.App)

