import argparse
import internals.configuration
import internals.recognizers
import internals.core


parser = argparse.ArgumentParser("Wallpaper application.")
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
    help="Sets the time interval which the change ocurres.",
    type=int,
)
parser.add_argument(
    "-r",
    "--repeat",
    default=False,
    action="store_true",
    required=False,
    help="used in conjuction with --timeset argument, tells program to repeat execution with same configuration. Default value is set to True.",
)
parser.add_argument(
    "-d",
    "--directory",
    required=False,
    type=str,
    help="Turns off the downloading images from sources, and sets the wallpapers from provided directory path. Tags if set, still apply.",
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

config = internals.configuration.AppConfiguration(commands.Config)

recognizer = internals.recognizers.DefaultRecognizer()

fetcher = internals.fetchers.RedditFetcher()

application = internals.core.Application(
    config, fetcher, recognizer
)

application.Invoke(commands.App)

