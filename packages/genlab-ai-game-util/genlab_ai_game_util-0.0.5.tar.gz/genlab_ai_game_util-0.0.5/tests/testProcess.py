from genlab_ai_game_util.process import BaseCommand


class My(BaseCommand):
    def command(self, intput_json):
        return f"{self.name} says meow!"


if __name__ == '__main__':
    My().run()