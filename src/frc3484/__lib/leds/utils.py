from wpilib import Color

def correct_gamma(self, color: Color) -> Color:
    return Color(color.red** self._gamma, color.green**self._gamma, color.blue**self._gamma)