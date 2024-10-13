import argparse
import os
import re  # Import re for regular expressions
from dotenv import load_dotenv, set_key
from .core import SQL
from .config import load_config

# Load environment variables
load_dotenv()

def search_env_var_regex(pattern):
    """
    Search for environment variables that match the specified regex pattern.
    """
    result = {}
    for key, value in os.environ.items():
        if re.search(pattern, key):
            result[key] = value
    return result

def update_env_var_regex(pattern, value):
    """
    Update the value of environment variables that match the specified regex pattern.
    """
    dotenv_path = os.getenv('DOTENV_PATH', '.env')  # Default to .env file
    updated = False  # Track if any variables were updated

    for key in os.environ.keys():
        if re.search(pattern, key):
            # Update environment variable in .env file
            set_key(dotenv_path, key, value)
            os.environ[key] = value  # Update current environment
            print(f"Environment variable {key} has been updated to {value}")
            updated = True

    if not updated:
        print(f"No environment variables matched the pattern '{pattern}'")

def show_help():
    """
    Display detailed usage instructions.
    """
    help_text = """
    dsqlenv: A Simple SQL Database Operation Tool

    Usage:
      dsqlenv db --action [get|insert|update|delete] --id <Record ID> --data <Record data>
      dsqlenv search-env --keyword <Search keyword>
      dsqlenv update-env --key <Environment variable key> --value <New value>
      dsqlenv re search <regex>      # Search for environment variables by regex
      dsqlenv re update <regex> <value> # Update environment variables by regex
      dsqlenv s <keyword>            # Shortcut for search-env
      dsqlenv u <key> <value>        # Shortcut for update-env

    Available Commands:
      db           Perform database operations such as get, insert, update, and delete.
                   --action: Choose between 'get', 'insert', 'update', 'delete'.
                   --id: Record ID for the operation (required for 'get', 'update', 'delete').
                   --data: Data to be inserted or updated (required for 'insert', 'update').

      search-env   Search for environment variables containing the specified keyword (case insensitive).
                   --keyword: The keyword to search for.

      update-env   Update a specific environment variable value.
                   --key: The environment variable to update.
                   --value: The new value for the environment variable.

      re           Perform regex operations on environment variables.
                   search <regex>: Search for environment variables matching the regex.
                   update <regex> <value>: Update environment variables matching the regex.

    Examples:
      # Search from db
      dsqlenv db --action get --id deepseek_base_url
      dsqlenv db get deepseek_base_url

      # Update db
        dsqlenv db --action update --id deepseek_base_url --data new_url
        dsqlenv db update deepseek_base_url new_url

      # Search from env
      dsqlenv search-env --keyword SECRET
      dsqlenv s SECRET
      
      # Update env
      dsqlenv update-env --key API_KEY --value new_value
      dsqlenv u API_KEY new_value
      
      # Search and update using regex (only for env)
      dsqlenv re search '^SECRET'
      dsqlenv re update '^API_' 'new_value'
      
    Help Flags:
      -h, --h, -help, --help   Show this detailed help message.
    """
    print(help_text)

def main():
    parser = argparse.ArgumentParser(description="dsqlenv is a simple SQL database operation tool.", add_help=False)

    # Custom help flags
    if any(arg in ['-h', '--h', '-help', '--help'] for arg in os.sys.argv):
        show_help()
        return

    subparsers = parser.add_subparsers(dest="command")

    # Database operation commands
    db_parser = subparsers.add_parser('db', help="Database operations: get, insert, update, delete")
    db_subparsers = db_parser.add_subparsers(dest="action")

    # Short forms for database actions
    get_parser = db_subparsers.add_parser('get', help="Get record")
    get_parser.add_argument('id', help="Record ID")

    insert_parser = db_subparsers.add_parser('insert', help="Insert record")
    insert_parser.add_argument('id', help="Record ID")
    insert_parser.add_argument('data', help="Record data")

    update_parser = db_subparsers.add_parser('update', help="Update record")
    update_parser.add_argument('id', help="Record ID")
    update_parser.add_argument('data', help="Record data")

    delete_parser = db_subparsers.add_parser('delete', help="Delete record")
    delete_parser.add_argument('id', help="Record ID")

    # Environment variable search command
    env_search_parser = subparsers.add_parser('search-env', help="Search environment variables by keyword")
    env_search_parser.add_argument('--keyword', required=True, help="Keyword to search in environment variables")

    # Environment variable update command
    env_update_parser = subparsers.add_parser('update-env', help="Update an environment variable")
    env_update_parser.add_argument('--key', required=True, help="The environment variable to update")
    env_update_parser.add_argument('--value', required=True, help="The new value for the environment variable")

    # Regex commands
    regex_parser = subparsers.add_parser('re', help="Regex operations on environment variables")
    regex_subparsers = regex_parser.add_subparsers(dest="regex_command")

    re_search_parser = regex_subparsers.add_parser('search', help="Search environment variables using regex")
    re_search_parser.add_argument('pattern', help="Regex pattern to search for")

    re_update_parser = regex_subparsers.add_parser('update', help="Update environment variables using regex")
    re_update_parser.add_argument('pattern', help="Regex pattern to match")
    re_update_parser.add_argument('value', help="New value for the environment variable")

    # Shortcuts
    s_parser = subparsers.add_parser('s', help="Shortcut for search-env")
    s_parser.add_argument('keyword', help="Keyword to search in environment variables")

    u_parser = subparsers.add_parser('u', help="Shortcut for update-env")
    u_parser.add_argument('key', help="The environment variable to update")
    u_parser.add_argument('value', help="The new value for the environment variable")

    args = parser.parse_args()

    if args.command == 'db':
        config = load_config()
        db = SQL(config)

        if args.action == 'get' and args.id:
            result = db.get_data_by_id(args.id)
            print(result)
        elif args.action == 'insert' and args.id and args.data:
            db.insert_data(args.id, args.data)
            print(f"Record with ID {args.id} has been inserted.")
        elif args.action == 'update' and args.id and args.data:
            db.update_data(args.id, args.data)
            print(f"Record with ID {args.id} has been updated.")
        elif args.action == 'delete' and args.id:
            db.delete_data(args.id)
            print(f"Record with ID {args.id} has been deleted.")
        else:
            raise ValueError("Invalid action")

    elif args.command == 'search-env' or args.command == 's':
        result = search_env_var(args.keyword)
        if result:
            print("Search results:")
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(f"No environment variables found matching the keyword '{args.keyword}'")

    elif args.command == 'update-env' or args.command == 'u':
        update_env_var(args.key, args.value)

    elif args.command == 're':
        if args.regex_command == 'search':
            result = search_env_var_regex(args.pattern)
            if result:
                print("Search results:")
                for key, value in result.items():
                    print(f"{key}: {value}")
            else:
                print(f"No environment variables found matching the regex pattern '{args.pattern}'")
        
        elif args.regex_command == 'update':
            update_env_var_regex(args.pattern, args.value)

    else:
        parser.print_help()

if __name__ == '__main__':
    main()
