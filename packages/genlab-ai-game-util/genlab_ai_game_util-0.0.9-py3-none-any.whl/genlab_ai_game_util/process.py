import json
import sys
import os


class BaseCommand:

    def __init__(self):
        # 获取所有环境变量
        env_vars = os.environ

        self.inputFile = sys.argv[1]
        self.outputFile = sys.argv[2]
        self.streamIdx = 0
        self.jdkToPythonEvn = json.loads(env_vars['__AI_ENV__'])
        # 输出所有环境变量
        for key, value in env_vars.items():
            print(f'{key}: {value}')

    # 获取jdk传递进来的环境变量
    def getEnv(self):
        return self.jdkToPythonEvn;

    def command(self, input_json):
        return ''

    def pushStreamResult(self, streamResult):
        idx = self.streamIdx
        self.streamIdx = self.streamIdx + 1
        # 开始流
        result = {
            # 0代表运行成功
            'resultCode': 0,
            # 流方式
            'stream': True,
            'streamFinish': False,
            'streamIdx': self.streamIdx
        }
        with open(self.outputFile, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)

        with open(self.outputFile + "_" + str(idx), 'w', encoding='utf-8') as file:
            json.dump(streamResult, file, indent=4)

    def run(self):
        try:
            with open(self.inputFile, 'r', encoding='utf-8') as file:
                data = file.read()
            # 入口参数
            input_json = json.loads(data)
            output_json = self.command(input_json)
            # 如果使用了流的方式
            if self.streamIdx > 0:
                output_json = {
                    # 0代表运行成功
                    'resultCode': 0,
                    # 流方式
                    'stream': True,
                    'streamFinish': True,
                    'streamIdx': self.streamIdx
                }
            with open(self.outputFile, 'w', encoding='utf-8') as file:
                json.dump(output_json, file, indent=4)
        except Exception as e:
            print(f"run python error :{e}")

