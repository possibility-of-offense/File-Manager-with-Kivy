import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, BooleanProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import os


class InfoWindow(Screen):
    info_results = ObjectProperty(None)

    def on_pre_enter(self, *args):
        try:
            with open(f'{TutorialOperations.__name__.lower()}.txt', 'r') as f_handle:
                self.info_results.text = ''

                if os.stat(f'{TutorialOperations.__name__.lower()}.txt').st_size == 0:
                    self.info_results.text = 'THE FILE IS STILL EMPTY'

                for line in f_handle:
                    self.info_results.text += line.rstrip() + '\n'
        except:
            self.info_results.text = 'THE FILE IS NOT CREATED YET!'


class TutorialGrid(Screen):
    tutorial_name = ObjectProperty(None)
    add_btn = ObjectProperty(None)
    put_in_queue = ObjectProperty(None)
    output = ObjectProperty(None)
    toggle_uppercase = ObjectProperty(None)
    output_results = ObjectProperty(None)
    info_buttons = ObjectProperty(None)

    to_uppercase = BooleanProperty(False)

    info = ListProperty([])
    temp_info = ListProperty([])

    #
    # Event Handlers
    #

    # Handle add button
    def handle_add_btn(self):
        self.output_results.text = ''
        self.output_results.opacity = 0

        if self.check_if_input_is_empty():
            pass
        else:
            pass
            # if self.tutorial_name.text != '' and len(self.info) == 0:
            #     self.show_output_cb('You need to put something in the queue first!')
            #     return

        self.output.height = (36 * len(self.info))

        separate_on_single_lines = "\n".join(self.info)
        self.show_output_cb(f'Info added')
        self.output_results.opacity = 1

        for item in range(len(self.info)):
            self.output_results.text += f'{item + 1}:  ' + self.info[item] + ', '
            if item == len(self.info) - 1 and len(self.info) > 1:
                self.output_results.text += f' {item + 1}:  ' + self.info[item] + '!'

        if len(self.info) > 0:
            self.handle_append_to_file()
            self.info = list()
            self.to_uppercase = False
            self.toggle_uppercase.state = 'normal'
            self.toggle_uppercase.background_color = 1, 1, 1, 1
            self.toggle_uppercase.background_down = 'atlas://data/images/defaulttheme/button_pressed'
            self.toggle_uppercase.text = 'Make all items uppercased'

            for child in [child for child in self.info_buttons.children]:
                self.info_buttons.remove_widget(child)

            self.toggle_uppercase.disabled = True
            self.toggle_uppercase.background_color = (0.7, 0, 0, 0.9)


    # Handle press on Tutorial Name TextInput
    def handle_press_tutorial_name(self):
        if self.check_if_input_is_empty():
            return

        self.handle_put_in_queue()
        self.tutorial_name.text_validate_unfocus = False
        self.tutorial_name.focus = True

    # Add items to the info list()
    def handle_put_in_queue(self):
        if self.check_if_input_is_empty():
            return

        self.toggle_uppercase.disabled = False
        self.toggle_uppercase.background_color = (1, 1, 1, 1)
        self.modify_inst_properties(self.info, 'append', self.tutorial_name.text)

        if len(self.info) >= 3:
            self.info_buttons.spacing = 10

        self.show_output_cb(f'{self.tutorial_name.text.strip()} added in the queue')
        self.tutorial_name.text = ''

        self.refill_output_results()
        self.output_results.opacity = 0

    # Remove from list
    def handle_remove_from_list(self, inst, ind):
        self.info.pop(ind)

        self.refill_output_results()

    # Handle Clear File
    def handle_clear_file(self):
        with open(f'{TutorialOperations.__name__.lower()}.txt', 'w') as f_handle:
            f_handle.close()

            self.show_output_cb('The file was cleared!')
            self.output_results.opacity = 0

    # Append to file | create if it is not
    def handle_append_to_file(self):
        with open(f'{TutorialOperations.__name__.lower()}.txt', 'a', encoding='utf-8') as f_handle:
            for item in self.info:
                f_handle.write(f'{item}\n')

            self.info = list()

    # Make some items uppercase
    def handle_upper_items(self):
        if len(self.info) == 0:
            return

        self.to_uppercase = not self.to_uppercase

        if self.to_uppercase:
            self.temp_info = self.info
            self.modify_list_items(self.info, lambda x: x.upper())
            self.toggle_uppercase.text = 'Restore the case for all items'

            if self.toggle_uppercase.state == 'down':
                self.toggle_uppercase.background_color = 0, 1, 1, .4
                self.toggle_uppercase.background_down = ''

        else:
            self.toggle_uppercase.background_color = 1, 1, 1, 1
            self.toggle_uppercase.background_down = 'atlas://data/images/defaulttheme/button_pressed'
            self.toggle_uppercase.text = 'Make all items uppercased'

            self.info = self.temp_info

    #
    # Additional Methods
    #

    # Check if input is empty
    def check_if_input_is_empty(self):
        if self.tutorial_name.text.strip() == '' and len(self.info) == 0:
            self.show_output_cb('Fill the input')
            self.tutorial_name.focus = True
            return True
        elif self.tutorial_name.text.strip() == '':
            return True
        else:
            return False

    # Setting text to the input
    def show_output_cb(self, msg):
        self.output.height = 40
        self.output.text = msg

    # Function to modify some instance properties
    def modify_inst_properties(self, prop, operator, data):
        if prop is self.info:
            if operator == 'append':
                if data.strip() != '':
                    prop.append(data.strip())
            # add operator for changing some item

    # Modify List Items
    def modify_list_items(self, lst, cb):
        self.info = list(map(cb, lst))

    # Rearrange the output results
    def refill_output_results(self):
        for child in [child for child in self.info_buttons.children]:
            self.info_buttons.remove_widget(child)

        if len(self.info) > 11:
            for item_ind in range(len(self.info[-12:])):
                btn = Button(text=self.info[-12:][item_ind])
                btn.bind(on_press=lambda *args: self.handle_remove_from_list(*args, item_ind))
                self.info_buttons.add_widget(btn)
        else:
            for item_ind in range(len(self.info)):
                btn = Button(text=self.info[item_ind])
                btn.bind(on_press=lambda *args: self.handle_remove_from_list(*args, item_ind))
                self.info_buttons.add_widget(btn)

        if len(self.info) == 0:
            self.show_output_cb('No items in the queue')
            self.toggle_uppercase.disabled = True
            self.toggle_uppercase.background_color = (0.7, 0, 0, 0.9)


class WindowManager(ScreenManager):

    pass


kv = Builder.load_file('ventsi.kv')


# Main Class
class TutorialOperations(App):
    def __init__(self, dims_size):
        super().__init__()
        self.dims_size = dims_size

    def build(self):
        # return TutorialGrid()
        return kv

if __name__ == '__main__':
    TutorialOperations((800, 200)).run()
