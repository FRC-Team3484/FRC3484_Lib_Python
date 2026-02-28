from wpilib import Color

def correct_gamma(color: Color, gamma: float) -> Color:
    return Color(color.red** gamma, color.green** gamma, color.blue** gamma)