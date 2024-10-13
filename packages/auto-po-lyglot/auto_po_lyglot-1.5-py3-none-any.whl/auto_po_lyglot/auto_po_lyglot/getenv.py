# pyright: reportAttributeAccessIssue=false

import logging
from pathlib import Path
from dotenv import load_dotenv
from os import environ
import argparse
import sys

import langcodes

logger = logging.getLogger(__name__)


def set_all_loggers_level(level):
    logger.info(f"Setting all loggers to level {logging.getLevelName(level)}")

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    for name in logging.root.manager.loggerDict:
      if not name.startswith('auto_po_lyglot.'):
        continue
      nlogger = logging.getLogger(name)
      nlogger.handlers = []
      nlogger.addHandler(handler)
      nlogger.setLevel(level)
      nlogger.propagate = False

    root = logging.getLogger()
    root.handlers = []
    root.addHandler(handler)
    root.setLevel(level)


# def inspect_logger(logger):
#     print(f"Logger: {logger.name}")
#     print(f"  Level: {logging.getLevelName(logger.level)}")
#     print(f"  Propagate: {logger.propagate}")
#     print("  Handlers:")
#     for idx, handler in enumerate(logger.handlers):
#         print(f"    Handler {idx}: {type(handler).__name__}")
#         print(f"      Level: {logging.getLevelName(handler.level)}")


class Params:
  pass


