import sys
from tkinter import Button, Checkbutton, Frame, IntVar, LEFT, Label, Menu, Tk, simpledialog

from PIL import Image, ImageTk

from constant import ADD, B, BRIGHTNESS, DIVISION, G, GAUSSIAN_BLUR_FILTER, GREYSCALE_1, GREYSCALE_2, MEDIAN_FILTER, \
    MULTIPLICATION, R, SHARP_CUT_FILTER, SMOOTHING_FILTER, SOBEL_FILTER, SUBTRACTION, WEAVE_MASKS
from operation import add_operation, brightness_operation, divide_operation, multiply_operation, subtract_operation


def load_file():
    print('Load file')


def save_file():
    print('Save file')


def reset(image, modified_label):
    photo_copy = ImageTk.PhotoImage(image)
    modified_label.config(image=photo_copy)
    modified_label.image = photo_copy  # keep a reference!


def create_button(root, text, action=None):
    button = Button(root, text=text, command=action)
    button.pack(side=LEFT, padx=2, pady=2)


def ask_for_value(title, parent, min_value=0, max_value=255):
    return simpledialog.askinteger(title, 'Enter the value', parent=parent, minvalue=min_value, maxvalue=max_value)


class Transformation:

    def __init__(self, master):
        menu = Menu(master)
        master.config(menu=menu)

        sub_menu_file = Menu(menu)
        menu.add_cascade(label='File', menu=sub_menu_file)
        sub_menu_file.add_command(label='Load', command=load_file)
        sub_menu_file.add_command(label='Save', command=save_file)
        sub_menu_file.add_separator()
        sub_menu_file.add_command(label='Exit', command=sys.exit)

        menu.add_command(label='Reset', command=lambda: reset(self.image, self.modified_label))

        main_frame = Frame(master)
        main_frame.pack()

        self.red_channel_enabled = IntVar()
        self.green_channel_enabled = IntVar()
        self.blue_channel_enabled = IntVar()

        self.point_transform_panel = Frame(main_frame)
        self.point_transform_panel.grid(row=0, columnspan=3)
        self.create_point_transform_panel()

        self.enhance_panel = Frame(main_frame)
        self.enhance_panel.grid(row=1, columnspan=3)
        self.create_enhance_panel()

        original_picture_panel = Frame(main_frame)
        original_picture_panel.grid(row=2, column=0)

        self.image = Image.open('pictures/lena.jpg').resize((300, 300))
        photo = ImageTk.PhotoImage(self.image)

        self.original_label = Label(original_picture_panel, image=photo)
        self.original_label.image = photo  # keep a reference!
        self.original_label.pack()

        checkbox_panel = Frame(main_frame)
        checkbox_panel.grid(row=2, column=1)
        Checkbutton(checkbox_panel, text=R, variable=self.red_channel_enabled).pack()
        Checkbutton(checkbox_panel, text=G, variable=self.green_channel_enabled).pack()
        Checkbutton(checkbox_panel, text=B, variable=self.blue_channel_enabled).pack()

        modified_picture_panel = Frame(main_frame)
        modified_picture_panel.grid(row=2, column=2)

        self.image_copy = Image.open('pictures/lena.jpg').resize((300, 300))
        photo_copy = ImageTk.PhotoImage(self.image_copy)

        self.modified_label = Label(modified_picture_panel, image=photo_copy)
        self.modified_label.image = photo_copy  # keep a reference!
        self.modified_label.pack()

    def create_point_transform_panel(self):
        create_button(self.point_transform_panel, ADD,
                      lambda: self.perform_point_transform(ADD, self.point_transform_panel))
        create_button(self.point_transform_panel, SUBTRACTION,
                      lambda: self.perform_point_transform(SUBTRACTION, self.point_transform_panel))
        create_button(self.point_transform_panel, MULTIPLICATION,
                      lambda: self.perform_point_transform(MULTIPLICATION, self.point_transform_panel))
        create_button(self.point_transform_panel, DIVISION,
                      lambda: self.perform_point_transform(DIVISION, self.point_transform_panel))
        create_button(self.point_transform_panel, BRIGHTNESS,
                      lambda: self.perform_point_transform(BRIGHTNESS, self.point_transform_panel, -255, 255))
        create_button(self.point_transform_panel, GREYSCALE_1, self.change_to_simple_greyscale)
        create_button(self.point_transform_panel, GREYSCALE_2, self.change_to_adv_greyscale)

    def create_enhance_panel(self):
        create_button(self.enhance_panel, SMOOTHING_FILTER)
        create_button(self.enhance_panel, MEDIAN_FILTER)
        create_button(self.enhance_panel, SOBEL_FILTER)
        create_button(self.enhance_panel, SHARP_CUT_FILTER)
        create_button(self.enhance_panel, GAUSSIAN_BLUR_FILTER)
        create_button(self.enhance_panel, WEAVE_MASKS)

    def perform_point_transform(self, title, parent, min_value=0, max_value=255):
        value = ask_for_value(title, parent, min_value, max_value)

        if value is not None:
            pixels = self.image_copy.load()
            for i in range(self.image_copy.size[0]):
                for j in range(self.image_copy.size[1]):
                    (r, g, b) = self.make_operation(title, value, pixels[i, j])
                    pixels[i, j] = (r, g, b)

            photo_copy = ImageTk.PhotoImage(self.image_copy)
            self.modified_label.config(image=photo_copy)
            self.modified_label.image = photo_copy  # keep a reference!

    def make_operation(self, title, value, rgb):
        red_channel_enabled_get = self.red_channel_enabled.get()
        green_channel_enabled_get = self.green_channel_enabled.get()
        blue_channel_enabled_get = self.blue_channel_enabled.get()

        if title == ADD:
            rgb = add_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get,
                                value)
        elif title == SUBTRACTION:
            rgb = subtract_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get,
                                     value)
        elif title == MULTIPLICATION:
            rgb = multiply_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get,
                                     value)
        elif title == DIVISION:
            rgb = divide_operation(rgb, blue_channel_enabled_get, green_channel_enabled_get, red_channel_enabled_get,
                                   value)
        elif title == BRIGHTNESS:
            rgb = brightness_operation(rgb, value)
        else:
            print('Operation not implemented!')

        return rgb

    def change_to_simple_greyscale(self):
        pixels = self.image_copy.load()
        for i in range(self.image_copy.size[0]):
            for j in range(self.image_copy.size[1]):
                (r, g, b) = pixels[i, j]
                mean = int((r + g + b) / 3)
                pixels[i, j] = (mean, mean, mean)

        photo_copy = ImageTk.PhotoImage(self.image_copy)
        self.modified_label.config(image=photo_copy)
        self.modified_label.image = photo_copy  # keep a reference!

    def change_to_adv_greyscale(self):
        pixels = self.image_copy.load()
        for i in range(self.image_copy.size[0]):
            for j in range(self.image_copy.size[1]):
                (r, g, b) = pixels[i, j]
                value = int((0.299 * r) + (0.587 * g) + (0.114 * b))
                pixels[i, j] = (value, value, value)

        photo_copy = ImageTk.PhotoImage(self.image_copy)
        self.modified_label.config(image=photo_copy)
        self.modified_label.image = photo_copy  # keep a reference!


if __name__ == '__main__':
    root = Tk()
    app = Transformation(root)
    root.mainloop()
