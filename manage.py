import sys

from app.bootstrap import create_app
from app.helpers import get_config_object

env = sys.argv[3] if len(sys.argv) > 3 else 'local'
config = get_config_object(env)
app = create_app(config)
host = sys.argv[1] if len(sys.argv) >= 2 else '127.0.0.1'
port = int(sys.argv[2]) if len(sys.argv) >= 3 else '8000'

app.run(host=host, port=port, workers=app.config.get('WORKERS'))
