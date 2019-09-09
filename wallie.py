import argparse
import json
import sources.configuration
import sources.recognizers
import sources.core
import sources.fetchers
import pprint


parser = argparse.ArgumentParser("Wallie - changes your wallpaper how you want it.")
parser.add_argument(
    "-n",
    "--now",
    required=False,
    default=True,
    action="store_true",
    help="Reloads the options and changes wallpaper.",
)

parser.add_argument(
    "-s",
    "--set",
    required=False,
    type=str,
    help="Sets the wallpaper from provided path.",
)
parser.add_argument(
    "-t",
    "--allowedTags",
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
    "-fet",
    "--fetcher",
    required=False,
    type=str,
    default="FromDirectory",
    help='Changes the fetcher to provided. If supported. The default one is named "rWallpapers"',
)

parser.add_argument(
    "-rec",
    "--recognizer",
    required=False,
    type=str,
    default="IntelNature",
    help='Changes the image recognizer to provided. If supported. The default one is named "IntelImagesRecognizer". Can be omitted by setting None.',
)
parser.add_argument(
    "-so",
    "--setOption",
    required=False,
    type=json.load,
    help="Allows user to set specified option in configuration.",
)

args = parser.parse_args()
arguments = sources.configuration.ArgsIntercepter(args)
config = sources.configuration.AppConfiguration(arguments.Config)
if arguments.App:
    recognizer = sources.recognizers.GetRecognizer(config.Instance)
    fetcher = sources.fetchers.GetFetcher(config.Instance)
    application = sources.core.Application(config.Instance, fetcher, recognizer)
    application.Invoke(arguments.App)

config.WriteChanges()

