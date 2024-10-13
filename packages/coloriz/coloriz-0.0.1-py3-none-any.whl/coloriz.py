# coloriz by .qmt

class Color:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    RESET = "\033[0m"

    red_to_magenta = "RedToMagenta"
    blue_to_cyan = "BlueToCyan"
    green_to_yellow = "GreenToYellow"
    red_to_yellow = "RedToYellow"
    blue_to_magenta = "BlueToMagenta"
    cyan_to_blue = "CyanToBlue"
    blue_to_red = "BlueToRed"
    red_to_blue = "RedToBlue"

    PREDEFINED_MIXES = {
        red_to_magenta: (RED, MAGENTA),
        blue_to_cyan: (BLUE, CYAN),
        green_to_yellow: (GREEN, YELLOW),
        red_to_yellow: (RED, YELLOW),
        blue_to_magenta: (BLUE, MAGENTA),
        cyan_to_blue: (CYAN, BLUE),
        blue_to_red:(BLUE, RED),
        red_to_blue:(RED,BLUE)
    }

    @classmethod
    def colored(cls, text, color):
        return f"{color}{text}{cls.RESET}"

    @staticmethod
    def custom(text, color1, color2):
        gradient_text = ""
        length = len(text)

        for i in range(length):
            ratio = i / (length - 1)
            r = int((1 - ratio) * Color._get_rgb(color1)[0] + ratio * Color._get_rgb(color2)[0])
            g = int((1 - ratio) * Color._get_rgb(color1)[1] + ratio * Color._get_rgb(color2)[1])
            b = int((1 - ratio) * Color._get_rgb(color1)[2] + ratio * Color._get_rgb(color2)[2])
            gradient_color = f"\033[38;2;{r};{g};{b}m"
            gradient_text += f"{gradient_color}{text[i]}"

        return f"{gradient_text}{Color.RESET}"

    @staticmethod
    def _get_rgb(color):
        color_map = {
            Color.RED: (255, 0, 0),
            Color.GREEN: (0, 255, 0),
            Color.YELLOW: (255, 255, 0),
            Color.BLUE: (0, 0, 255),
            Color.MAGENTA: (255, 0, 255),
            Color.CYAN: (0, 255, 255),
            Color.WHITE: (255, 255, 255),
        }
        return color_map.get(color, (255, 255, 255))

    @classmethod
    def gradient(cls, mix_name, text):
        if mix_name in cls.PREDEFINED_MIXES:
            color1, color2 = cls.PREDEFINED_MIXES[mix_name]
            return cls.custom(text, color1, color2)
        else:
            raise ValueError(f" {mix_name} n'existe pas. listes des couleurs : {', '.join(cls.PREDEFINED_MIXES.keys())}")

    