class ParamsLoader:
  parser_description = """
Creates a .po translation file based on an existing one using a given model and llm type.
It reads the parameters from the command line and completes them if necessary from the .env in the same directory.
It iterates over the provided target languages, and for each language iterates over the entries of the input po file and,
using the provided client, model and prompt, translates the original phrase into the target language with the help of
the context translation."""

  def __init__(self, additional_args=None):
    """
    additional_args is a list of dictionaries where each dictionary represents an additional argument that can be given to
    the script. Each dictionary must contain the following key:
    - arg: the argument itself (e.g. '--foo' or '-f') or an array of arguments (e.g. ['-'f', '--foo'])
    - help: the help message associated to the argument
    Each dictionary can contain the following keys:
    - type: the type of the argument (e.g. str, int, float)
    or
    - action: the action associated to the argument (e.g. 'store_true')
    - env: the environment variable associated to the argument (e.g. 'FOO')
    - default: the default value of the argument (e.g. 'bar')
    """
    self.additional_args = additional_args

  def add_parser_arguments(self, parser):
    parser.add_argument('-p', '--show-prompts',
                        action='store_true',
                        help='show the prompts used for translation and exits')
    parser.add_argument('-l', '--llm',
                        type=str,
                        help='Le type of LLM you want to use. Can be openai, ollama, claude or claude_cached. '
                             'For openai or claude[_cached], you need to set the api key in the environment. '
                             'Supersedes LLM_CLIENT in .env. Default is ollama',
                        choices=['openai', 'ollama', 'claude', 'claude_cached', 'gemini', 'grok'])
    parser.add_argument('-m', '--model',
                        type=str,
                        help='the name of the model to use. Supersedes LLM_MODEL in .env. If not provided at all, '
                             'a default model will be used, based on the chosen client')
    parser.add_argument('-t', '--temperature',
                        type=float,
                        help='the temperature of the model. Supersedes TEMPERATURE in .env. If not provided at all, '
                             'a default value of 0.2 will be used')
    parser.add_argument('--original-language',
                        type=str,
                        help='the language of the original phrase. Supersedes ORIGINAL_LANGUAGE in .env. ')
    parser.add_argument('--context-language',
                        type=str,
                        help='the language of the context translation. Supersedes CONTEXT_LANGUAGE in .env. ')
    parser.add_argument('--target-language',
                        type=str,
                        help='the language into which the original phrase will be translated. Supersedes '
                             'TARGET_LANGUAGE in .env. ')
    parser.add_argument('-i', '--input-po',
                        type=str,
                        help='the .po file containing the msgids (phrases to be translated) '
                             'and msgstrs (context translations). Supersedes INPUT_PO in .env.')
    parser.add_argument('-o', '--output-po',
                        type=str,
                        help='the .po file where the translated results will be written. If not provided, '
                             'it will be created in the same directory as the input_po except if the input po file has '
                             'the specific format .../locale/<context language code>/LC_MESSAGES/<input po file name>. '
                             'In this case, the output po file will be created as '
                             '.../locale/<target language code>/LC_MESSAGES/<input po file name>. Supersedes '
                             'OUTPUT_PO in .env.')
    parser.add_argument('-oo', '--overwrite-output',
                        action='store_true',
                        help='Overwrites the output po file if it already exists. Supersedes OVERWRITE_OUTPUT in .env. '
                             'Default is False')
    parser.add_argument('-f', '--force',
                        action='store_true',
                        help='Forces translating already translated entries. Supersedes FORCE in .env. Default is False')
    parser.add_argument('-c', '--compile',
                        action='store_true',
                        help='Compiles the output po file to an mo file. Supersedes COMPILE in .env. Default is False')
    parser.add_argument('--fuzzy',
                        action='store_true',
                        help='Translates fuzzy entries in the input po file. Supersedes FUZZY in .env. Default is False')
    parser.add_argument('--owner',
                        type=str,
                        help='Owner of the project. Supersersedes OWNER in .env. Default is <OWNER>')
    parser.add_argument('--owner_mail',
                        type=str,
                        help='Email of the owner. Supersersedes OWNER_MAIL in .env. Default is <OWNER EMAIL>')

    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode. Equivalent to LOG_LEVEL=INFO in .env')
    parser.add_argument('-vv', '--debug', action='store_true', help='debug mode. Equivalent to LOG_LEVEL=DEBUG in .env')
    if self.additional_args:
      for arg in self.additional_args:
        if arg.get('action'):
          parser.add_argument(
              *(arg.get('arg') if isinstance(arg.get('arg'), list) else [arg.get('arg')]),
              action=arg.get('action'),
              help=arg.get('help')
          )
        else:
          parser.add_argument(
            *(arg.get('arg') if isinstance(arg.get('arg'), list) else [arg.get('arg')]),
            type=arg.get('type'),
            help=arg.get('help')
          )

  def load_params_from_env(self, args=None):
    "Update missing args from the .env file"

    params = ParamsLoader()
    load_dotenv(override=True)

    if (args and args.debug) or ((args and not args.verbose) and environ.get('LOG_LEVEL', None) == 'DEBUG'):
      params.log_level = logging.DEBUG
    elif (args and args.verbose) or environ.get('LOG_LEVEL', None) == 'INFO':
      params.log_level = logging.INFO
    else:
      params.log_level = logging.WARNING
    set_all_loggers_level(params.log_level)

    # original language
    params.original_language = (args and args.original_language) or environ.get('ORIGINAL_LANGUAGE', 'English')
    # context translation language
    params.context_language = (args and args.context_language) or environ.get('CONTEXT_LANGUAGE', 'French')
    # LLM client and model
    params.llm_client = (args and args.llm) or environ.get('LLM_CLIENT', 'ollama')
    params.model = (args and args.model) or environ.get('LLM_MODEL', None)

    # ollama base url if needed
    params.ollama_base_url = environ.get('OLLAMA_BASE_URL', 'http://localhost:11434/v1')

    # the target languages to test for translation
    params.target_languages = [args.target_language] if args and args.target_language else \
      environ.get('TARGET_LANGUAGES', 'Spanish').split(',')

    params.system_prompt = environ.get('SYSTEM_PROMPT', None)
    if params.system_prompt:
      logger.debug(f"SYSTEM_PROMPT environment variable is set to '{params.system_prompt}'")

    params.user_prompt = environ.get('USER_PROMPT', None)
    if params.user_prompt:
      logger.debug(f"USER_PROMPT environment variable is set to '{params.user_prompt}'")

    params.temperature = (args and args.temperature) or float(environ.get('TEMPERATURE', 0.2))

    params.input_po = (args and args.input_po) or environ.get('INPUT_PO', None)
    params.output_po = (args and args.output_po) or environ.get('OUTPUT_PO', None)

    params.fuzzy = (args and args.fuzzy) or environ.get('FUZZY', False)
    params.force = (args and args.force) or environ.get('FORCE', False)
    params.overwrite_output = (args and args.overwrite_output) or environ.get('OVERWRITE_OUTPUT', False)
    params.compile = (args and args.compile) or environ.get('COMPILE', False)

    params.owner = (args and args.owner) or environ.get('OWNER', '<OWNER>')
    params.owner_mail = (args and args.owner_mail) or environ.get('OWNER_MAIL', '<OWNER EMAIL>')

    params.show_prompts = False
    # generic processing of additional arguments
    if self.additional_args:
      for argument in self.additional_args:
        arg = argument.get('arg')
        if isinstance(arg, list):
          arg_ns = [arg_n for arg_n in arg if arg_n.startswith('--')]
          # tries to take the 1rst param starting with -- otherwise takes the 1rst param
          arg_name = arg_ns[0] if len(arg_ns) > 0 else arg[0]
        else:
          arg_name = arg
        arg_name = arg_name.lstrip('-').lower().replace('-', '_')
        val = getattr(args, arg_name) or environ.get(argument.get('env', 'UNDEFINED_VARIABLE'), argument.get('default', None))
        setattr(params, arg_name, val)

    return params

  def load(self) -> Params:
    "looks at args and returns an object with attributes of these args completed by the environ variables where needed"

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description=self.parser_description)
    # Add arguments
    self.add_parser_arguments(parser)
    # Analyze the arguments
    args = parser.parse_args()

    if args.show_prompts:
      params = Params()
      params.show_prompts = True
      return params  # will exit just after showing prompts, no need to continue

    # Update missing args from the .env file
    params = self.load_params_from_env(args)

    logger.info(f"Loaded Params: {params.__dict__}")
    return params


