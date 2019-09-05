import argparse
import sources.configuration
import sources.recognizers
import sources.core


parser = argparse.ArgumentParser("Wallie - changes your wallpaper how you want it.")
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
    help="Changes the tags which define allow wallpapers. If set without --now flag, the change occurs after previously defined or default interval.",
    nargs="+",
)
parser.add_argument(
    "-i", "--interval", required=False, help="Sets the repeat change delay.", type=int
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
    default="IntelImagesRecognizer",
    help='Changes the image recognizer to provided. If supported. The default one is named "IntelImagesRecognizer".',
)

parser.add_argument(
    "-s",
    "--set",
    required=False,
    type=str,
    help="Sets the wallpaper from provided path.",
)

args = parser.parse_args()
arguments = sources.configuration.ArgsInterceptor(args)
config = sources.configuration.AppConfiguration(arguments.Config)

if arguments.App:
    recognizer = sources.recognizers.GetRecognizer(config.Recognizer.Name)
    fetcher = sources.fetchers.GetFetcher(config.Fetcher.Name)
    application = sources.core.Application(config, fetcher, recognizer)
    application.Invoke(arguments.App)

config.WriteChanges()

