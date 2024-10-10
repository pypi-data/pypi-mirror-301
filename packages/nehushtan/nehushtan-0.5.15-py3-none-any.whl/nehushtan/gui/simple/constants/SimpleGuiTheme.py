from PySimpleGUI import LOOK_AND_FEEL_TABLE


class SimpleGuiTheme:

    def __init__(self, theme_name: str):
        self.__theme_name = theme_name

    def get_theme_name(self) -> str:
        return self.__theme_name

    @staticmethod
    def use_system_default():
        return SimpleGuiTheme("SystemDefault")

    @staticmethod
    def use_system_default_for_real():
        return SimpleGuiTheme("SystemDefaultForReal")

    @staticmethod
    def use_system_default_1():
        return SimpleGuiTheme("SystemDefault1")

    @staticmethod
    def use_material_1():
        return SimpleGuiTheme("Material1")

    @staticmethod
    def use_material_2():
        return SimpleGuiTheme("Material2")

    @staticmethod
    def use_reddit():
        return SimpleGuiTheme("Reddit")

    @staticmethod
    def use_topanga():
        return SimpleGuiTheme("Topanga")

    @staticmethod
    def use_green_tan():
        return SimpleGuiTheme("GreenTan")

    @staticmethod
    def use_dark():
        return SimpleGuiTheme("Dark")

    @staticmethod
    def use_light_green():
        return SimpleGuiTheme("LightGreen")

    @staticmethod
    def use_dark_2():
        return SimpleGuiTheme("Dark2")

    @staticmethod
    def use_black():
        return SimpleGuiTheme("Black")

    @staticmethod
    def use_tan():
        return SimpleGuiTheme("Tan")

    @staticmethod
    def use_tan_blue():
        return SimpleGuiTheme("TanBlue")

    @staticmethod
    def use_dark_tan_blue():
        return SimpleGuiTheme("DarkTanBlue")

    @staticmethod
    def use_dark_amber():
        return SimpleGuiTheme("DarkAmber")

    @staticmethod
    def use_dark_blue():
        return SimpleGuiTheme("DarkBlue")

    @staticmethod
    def use_reds():
        return SimpleGuiTheme("Reds")

    @staticmethod
    def use_green():
        return SimpleGuiTheme("Green")

    @staticmethod
    def use_blue_purple():
        return SimpleGuiTheme("BluePurple")

    @staticmethod
    def use_purple():
        return SimpleGuiTheme("Purple")

    @staticmethod
    def use_blue_mono():
        return SimpleGuiTheme("BlueMono")

    @staticmethod
    def use_green_mono():
        return SimpleGuiTheme("GreenMono")

    @staticmethod
    def use_brown_blue():
        return SimpleGuiTheme("BrownBlue")

    @staticmethod
    def use_bright_colors():
        return SimpleGuiTheme("BrightColors")

    @staticmethod
    def use_neutral_blue():
        return SimpleGuiTheme("NeutralBlue")

    @staticmethod
    def use_kayak():
        return SimpleGuiTheme("Kayak")

    @staticmethod
    def use_sandy_beach():
        return SimpleGuiTheme("SandyBeach")

    @staticmethod
    def use_teal_mono():
        return SimpleGuiTheme("TealMono")

    @staticmethod
    def use_default():
        return SimpleGuiTheme("Default")

    @staticmethod
    def use_default_1():
        return SimpleGuiTheme("Default1")

    @staticmethod
    def use_default_no_more_nagging():
        return SimpleGuiTheme("DefaultNoMoreNagging")

    @staticmethod
    def use_gray_gray_gray():
        return SimpleGuiTheme("GrayGrayGray")

    @staticmethod
    def use_light_blue():
        return SimpleGuiTheme("LightBlue")

    @staticmethod
    def use_light_grey():
        return SimpleGuiTheme("LightGrey")

    @staticmethod
    def use_light_grey_1():
        return SimpleGuiTheme("LightGrey1")

    @staticmethod
    def use_dark_brown():
        return SimpleGuiTheme("DarkBrown")

    @staticmethod
    def use_light_green_1():
        return SimpleGuiTheme("LightGreen1")

    @staticmethod
    def use_dark_grey():
        return SimpleGuiTheme("DarkGrey")

    @staticmethod
    def use_light_green_2():
        return SimpleGuiTheme("LightGreen2")

    @staticmethod
    def use_dark_grey_1():
        return SimpleGuiTheme("DarkGrey1")

    @staticmethod
    def use_dark_black():
        return SimpleGuiTheme("DarkBlack")

    @staticmethod
    def use_light_brown():
        return SimpleGuiTheme("LightBrown")

    @staticmethod
    def use_light_brown_1():
        return SimpleGuiTheme("LightBrown1")

    @staticmethod
    def use_dark_blue_1():
        return SimpleGuiTheme("DarkBlue1")

    @staticmethod
    def use_dark_brown_1():
        return SimpleGuiTheme("DarkBrown1")

    @staticmethod
    def use_dark_blue_2():
        return SimpleGuiTheme("DarkBlue2")

    @staticmethod
    def use_dark_brown_2():
        return SimpleGuiTheme("DarkBrown2")

    @staticmethod
    def use_dark_green():
        return SimpleGuiTheme("DarkGreen")

    @staticmethod
    def use_light_blue_1():
        return SimpleGuiTheme("LightBlue1")

    @staticmethod
    def use_light_purple():
        return SimpleGuiTheme("LightPurple")

    @staticmethod
    def use_light_blue_2():
        return SimpleGuiTheme("LightBlue2")

    @staticmethod
    def use_light_green_3():
        return SimpleGuiTheme("LightGreen3")

    @staticmethod
    def use_dark_blue_3():
        return SimpleGuiTheme("DarkBlue3")

    @staticmethod
    def use_light_green_4():
        return SimpleGuiTheme("LightGreen4")

    @staticmethod
    def use_light_green_5():
        return SimpleGuiTheme("LightGreen5")

    @staticmethod
    def use_light_brown_2():
        return SimpleGuiTheme("LightBrown2")

    @staticmethod
    def use_light_brown_3():
        return SimpleGuiTheme("LightBrown3")

    @staticmethod
    def use_light_blue_3():
        return SimpleGuiTheme("LightBlue3")

    @staticmethod
    def use_light_brown_4():
        return SimpleGuiTheme("LightBrown4")

    @staticmethod
    def use_dark_teal():
        return SimpleGuiTheme("DarkTeal")

    @staticmethod
    def use_dark_purple():
        return SimpleGuiTheme("DarkPurple")

    @staticmethod
    def use_light_green_6():
        return SimpleGuiTheme("LightGreen6")

    @staticmethod
    def use_dark_grey_2():
        return SimpleGuiTheme("DarkGrey2")

    @staticmethod
    def use_light_brown_6():
        return SimpleGuiTheme("LightBrown6")

    @staticmethod
    def use_dark_teal_1():
        return SimpleGuiTheme("DarkTeal1")

    @staticmethod
    def use_light_brown_7():
        return SimpleGuiTheme("LightBrown7")

    @staticmethod
    def use_dark_purple_1():
        return SimpleGuiTheme("DarkPurple1")

    @staticmethod
    def use_dark_grey_3():
        return SimpleGuiTheme("DarkGrey3")

    @staticmethod
    def use_light_brown_8():
        return SimpleGuiTheme("LightBrown8")

    @staticmethod
    def use_dark_blue_4():
        return SimpleGuiTheme("DarkBlue4")

    @staticmethod
    def use_light_blue_4():
        return SimpleGuiTheme("LightBlue4")

    @staticmethod
    def use_dark_teal_2():
        return SimpleGuiTheme("DarkTeal2")

    @staticmethod
    def use_dark_teal_3():
        return SimpleGuiTheme("DarkTeal3")

    @staticmethod
    def use_dark_purple_5():
        return SimpleGuiTheme("DarkPurple5")

    @staticmethod
    def use_dark_purple_2():
        return SimpleGuiTheme("DarkPurple2")

    @staticmethod
    def use_dark_blue_5():
        return SimpleGuiTheme("DarkBlue5")

    @staticmethod
    def use_light_grey_2():
        return SimpleGuiTheme("LightGrey2")

    @staticmethod
    def use_light_grey_3():
        return SimpleGuiTheme("LightGrey3")

    @staticmethod
    def use_dark_blue_6():
        return SimpleGuiTheme("DarkBlue6")

    @staticmethod
    def use_dark_blue_7():
        return SimpleGuiTheme("DarkBlue7")

    @staticmethod
    def use_light_brown_9():
        return SimpleGuiTheme("LightBrown9")

    @staticmethod
    def use_dark_purple_3():
        return SimpleGuiTheme("DarkPurple3")

    @staticmethod
    def use_light_brown_10():
        return SimpleGuiTheme("LightBrown10")

    @staticmethod
    def use_dark_purple_4():
        return SimpleGuiTheme("DarkPurple4")

    @staticmethod
    def use_light_blue_5():
        return SimpleGuiTheme("LightBlue5")

    @staticmethod
    def use_dark_teal_4():
        return SimpleGuiTheme("DarkTeal4")

    @staticmethod
    def use_light_teal():
        return SimpleGuiTheme("LightTeal")

    @staticmethod
    def use_dark_teal_5():
        return SimpleGuiTheme("DarkTeal5")

    @staticmethod
    def use_light_grey_4():
        return SimpleGuiTheme("LightGrey4")

    @staticmethod
    def use_light_green_7():
        return SimpleGuiTheme("LightGreen7")

    @staticmethod
    def use_light_grey_5():
        return SimpleGuiTheme("LightGrey5")

    @staticmethod
    def use_dark_brown_3():
        return SimpleGuiTheme("DarkBrown3")

    @staticmethod
    def use_light_brown1_1():
        return SimpleGuiTheme("LightBrown11")

    @staticmethod
    def use_dark_red():
        return SimpleGuiTheme("DarkRed")

    @staticmethod
    def use_dark_teal_6():
        return SimpleGuiTheme("DarkTeal6")

    @staticmethod
    def use_dark_brown_4():
        return SimpleGuiTheme("DarkBrown4")

    @staticmethod
    def use_light_yellow():
        return SimpleGuiTheme("LightYellow")

    @staticmethod
    def use_dark_green_1():
        return SimpleGuiTheme("DarkGreen1")

    @staticmethod
    def use_light_green_8():
        return SimpleGuiTheme("LightGreen8")

    @staticmethod
    def use_dark_teal_7():
        return SimpleGuiTheme("DarkTeal7")

    @staticmethod
    def use_dark_blue_8():
        return SimpleGuiTheme("DarkBlue8")

    @staticmethod
    def use_dark_blue_9():
        return SimpleGuiTheme("DarkBlue9")

    @staticmethod
    def use_dark_blue_10():
        return SimpleGuiTheme("DarkBlue10")

    @staticmethod
    def use_dark_blue_11():
        return SimpleGuiTheme("DarkBlue11")

    @staticmethod
    def use_dark_teal_8():
        return SimpleGuiTheme("DarkTeal8")

    @staticmethod
    def use_dark_red_1():
        return SimpleGuiTheme("DarkRed1")

    @staticmethod
    def use_light_brown_5():
        return SimpleGuiTheme("LightBrown5")

    @staticmethod
    def use_light_green_9():
        return SimpleGuiTheme("LightGreen9")

    @staticmethod
    def use_dark_green_2():
        return SimpleGuiTheme("DarkGreen2")

    @staticmethod
    def use_light_gray_1():
        return SimpleGuiTheme("LightGray1")

    @staticmethod
    def use_dark_grey_4():
        return SimpleGuiTheme("DarkGrey4")

    @staticmethod
    def use_dark_blue_12():
        return SimpleGuiTheme("DarkBlue12")

    @staticmethod
    def use_dark_purple_6():
        return SimpleGuiTheme("DarkPurple6")

    @staticmethod
    def use_dark_purple_7():
        return SimpleGuiTheme("DarkPurple7")

    @staticmethod
    def use_dark_blue_13():
        return SimpleGuiTheme("DarkBlue13")

    @staticmethod
    def use_dark_brown_5():
        return SimpleGuiTheme("DarkBrown5")

    @staticmethod
    def use_dark_green_3():
        return SimpleGuiTheme("DarkGreen3")

    @staticmethod
    def use_dark_black_1():
        return SimpleGuiTheme("DarkBlack1")

    @staticmethod
    def use_dark_grey_5():
        return SimpleGuiTheme("DarkGrey5")

    @staticmethod
    def use_light_brown_12():
        return SimpleGuiTheme("LightBrown12")

    @staticmethod
    def use_dark_teal_9():
        return SimpleGuiTheme("DarkTeal9")

    @staticmethod
    def use_dark_blue_14():
        return SimpleGuiTheme("DarkBlue14")

    @staticmethod
    def use_light_blue_6():
        return SimpleGuiTheme("LightBlue6")

    @staticmethod
    def use_dark_green_4():
        return SimpleGuiTheme("DarkGreen4")

    @staticmethod
    def use_dark_green_5():
        return SimpleGuiTheme("DarkGreen5")

    @staticmethod
    def use_dark_teal_10():
        return SimpleGuiTheme("DarkTeal10")

    @staticmethod
    def use_dark_grey_6():
        return SimpleGuiTheme("DarkGrey6")

    @staticmethod
    def use_dark_teal_11():
        return SimpleGuiTheme("DarkTeal11")

    @staticmethod
    def use_light_blue_7():
        return SimpleGuiTheme("LightBlue7")

    @staticmethod
    def use_light_green_10():
        return SimpleGuiTheme("LightGreen10")

    @staticmethod
    def use_dark_blue_15():
        return SimpleGuiTheme("DarkBlue15")

    @staticmethod
    def use_dark_blue_16():
        return SimpleGuiTheme("DarkBlue16")

    @staticmethod
    def use_dark_teal_12():
        return SimpleGuiTheme("DarkTeal12")

    @staticmethod
    def use_light_brown_13():
        return SimpleGuiTheme("LightBrown13")

    @staticmethod
    def use_dark_blue_17():
        return SimpleGuiTheme("DarkBlue17")

    @staticmethod
    def use_dark_brown_6():
        return SimpleGuiTheme("DarkBrown6")

    @staticmethod
    def use_dark_green_6():
        return SimpleGuiTheme("DarkGreen6")

    @staticmethod
    def use_dark_green_7():
        return SimpleGuiTheme("DarkGreen7")

    @staticmethod
    def use_dark_grey_7():
        return SimpleGuiTheme("DarkGrey7")

    @staticmethod
    def use_dark_red_2():
        return SimpleGuiTheme("DarkRed2")

    @staticmethod
    def use_light_grey_6():
        return SimpleGuiTheme("LightGrey6")

    @staticmethod
    def use_hot_dog_stand():
        return SimpleGuiTheme("HotDogStand")

    @staticmethod
    def use_dark_grey_8():
        return SimpleGuiTheme("DarkGrey8")

    @staticmethod
    def use_dark_grey_9():
        return SimpleGuiTheme("DarkGrey9")

    @staticmethod
    def use_dark_grey_10():
        return SimpleGuiTheme("DarkGrey10")

    @staticmethod
    def use_dark_grey_11():
        return SimpleGuiTheme("DarkGrey11")

    @staticmethod
    def use_dark_grey_12():
        return SimpleGuiTheme("DarkGrey12")

    @staticmethod
    def use_dark_grey_13():
        return SimpleGuiTheme("DarkGrey13")

    @staticmethod
    def use_dark_grey_14():
        return SimpleGuiTheme("DarkGrey14")

    @staticmethod
    def use_dark_grey_15():
        return SimpleGuiTheme("DarkGrey15")

    @staticmethod
    def use_dark_brown_7():
        return SimpleGuiTheme("DarkBrown7")

    @staticmethod
    def use_python():
        return SimpleGuiTheme("Python")

    @staticmethod
    def use_python_plus():
        return SimpleGuiTheme("PythonPlus")


if __name__ == '__main__':
    for key in LOOK_AND_FEEL_TABLE.keys():
        print(f'@staticmethod\ndef use{key}():\n    return SimpleGuiTheme("{key}")\n\n')