class ClientBuilder:
  _client = None

  def __init__(self, params):
    self.params = params

  def get_client(self):
    if not self._client:

      match self.params.llm_client:
        case 'ollama':
          from .clients.openai_ollama_client import OllamaClient as LLMClient
        case 'openai':
          # uses OpenAI GPT-4o by default
          from .clients.openai_ollama_client import OpenAIClient as LLMClient
        case 'claude':
          # uses Claude Sonnet 3.5 by default
          from .clients.claude_client import ClaudeClient as LLMClient
        case 'claude_cached':
          # uses Claude Sonnet 3.5, cached mode for long system prompts
          from .clients.claude_client import CachedClaudeClient as LLMClient
        case 'gemini':
          from .clients.gemini_client import GeminiClient as LLMClient
        case 'grok':
          from .clients.grok_client import GrokClient as LLMClient
        case _:
          raise Exception(
            f"LLM_CLIENT must be one of 'ollama', 'openai', 'claude' or 'claude_cached', not '{self.params.llm_client}'"
            )
      self._client = LLMClient(self.params, self.params.target_language if hasattr(self.params, 'target_language') else "")

    return self._client


def get_language_code(language_name):
    try:
        # Search language by name
        lang = langcodes.find(language_name)
        # Returns ISO 639-1 code (2 characters)
        return lang.language
    except LookupError:
        return None


def get_outfile_name(llm_client):

    """
    Compute the output file name based on the input file name and the target language code
    If the input file is in a directory like .../locale/<context_lang_code>/LC_MESSAGES/file.po,
    the output file will be in a directory like .../locale/<target_lang_code>/LC_MESSAGES/file.po
    Otherwise, the output file name will be the input file name with the model name and the target language code appended.
    If the output file already exists and llm_client.params.overwrite_output is False, a number will be appended to the
    filename to make it unique.

    Parameters
    ----------
    llm_client (LLMClient) : ClientBase
        The llm client to use

    Returns
    -------
    Path
        The output file name
    """
    p = Path(llm_client.params.input_po)
    parent = p.parent
    grandparent = parent.parent
    context_lang_code = get_language_code(llm_client.params.context_language) or 'xx'
    target_code = get_language_code(llm_client.target_language) or 'xx'
    if parent.name == 'LC_MESSAGES' and grandparent.name == context_lang_code:
      # we're in something like .../locale/<lang_code>/LC_MESSAGES/file.po
      # let's try to build the same with the target language code
      dir = grandparent.parent / target_code / 'LC_MESSAGES'
      # create the directory if it doesn't exist
      dir.mkdir(parents=True, exist_ok=True)
      outfile = dir / p.name
    else:  # otherwise, just add the model name and the target language code in the file name
      model_name = llm_client.params.model.replace(':', '-')
      outfile = p.with_suffix(f'.{model_name}.{target_code}.po')

    logger.info(f"Output file: {outfile}")
    if outfile.exists() and not llm_client.params.overwrite_output:
      logger.info("Output file already exists, won't overwrite.")
      i = 0
      i_outfile = outfile
      # append a number to the filename
      while i_outfile.exists():
        i_outfile = outfile.with_suffix(f'.{i}.po')
        i += 1
      outfile = i_outfile
      logger.info(f"Corrected output file: {outfile}")

    return outfile
