import sys

from pygame import K_UP, K_DOWN, K_RETURN

from . import TextRenderer


class MenuRenderer(TextRenderer):
    """
    Render menu options
    """
    def __init__(self, screen, option_texts):
        """
        Setup class variables and containers for text
        :param screen: Surface where the menu is rendered
        :param option_texts: List of all option texts
        """
        super().__init__(screen)
        self.active_color = (0, 158, 138)
        self.active_index = 0
        self.texts = option_texts
        self.menu_options = self.create_options(option_texts)
        self.menu_shown = True

    def create_options(self, option_list):
        """
        Create a menu option
        :param option_list A list of text for options that should be created
        :return A dictionary mapping every option surface to its relevant rectangle
        """
        half = len(option_list)/2
        options = {}
        for index, option in enumerate(option_list):
            if self.active_index == index:
                option_text = self.font.render(option, 1, self.active_color)
            else:
                option_text = self.font.render(option, 1, self.text_color)
            option_rect = option_text.get_rect()
            option_rect.x = self.width/2 - option_rect.width/2
            option_rect.y = self.height/2 - option_rect.height/2
            if index < half:
                option_rect.y -= (self.font_size * (half-index))
            else:
                option_rect.y += (self.font_size * (index-half))
            options[option_text] = {"text": option, 'rect': option_rect, 'order': index}
        return options

    def handle_key_press(self, user_input):
        """
        Handle key presses to navigate the menu
        """
        if user_input.key == K_UP:
            self.move_up()
        elif user_input.key == K_DOWN:
            self.move_down()
        elif user_input.key == K_RETURN:
            if self.active_index == 0:
                return True
            elif self.active_index == 1:
                self.menu_shown = False
            elif self.active_index == 3:
                sys.exit()

    def handle_return(self, user_input):
        """
        Handle returning from a sub-menu
        """
        if user_input.key == K_RETURN:
            self.menu_shown = True

    def move_down(self):
        """
        Rerender menu list with the active item now being below the previously active item
        """
        if self.active_index != len(self.texts)-1:
            self.active_index += 1
            self.menu_options = self.create_options(self.texts)

    def move_up(self):
        """
        Rerender menu list with the active item now being above the previously active item
        """
        if self.active_index != 0:
            self.active_index -= 1
            self.menu_options = self.create_options(self.texts)

    def render(self):
        """
        Render menu options
        """
        for option in self.menu_options:
            self.background.blit(option, self.menu_options[option]['rect'])
