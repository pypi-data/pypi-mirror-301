import json
import sys

class BaseCommand:

    def __init__(self):
        self.inputFile = sys.argv[1]
        self.outputFile = sys.argv[2]

    def command(self, input_json):
        return ''

    def pushStreamResult(self, result):
        with open(self.outputFile, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)

    def run(self):
        with open(self.inputFile, 'r', encoding='utf-8') as file:
            data = file.read()
        # 入口参数
        input_json = json.loads(data)
        output_json = self.command(input_json)
        with open(self.outputFile, 'w', encoding='utf-8') as file:
            json.dump(output_json, file, indent=4)
