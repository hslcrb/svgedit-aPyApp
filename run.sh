#!/bin/bash
# 스크립트가 위치한 디렉토리 가져오기 / Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# 가상 환경이 존재하면 활성화 / Activate virtual environment if it exists
if [ -f "app/venv/bin/activate" ]; then
    source app/venv/bin/activate
elif [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# 애플리케이션 실행 / Run the application
# 필요한 경우 import가 작동하도록 PYTHONPATH 사용 / Use PYTHONPATH to ensure imports work if necessary
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/app

python3 app/main.py "$@"
